@echo off
chcp 65001 > nul
echo ===========================================
echo         Sliver's 博客管理工具
echo ===========================================
echo 1. 新建文章 (New Post)
echo 2. 发布博客 (Deploy)
echo 3. 退出 (Exit)
echo ===========================================
set /p opt="请选择操作序号: "

if %opt%==1 goto NEW_POST
if %opt%==2 goto DEPLOY
if %opt%==3 exit

:NEW_POST
set /p title="请输入文章标题: "
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
echo draft: false >> "%filepath%"
echo --- >> "%filepath%"
echo. >> "%filepath%"
echo ## 这里开始写正文 >> "%filepath%"

echo [成功] 文章已创建: %filepath%
pause
goto exit

:DEPLOY
echo [1/3] 正在添加更改...
git add .
echo [2/3] 正在提交 (自动化部署)...
git commit -m "自动化部署: %date% %time%"
echo [3/3] 正在上传至 GitHub...
git push origin main
echo [OK] 指令已发送！3 天前的旧任务将在部署后被自动清理。
pause
exit