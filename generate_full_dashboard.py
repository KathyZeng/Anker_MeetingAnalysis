#!/usr/bin/env python3
"""
完整交互式仪表盘生成器
按照《可视化报表页面设计方案.md》实现四大模块
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'meeting_analysis'))

from meeting_analysis.data_loader import MeetingDataLoader
from meeting_analysis.calculator import MeetingMetricsCalculator
from meeting_analysis.analyzer import MeetingDataAnalyzer
from meeting_analysis.dashboard_generator import InteractiveDashboardGenerator
from meeting_analysis.full_dashboard_gen import FullDashboardGenerator


def main():
    print("=" * 70)
    print("        会议改善效果评估 - 完整交互式仪表盘生成器")
    print("=" * 70)

    # 1. 加载数据
    print("\n[1/4] 加载数据...")
    data_loader = MeetingDataLoader("input")
    all_data = data_loader.load_all_data()

    if all_data is None or all_data.empty:
        print("❌ 数据加载失败")
        return

    baseline = data_loader.get_baseline_data()
    current = data_loader.get_recent_weeks_data(4)

    if baseline is None or current is None:
        print("❌ 基线期或当前期数据缺失")
        return

    print(f"   ✓ 已加载 {len(all_data)} 条记录")
    print(f"   ✓ 基线期: {len(baseline)} 条")
    print(f"   ✓ 当前期: {len(current)} 条")

    # 2. 准备数据
    print("\n[2/4] 准备分析数据...")
    calculator = MeetingMetricsCalculator(baseline, current)
    analyzer = MeetingDataAnalyzer(all_data)

    dashboard_gen = InteractiveDashboardGenerator(data_loader, calculator, analyzer)
    dashboard_data = dashboard_gen.prepare_data()

    print(f"   ✓ KPI指标: {len(dashboard_data['kpis'])} 组")
    print(f"   ✓ Top10用户: {len(dashboard_data['top10_users'])} 人")
    print(f"   ✓ 异常检测: {len(dashboard_data['anomalies'])} 个")
    print(f"   ✓ 原始数据: {len(dashboard_data['raw_data'])} 条")
    print(f"   ✓ 周期对比: {len(dashboard_data['period_comparison'])} 个周期")

    # 3. 生成完整仪表盘
    print("\n[3/4] 生成完整HTML仪表盘...")
    full_gen = FullDashboardGenerator("output")
    output_file = full_gen.generate(dashboard_data)

    print(f"   ✓ 仪表盘生成成功")

    # 4. 生成数据报告
    print("\n[4/4] 生成数据统计...")
    kpis = dashboard_data['kpis'].get('主要KPI', {})
    达标数 = sum(1 for kpi in kpis.values() if kpi.get('达标', False))
    总数 = len(kpis)

    print(f"   ✓ KPI达标情况: {达标数}/{总数}")
    print(f"   ✓ 高频用户: {len(dashboard_data['user_tiers'].get('high', []))} 人")
    print(f"   ✓ 中频用户: {len(dashboard_data['user_tiers'].get('medium', []))} 人")
    print(f"   ✓ 低频用户: {len(dashboard_data['user_tiers'].get('low', []))} 人")

    # 完成
    print("\n" + "=" * 70)
    print("✅ 完整仪表盘生成完成!")
    print("=" * 70)
    print(f"\n📄 文件位置: {output_file}")
    print(f"🌐 打开方式: open {output_file}")
    print(f"📊 包含模块: 概览页面 | 原始数据 | 分析结果 | 人员详情")
    print("\n" + "=" * 70)


if __name__ == "__main__":
    main()
