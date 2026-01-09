@echo off
chcp 65001 > nul

:MENU
cls
echo ===========================================
echo          余林阳博客管理工具
echo ===========================================
echo  1. 内容管理 (新建/置顶/评论/图片)
echo  2. 删除文章 (输入编号删除)
echo  3. 本地预览 (自动修端口)
echo  4. 发布博客 (自动备份 + 推送)
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
if not exist img_fixer.py (
    echo [错误] 没找到 img_fixer.py！
    pause
    goto MENU
)
python img_fixer.py
if %errorlevel% neq 0 (
    echo.
    echo [报错] Python 脚本出错了，看上面报错信息。
    pause
)
goto MENU

:DELETE_POST
cls
echo --- 文章列表 ---
set count=0
setlocal enabledelayedexpansion
for /r "src\content\posts" %%f in (*.md *.mdx) do (
    set /a count+=1
    set "file!count!=%%f"
    set "fullp=%%f"
    set "relp=!fullp:*src\content\posts\=!"
    echo  [!count!] !relp!
)
set /p del_num="输入要删除的编号 (回车取消): "
if "!del_num!"=="" goto MENU
if defined file%del_num% (
    set "target=!file%del_num%!"
    echo 正在删除: !target!
    del /f /q "!target!"
    echo [OK] 删除了。
) else (
    echo [错误] 编号不对。
)
pause
endlocal
goto MENU

:DEV
cls
echo 正在清理旧进程并启动预览...
taskkill /f /im node.exe >nul 2>&1
start "" http://localhost:4321
cmd /k "pnpm dev"
goto MENU

:DEPLOY
cls
echo ===========================================
echo        正在执行发布流程
echo ===========================================

:: --- 自动备份逻辑开始 ---
echo [1/3] 正在创建备份...
if not exist backups mkdir backups

:: 获取当前时间 (YYYYMMDD_HH)
for /f "tokens=2 delims==" %%I in ('wmic os get localdatetime /value') do set datetime=%%I
set "timestamp=%datetime:~0,4%%datetime:~4,2%%datetime:~6,2%_%datetime:~8,2%"

:: 使用 tar 打包 src 和 public 目录到 backups 文件夹
:: 文件名格式: backups\YYYYMMDD_HH.bak
tar -cf "backups\%timestamp%.bak" src public

echo [备份成功] 已保存到 backups\%timestamp%.bak
:: --- 自动备份逻辑结束 ---

echo.
echo [2/3] 添加文件...
git add .
echo [3/3] 提交并推送...
git commit -m "auto-deploy: %date% %time%"
git push origin main
echo.
echo [完成] 博客已发布！
pause
goto MENU