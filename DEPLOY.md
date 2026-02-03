# CI/CD 部署指南

本文档详细说明如何配置 GitHub Actions 自动部署到你的服务器。

## 架构概览

```
┌─────────────┐     push      ┌──────────────┐     deploy     ┌─────────────┐
│   开发者     │ ───────────► │ GitHub Actions│ ────────────► │   服务器     │
└─────────────┘               └──────────────┘                └─────────────┘
                                     │
                                     ▼
                              ┌──────────────┐
                              │ GitHub       │
                              │ Container    │
                              │ Registry     │
                              └──────────────┘
```

**部署流程:**
1. 推送代码到 `main` 分支
2. GitHub Actions 自动构建 Docker 镜像
3. 推送镜像到 GitHub Container Registry
4. SSH 连接服务器拉取最新镜像
5. 重启 Docker 容器完成部署

---

## 第一步：配置 GitHub 仓库

### 1.1 初始化 Git 仓库

```bash
cd /home/cai/leetcode

# 初始化 Git
git init
git add .
git commit -m "Initial commit: LeetCode Hot 100 管理工具"

# 添加远程仓库（替换为你的仓库地址）
git remote add origin git@github.com:你的用户名/leetcode.git
git branch -M main
git push -u origin main
```

### 1.2 配置 GitHub Secrets

进入 GitHub 仓库 → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

添加以下 Secrets：

| Secret 名称 | 说明 | 示例值 |
|------------|------|--------|
| `SERVER_HOST` | 服务器 IP 或域名 | `123.45.67.89` |
| `SERVER_USER` | SSH 登录用户名 | `root` 或 `ubuntu` |
| `SERVER_SSH_KEY` | SSH 私钥 | 见下方说明 |
| `SERVER_PORT` | SSH 端口（可选） | `22` |
| `DEPLOY_PATH` | 部署目录（可选） | `/opt/leetcode` |

### 1.3 生成 SSH 密钥

在**本地**生成专用的部署密钥：

```bash
# 生成密钥对
ssh-keygen -t ed25519 -C "github-actions-deploy" -f ~/.ssh/deploy_key

# 查看私钥（复制到 GitHub Secrets 的 SERVER_SSH_KEY）
cat ~/.ssh/deploy_key

# 查看公钥（添加到服务器）
cat ~/.ssh/deploy_key.pub
```

---

## 第二步：配置服务器

### 2.1 添加 SSH 公钥

在服务器上执行：

```bash
# 将公钥添加到 authorized_keys
echo "你的公钥内容" >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```

### 2.2 安装 Docker（如果未安装）

```bash
# Ubuntu/Debian
curl -fsSL https://get.docker.com | sh
sudo usermod -aG docker $USER

# 安装 Docker Compose
sudo apt install docker-compose-plugin

# 重新登录使权限生效
```

### 2.3 初始化项目目录

```bash
# 创建项目目录
sudo mkdir -p /opt/leetcode
sudo chown $USER:$USER /opt/leetcode
cd /opt/leetcode

# 创建 docker-compose.yml（替换 你的用户名/leetcode 为实际仓库名）
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  backend:
    image: ghcr.io/你的用户名/leetcode/backend:latest
    container_name: leetcode-backend
    restart: always
    volumes:
      - sqlite_data:/app
    networks:
      - leetcode-network

  frontend:
    image: ghcr.io/你的用户名/leetcode/frontend:latest
    container_name: leetcode-frontend
    restart: always
    ports:
      - "80:80"
    depends_on:
      - backend
    networks:
      - leetcode-network

networks:
  leetcode-network:
    driver: bridge

volumes:
  sqlite_data:
EOF
```

### 2.4 配置防火墙

```bash
# 开放 80 端口
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp  # 如果需要 HTTPS
```

---

## 第三步：触发部署

### 自动部署

推送代码到 `main` 分支即可自动触发：

```bash
git add .
git commit -m "feat: 新功能"
git push origin main
```

### 手动部署

1. 进入 GitHub 仓库 → **Actions**
2. 选择 **Deploy to Server** 工作流
3. 点击 **Run workflow**

### 查看部署状态

- GitHub Actions 页面查看构建日志
- 服务器上查看容器状态：`docker ps`
- 查看容器日志：`docker logs leetcode-backend`

---

## 常用运维命令

### 服务器上执行

```bash
cd /opt/leetcode

# 查看容器状态
docker ps

# 查看日志
docker logs leetcode-backend
docker logs leetcode-frontend

# 重启服务
docker compose restart

# 停止服务
docker compose down

# 手动更新
docker compose pull
docker compose up -d

# 查看数据库（进入容器）
docker exec -it leetcode-backend sh
```

### 备份数据

```bash
# 备份 SQLite 数据库
docker cp leetcode-backend:/app/leetcode.db ./backup_$(date +%Y%m%d).db
```

---

## 配置 HTTPS（可选）

如果需要 HTTPS，可以使用 Caddy 或 Nginx + Let's Encrypt：

### 方案1：使用 Caddy（推荐）

修改 `docker-compose.yml`：

```yaml
services:
  caddy:
    image: caddy:alpine
    container_name: leetcode-caddy
    restart: always
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./Caddyfile:/etc/caddy/Caddyfile
      - caddy_data:/data
    depends_on:
      - frontend
    networks:
      - leetcode-network

  frontend:
    # 移除 ports 配置，只暴露给内部网络
    expose:
      - "80"
```

创建 `Caddyfile`：

```
你的域名.com {
    reverse_proxy frontend:80
}
```

### 方案2：使用 Nginx + Certbot

参考 Let's Encrypt 官方文档配置。

---

## 故障排查

### 构建失败

1. 检查 Dockerfile 语法
2. 查看 GitHub Actions 日志
3. 本地测试：`docker build -t test ./backend`

### 部署失败

1. 检查 SSH 连接：`ssh -i deploy_key user@server`
2. 检查 Secrets 配置是否正确
3. 服务器上手动拉取测试：`docker pull ghcr.io/用户名/仓库名/backend:latest`

### 容器无法启动

```bash
# 查看详细日志
docker logs leetcode-backend --tail 100

# 检查端口占用
sudo netstat -tlnp | grep 80
```

---

## 项目结构

```
leetcode/
├── .github/
│   └── workflows/
│       └── deploy.yml          # GitHub Actions 工作流
├── backend/
│   ├── Dockerfile              # 后端 Docker 镜像
│   └── ...
├── frontend/
│   ├── Dockerfile              # 前端 Docker 镜像
│   ├── nginx.conf              # Nginx 配置
│   └── ...
├── docker-compose.yml          # 本地开发用
├── docker-compose.prod.yml     # 生产环境模板
├── DEPLOY.md                   # 本文档
└── scripts/
    └── server-setup.sh         # 服务器初始化脚本
```
