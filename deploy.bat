@echo off
echo [1/3] 正在添加更改...
git add .

echo [2/3] 正在提交更改 (自动化部署)...
git commit -m "自动化部署: %date% %time%"

echo [3/3] 正在推送到 GitHub...
git push origin main

echo ---------------------------------------
echo [OK] 部署指令已发送！请等待 1 分钟左右查看网站。
pause