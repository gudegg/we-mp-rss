import json
import requests
import time
import random
import yaml
import re
import logging
from bs4 import BeautifulSoup
from core.wx.base import WxGather
from core.print import print_error, print_info, print_warning
from core.log import logger

# 配置模块日志
module_logger = logging.getLogger(__name__)
# 继承 BaseGather 类
class MpsAppMsg(WxGather):

    # 重写 content_extract 方法
    def content_extract(self,  url):
        try:
            from driver.wxarticle import Web as App
            r = App.get_article_content(url)
            if r!=None:
                text = r.get("content","")
                text=self.remove_common_html_elements(text)
                return  text
        except Exception as e:
            logger.error(e)
        return ""
    # 重写 get_Articles 方法
    def get_Articles(self, faker_id:str=None,Mps_id:str=None,Mps_title="",CallBack=None,start_page:int=0,MaxPage:int=1,interval=10,Gather_Content=False,Item_Over_CallBack=None,Over_CallBack=None):
        """
        获取公众号文章列表
        
        Args:
            faker_id: 公众号的faker_id
            Mps_id: 公众号ID
            Mps_title: 公众号名称
            CallBack: 文章回调函数
            start_page: 起始页码
            MaxPage: 最大页数
            interval: 请求间隔(秒)
            Gather_Content: 是否采集内容
            Item_Over_CallBack: 单项完成回调
            Over_CallBack: 全部完成回调
        """
        module_logger.info("=" * 60)
        module_logger.info(f"========== 开始获取文章列表 ==========")
        module_logger.info(f"公众号: {Mps_title} (ID: {Mps_id})")
        module_logger.info(f"FakerID: {faker_id}")
        module_logger.info(f"页码范围: {start_page} - {MaxPage}")
        
        super().Start(mp_id=Mps_id)
        
        if self.Gather_Content:
            Gather_Content=True
        
        # 检查Token状态
        if not self.token:
            module_logger.error("Token为空！无法获取文章列表，请先扫码登录")
            print_error("Token为空！无法获取文章列表，请先扫码登录")
            super().Error("Token为空，请先扫码登录公众号平台", code="Invalid Session")
            return
        
        token_display = f"{str(self.token)[:10]}..." if self.token and len(str(self.token)) > 10 else self.token
        module_logger.info(f"当前Token: {token_display}")
        
        print_info(f"APP浏览器模式,是否采集[{Mps_title}]内容：{Gather_Content}")
        
        # 请求参数
        url = "https://mp.weixin.qq.com/cgi-bin/appmsgpublish"
        count=5
        params = {
            "sub": "list",
            "sub_action": "list_ex",
            "begin":start_page,
            "count": count,
            "fakeid": faker_id,
            "token": self.token,
            "lang": "zh_CN",
            "f": "json",
            "ajax": 1
        }
        
        module_logger.info(f"请求URL: {url}")
        module_logger.info(f"请求参数: fakeid={faker_id}, token={token_display}, count={count}")
        
        # 连接超时
        session=self.session
        # 起始页数
        i = start_page
        article_count = 0
        
        while True:
            if i >= MaxPage:
                module_logger.info(f"已达到最大页数限制: {MaxPage}")
                break
            begin = i * count
            params["begin"] = str(begin)
            
            module_logger.info(f"正在获取第{i+1}页 (begin={begin})")
            print_info(f"第{i+1}页开始爬取")
            
            # 随机暂停几秒，避免过快的请求导致过快的被查到
            wait_time = random.randint(0,interval)
            if wait_time > 0:
                module_logger.debug(f"等待 {wait_time} 秒后继续...")
            time.sleep(wait_time)
            
            try:
                headers = self.fix_header(url)
                module_logger.debug(f"请求头: Cookie长度={len(headers.get('Cookie', ''))}")
                
                resp = session.get(url, headers=headers, params = params, verify=False)
                
                module_logger.info(f"响应状态码: {resp.status_code}")
                
                # 检查响应内容类型
                content_type = resp.headers.get('Content-Type', '')
                if 'application/json' not in content_type and 'text/json' not in content_type:
                    module_logger.warning(f"响应Content-Type不是JSON: {content_type}")
                    module_logger.warning(f"响应内容(前500字符): {resp.text[:500]}")
                
                try:
                    msg = resp.json()
                except json.JSONDecodeError as je:
                    module_logger.error(f"JSON解析失败: {je}")
                    module_logger.error(f"响应内容: {resp.text[:1000]}")
                    break
                
                self._cookies = resp.cookies
                
                # 记录响应基本信息
                ret_code = msg.get('base_resp', {}).get('ret', 'N/A')
                err_msg = msg.get('base_resp', {}).get('err_msg', '')
                module_logger.info(f"API响应: ret={ret_code}, err_msg={err_msg}")
                
                # 流量控制了, 退出
                if msg['base_resp']['ret'] == 200013:
                    module_logger.error(f"触发流量控制(200013)! 当前位置: begin={begin}")
                    print_error(f"触发流量控制，请稍后再试")
                    super().Error("frequencey control, stop at {}".format(str(begin)))
                    break
                
                # Session无效
                if msg['base_resp']['ret'] == 200003:
                    module_logger.error(f"Session无效(200003)! Token可能已过期")
                    module_logger.error(f"当前Token: {token_display}")
                    module_logger.error(f"请重新扫码登录公众号平台获取新的Token")
                    print_error(f"Session无效，Token已过期，请重新扫码登录！")
                    super().Error("Invalid Session, stop at {}".format(str(begin)),code="Invalid Session")
                    break
                
                if msg['base_resp']['ret'] != 0:
                    module_logger.error(f"API返回错误: ret={ret_code}, err_msg={err_msg}")
                    print_error(f"API错误: {err_msg} (代码: {ret_code})")
                    super().Error("错误原因:{}:代码:{}".format(msg['base_resp']['err_msg'],msg['base_resp']['ret']),code=msg['base_resp']['err_msg'])
                    break
                
                # 如果返回的内容中为空则结束
                if 'publish_page' not in msg:
                    module_logger.info("没有更多文章了 (publish_page不存在)")
                    super().Error("all ariticle parsed")
                    break
                
                if "publish_page" in msg:
                    msg["publish_page"]=json.loads(msg['publish_page'])
                    publish_list = msg["publish_page"].get('publish_list', [])
                    module_logger.info(f"本页获取到 {len(publish_list)} 条发布记录")
                    
                    for item in publish_list:
                        if "publish_info" in item:
                            publish_info= json.loads(item['publish_info'])
                       
                            if "appmsgex" in publish_info:
                                for article in publish_info["appmsgex"]:
                                    article_count += 1
                                    module_logger.debug(f"处理文章: {article.get('title', 'N/A')[:30]}...")
                                    
                                    if Gather_Content:
                                        if not super().HasGathered(article["aid"]):
                                            article["content"] = self.content_extract(article['link'])
                                            super().Wait(3,10,tips=f"{article['title']} 采集完成")
                                    else:
                                        article["content"] = ""
                                    article["id"] = article["aid"]
                                    article["mp_id"] = Mps_id
                                    if CallBack is not None:
                                        super().FillBack(CallBack=CallBack,data=article,Ext_Data={"mp_title":Mps_title,"mp_id":Mps_id})
                    
                    module_logger.info(f"第{i+1}页爬取成功，累计处理 {article_count} 篇文章")
                    print_info(f"第{i+1}页爬取成功")
                
                # 翻页
                i += 1
                
            except requests.exceptions.Timeout:
                module_logger.error("请求超时!")
                print_error("请求超时")
                break
            except requests.exceptions.RequestException as e:
                module_logger.error(f"请求异常: {e}")
                print_error(f"请求错误: {e}")
                break
            except Exception as e:
                module_logger.error(f"未知错误: {e}")
                import traceback
                module_logger.error(f"错误详情: {traceback.format_exc()}")
                break
            finally:
                super().Item_Over(item={"mps_id":Mps_id,"mps_title":Mps_title},CallBack=Item_Over_CallBack)
        
        module_logger.info(f"文章获取完成，共处理 {article_count} 篇文章")
        module_logger.info("=" * 60)
        super().Over(CallBack=Over_CallBack)