#!/bin/bash

set -e

echo "====== GdutInfoHub 环境初始化 (Linux/macOS) ======"

# 1. 检查命令是否存在
check_cmd () {
  if ! command -v $1 >/dev/null 2>&1; then
    echo "❌ 未检测到 $1，请先安装"
    exit 1
  fi
}

check_cmd node
check_cmd npm
check_cmd python
check_cmd pip

echo "✅ Node.js 版本: $(node -v)"
echo "✅ npm 版本: $(npm -v)"
echo "✅ Python 版本: $(python --version)"

# 2. 安装前端依赖
echo "📦 安装前端依赖..."
cd gdut-info-hub
npm install

# 3. 安装后端依赖
echo "📦 安装后端依赖..."
cd ..
pip install volcengine-python-sdk[ark] jieba flask

echo "🎉 环境初始化完成！"
echo "👉 运行：bash scripts/start.sh 启动项目"
