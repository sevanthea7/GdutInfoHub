Write-Host "====== GdutInfoHub 环境初始化 (Windows) ======"

function Check-Cmd {
    param ($cmd)
    if (-not (Get-Command $cmd -ErrorAction SilentlyContinue)) {
        Write-Host "❌ 未检测到 $cmd，请先安装" -ForegroundColor Red
        exit 1
    }
}

Check-Cmd node
Check-Cmd npm
Check-Cmd python
Check-Cmd pip

Write-Host "✅ Node.js 版本:" (node -v)
Write-Host "✅ npm 版本:" (npm -v)
Write-Host "✅ Python 版本:" (python --version)

# 前端依赖
Write-Host "📦 安装前端依赖..."
Set-Location gdut-info-hub
npm install

# 后端依赖
Write-Host "📦 安装后端依赖..."
Set-Location ..
pip install volcengine-python-sdk[ark] jieba flask

Write-Host "🎉 环境初始化完成！"
Write-Host "👉 运行：scripts\\start.ps1 启动项目"
