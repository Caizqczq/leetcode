#!/bin/bash
# LeetCode Hot 100 管理工具 - 一键部署脚本
# 支持：本地打包 / 服务器部署 / 更新重启

set -e

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

# 颜色输出
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo "=========================================="
echo "  LeetCode Hot 100 管理工具 - 一键部署"
echo "=========================================="

# 1. 打包前端
echo ""
echo -e "${YELLOW}[1/4] 打包前端...${NC}"
cd frontend
npm install --silent
npm run build
echo -e "${GREEN}✓ 前端打包完成${NC}"

# 2. 复制前端文件到后端
echo ""
echo -e "${YELLOW}[2/4] 复制静态文件...${NC}"
cd "$SCRIPT_DIR"
rm -rf backend/static
cp -r frontend/dist backend/static
echo -e "${GREEN}✓ 静态文件已复制${NC}"

# 3. 安装/更新后端依赖
echo ""
echo -e "${YELLOW}[3/4] 安装后端依赖...${NC}"
cd backend

# 创建虚拟环境（如果不存在）
if [ ! -d "venv" ]; then
    echo "创建虚拟环境..."
    python3 -m venv venv
fi

source venv/bin/activate
pip install --upgrade pip -q
pip install -r requirements.txt -q
echo -e "${GREEN}✓ 依赖安装完成${NC}"

# 4. 启动/重启服务
echo ""
echo -e "${YELLOW}[4/4] 启动服务...${NC}"

# 停止旧进程
if pgrep -f "uvicorn app.main:app" > /dev/null; then
    echo "停止旧服务..."
    pkill -f "uvicorn app.main:app" || true
    sleep 2
fi

# 后台启动
nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 > app.log 2>&1 &
sleep 3

# 验证服务是否启动成功
if curl -s http://localhost:8000/api > /dev/null; then
    echo -e "${GREEN}✓ 服务启动成功${NC}"
else
    echo "服务启动可能失败，查看日志: tail -f $SCRIPT_DIR/backend/app.log"
fi

echo ""
echo "=========================================="
echo -e "${GREEN}  部署完成！${NC}"
echo "=========================================="
echo ""
echo "访问地址: http://$(hostname -I | awk '{print $1}'):8000"
echo ""
echo "常用命令:"
echo "  查看日志: tail -f $SCRIPT_DIR/backend/app.log"
echo "  停止服务: pkill -f 'uvicorn app.main:app'"
echo "  重启服务: cd $SCRIPT_DIR && ./deploy.sh"
echo ""
