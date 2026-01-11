@echo off
chcp 65001 > nul

:MENU
cls
echo ===========================================
echo          余林阳博客管理工具
echo ===========================================
echo  1. 进入内容管理 (新建/置顶/规范化/图片)
echo  2. 删除文章 (全目录搜索)
echo  3. 本地预览 (修复端口冲突)
echo  4. 发布博客 (Git Push)
echo  5. 退出
echo ===========================================
set /p opt="请选择序号: "

if "%opt%"=="1" goto CONTENT_TASK
if "%opt%"=="2" goto DELETE_POST
if "%opt%"=="3" goto DEV
if "%opt%"=="4" goto DEPLOY
if "%opt%"=="5" exit
goto MENU

:CONTENT_TASK
cls
:: 检查文件是否存在
if not exist img_fixer.py (
    echo [错误] 找不到 img_fixer.py 脚本！
    pause
    goto MENU
)
:: 运行并捕获错误
python img_fixer.py
if %errorlevel% neq 0 (
    echo.
    echo [报错] Python 脚本运行崩溃，请检查上方错误信息。
    pause
)
goto MENU

:DELETE_POST
cls
echo --- 文章列表 ---
set count=0
for /r "src\content\posts" %%f in (*.md *.mdx) do (
    set /a count+=1
    set "file!count!=%%f"
    set "fullp=%%f"
    set "relp=!fullp:*src\content\posts\=!"
    echo  [!count!] !relp!
)
set /p del_num="编号: "
if not "!file%del_num%!"=="" (
    del /f /q "!file%del_num%!"
    echo [OK] 已删除。
)
pause
goto MENU

:DEV
cls
taskkill /f /im node.exe >nul 2>&1
start "" http://localhost:4321
cmd /k "pnpm dev"
goto MENU

:DEPLOY
cls
git add .
git commit -m "update: %date% %time%"
git push origin main
pause
goto MENU