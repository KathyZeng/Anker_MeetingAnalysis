#!/usr/bin/env python3
"""
报告生成模块
生成各类格式的分析报告(Markdown, HTML, PDF等)
"""

import pandas as pd
from typing import Dict, List
from datetime import datetime
import os


class MeetingReportGenerator:
    """会议分析报告生成器"""

    def __init__(self, output_dir: str = "output"):
        """
        初始化报告生成器

        Args:
            output_dir: 输出目录
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def generate_executive_summary(self, kpi_results: Dict, filename: str = "executive_summary.md") -> str:
        """
        生成管理层摘要报告

        Args:
            kpi_results: KPI计算结果
            filename: 文件名

        Returns:
            str: 报告文件路径
        """
        lines = []

        # 标题
        lines.append("# 会议改善效果评估 - 管理层摘要报告")
        lines.append("")
        lines.append(f"**报告生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")
        lines.append("---")
        lines.append("")

        # 核心结论
        lines.append("## 📊 核心结论")
        lines.append("")

        # 统计达标情况
        primary_kpis = kpi_results.get('主要KPI', {})
        total_达标 = sum(1 for kpi in primary_kpis.values() if kpi.get('达标', False))
        total_count = len(primary_kpis)

        lines.append(f"**主要KPI达标情况**: {total_达标}/{total_count} 项达标")
        lines.append("")

        if total_达标 == total_count:
            lines.append("✅ **评估结论**: 会议改善措施效果显著,所有主要KPI均已达标!")
        elif total_达标 >= total_count / 2:
            lines.append("⚠️ **评估结论**: 会议改善措施取得一定成效,部分KPI已达标,仍需持续优化")
        else:
            lines.append("❌ **评估结论**: 会议改善效果不明显,需要重新审视改善措施并加强执行")

        lines.append("")
        lines.append("---")
        lines.append("")

        # 主要KPI详情
        lines.append("## 🎯 主要KPI指标")
        lines.append("")

        for kpi_name, kpi_data in primary_kpis.items():
            达标 = kpi_data.get('达标', False)
            status_icon = "✅" if 达标 else "❌"

            lines.append(f"### {status_icon} {kpi_name}")
            lines.append("")

            # 创建表格
            lines.append("| 指标 | 数值 |")
            lines.append("|------|------|")

            for key, value in kpi_data.items():
                if key == '达标':
                    continue
                if isinstance(value, float):
                    lines.append(f"| {key} | {value:.2f} |")
                else:
                    lines.append(f"| {key} | {value} |")

            lines.append("")

        # 次要KPI概览
        lines.append("---")
        lines.append("")
        lines.append("## 📈 次要KPI概览")
        lines.append("")

        secondary_kpis = kpi_results.get('次要KPI', {})
        for kpi_name, kpi_data in secondary_kpis.items():
            达标 = kpi_data.get('达标', False)
            status_icon = "✅" if 达标 else "⚠️"

            # 构建完整的行
            line_text = f"- {status_icon} **{kpi_name}**: "

            # 提取关键值
            if '改善率(%)' in kpi_data:
                line_text += f"改善率 {kpi_data['改善率(%)']:.1f}%"
            elif '效率提升(%)' in kpi_data:
                line_text += f"效率提升 {kpi_data['效率提升(%)']:.1f}%"
            elif '替代率(%)' in kpi_data:
                line_text += f"替代率 {kpi_data['替代率(%)']:.1f}%"

            lines.append(line_text)
            lines.append("")

        # 监控指标
        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("## 🔍 监控指标")
        lines.append("")

        monitoring = kpi_results.get('监控指标', {})
        for indicator_name, indicator_data in monitoring.items():
            lines.append(f"### {indicator_name}")
            lines.append("")
            lines.append("| 指标 | 数值 |")
            lines.append("|------|------|")

            for key, value in indicator_data.items():
                if isinstance(value, bool):
                    value_str = "✓ 是" if value else "✗ 否"
                elif isinstance(value, float):
                    value_str = f"{value:.2f}"
                else:
                    value_str = str(value)
                lines.append(f"| {key} | {value_str} |")

            lines.append("")

        # 行动建议
        lines.append("---")
        lines.append("")
        lines.append("## 💡 行动建议")
        lines.append("")

        if total_达标 == total_count:
            lines.append("1. **巩固成果**: 继续保持当前的会议管理机制,避免反弹")
            lines.append("2. **经验总结**: 总结固定会议窗口等有效措施,形成最佳实践")
            lines.append("3. **持续监控**: 保持每周监控,关注波动性指标")
        else:
            lines.append("1. **重点改进**: 针对未达标的KPI制定专项改善计划")
            lines.append("2. **强化执行**: 加强对固定会议窗口制度的宣贯和执行监督")
            lines.append("3. **个性化辅导**: 针对Top 10重度会议用户进行一对一辅导")
            lines.append("4. **工具优化**: 评估是否需要优化日程管理工具和会议室预订流程")

        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("*本报告由会议分析系统自动生成*")

        # 保存报告
        content = '\n'.join(lines)
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        return filepath

    def generate_detailed_report(self, kpi_results: Dict, trend_analysis: Dict,
                                anomalies: pd.DataFrame, top_users: pd.DataFrame,
                                filename: str = "detailed_report.md") -> str:
        """
        生成详细分析报告

        Args:
            kpi_results: KPI结果
            trend_analysis: 趋势分析结果
            anomalies: 异常数据
            top_users: Top用户数据
            filename: 文件名

        Returns:
            str: 文件路径
        """
        lines = []

        # 标题
        lines.append("# 会议改善效果评估 - 详细分析报告")
        lines.append("")
        lines.append(f"**报告生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")
        lines.append("---")
        lines.append("")

        # 目录
        lines.append("## 📑 目录")
        lines.append("")
        lines.append("1. [KPI指标详情](#kpi指标详情)")
        lines.append("2. [趋势分析](#趋势分析)")
        lines.append("3. [异常检测](#异常检测)")
        lines.append("4. [Top用户分析](#top用户分析)")
        lines.append("5. [改善建议](#改善建议)")
        lines.append("")
        lines.append("---")
        lines.append("")

        # 1. KPI指标详情
        lines.append("## KPI指标详情")
        lines.append("")

        lines.append("### 主要KPI")
        lines.append("")
        for kpi_name, kpi_data in kpi_results.get('主要KPI', {}).items():
            lines.append(f"#### {kpi_name}")
            lines.append("")
            lines.append("```")
            for key, value in kpi_data.items():
                if isinstance(value, float):
                    lines.append(f"{key:30s}: {value:>10.2f}")
                elif isinstance(value, bool):
                    lines.append(f"{key:30s}: {('✓ 是' if value else '✗ 否'):>10s}")
                else:
                    lines.append(f"{key:30s}: {str(value):>10s}")
            lines.append("```")
            lines.append("")

        lines.append("### 次要KPI")
        lines.append("")
        for kpi_name, kpi_data in kpi_results.get('次要KPI', {}).items():
            lines.append(f"#### {kpi_name}")
            lines.append("")
            lines.append("```")
            for key, value in kpi_data.items():
                if isinstance(value, float):
                    lines.append(f"{key:30s}: {value:>10.2f}")
                elif isinstance(value, bool):
                    lines.append(f"{key:30s}: {('✓ 是' if value else '✗ 否'):>10s}")
                else:
                    lines.append(f"{key:30s}: {str(value):>10s}")
            lines.append("```")
            lines.append("")

        # 2. 趋势分析
        lines.append("---")
        lines.append("")
        lines.append("## 趋势分析")
        lines.append("")

        for metric_name, trend_data in trend_analysis.items():
            if 'error' in trend_data:
                continue

            lines.append(f"### {metric_name}")
            lines.append("")
            lines.append(f"- **趋势方向**: {trend_data.get('direction', 'unknown')}")
            lines.append(f"- **变化率**: {trend_data.get('change_rate', 0):.2f}%")
            lines.append(f"- **R² 拟合度**: {trend_data.get('r_squared', 0):.4f}")
            lines.append(f"- **起始值**: {trend_data.get('first_value', 0):.2f}")
            lines.append(f"- **结束值**: {trend_data.get('last_value', 0):.2f}")
            lines.append("")

        # 3. 异常检测
        lines.append("---")
        lines.append("")
        lines.append("## 异常检测")
        lines.append("")

        if anomalies is not None and not anomalies.empty:
            lines.append(f"检测到 **{len(anomalies)}** 个异常数据点:")
            lines.append("")
            lines.append(anomalies.to_markdown(index=False))
        else:
            lines.append("✅ 未检测到明显异常")

        lines.append("")

        # 4. Top用户分析
        lines.append("---")
        lines.append("")
        lines.append("## Top用户分析")
        lines.append("")

        if top_users is not None and not top_users.empty:
            lines.append("### Top 10 会议最多的用户")
            lines.append("")
            lines.append(top_users.to_markdown(index=False))
            lines.append("")
        else:
            lines.append("无数据")
            lines.append("")

        # 5. 改善建议
        lines.append("---")
        lines.append("")
        lines.append("## 改善建议")
        lines.append("")

        # 基于KPI达标情况生成建议
        primary_kpis = kpi_results.get('主要KPI', {})
        未达标_kpis = [name for name, data in primary_kpis.items() if not data.get('达标', False)]

        if not 未达标_kpis:
            lines.append("### ✅ 整体表现优秀")
            lines.append("")
            lines.append("所有主要KPI均已达标,建议:")
            lines.append("")
            lines.append("1. 继续保持当前的会议管理实践")
            lines.append("2. 定期监控波动性,防止反弹")
            lines.append("3. 将成功经验推广到其他团队")
        else:
            lines.append("### ⚠️ 需要重点改进的领域")
            lines.append("")
            for kpi_name in 未达标_kpis:
                lines.append(f"#### {kpi_name}")
                lines.append("")

                if "会议数" in kpi_name:
                    lines.append("**建议措施**:")
                    lines.append("- 严格执行会议审批制度")
                    lines.append("- 推广异步沟通工具使用")
                    lines.append("- 优化会议邀请人员范围")
                elif "会议时长" in kpi_name:
                    lines.append("**建议措施**:")
                    lines.append("- 强制要求会议设置明确议程")
                    lines.append("- 推行30分钟和45分钟标准会议时长")
                    lines.append("- 培训主持人会议管理技巧")
                elif "即时会议" in kpi_name:
                    lines.append("**建议措施**:")
                    lines.append("- 加强日程管理培训")
                    lines.append("- 要求提前24小时安排会议")
                    lines.append("- 限制即时会议发起权限")

                lines.append("")

        lines.append("---")
        lines.append("")
        lines.append("*本报告由会议分析系统自动生成*")

        # 保存报告
        content = '\n'.join(lines)
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        return filepath

    def generate_personal_report(self, user_data: pd.DataFrame, user_name: str,
                                 team_avg: Dict, filename: str = None) -> str:
        """
        生成个人会议健康报告

        Args:
            user_data: 用户数据
            user_name: 用户名
            team_avg: 团队平均数据
            filename: 文件名

        Returns:
            str: 文件路径
        """
        if filename is None:
            filename = f"personal_report_{user_name}.md"

        lines = []

        # 标题
        lines.append(f"# 个人会议健康报告 - {user_name}")
        lines.append("")
        lines.append(f"**报告生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")
        lines.append("---")
        lines.append("")

        # 个人数据概览
        lines.append("## 📊 个人数据概览")
        lines.append("")

        if not user_data.empty:
            avg_meetings = user_data['日人均线上会议数'].mean()
            avg_duration = user_data['日人均线上会议时长(分钟)'].mean()

            lines.append("| 指标 | 个人均值 | 团队均值 | 对比 |")
            lines.append("|------|---------|---------|------|")

            # 会议数对比
            team_meetings = team_avg.get('日人均线上会议数', avg_meetings)
            diff_meetings = ((avg_meetings - team_meetings) / team_meetings * 100) if team_meetings > 0 else 0
            trend_icon = "⬇️" if avg_meetings < team_meetings else "⬆️"
            lines.append(f"| 日人均会议数 | {avg_meetings:.2f} | {team_meetings:.2f} | {trend_icon} {diff_meetings:+.1f}% |")

            # 时长对比
            team_duration = team_avg.get('日人均线上会议时长(分钟)', avg_duration)
            diff_duration = ((avg_duration - team_duration) / team_duration * 100) if team_duration > 0 else 0
            trend_icon = "⬇️" if avg_duration < team_duration else "⬆️"
            lines.append(f"| 日人均会议时长 | {avg_duration:.2f} | {team_duration:.2f} | {trend_icon} {diff_duration:+.1f}% |")

            lines.append("")

        # 趋势分析
        lines.append("---")
        lines.append("")
        lines.append("## 📈 个人趋势")
        lines.append("")

        if not user_data.empty and 'period_name' in user_data.columns:
            trend_data = user_data.groupby('period_name')['日人均线上会议数'].mean().reset_index()

            lines.append("### 会议数变化趋势")
            lines.append("")
            lines.append("| 周期 | 日人均会议数 |")
            lines.append("|------|-------------|")

            for _, row in trend_data.iterrows():
                lines.append(f"| {row['period_name']} | {row['日人均线上会议数']:.2f} |")

            lines.append("")

        # 健康建议
        lines.append("---")
        lines.append("")
        lines.append("## 💡 健康建议")
        lines.append("")

        if not user_data.empty:
            if avg_meetings > team_meetings * 1.2:
                lines.append("### ⚠️ 会议负担较重")
                lines.append("")
                lines.append("您的会议数量明显高于团队平均水平,建议:")
                lines.append("")
                lines.append("1. 审查日历,识别可以拒绝或委托他人参加的会议")
                lines.append("2. 与主管讨论优先级,聚焦核心工作")
                lines.append("3. 尝试将部分会议改为异步沟通")
                lines.append("")
            elif avg_meetings < team_meetings * 0.8:
                lines.append("### ✅ 会议管理良好")
                lines.append("")
                lines.append("您的会议数量控制得很好,低于团队平均水平。")
                lines.append("")
            else:
                lines.append("### ✅ 会议负担适中")
                lines.append("")
                lines.append("您的会议数量处于健康范围内。")
                lines.append("")

        lines.append("---")
        lines.append("")
        lines.append("*本报告由会议分析系统自动生成,仅供个人参考*")

        # 保存报告
        content = '\n'.join(lines)
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        return filepath

    def generate_weekly_summary(self, week_data: pd.DataFrame, week_name: str,
                               filename: str = None) -> str:
        """
        生成周报

        Args:
            week_data: 本周数据
            week_name: 周期名称
            filename: 文件名

        Returns:
            str: 文件路径
        """
        if filename is None:
            filename = f"weekly_summary_{week_name}.md"

        lines = []

        # 标题
        lines.append(f"# 会议数据周报 - {week_name}")
        lines.append("")
        lines.append(f"**报告生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        lines.append("")
        lines.append("---")
        lines.append("")

        # 本周概览
        lines.append("## 📊 本周概览")
        lines.append("")

        if not week_data.empty:
            total_records = len(week_data)
            avg_meetings = week_data['日人均线上会议数'].mean()
            avg_duration = week_data['日人均线上会议时长(分钟)'].mean()

            lines.append(f"- **数据记录数**: {total_records}")
            lines.append(f"- **日人均会议数**: {avg_meetings:.2f}")
            lines.append(f"- **日人均会议时长**: {avg_duration:.2f} 分钟")
            lines.append("")

        # Top 10 用户
        lines.append("---")
        lines.append("")
        lines.append("## 👥 Top 10 会议最多的用户")
        lines.append("")

        if not week_data.empty and 'user_name' in week_data.columns:
            top10 = week_data.nlargest(10, '日人均线上会议数')[['user_name', '日人均线上会议数', '日人均线上会议时长(分钟)']]
            lines.append(top10.to_markdown(index=False))
        else:
            lines.append("无数据")

        lines.append("")
        lines.append("---")
        lines.append("")
        lines.append("*本周报由会议分析系统自动生成*")

        # 保存报告
        content = '\n'.join(lines)
        filepath = os.path.join(self.output_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        return filepath


def test_reporter():
    """测试报告生成器"""
    print("=" * 60)
    print("测试报告生成器")
    print("=" * 60)

    from data_loader import MeetingDataLoader
    from calculator import MeetingMetricsCalculator
    from analyzer import MeetingDataAnalyzer

    # 加载数据
    loader = MeetingDataLoader()
    data = loader.load_all_data()

    if data is None:
        print("❌ 数据加载失败")
        return

    # 获取基线期和当前期数据
    baseline = loader.get_baseline_data()
    current = loader.get_recent_weeks_data(4)

    # 计算KPI
    calculator = MeetingMetricsCalculator(baseline, current)
    kpi_results = calculator.calculate_all_kpis(loader.get_data_by_period_type('weekly'))

    # 创建分析器
    analyzer = MeetingDataAnalyzer(data)

    # 趋势分析
    trend_analysis = {
        '日人均线上会议数': analyzer.analyze_trend('日人均线上会议数'),
        '日人均线上会议时长': analyzer.analyze_trend('日人均线上会议时长(分钟)')
    }

    # 异常检测
    anomalies = analyzer.detect_anomalies('日人均线上会议数', threshold=2.0)

    # Top用户
    top_users = analyzer.identify_top_users('日人均线上会议数', n=10)

    # 创建报告生成器
    reporter = MeetingReportGenerator()

    # 1. 生成管理层摘要
    print("\n生成管理层摘要报告...")
    exec_report = reporter.generate_executive_summary(kpi_results)
    print(f"✓ 已保存: {exec_report}")

    # 2. 生成详细报告
    print("\n生成详细分析报告...")
    detail_report = reporter.generate_detailed_report(
        kpi_results,
        trend_analysis,
        anomalies,
        top_users
    )
    print(f"✓ 已保存: {detail_report}")

    # 3. 生成个人报告示例
    if 'user_name' in data.columns and len(data) > 0:
        print("\n生成个人报告示例...")
        sample_user = data['user_name'].iloc[0]
        user_data = data[data['user_name'] == sample_user]
        team_avg = {
            '日人均线上会议数': data['日人均线上会议数'].mean(),
            '日人均线上会议时长(分钟)': data['日人均线上会议时长(分钟)'].mean()
        }
        personal_report = reporter.generate_personal_report(user_data, sample_user, team_avg)
        print(f"✓ 已保存: {personal_report}")

    # 4. 生成周报示例
    print("\n生成周报示例...")
    periods = loader.get_period_list()
    if periods:
        latest_period = periods[-1]['period_name']
        week_data = loader.get_data_by_period(latest_period)
        weekly_report = reporter.generate_weekly_summary(week_data, latest_period)
        print(f"✓ 已保存: {weekly_report}")

    print("\n✅ 报告生成测试完成")


if __name__ == "__main__":
    test_reporter()
