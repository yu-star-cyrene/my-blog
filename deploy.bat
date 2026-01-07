@echo off
:: 设置字符集为 UTF-8，解决中文乱码
chcp 65001 > nul

echo [1/3] 正在同步本地更改...
git add .

echo [2/3] 正在提交更改 (自动化部署)...
:: 记录当前时间作为提交信息
git commit -m "自动化部署: %date% %time%"

echo [3/3] 正在上传至 GitHub...
:: 将代码推送到 main 分支
git push origin main

echo ---------------------------------------
echo [OK] 部署指令已发送！
echo 请等待 1-2 分钟，GitHub Actions 正在后台为你编译网站。
echo ---------------------------------------
pause