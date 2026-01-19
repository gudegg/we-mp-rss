# Agents - We-MP-RSS AI 助手配置

本文档定义了 We-MP-RSS 项目中 AI 助手的工作模式和开发规范。

## 项目概述

We-MP-RSS 是一个微信公众号 RSS 订阅助手，采用前后端分离架构：
- **后端**: Python 3.13+ + FastAPI
- **前端**: Vue 3 + Vite + Arco Design
- **数据库**: SQLite (默认) / MySQL
- **主要功能**: 公众号内容抓取、RSS 订阅生成、Web 管理界面、定时任务、通知系统

## 开发模式

### 后端开发 Agent

**职责**:
- 实现和优化后端 API 接口
- 开发和调试微信公众号抓取逻辑
- 实现数据库模型和操作
- 配置定时任务和异步队列

**工作规范**:
- 使用 FastAPI 路由装饰器定义 API 端点
- 遵循 Pydantic 模型进行数据验证
- 数据库操作使用 SQLAlchemy ORM
- 日志使用项目提供的 log 模块
- 配置通过 `config.yaml` 管理，使用 `core.config` 模块读取

**常用模块**:
```python
from core import config, database, db, log
from core.models import *
from apis import *
from driver import wx, playwright_driver
```

**关键目录**:
- `core/` - 核心业务逻辑
- `apis/` - API 路由定义
- `driver/` - 微信抓取驱动
- `jobs/` - 定时任务
- `tools/` - 工具函数

### 前端开发 Agent

**职责**:
- 开发和优化 Vue 3 组件
- 实现用户界面交互
- 集成 Arco Design 组件库
- 使用 Vue Router 管理路由
- 调用后端 API

**工作规范**:
- 使用 Composition API 编写组件
- 组件命名使用 PascalCase
- 样式使用 scoped CSS
- API 调用使用 axios
- 国际化支持使用 i18n-jsautotranslate

**技术栈**:
- Vue 3 + TypeScript
- Arco Design (主要) / Ant Design Vue
- Vue Router 4
- Vite 构建工具

**关键目录**:
- `web_ui/src/` - 源代码目录
  - `views/` - 页面组件
  - `components/` - 可复用组件
  - `api/` - API 调用封装
  - `router/` - 路由配置

### 数据库 Agent

**职责**:
- 设计和优化数据库模型
- 编写数据库迁移脚本
- 优化查询性能
- 管理数据同步

**工作规范**:
- 模型定义在 `core/models/` 目录
- 使用 SQLAlchemy ORM
- 支持 SQLite 和 MySQL
- 数据库连接通过 `core.db` 模块管理

### 抓取驱动 Agent

**职责**:
- 开发和维护微信公众号内容抓取逻辑
- 处理反爬虫机制
- 管理浏览器自动化
- 优化抓取性能和稳定性

**工作规范**:
- 使用 Playwright 进行浏览器自动化
- 实现反爬虫策略 (行为模拟、指纹规避)
- Cookie 和 Token 管理在 `driver/` 目录
- 支持多种抓取模式切换

**关键模块**:
- `driver/playwright_driver.py` - Playwright 驱动
- `driver/wx.py` - 微信业务逻辑
- `driver/anti_crawler_*.js` - 反爬虫策略

### RSS 生成 Agent

**职责**:
- 生成标准 RSS feeds
- 处理文章内容格式化
- 管理 RSS 缓存
- 优化 RSS 输出

**工作规范**:
- RSS 生成逻辑在 `core/rss.py`
- 支持自定义标题、描述、封面
- 支持分页配置
- 支持全文/摘要模式

### 通知系统 Agent

**职责**:
- 实现多渠道通知功能
- 管理通知模板
- 处理授权过期提醒
- 集成 Webhook

**工作规范**:
- 支持钉钉、微信、飞书、自定义 Webhook
- 通知配置在 `config.yaml` 的 `notice` 部分
- 消息格式化在 `core/notice/` 目录

## 通用规范

