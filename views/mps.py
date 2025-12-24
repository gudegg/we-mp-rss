from fastapi import APIRouter, Request, Depends, Query, HTTPException
from fastapi.responses import HTMLResponse
from typing import Optional
import os
import json
from datetime import datetime

from core.db import DB
from core.models.tags import Tags
from core.models.feed import Feed
from core.models.article import Article
from core.lax.template_parser import TemplateParser
from views.config import base
from driver.wxarticle import Web
from core.cache import cache_view, clear_cache_pattern
# 创建路由器
router = APIRouter(tags=["公众号"])

@router.get("/mps", response_class=HTMLResponse, summary="公众号 - 显示所有公众号")
@cache_view("mps_page", ttl=1800)  # 缓存30分钟
async def home_view(
    request: Request,
    page: int = Query(1, ge=1, description="页码"),
    limit: int = Query(12, ge=1, le=50, description="每页数量")
):
    """
    首页显示所有公众号，支持分页
    """
    session = DB.get_session()
    try:
        # 查询标签总数
        total = session.query(Feed).filter(Feed.status == 1).count()
        
        # 计算偏移量
        offset = (page - 1) * limit

        # 查询公众号列表
        feeds = session.query(Feed).filter(Feed.status == 1).order_by(Feed.created_at.desc()).offset(offset).limit(limit).all()
        
        # 处理公众号数据
        feed_list = []
        for feed in feeds:
            # 对于 Feed 表，id 就是公众号的 ID
            mp_id = feed.id
            
            # 统计该公众号的文章数量
            article_count = session.query(Article).filter(
                Article.mp_id == mp_id,
                Article.status == 1
            ).count()
            
            feed_data = {
                "id": feed.id,
                "name": feed.mp_name,
                "cover": Web.get_image_url(feed.mp_cover) if feed.mp_cover else "",
                "intro": feed.mp_intro,
                "mp_count": 1,  # Feed 本身就是一个公众号
                "article_count": article_count,
                "sync_time": datetime.fromtimestamp(feed.sync_time).strftime('%Y-%m-%d %H:%M') if feed.sync_time else "未同步",
                "created_at": feed.created_at.strftime('%Y-%m-%d') if feed.created_at else ""
            }
            feed_list.append(feed_data)
        
        # 计算分页信息
        total_pages = (total + limit - 1) // limit
        has_prev = page > 1
        has_next = page < total_pages
        
        # 构建面包屑
        breadcrumb = [
            {"name": "公众号", "url": "/views/mps"}
        ]
        
        # 读取模板文件
        template_path = base.home_template
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        # 使用模板引擎渲染
        parser = TemplateParser(template_content, template_dir=base.public_dir)
        html_content = parser.render({
            "feeds": feed_list,
            "current_page": page,
            "total_pages": total_pages,
            "total_items": total,
            "limit": limit,
            "has_prev": has_prev,
            "has_next": has_next,
            "breadcrumb": breadcrumb
        })
        
        return HTMLResponse(content=html_content)
        
    except Exception as e:
        print(f"获取首页数据错误: {str(e)}")
        # 读取模板文件
        template_path = base.mps_template
        with open(template_path, 'r', encoding='utf-8') as f:
            template_content = f.read()
        
        parser = TemplateParser(template_content, template_dir=base.public_dir)
        html_content = parser.render({
            "error": f"加载数据时出现错误: {str(e)}",
            "breadcrumb": [{"name": "公众号", "url": "/views/mps"}]
        })
        
        return HTMLResponse(content=html_content)
    finally:
        session.close()