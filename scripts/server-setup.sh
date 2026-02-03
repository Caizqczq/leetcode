#!/bin/bash
# 服务器初始化脚本 - 在服务器上运行一次即可

set -e

DEPLOY_PATH="/opt/leetcode"

echo "🚀 开始初始化服务器..."

# 1. 创建项目目录
echo "📁 创建项目目录..."
sudo mkdir -p $DEPLOY_PATH
sudo chown $USER:$USER $DEPLOY_PATH
cd $DEPLOY_PATH

# 2. 创建 docker-compose.yml
echo "📝 创建 docker-compose.yml..."
cat > docker-compose.yml << 'EOF'
version: '3.8'

services:
  backend:
    image: ghcr.io/caizqczq/leetcode/backend:latest
    container_name: leetcode-backend
    restart: always
    volumes:
      - sqlite_data:/app
    environment:
      - DATABASE_URL=sqlite+aiosqlite:///./leetcode.db
    networks:
      - leetcode-network

  frontend:
    image: ghcr.io/caizqczq/leetcode/frontend:latest
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

echo ""
echo "✅ 服务器初始化完成!"
echo ""
echo "📋 后续步骤:"
echo "1. 确保已在 GitHub 仓库配置 Secrets"
echo "2. 推送代码到 main 分支触发自动部署"
echo "3. 或手动拉取运行:"
echo "   docker login ghcr.io -u Caizqczq"
echo "   docker compose pull"
echo "   docker compose up -d"
