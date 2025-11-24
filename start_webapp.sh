#!/bin/bash

# 会议分析系统 - Web应用启动脚本

echo "======================================================================"
echo "           会议改善效果评估系统 - Web应用启动"
echo "======================================================================"
echo ""

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 Python3，请先安装 Python"
    exit 1
fi

# 检查Streamlit
if ! python3 -c "import streamlit" &> /dev/null; then
    echo "⚠️  未安装Streamlit，正在安装依赖..."
    pip3 install -r requirements.txt
fi

echo "🚀 启动Web应用..."
echo ""
echo "📊 应用将在浏览器中自动打开"
echo "🌐 访问地址: http://localhost:8501"
echo ""
echo "💡 提示："
echo "   - 停止应用: 按 Ctrl+C"
echo "   - 关闭此终端窗口将停止应用"
echo ""
echo "======================================================================"
echo ""

# 启动Streamlit应用
streamlit run app.py
