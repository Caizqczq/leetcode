# LeetCode Hot 100 刷题管理工具

一个帮助你系统性刷 LeetCode Hot 100 题目的管理工具，支持进度追踪、笔记记录和艾宾浩斯复习计划。

## 功能特性

- **题目管理**: 预置 Hot 100 全部题目，支持按难度、分类、状态筛选
- **进度追踪**: 记录每道题的状态（未开始/已尝试/复习中/已掌握）和掌握程度
- **笔记系统**: 记录解题思路、代码、时间/空间复杂度和关键点
- **标签系统**: 预置常用标签，支持自定义标签
- **复习计划**: 基于艾宾浩斯遗忘曲线自动生成复习计划（1/2/4/7/15天）
- **统计分析**: 可视化展示刷题进度、难度分布、分类完成率等

## 技术栈

### 前端
- Vue 3 + TypeScript + Vite
- Element Plus
- Pinia
- Vue Router 4
- ECharts + vue-echarts

### 后端
- Python FastAPI
- SQLAlchemy 2.0
- SQLite (异步)
- Pydantic

## 快速开始

### 1. 启动后端

```bash
cd backend

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或 venv\Scripts\activate  # Windows

# 安装依赖
pip install -r requirements.txt

# 启动服务
uvicorn app.main:app --reload --port 8000
```

后端服务将运行在 http://localhost:8000

### 2. 启动前端

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端服务将运行在 http://localhost:5173

## 项目结构

```
leetcode/
├── frontend/                   # Vue3 前端
│   ├── src/
│   │   ├── api/               # API 接口封装
│   │   ├── router/            # 路由配置
│   │   ├── stores/            # Pinia 状态管理
│   │   └── views/             # 页面组件
│   │       ├── Dashboard/     # 仪表盘
│   │       ├── Problems/      # 题目列表
│   │       ├── ProblemDetail/ # 题目详情
│   │       ├── Review/        # 复习计划
│   │       └── Stats/         # 统计分析
│   └── package.json
│
├── backend/                    # FastAPI 后端
│   ├── app/
│   │   ├── api/               # API 路由
│   │   ├── models/            # 数据库模型
│   │   ├── schemas/           # Pydantic 模式
│   │   ├── services/          # 业务逻辑
│   │   ├── core/              # 核心配置
│   │   └── data/              # 初始数据
│   └── requirements.txt
│
└── README.md
```

## 使用说明

### 刷题流程

1. 进入**题目列表**，选择要刷的题目
2. 点击**LeetCode**链接去做题
3. 做完后更新**状态**和**掌握程度**
4. 在**题目详情**页记录笔记
5. 系统会自动生成**复习计划**
6. 每天查看**复习计划**页面完成复习

### 复习机制

当你将一道题标记为"已尝试"或"复习中"时，系统会自动生成 5 轮复习计划：
- 第 1 天后
- 第 2 天后
- 第 4 天后
- 第 7 天后
- 第 15 天后

## API 文档

启动后端后，访问 http://localhost:8000/docs 查看自动生成的 Swagger API 文档。

## License

MIT
