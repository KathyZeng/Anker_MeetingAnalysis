#!/bin/bash

echo "======================================================================"
echo "         会议改善效果评估系统 - Web应用 V2"
echo "======================================================================"
echo ""
echo "🚀 启动Web应用V2..."
echo ""
echo "📊 应用将在浏览器中自动打开"
echo "🌐 访问地址: http://localhost:8502"
echo ""
echo "💡 提示："
echo "   - 停止应用: 按 Ctrl+C"
echo "   - 关闭此终端窗口将停止应用"
echo ""
echo "======================================================================"
echo ""

# 启动streamlit
STREAMLIT_SERVER_HEADLESS=true python3 -m streamlit run app_v2.py \
    --server.port 8502 \
    --server.headless true \
    --browser.gatherUsageStats false

# 如果失败，尝试备用方式
if [ $? -ne 0 ]; then
    echo ""
    echo "⚠️  启动失败，尝试备用方式..."
    python3 -m streamlit run app_v2.py --server.port 8502
fi
