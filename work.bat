@echo off
:: 设置为 UTF-8 运行环境
chcp 65001 > nul

:MENU
cls
echo ===========================================
echo         Sliver's 博客终极管理工具
echo ===========================================
echo  1. 新建文章
echo  2. 删除文章
echo  3. 修改属性 (置顶/标题)
echo  4. 修改站名 (Site Title)
echo  5. 修复并搬运图片 (Python 稳定版)
echo  6. 本地预览 (pnpm dev)
echo  7. 发布博客 (含历史清理)
echo  8. 退出
echo ===========================================
set /p opt="请选择序号: "

if "%opt%"=="1" goto NEW_POST
if "%opt%"=="2" goto DELETE_POST
if "%opt%"=="3" goto EDIT_POST
if "%opt%"=="4" goto SITE_SETTING
if "%opt%"=="5" goto FIX_IMAGES
if "%opt%"=="6" goto DEV
if "%opt%"=="7" goto DEPLOY
if "%opt%"=="8" exit
goto MENU

:FIX_IMAGES
:: 直接调用 Python 脚本，稳定、报错清晰、支持所有特殊路径
python img_fixer.py
goto MENU

:DEV
start cmd /k "pnpm dev"
goto MENU

:DEPLOY
git add .
git commit -m "自动化部署: %date% %time%"
git push origin main
pause
goto MENU

:: ... [此处接你之前的 NEW_POST, DELETE_POST 逻辑，保持不变] ...