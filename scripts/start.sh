#!/bin/bash

set -e

echo "====== 启动 GdutInfoHub ======"

# 启动后端
echo "🚀 启动后端..."
python -m src.app.app &

# 启动前端
echo "🚀 启动前端..."
cd gdut-info-hub
npm run dev