### 代码风格
- **Python**: 遵循 PEP 8 规范
- **TypeScript/Vue**: 遵循 Vue 官方风格指南
- 使用 4 空格缩进
- 函数和变量使用 snake_case (Python) 或 camelCase (JS/TS)
- 类名使用 PascalCase

### 提交规范
- feat: 新功能
- fix: 修复 bug
- docs: 文档更新
- style: 代码格式调整
- refactor: 重构
- test: 测试相关
- chore: 构建/工具相关

### 测试要求
- 后端 API 需要编写单元测试
- 前端组件需要编写测试用例
- 抓取逻辑需要定期测试稳定性

## 环境配置

### 后端依赖安装
```bash
pip install -r requirements.txt
```

### 前端依赖安装
```bash
cd web_ui
yarn install
```

### 启动服务
```bash
# 后端
python main.py -job True -init True

# 前端开发
cd web_ui
yarn dev
```

## 注意事项

1. **安全性**: 不要提交 `config.yaml` 文件（包含敏感配置），使用 `config.example.yaml` 作为模板
2. **数据库**: 默认使用 SQLite，生产环境建议使用 MySQL
3. **抓取频率**: 注意合理的抓取频率，避免被封禁
4. **日志**: 关键操作需要记录日志，便于排查问题
5. **错误处理**: 所有 API 调用需要适当的错误处理
6. **性能**: 大量数据操作需要考虑分页和缓存
7. **兼容性**: 确保在不同浏览器和设备上正常运行

## 开发工作流

1. 从 `config.example.yaml` 创建 `config.yaml`
2. 根据需求修改配置文件
3. 启动后端服务: `python main.py -job True -init True`
4. 启动前端服务 (如需开发): `cd web_ui && yarn dev`
5. 访问 `http://localhost:8001` 查看效果
6. 使用热重载进行开发调试
7. 测试完成后提交代码

## 扩展开发

### 添加新的抓取驱动
1. 在 `driver/` 创建新的驱动文件
2. 实现统一接口（参考 `driver/base.py`）
3. 在 `driver/switch.py` 注册驱动
4. 配置文件添加驱动选项

### 添加新的通知渠道
1. 在 `core/notice/` 创建通知模块
2. 实现发送逻辑
3. 在 `config.yaml` 添加配置项
4. 在 `core/notice/` 注册通知渠道

### 添加新的导出格式
1. 在相关导出模块添加格式支持
2. 实现格式转换逻辑
3. 在 API 添加相应端点
4. 前端添加导出选项

## 调试技巧

### 后端调试
- 设置 `config.yaml` 中的 `DEBUG: True`
- 查看日志文件: `tail -f data/logs/app.log`
- 使用 Python 调试器: `pdb` 或 IDE 断点

### 前端调试
- 使用浏览器开发者工具
- Vue DevTools 扩展
- Network 面板查看 API 调用
- Console 查看错误信息

### 抓取问题调试
- 查看浏览器截图: `data/screenshots/`
- 检查反爬虫日志
- 手动测试抓取逻辑: `python test_article.py`

## 相关文档

- [项目 README](README.md)
- [中文文档](README.zh-CN.md)
- [贡献指南](CONTRIBUTING.md)
- [配置示例](config.example.yaml)

## 更新日志

agents.md 记录 AI 助手在项目中的工作规范和最佳实践，如有更新请同步修改此文件。

---

## 完整目录结构

