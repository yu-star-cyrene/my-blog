@echo off
:: 解决中文乱码问题
chcp 65001 > nul
setlocal enabledelayedexpansion

:MENU
cls
echo ===========================================
echo          Sliver's 博客终极管理工具
echo ===========================================
echo  1. 新建文章
echo  2. 删除文章 (全目录智能搜索)
echo  3. 修改文章属性 (封面/置顶/标题/搬运)
echo  4. 修改站名 (Site Title)
echo  5. 本地预览 (修复端口冲突)
echo  6. 发布博客 (含 3 天历史清理)
echo  7. 退出
echo ===========================================
set /p opt="请选择序号: "

if "%opt%"=="1" goto NEW_POST
if "%opt%"=="2" goto DELETE_POST
if "%opt%"=="3" goto EDIT_POST
if "%opt%"=="4" goto SITE_SETTING
if "%opt%"=="5" goto DEV
if "%opt%"=="6" goto DEPLOY
if "%opt%"=="7" exit
goto MENU

:NEW_POST
cls
set /p title="标题: "
set "filepath=src\content\posts\%title%.md"
echo --- > "%filepath%"
echo title: %title% >> "%filepath%"
echo published: %date:~0,10% >> "%filepath%"
:: 修正：使用主题支持的 pinned 字段
echo pinned: false >> "%filepath%"
echo image: '' >> "%filepath%"
echo --- >> "%filepath%"
echo ## 正文开始 >> "%filepath%"
echo [OK] 已创建文章。
pause
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

:EDIT_POST
:: 调用 Python 稳定处理
python img_fixer.py
goto MENU

:SITE_SETTING
cls
set /p nst="新站名: "
powershell -Command "(gc src/config/siteConfig.ts) -replace 'title: \'.*\'', 'title: ''%nst%''' | Out-File -encoding utf8 src/config/siteConfig.ts"
goto MENU

:DEV
cls
echo [1/2] 正在清理 4321 端口占用...
taskkill /f /im node.exe >nul 2>&1
echo [2/2] 启动预览: http://localhost:4321
start "博客预览" cmd /k "pnpm dev"
pause
goto MENU

:DEPLOY
cls
git add .
git commit -m "自动化部署: %date% %time%"
git push origin main
echo [OK] 部署指令已发送。
pause
goto MENU