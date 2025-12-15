Write-Host "====== 启动 GdutInfoHub ======"

# 启动后端（新窗口）
Write-Host "🚀 启动后端..."
Start-Process powershell -ArgumentList "python -m src.app.app"

# 启动前端
Write-Host "🚀 启动前端..."
Set-Location gdut-info-hub
npm run dev
