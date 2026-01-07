@echo off
chcp 65001 > nul
setlocal enabledelayedexpansion

:MENU
cls
echo ===========================================
echo         Sliver's 博客全能管理工具
echo ===========================================
echo  1. 新建文章 (支持置顶)
echo  2. 删除文章 (全目录智能搜索)
echo  3. 本地预览 (pnpm dev)
echo  4. 发布博客 (含 3 天历史清理)
echo  5. 退出
echo ===========================================
set /p opt="请选择操作序号: "

if "%opt%"=="1" goto NEW_POST
if "%opt%"=="2" goto DELETE_POST
if "%opt%"=="3" goto DEV
if "%opt%"=="4" goto DEPLOY
if "%opt%"=="5" exit
goto MENU

:NEW_POST
cls
set /p title="请输入文章标题: "
set /p sticky="是否置顶? (0为不置顶, 数字越大越靠前): "
set "filename=%title%.md"
set "filepath=src\content\posts\%filename%"
set "currentDate=%date:~0,4%-%date:~5,2%-%date:~8,2%"

echo --- > "%filepath%"
echo title: %title% >> "%filepath%"
echo published: %currentDate% >> "%filepath%"
echo description: '' >> "%filepath%"
echo image: '' >> "%filepath%"
echo tags: [] >> "%filepath%"
echo category: '未分类' >> "%filepath%"
echo sticky: %sticky% >> "%filepath%"
echo draft: false >> "%filepath%"
echo --- >> "%filepath%"
echo. >> "%filepath%"
echo ## 这里开始写正文 >> "%filepath%"
echo [成功] 文章已创建: %filepath%
pause
goto MENU

:DELETE_POST
cls
echo --- 当前所有文章列表 (含子目录) ---
set count=0
:: 递归搜索所有 .md 和 .mdx 文件
for /r "src\content\posts" %%f in (*.md *.mdx) do (
    set /a count+=1
    set "file!count!=%%f"
    :: 获取相对路径显示给用户
    set "fullp=%%f"
    set "relp=!fullp:*src\content\posts\=!"
    echo  [!count!] !relp!
)
echo ---------------------------------------
if %count%==0 (
    echo [!] 没找到任何文章。
    pause
    goto MENU
)

set /p del_num="请输入要删除的文章编号 (回车取消): "
if "%del_num%"=="" goto MENU

:: 执行删除逻辑
set "target=!file%del_num%!"
if "!target!"=="" (
    echo [错误] 编号不存在！
    pause
    goto DELETE_POST
)

echo.
echo [警告] 准备删除: !target!
set /p confirm="确定删除吗? (y/n): "
if /i "%confirm%"=="y" (
    del /f /q "!target!"
    echo [OK] 文件已删除。
    
    :: 自动清理空的子文件夹 (如 guide 文件夹)
    for /d /r "src\content\posts" %%d in (*) do (
        dir /b "%%d" | findstr "^" >nul || (
            rd "%%d"
            echo [OK] 已清理空文件夹: %%d
        )
    )
)
pause
goto MENU

:DEV
cls
echo 正在启动预览预览...
echo 访问地址: http://localhost:4321
start cmd /k "pnpm dev"
goto MENU

:DEPLOY
cls
echo [1/3] 添加更改...
git add .
echo [2/3] 提交更改 (自动化部署)...
git commit -m "自动化部署: %date% %time%"
echo [3/3] 推送到 GitHub...
git push origin main
echo [OK] 部署指令已发送，3天前记录将自动清理。
pause
goto MENU