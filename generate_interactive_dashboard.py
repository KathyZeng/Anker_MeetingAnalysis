#!/usr/bin/env python3
"""生成交互式仪表盘"""

import sys
sys.path.insert(0, 'meeting_analysis')

from dashboard_generator import InteractiveDashboardGenerator
from data_loader import MeetingDataLoader
from calculator import MeetingMetricsCalculator
from analyzer import MeetingDataAnalyzer

# 加载数据
loader = MeetingDataLoader('input')
all_data = loader.load_all_data()

if all_data is None or all_data.empty:
    print("❌ 数据加载失败")
    sys.exit(1)

# 获取基线期和当前期数据
baseline = loader.get_baseline_data()
current = loader.get_recent_weeks_data(4)

# 创建计算器和分析器
calculator = MeetingMetricsCalculator(baseline, current)
analyzer = MeetingDataAnalyzer(all_data)

# 生成交互式仪表盘
print("开始生成交互式仪表盘...")
generator = InteractiveDashboardGenerator(loader, calculator, analyzer)
output_file = generator.generate_html('output/interactive_dashboard.html')

print(f"✅ 交互式仪表盘已生成: {output_file}")
print(f"\n💡 在浏览器中打开: open {output_file}")
