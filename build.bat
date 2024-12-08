@echo off
chcp 65001 > nul
setlocal EnableDelayedExpansion

echo ========================================
echo 开始构建 Excel智能检索系统
echo ========================================

:: 设置版本号
set VERSION=1.0.0

:: 设置路径
set BUILD_DIR=build
set DIST_DIR=dist
set OBFUSCATED_DIR=obfuscated
set RESOURCES_DIR=resources

echo 清理旧文件...
if exist %BUILD_DIR% rd /s /q %BUILD_DIR%
if exist %DIST_DIR% rd /s /q %DIST_DIR%
if exist %OBFUSCATED_DIR% rd /s /q %OBFUSCATED_DIR%

echo 创建目录...
mkdir %BUILD_DIR%
mkdir %DIST_DIR%
mkdir %OBFUSCATED_DIR%

echo ========================================
echo 开始代码混淆...
echo ========================================

:: 使用 pyarmor 6.8.1 的正确命令格式
pyarmor obfuscate ^
    -O %OBFUSCATED_DIR% ^
    -r ^
    run.py

if errorlevel 1 (
    echo 混淆失败！
    goto :error
)

echo 复制必要文件...
xcopy /E /I /Y resources %OBFUSCATED_DIR%\resources
xcopy /E /I /Y src %OBFUSCATED_DIR%\src
copy /Y app.rc %OBFUSCATED_DIR%\
copy /Y requirements.txt %OBFUSCATED_DIR%\
copy /Y config.json %OBFUSCATED_DIR%\

echo ========================================
echo 开始打包程序...
echo ========================================

cd %OBFUSCATED_DIR%

python -m nuitka ^
    --standalone ^
    --onefile ^
    --windows-icon-from-ico=resources/icon.ico ^
    --company-name="Excel智能检索系统" ^
    --product-name="Excel智能检索系统" ^
    --file-version=%VERSION% ^
    --product-version=%VERSION% ^
    --file-description="Excel智能检索系统" ^
    --windows-uac-admin ^
    --enable-plugin=pyqt6 ^
    --include-package=pandas ^
    --include-package=openpyxl ^
    --include-data-dir=resources=resources ^
    --windows-console-mode=disable ^
    --remove-output ^
    --assume-yes-for-downloads ^
    --static-libpython=no ^
    --disable-ccache ^
    --mingw64 ^
    --output-dir=..\%DIST_DIR% ^
    run.py

if errorlevel 1 (
    cd ..
    echo 打包失败！
    goto :error
)

cd ..

echo ========================================
echo 清理临时文件...
echo ========================================
rd /s /q %BUILD_DIR%
rd /s /q %OBFUSCATED_DIR%

echo ========================================
echo 构建完成！
echo 输出文件位置: %DIST_DIR%\run.exe
echo ========================================
goto :end

:error
echo ========================================
echo 构建过程中出现错误！
echo ========================================
exit /b 1

:end
pause