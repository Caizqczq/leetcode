#!/bin/bash
# LeetCode Hot 100 管理工具 - 打包部署脚本

set -e

echo "=========================================="
echo "  LeetCode Hot 100 管理工具 - 打包部署"
echo "=========================================="

# 1. 打包前端
echo ""
echo "[1/3] 打包前端..."
cd frontend
npm install --silent
npm run build
echo "✓ 前端打包完成"

# 2. 复制前端文件到后端 static 目录
echo ""
echo "[2/3] 复制静态文件..."
cd ..
rm -rf backend/static
cp -r frontend/dist backend/static
echo "✓ 静态文件已复制到 backend/static"

# 3. 创建部署包
echo ""
echo "[3/3] 创建部署包..."
DEPLOY_DIR="leetcode-deploy"
rm -rf $DEPLOY_DIR
mkdir -p $DEPLOY_DIR

# 复制后端代码
cp -r backend/app $DEPLOY_DIR/
cp -r backend/static $DEPLOY_DIR/
cp backend/requirements.txt $DEPLOY_DIR/

# 创建启动脚本
cat > $DEPLOY_DIR/start.sh << 'EOF'
#!/bin/bash
# 启动服务

# 激活虚拟环境（如果存在）
if [ -d "venv" ]; then
    source venv/bin/activate
fi

# 启动服务（生产模式）
# --host 0.0.0.0 允许外部访问
# --workers 可根据 CPU 核心数调整
uvicorn app.main:app --host 0.0.0.0 --port 8000
EOF
chmod +x $DEPLOY_DIR/start.sh

# 创建安装脚本
cat > $DEPLOY_DIR/install.sh << 'EOF'
#!/bin/bash
# 安装依赖

echo "创建虚拟环境..."
python3 -m venv venv
source venv/bin/activate

echo "安装依赖..."
pip install -r requirements.txt

echo ""
echo "✓ 安装完成！"
echo ""
echo "启动服务: ./start.sh"
echo "访问地址: http://localhost:8000"
EOF
chmod +x $DEPLOY_DIR/install.sh

# 打包
tar -czf leetcode-deploy.tar.gz $DEPLOY_DIR
rm -rf $DEPLOY_DIR

echo "✓ 部署包已创建: leetcode-deploy.tar.gz"

echo ""
echo "=========================================="
echo "  打包完成！"
echo "=========================================="
echo ""
echo "部署步骤:"
echo "  1. 上传 leetcode-deploy.tar.gz 到服务器"
echo "  2. tar -xzf leetcode-deploy.tar.gz"
echo "  3. cd leetcode-deploy"
echo "  4. ./install.sh  # 安装依赖"
echo "  5. ./start.sh    # 启动服务"
echo ""
echo "服务将运行在 http://your-server:8000"
echo ""
