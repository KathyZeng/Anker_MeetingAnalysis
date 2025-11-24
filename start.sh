#!/bin/bash

# 会议改善效果评估系统 V2 - 启动脚本

echo "🚀 正在启动会议改善效果评估系统 V2..."

# 检查端口是否被占用
if lsof -Pi :8502 -sTCP:LISTEN -t >/dev/null 2>&1 ; then
    echo "⚠️  端口 8502 已被占用，正在清理..."
    lsof -ti:8502 | xargs kill -9 2>/dev/null
    sleep 2
fi

# 启动应用
echo "✅ 启动应用中..."
python3 -m streamlit run app_v2.py --server.port 8502 --server.headless true --browser.gatherUsageStats false

echo "✅ 应用已启动！"
echo "📍 访问地址: http://localhost:8502"
