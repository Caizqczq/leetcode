#!/bin/bash
# LeetCode Hot 100 管理工具 - 一键部署脚本
# 
# 用法:
#   ./deploy.sh          完整部署（打包+安装+启动）
#   ./deploy.sh -r       只重启服务
#   ./deploy.sh -s       停止服务
#   ./deploy.sh -l       查看日志
#   ./deploy.sh --status 查看服务状态
#   ./deploy.sh -h       显示帮助

set -e

# 获取脚本所在目录
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
BACKEND_DIR="$SCRIPT_DIR/backend"
LOG_FILE="$BACKEND_DIR/app.log"
SERVICE_CMD="uvicorn app.main:app"

# 颜色输出
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# 显示帮助
show_help() {
    echo "LeetCode Hot 100 管理工具 - 部署脚本"
    echo ""
    echo "用法: ./deploy.sh [选项]"
    echo ""
    echo "选项:"
    echo "  (无参数)     完整部署（打包前端+安装依赖+启动服务）"
    echo "  -r, --restart    只重启服务（不重新打包）"
    echo "  -s, --stop       停止服务"
    echo "  -l, --logs       查看实时日志"
    echo "  --status         查看服务状态"
    echo "  -h, --help       显示此帮助信息"
    echo ""
}

# 停止服务
stop_service() {
    if pgrep -f "$SERVICE_CMD" > /dev/null; then
        echo -e "${YELLOW}停止服务...${NC}"
        pkill -f "$SERVICE_CMD" || true
        sleep 2
        echo -e "${GREEN}✓ 服务已停止${NC}"
    else
        echo "服务未运行"
    fi
}

# 启动服务
start_service() {
    cd "$BACKEND_DIR"
    source venv/bin/activate
    
    echo -e "${YELLOW}启动服务...${NC}"
    nohup uvicorn app.main:app --host 0.0.0.0 --port 8000 > app.log 2>&1 &
    sleep 3
    
    if curl -s http://localhost:8000/api > /dev/null; then
        echo -e "${GREEN}✓ 服务启动成功${NC}"
        echo ""
        echo "访问地址: http://$(hostname -I | awk '{print $1}'):8000"
    else
        echo -e "${RED}✗ 服务启动失败，查看日志:${NC}"
        tail -20 "$LOG_FILE"
    fi
}

# 重启服务
restart_service() {
    echo "=========================================="
    echo "  重启服务"
    echo "=========================================="
    stop_service
    start_service
}

# 查看状态
show_status() {
    echo "=========================================="
    echo "  服务状态"
    echo "=========================================="
    if pgrep -f "$SERVICE_CMD" > /dev/null; then
        echo -e "${GREEN}● 服务运行中${NC}"
        echo ""
        echo "进程信息:"
        ps aux | grep "$SERVICE_CMD" | grep -v grep
        echo ""
        echo "访问地址: http://$(hostname -I | awk '{print $1}'):8000"
    else
        echo -e "${RED}● 服务未运行${NC}"
    fi
}

# 查看日志
show_logs() {
    if [ -f "$LOG_FILE" ]; then
        tail -f "$LOG_FILE"
    else
        echo "日志文件不存在: $LOG_FILE"
    fi
}

# 完整部署
full_deploy() {
    echo "=========================================="
    echo "  LeetCode Hot 100 - 完整部署"
    echo "=========================================="

    # 1. 打包前端
    echo ""
    echo -e "${YELLOW}[1/4] 打包前端...${NC}"
    cd "$SCRIPT_DIR/frontend"
    npm install --silent
    npm run build
    echo -e "${GREEN}✓ 前端打包完成${NC}"

    # 2. 复制静态文件
    echo ""
    echo -e "${YELLOW}[2/4] 复制静态文件...${NC}"
    rm -rf "$BACKEND_DIR/static"
    cp -r "$SCRIPT_DIR/frontend/dist" "$BACKEND_DIR/static"
    echo -e "${GREEN}✓ 静态文件已复制${NC}"

    # 3. 安装依赖
    echo ""
    echo -e "${YELLOW}[3/4] 安装后端依赖...${NC}"
    cd "$BACKEND_DIR"
    
    if [ ! -d "venv" ]; then
        echo "创建虚拟环境..."
        python3 -m venv venv
    fi
    
    source venv/bin/activate
    pip install --upgrade pip -q
    pip install -r requirements.txt -q
    echo -e "${GREEN}✓ 依赖安装完成${NC}"

    # 4. 启动服务
    echo ""
    echo -e "${YELLOW}[4/4] 启动服务...${NC}"
    stop_service
    start_service

    echo ""
    echo "=========================================="
    echo -e "${GREEN}  部署完成！${NC}"
    echo "=========================================="
    echo ""
    echo "常用命令:"
    echo "  ./deploy.sh -r      重启服务"
    echo "  ./deploy.sh -s      停止服务"
    echo "  ./deploy.sh -l      查看日志"
    echo "  ./deploy.sh --status 查看状态"
    echo ""
}

# 主逻辑
case "${1:-}" in
    -h|--help)
        show_help
        ;;
    -r|--restart)
        restart_service
        ;;
    -s|--stop)
        stop_service
        ;;
    -l|--logs)
        show_logs
        ;;
    --status)
        show_status
        ;;
    "")
        full_deploy
        ;;
    *)
        echo -e "${RED}未知参数: $1${NC}"
        echo ""
        show_help
        exit 1
        ;;
esac
