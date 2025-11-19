#!/usr/bin/env python3
"""
会议改善效果评估 - 主执行脚本
提供完整的分析流程,从数据加载到报告生成
"""

import argparse
import sys
from datetime import datetime

from data_loader import MeetingDataLoader
from calculator import MeetingMetricsCalculator
from analyzer import MeetingDataAnalyzer
from visualizer import MeetingVisualizer
from reporter import MeetingReportGenerator
from html_generator_v2 import HTMLDashboardGeneratorV2


def print_banner():
    """打印横幅"""
    banner = """
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║        会议改善效果评估系统 v1.0                              ║
║        Meeting Improvement Evaluation System                ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝
    """
    print(banner)


def run_full_analysis(data_dir="input", output_dir="output", verbose=True):
    """
    运行完整分析流程

    Args:
        data_dir: 数据目录
        output_dir: 输出目录
        verbose: 是否显示详细信息

    Returns:
        dict: 分析结果
    """
    results = {}

    # ====== 步骤1: 数据加载 ======
    if verbose:
        print("\n" + "=" * 60)
        print("步骤 1/5: 数据加载")
        print("=" * 60)

    loader = MeetingDataLoader(data_dir)
    all_data = loader.load_all_data()

    if all_data is None:
        print("\n❌ 数据加载失败,请检查数据文件")
        return None

    results['data_loader'] = loader
    results['all_data'] = all_data

    # 获取基线期和当前期数据
    baseline_data = loader.get_baseline_data()
    current_data = loader.get_recent_weeks_data(4)

    if baseline_data is None or baseline_data.empty:
        print("\n❌ 未找到基线期数据(9月和10月)")
        return None

    if current_data is None or current_data.empty:
        print("\n❌ 未找到当前期数据(最近4周)")
        return None

    if verbose:
        print(f"\n✓ 基线期数据: {len(baseline_data)} 条记录")
        print(f"✓ 当前期数据: {len(current_data)} 条记录")

    results['baseline_data'] = baseline_data
    results['current_data'] = current_data

    # ====== 步骤2: KPI指标计算 ======
    if verbose:
        print("\n" + "=" * 60)
        print("步骤 2/5: KPI指标计算")
        print("=" * 60)

    calculator = MeetingMetricsCalculator(baseline_data, current_data)
    weekly_data = loader.get_data_by_period_type('weekly')
    kpi_results = calculator.calculate_all_kpis(weekly_data)

    results['kpi_results'] = kpi_results

    if verbose:
        # 显示主要KPI达标情况
        primary_kpis = kpi_results.get('主要KPI', {})
        print("\n主要KPI达标情况:")
        for kpi_name, kpi_data in primary_kpis.items():
            达标 = kpi_data.get('达标', False)
            icon = "✓" if 达标 else "✗"
            print(f"  {icon} {kpi_name}")

    # ====== 步骤3: 统计分析 ======
    if verbose:
        print("\n" + "=" * 60)
        print("步骤 3/5: 统计分析")
        print("=" * 60)

    analyzer = MeetingDataAnalyzer(all_data)

    # 趋势分析
    trend_analysis = {}
    metrics = ['日人均线上会议数', '日人均线上会议时长(分钟)']
    for metric in metrics:
        trend_analysis[metric] = analyzer.analyze_trend(metric)
        if verbose and 'error' not in trend_analysis[metric]:
            direction = trend_analysis[metric]['direction']
            change_rate = trend_analysis[metric]['change_rate']
            print(f"\n✓ {metric} 趋势: {direction} (变化率: {change_rate:.2f}%)")

    results['trend_analysis'] = trend_analysis

    # 异常检测
    anomalies = analyzer.detect_anomalies('日人均线上会议数', threshold=2.0)
    results['anomalies'] = anomalies

    if verbose:
        if not anomalies.empty:
            print(f"\n⚠️  检测到 {len(anomalies)} 个异常数据点")
        else:
            print("\n✓ 未检测到异常")

    # Top用户分析
    top_users = analyzer.identify_top_users('日人均线上会议数', n=10)
    results['top_users'] = top_users

    if verbose:
        print(f"\n✓ 识别Top 10会议用户")

    # ====== 步骤4: 可视化 ======
    if verbose:
        print("\n" + "=" * 60)
        print("步骤 4/5: 可视化生成")
        print("=" * 60)

    visualizer = MeetingVisualizer(output_dir)

    # 趋势图
    period_data = all_data.groupby('period_name')['日人均线上会议数'].mean().reset_index()
    trend_file = visualizer.plot_trend_line(
        period_data,
        'period_name',
        '日人均线上会议数',
        '日人均会议数趋势',
        '周期',
        '日人均会议数',
        'trend_meetings.png'
    )
    if verbose:
        print(f"\n✓ 趋势图: {trend_file}")

    # 对比图
    categories = ['日人均会议数', '日人均会议时长']
    baseline_vals = [
        baseline_data['日人均线上会议数'].mean(),
        baseline_data['日人均线上会议时长(分钟)'].mean()
    ]
    current_vals = [
        current_data['日人均线上会议数'].mean(),
        current_data['日人均线上会议时长(分钟)'].mean()
    ]
    comparison_file = visualizer.plot_comparison_bar(
        categories,
        baseline_vals,
        current_vals,
        '基线期 vs 当前期对比',
        '数值',
        'comparison.png'
    )
    if verbose:
        print(f"✓ 对比图: {comparison_file}")

    # 仪表盘摘要
    dashboard_file = visualizer.create_dashboard_summary(kpi_results)
    if verbose:
        print(f"✓ 仪表盘摘要: {dashboard_file}")

    results['visualizer'] = visualizer

    # ====== 步骤5: 报告生成 ======
    if verbose:
        print("\n" + "=" * 60)
        print("步骤 5/5: 报告生成")
        print("=" * 60)

    reporter = MeetingReportGenerator(output_dir)

    # 管理层摘要报告
    exec_report = reporter.generate_executive_summary(kpi_results)
    if verbose:
        print(f"\n✓ 管理层摘要: {exec_report}")

    # 详细分析报告
    detail_report = reporter.generate_detailed_report(
        kpi_results,
        trend_analysis,
        anomalies,
        top_users
    )
    if verbose:
        print(f"✓ 详细报告: {detail_report}")

    # 周报 (生成最近一周的)
    periods = loader.get_period_list()
    if periods:
        latest_period = periods[-1]['period_name']
        week_data = loader.get_data_by_period(latest_period)
        weekly_report = reporter.generate_weekly_summary(week_data, latest_period)
        if verbose:
            print(f"✓ 周报: {weekly_report}")

    results['reporter'] = reporter

    # ====== 步骤6: 生成HTML仪表盘 ======
    if verbose:
        print("\n" + "=" * 60)
        print("步骤 6/6: 生成HTML仪表盘")
        print("=" * 60)

    html_generator = HTMLDashboardGeneratorV2(output_dir)
    html_dashboard = html_generator.generate_dashboard(
        kpi_results,
        trend_analysis,
        len(anomalies),
        len(top_users)
    )
    if verbose:
        print(f"\n✓ HTML仪表盘: {html_dashboard}")

    results['html_generator'] = html_generator

    # ====== 完成 ======
    if verbose:
        print("\n" + "=" * 60)
        print("✅ 分析完成!")
        print("=" * 60)
        print(f"\n所有输出文件已保存至: {output_dir}/")
        print("\n主要文件:")
        print(f"  - {output_dir}/dashboard.html             (🌟 交互式仪表盘)")
        print(f"  - {output_dir}/executive_summary.md       (管理层摘要)")
        print(f"  - {output_dir}/detailed_report.md         (详细分析)")
        print(f"  - {output_dir}/dashboard_summary.txt      (仪表盘文本)")
        print(f"  - {output_dir}/trend_meetings.png         (趋势图)")
        print(f"  - {output_dir}/comparison.png             (对比图)")
        print(f"\n💡 在浏览器中打开: open {output_dir}/dashboard.html")

    return results


