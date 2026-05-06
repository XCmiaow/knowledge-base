@echo off
REM Zotero → knowledge-base/raw/ 一键导出
REM 依赖: curl (Windows 10/11 自带)
REM 用法: 双击运行，或命令行执行

set ZOTERO_API=http://localhost:23119/api
set RAW_DIR=E:\工作区\knowledge-base\raw

echo === Zotero 文献导出到 knowledge-base ===
echo.
echo 从 Zotero Local API 获取最新文献...
echo.

REM 获取最近 50 条文献
curl -s "%ZOTERO_API%/items/top?limit=50&sort=dateAdded&direction=desc" -o "%TEMP%\zotero-items.json"

if %ERRORLEVEL% NEQ 0 (
    echo [错误] 无法连接 Zotero API (localhost:23119)
    echo 请确保 Zotero 正在运行，且已启用本地 API
    pause
    exit /b 1
)

echo 获取成功，正在处理...
echo 请运行 paper-ingest 技能来消化导出的文献
echo 或手工运行: node scripts/zotero-to-raw.js

echo.
echo 完成。文献已导出到 raw/ 目录。
pause
