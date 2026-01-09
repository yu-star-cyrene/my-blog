@echo off
chcp 65001 > nul

:MENU
cls
echo === 博客管理工具 ===
echo 1. 管理文章 (Python)
echo 2. 删除文章
echo 3. 本地预览
echo 4. 发布 (清理+备份+推送)
echo 5. 退出
echo ====================
set /p opt="选择: "

if "%opt%"=="1" goto PY_TOOL
if "%opt%"=="2" goto DEL_POST
if "%opt%"=="3" goto DEV
if "%opt%"=="4" goto DEPLOY
if "%opt%"=="5" exit
goto MENU

:PY_TOOL
cls
if not exist img_fixer.py echo [错] 缺 img_fixer.py & pause & goto MENU
python img_fixer.py
goto MENU

:DEL_POST
cls
setlocal enabledelayedexpansion
set i=0
for /r "src\content\posts" %%f in (*.md) do (
    set /a i+=1
    set "p!i!=%%f"
    echo [!i!] %%~nxf
)
set /p n="删除编号: "
if defined p%n% del "!p%n%!" & echo [删除了]
endlocal & pause & goto MENU

:DEV
cls
taskkill /f /im node.exe >nul 2>&1
start "" http://localhost:4321
cmd /k "pnpm dev"
goto MENU

:DEPLOY
cls
echo [1/4] 清理 .bak 垃圾文件...
del /s /q src\*.bak >nul 2>&1

echo [2/4] 备份到 C:\Users\G1731\Blog_Backups ...
set "BAK_DIR=C:\Users\G1731\Blog_Backups"
if not exist "%BAK_DIR%" mkdir "%BAK_DIR%"
for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value') do set t=%%I
set "name=%t:~0,8%_%t:~8,4%"
tar -cf "%BAK_DIR%\%name%.bak" src public

echo [3/4] 清理旧备份 (保留最新5个)...
pushd "%BAK_DIR%"
for /f "skip=5 delims=" %%F in ('dir *.bak /b /o-d /t:w') do del "%%F"
popd

echo [4/4] 提交 GitHub...
git add .
git commit -m "deploy: %date% %time%"
git push origin main
echo [完成]
pause
goto MENU