def run_quick_summary(data_dir="input"):
    """
    快速摘要模式 - 仅显示关键指标

    Args:
        data_dir: 数据目录
    """
    print("\n" + "=" * 60)
    print("快速摘要模式")
    print("=" * 60)

    # 加载数据
    loader = MeetingDataLoader(data_dir)
    all_data = loader.load_all_data()

    if all_data is None:
        print("\n❌ 数据加载失败")
        return

    baseline_data = loader.get_baseline_data()
    current_data = loader.get_recent_weeks_data(4)

    if baseline_data is None or current_data is None:
        print("\n❌ 缺少基线期或当前期数据")
        return

    # 计算KPI
    calculator = MeetingMetricsCalculator(baseline_data, current_data)
    weekly_data = loader.get_data_by_period_type('weekly')
    kpi_results = calculator.calculate_all_kpis(weekly_data)

    # 显示主要KPI
    print("\n【主要KPI】")
    print("-" * 60)
    for kpi_name, kpi_data in kpi_results.get('主要KPI', {}).items():
        达标 = kpi_data.get('达标', False)
        icon = "✅" if 达标 else "❌"
        print(f"\n{icon} {kpi_name}")

        for key, value in kpi_data.items():
            if key == '达标':
                continue
            if isinstance(value, float):
                print(f"  {key}: {value:.2f}")
            else:
                print(f"  {key}: {value}")

    # 统计达标情况
    total_达标 = sum(1 for kpi in kpi_results['主要KPI'].values() if kpi.get('达标', False))
    total_count = len(kpi_results['主要KPI'])

    print("\n" + "=" * 60)
    print(f"达标情况: {total_达标}/{total_count}")
    print("=" * 60)


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='会议改善效果评估系统')

    parser.add_argument(
        '--mode',
        choices=['full', 'quick'],
        default='full',
        help='运行模式: full=完整分析, quick=快速摘要 (默认: full)'
    )

    parser.add_argument(
        '--data-dir',
        default='input',
        help='数据目录路径 (默认: input)'
    )

    parser.add_argument(
        '--output-dir',
        default='output',
        help='输出目录路径 (默认: output)'
    )

    parser.add_argument(
        '--quiet',
        action='store_true',
        help='静默模式,减少输出信息'
    )

    args = parser.parse_args()

    # 打印横幅
    if not args.quiet:
        print_banner()
        print(f"开始时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    try:
        if args.mode == 'quick':
            run_quick_summary(args.data_dir)
        else:
            run_full_analysis(
                data_dir=args.data_dir,
                output_dir=args.output_dir,
                verbose=not args.quiet
            )

        if not args.quiet:
            print(f"\n结束时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    except Exception as e:
        print(f"\n❌ 执行出错: {str(e)}")
        if not args.quiet:
            import traceback
            traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