```
we-mp-rss/
├── apis/                    # API 路由定义
│   ├── article.py           # 文章相关 API
│   ├── auth.py              # 认证相关 API
│   ├── base.py              # 基础 API 类
│   ├── cache.py             # 缓存 API
│   ├── config_management.py # 配置管理 API
│   ├── export.py            # 导出 API
│   ├── github_update.py     # 更新检测 API
│   ├── message_task.py      # 消息任务 API
│   ├── mps.py               # 公众号 API
│   ├── res.py               # 资源 API
│   ├── rss.py               # RSS API
│   ├── sys_info.py          # 系统信息 API
│   ├── tags.py              # 标签 API
│   ├── tools.py             # 工具 API
│   └── user.py              # 用户 API
├── core/                    # 核心业务逻辑
│   ├── auth.py              # 认证模块
│   ├── cache.py             # 缓存模块
│   ├── config.py            # 配置读取
│   ├── content_format.py    # 内容格式化
│   ├── database.py          # 数据库初始化
│   ├── db.py                # 数据库连接
│   ├── log.py               # 日志模块
│   ├── rss.py               # RSS 生成
│   ├── task.py              # 任务调度
│   ├── thread.py            # 线程管理
│   ├── webhook.py           # Webhook 处理
│   ├── wx/                  # 微信相关业务
│   ├── models/              # 数据库模型
│   │   ├── article.py       # 文章模型
│   │   ├── base.py          # 基础模型类
│   │   ├── feed.py          # 订阅源模型
│   │   ├── message_task.py  # 消息任务模型
│   │   ├── tags.py          # 标签模型
│   │   └── user.py          # 用户模型
│   └── notice/              # 通知模块
├── driver/                  # 抓取驱动
│   ├── playwright_driver.py # Playwright 驱动
│   ├── wx.py                # 微信业务逻辑
│   ├── wx_api.py            # 微信 API
│   ├── wxarticle.py         # 文章抓取
│   ├── auth.py              # 授权处理
│   ├── token.py             # Token 管理
│   ├── cookies.py           # Cookie 管理
│   ├── switch.py            # 驱动切换
│   └── anti_crawler_*.js    # 反爬虫脚本
├── jobs/                    # 定时任务
├── tools/                   # 工具函数
├── web_ui/                  # 前端项目
│   └── src/
│       ├── views/           # 页面组件
│       ├── components/      # 可复用组件
│       ├── api/             # API 调用封装
│       └── router/          # 路由配置
├── schemas/                 # Pydantic 模型
├── views/                   # 视图模板
├── data/                    # 数据目录
│   ├── cache/               # 缓存文件
│   ├── logs/                # 日志文件
│   └── screenshots/         # 截图文件
└── config.yaml              # 配置文件
```

---

## 核心数据模型

### Article (文章)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | String | 文章唯一标识 |
| mp_id | String | 公众号 ID |
| title | String | 文章标题 |
| pic_url | String | 封面图 URL |
| url | String | 原文链接 |
| description | Text | 摘要描述 |
| content | Text | 文章内容 |
| status | Integer | 状态 (1:正常, 1000:已删除) |
| publish_time | Integer | 发布时间戳 |
| is_read | Integer | 是否已读 |
| is_export | Integer | 是否已导出 |

### Feed (订阅源)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | String | 订阅源 ID |
| mp_name | String | 公众号名称 |
| mp_cover | String | 公众号封面 |
| mp_intro | String | 公众号介绍 |
| status | Integer | 状态 |
| sync_time | Integer | 最后同步时间 |
| faker_id | String | 虚拟 ID |

### User (用户)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | String | 用户 ID |
| username | String | 用户名 (唯一) |
| password_hash | String | 密码哈希 |
| role | String | 角色 (admin/editor/user) |
| permissions | Text | 权限列表 |
| is_active | Boolean | 是否激活 |

### MessageTask (消息任务)
| 字段 | 类型 | 说明 |
|------|------|------|
| id | String | 任务 ID |
| type | Integer | 消息类型 |
| content | Text | 消息内容 |
| status | Integer | 执行状态 |
| retry_count | Integer | 重试次数 |
| created_at | DateTime | 创建时间 |

---

## API 响应格式规范

### 成功响应
```json
{
  "code": 200,
  "data": {
    // 业务数据
  },
  "message": "操作成功"
}
```

### 分页响应
```json
{
  "code": 200,
  "data": {
    "items": [],
    "total": 100,
    "page": 1,
    "page_size": 20
  },
  "message": "获取成功"
}
```

### 错误响应
```json
{
  "code": 400,
  "data": null,
  "message": "参数错误"
}
```

### 常用状态码
| 状态码 | 说明 |
|--------|------|
| 200 | 成功 |
| 400 | 请求参数错误 |
| 401 | 未认证 |
| 403 | 无权限 |
| 404 | 资源不存在 |
| 500 | 服务器内部错误 |

---

## 错误处理规范

### 后端异常处理
```python
from fastapi import HTTPException
from core.log import logger

# 抛出 HTTP 异常
raise HTTPException(status_code=400, detail="参数错误")

# 记录错误日志
try:
    # 业务逻辑
except Exception as e:
    logger.error(f"操作失败: {str(e)}")
    raise HTTPException(status_code=500, detail="服务器内部错误")
```

### 统一错误处理
- 在 `core/base.py` 中定义统一异常处理器
- 所有 API 错误使用 `HTTPException` 抛出
- 敏感信息不在错误响应中返回
- 记录完整错误堆栈便于排查

---

## 安全规范

### 输入验证
- 所有 API 参数使用 Pydantic 模型验证
- 禁止直接拼接 SQL 语句，使用 ORM 或参数化查询
- 用户输入内容进行 XSS 过滤
- 文件上传验证文件类型和大小

### 认证授权
- 使用 JWT Token 进行身份认证
- Token 有效期可配置 (默认 4320 分钟)
- 敏感操作需要管理员权限
- 密码使用 bcrypt 算法加密存储

### 配置安全
- `config.yaml` 不提交到版本控制
- 数据库连接信息加密存储
- API 密钥通过环境变量注入
- 定期轮换密钥和 Token

### 接口安全
- 关键接口添加速率限制
- CORS 配置只允许可信域名
- 防止 SQL 注入和 XSS 攻击
- 日志中不记录敏感信息

---

## 贡献流程

### 开发流程
1. Fork 项目仓库
2. 创建功能分支: `git checkout -b feat/xxx`
3. 提交代码: `git commit -m "feat: 添加新功能"`
4. 推送分支: `git push origin feat/xxx`
5. 创建 Pull Request

### 代码 Review 要求
- 所有代码必须经过 Review 才能合并
- 检查代码风格和规范
- 验证功能正确性
- 确保测试通过

### Commit Message 规范
```
<type>(<scope>): <subject>

feat(api): 新增文章导出功能
fix(driver): 修复 Cookie 过期问题
docs(readme): 更新安装指南
refactor(core): 重构缓存模块
```

---

## 性能优化

### 数据库优化
- 使用索引加速查询 (如 `publish_time` 字段)
- 大数据量分页查询使用游标分页
- 定期清理无用数据和日志
- 使用连接池管理数据库连接

### 缓存策略
- RSS feed 生成结果缓存
- 公众号信息缓存
- 配置信息缓存
- 缓存过期时间根据数据更新频率设置

### 抓取优化
- 控制并发抓取数量
- 使用代理池分散请求
- 遵守公众号请求频率限制
- 失败任务自动重试

### 前端优化
- 路由懒加载
- 组件按需引入
- 图片懒加载
- 静态资源压缩

---

## 部署指南

### Docker 部署
```bash
# 官方镜像
docker run -d \
  --name we-mp-rss \
  -p 8001:8001 \
  -v ./data:/app/data \
  ghcr.io/rachelos/we-mp-rss:latest

# 国内镜像 (加速)
docker run -d \
  --name we-mp-rss \
  -p 8001:8001 \
  -v ./data:/app/data \
  docker.1ms.run/rachelos/we-mp-rss:latest
```

### Docker Compose 部署
```yaml
version: '3.8'
services:
  we-mp-rss:
    image: ghcr.io/rachelos/we-mp-rss:latest
    container_name: we-mp-rss
    ports:
      - "8001:8001"
    volumes:
      - ./data:/app/data
    restart: unless-stopped
```

### 生产环境配置
```yaml
# config.yaml
SERVER_NAME: we-mp-rss
DEBUG: False
DB: mysql+pymysql://user:pass@localhost:3306/wer ss
ENABLE_JOB: True
THREADS: 4
LOG_LEVEL: WARNING
TOKEN_EXPIRE_MINUTES: 4320
```

### Nginx 反向代理
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 监控告警
- 监控服务健康状态
- 监控抓取成功率
- 监控数据库连接数
- 配置授权过期提醒