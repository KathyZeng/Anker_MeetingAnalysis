#!/usr/bin/env python3
"""
指标计算模块
负责计算各类会议改善效果评估指标
"""

import pandas as pd
import numpy as np
from typing import Dict, Tuple


class MeetingMetricsCalculator:
    """会议指标计算器"""

    def __init__(self, baseline_data: pd.DataFrame, current_data: pd.DataFrame):
        """
        初始化计算器

        Args:
            baseline_data: 基线期数据 (9月和10月)
            current_data: 当前期数据 (最近4周)
        """
        self.baseline_data = baseline_data
        self.current_data = current_data

    def _calculate_daily_avg_meetings(self, data: pd.DataFrame) -> float:
        """
        计算日人均会议数 (所有线上会议,包括即时、日程、1v1)

        Args:
            data: 数据DataFrame

        Returns:
            float: 日人均会议数
        """
        if data.empty:
            return 0.0

        # 使用总会议数字段
        if '日人均线上会议数' in data.columns:
            return data['日人均线上会议数'].mean()

        return 0.0

    def _calculate_daily_avg_duration(self, data: pd.DataFrame) -> float:
        """
        计算日人均会议时长(分钟) (所有线上会议,包括即时、日程、1v1)

        Args:
            data: 数据DataFrame

        Returns:
            float: 日人均会议时长
        """
        if data.empty:
            return 0.0

        # 使用总会议时长字段
        if '日人均线上会议时长(分钟)' in data.columns:
            return data['日人均线上会议时长(分钟)'].mean()

        if '日人均线上会议时长' in data.columns:
            return data['日人均线上会议时长'].mean()

        return 0.0

    def _calculate_instant_meeting_ratio(self, data: pd.DataFrame) -> float:
        """
        计算即时会议占比

        公式: 即时会议占比 = 即时会议数 / 人的会议数 × 100%

        Args:
            data: 数据DataFrame

        Returns:
            float: 即时会议占比 (0-100, 百分比)
        """
        if data.empty:
            return 0.0

        # 使用新公式: 即时会议数 / 人的会议数
        if '即时会议数' in data.columns and '人的会议数' in data.columns:
            total_instant = data['即时会议数'].sum()
            total_meetings = data['人的会议数'].sum()

            if total_meetings > 0:
                return (total_instant / total_meetings) * 100

        # 备用: 使用即时会议字段
        if '即时会议' in data.columns and '人的会议数' in data.columns:
            total_instant = data['即时会议'].sum()
            total_meetings = data['人的会议数'].sum()

            if total_meetings > 0:
                return (total_instant / total_meetings) * 100

        return 0.0

    def calculate_primary_kpis(self) -> Dict[str, Dict[str, float]]:
        """
        计算主要KPI指标

        Returns:
            dict: 包含3个主要KPI的详细信息
        """
        # 1. 日人均会议数减少率
        baseline_meetings = self._calculate_daily_avg_meetings(self.baseline_data)
        current_meetings = self._calculate_daily_avg_meetings(self.current_data)
        meeting_reduction_rate = (
            (baseline_meetings - current_meetings) / baseline_meetings * 100
            if baseline_meetings > 0 else 0.0
        )

        # 2. 日人均会议时长减少率
        baseline_duration = self._calculate_daily_avg_duration(self.baseline_data)
        current_duration = self._calculate_daily_avg_duration(self.current_data)
        duration_reduction_rate = (
            (baseline_duration - current_duration) / baseline_duration * 100
            if baseline_duration > 0 else 0.0
        )

        # 3. 即时会议占比下降
        baseline_ratio = self._calculate_instant_meeting_ratio(self.baseline_data)
        current_ratio = self._calculate_instant_meeting_ratio(self.current_data)
        # baseline_ratio 和 current_ratio 已经是百分比,直接相减得到百分点变化
        instant_meeting_decline = baseline_ratio - current_ratio

        return {
            '日人均会议数减少率': {
                '基线期均值': baseline_meetings,
                '当前期均值': current_meetings,
                '减少率(%)': meeting_reduction_rate,
                '目标': '≥10%',
                '达标': meeting_reduction_rate >= 10
            },
            '日人均会议时长减少率': {
                '基线期均值(分钟)': baseline_duration,
                '当前期均值(分钟)': current_duration,
                '减少率(%)': duration_reduction_rate,
                '目标': '≥10%',
                '达标': duration_reduction_rate >= 10
            },
            '即时会议占比下降': {
                '基线期占比(%)': baseline_ratio,
                '当前期占比(%)': current_ratio,
                '下降幅度(百分点)': instant_meeting_decline,
                '目标': '≥10个百分点',
                '达标': instant_meeting_decline >= 10
            }
        }

    def calculate_meeting_efficiency(self) -> Dict[str, float]:
        """
        计算平均单次会议时长变化

        公式: 直接使用日人均线上会议时长(分钟)字段(该字段已经是平均单次会议时长)

        Returns:
            dict: 平均单次会议时长相关指标
        """
        # 基线期 - 直接使用日人均会议时长字段
        baseline_duration_col = '日人均线上会议时长(分钟)'

        if baseline_duration_col in self.baseline_data.columns:
            baseline_avg_duration = self.baseline_data[baseline_duration_col].mean()
        else:
            baseline_avg_duration = 0

        # 当前期 - 直接使用日人均会议时长字段
        if baseline_duration_col in self.current_data.columns:
            current_avg_duration = self.current_data[baseline_duration_col].mean()
        else:
            current_avg_duration = 0

        # 时长变化率 (负值表示时长缩短,效率提升)
        change_rate = (
            (current_avg_duration - baseline_avg_duration) / baseline_avg_duration * 100
            if baseline_avg_duration > 0 else 0.0
        )

        # 缩短率 (正值表示缩短)
        reduction_rate = -change_rate

        return {
            '基线期平均单次会议时长(分钟)': baseline_avg_duration,
            '当前期平均单次会议时长(分钟)': current_avg_duration,
            '时长变化(分钟)': current_avg_duration - baseline_avg_duration,
            '时长缩短率(%)': reduction_rate,
            '目标': '时长缩短≥10%',
            '达标': reduction_rate >= 10
        }

    def calculate_1v1_substitution_rate(self) -> Dict[str, float]:
        """
        计算1v1通话占比变化

        公式: 1v1通话占比 = 1v1通话数 / 人的会议数 × 100%

        Returns:
            dict: 1v1通话占比相关指标
        """
        # 基线期1v1占比
        if '1v1通话数' in self.baseline_data.columns and '人的会议数' in self.baseline_data.columns:
            baseline_1v1 = self.baseline_data['1v1通话数'].sum()
            baseline_total = self.baseline_data['人的会议数'].sum()
            baseline_ratio = (baseline_1v1 / baseline_total * 100) if baseline_total > 0 else 0
        else:
            baseline_ratio = 0

        # 当前期1v1占比
        if '1v1通话数' in self.current_data.columns and '人的会议数' in self.current_data.columns:
            current_1v1 = self.current_data['1v1通话数'].sum()
            current_total = self.current_data['人的会议数'].sum()
            current_ratio = (current_1v1 / current_total * 100) if current_total > 0 else 0
        else:
            current_ratio = 0

        # 占比变化(百分点) - 正值表示增加,负值表示减少
        ratio_change = current_ratio - baseline_ratio

        # 下降幅度(百分点) - 用于评估目标达成,正值表示下降
        decline = baseline_ratio - current_ratio

        # 判断状态 - 目标是减少5-10个百分点
        if 5 <= decline <= 10:
            status = '良好'
            达标 = True
        elif decline > 10:
            status = '优秀'
            达标 = True
        elif 0 <= decline < 5:
            status = '接近目标'
            达标 = False
        else:
            status = '需关注'
            达标 = False

        return {
            '基线期1v1占比(%)': baseline_ratio,
            '当前期1v1占比(%)': current_ratio,
            '占比变化(百分点)': ratio_change,
            '下降幅度(百分点)': decline,
            '状态': status,
            '目标': '减少5-10个百分点',
            '达标': 达标
        }

    def calculate_burden_distribution(self) -> Dict[str, float]:
        """
        计算团队会议负担分布均衡度

        使用变异系数 (CV = 标准差 / 均值)
        CV越小表示分布越均衡

        Returns:
            dict: 负担分布相关指标
        """
        # 基线期变异系数
        if '日人均线上会议数' in self.baseline_data.columns:
            baseline_meetings = self.baseline_data['日人均线上会议数']
            baseline_cv = baseline_meetings.std() / baseline_meetings.mean() if baseline_meetings.mean() > 0 else 0
        else:
            baseline_cv = 0

        # 当前期变异系数
        if '日人均线上会议数' in self.current_data.columns:
            current_meetings = self.current_data['日人均线上会议数']
            current_cv = current_meetings.std() / current_meetings.mean() if current_meetings.mean() > 0 else 0
        else:
            current_cv = 0

        # 均衡度改善
        improvement = (baseline_cv - current_cv) / baseline_cv * 100 if baseline_cv > 0 else 0

        return {
            '基线期变异系数': baseline_cv,
            '当前期变异系数': current_cv,
            '均衡度改善(%)': improvement,
            '目标': '变异系数下降≥10%',
            '达标': improvement >= 10
        }

    def calculate_weekly_volatility(self, weekly_data: pd.DataFrame) -> Dict[str, float]:
        """
        计算周度波动性

        Args:
            weekly_data: 按周分组的数据

        Returns:
            dict: 波动性指标
        """
        if weekly_data.empty or 'period_name' not in weekly_data.columns:
            return {
                '周度标准差': 0.0,
                '平均值': 0.0,
                '波动系数': 0.0,
                '目标': '<0.15',
                '达标': False
            }

        # 按周计算平均会议数
        weekly_avg = weekly_data.groupby('period_name')['日人均线上会议数'].mean()

        std_dev = weekly_avg.std()
        mean_val = weekly_avg.mean()
        volatility = std_dev / mean_val if mean_val > 0 else 0

        return {
            '周度标准差': std_dev,
            '平均值': mean_val,
            '波动系数': volatility,
            '目标': '<0.15',
            '达标': volatility < 0.15
        }

    def calculate_top10_improvement(self) -> Dict[str, float]:
        """
        计算Top 10重度会议用户改善率

        Returns:
            dict: Top 10用户改善情况
        """
        # 基线期Top 10用户
        if '日人均线上会议数' in self.baseline_data.columns and 'user_name' in self.baseline_data.columns:
            baseline_top10 = self.baseline_data.nlargest(10, '日人均线上会议数')['user_name'].tolist()
            baseline_avg = self.baseline_data[self.baseline_data['user_name'].isin(baseline_top10)]['日人均线上会议数'].mean()
        else:
            return {'错误': '缺少必要字段'}

        # 当前期这些用户的表现
        if '日人均线上会议数' in self.current_data.columns and 'user_name' in self.current_data.columns:
            current_top10_data = self.current_data[self.current_data['user_name'].isin(baseline_top10)]
            current_avg = current_top10_data['日人均线上会议数'].mean() if not current_top10_data.empty else baseline_avg
        else:
            current_avg = baseline_avg

        # 改善率
        improvement_rate = (baseline_avg - current_avg) / baseline_avg * 100 if baseline_avg > 0 else 0

        return {
            '基线期Top10平均会议数': baseline_avg,
            '当前期Top10平均会议数': current_avg,
            '改善率(%)': improvement_rate,
            '目标': '≥20%',
            '达标': improvement_rate >= 20
        }

    def calculate_all_kpis(self, weekly_data: pd.DataFrame = None) -> Dict[str, Dict]:
        """
        计算所有KPI指标

        Args:
            weekly_data: 周度数据 (用于计算波动性)

        Returns:
            dict: 所有KPI指标的完整结果
        """
        results = {
            '主要KPI': self.calculate_primary_kpis(),
            '次要KPI': {
                '1v1通话占比': self.calculate_1v1_substitution_rate(),
                '团队会议负担分布均衡度': self.calculate_burden_distribution()
            },
            '监控指标': {
                'Top10重度用户改善率': self.calculate_top10_improvement()
            }
        }

        if weekly_data is not None:
            results['监控指标']['周度波动性'] = self.calculate_weekly_volatility(weekly_data)

        return results

    def calculate_period_comparison(self, periods_data: Dict[str, pd.DataFrame]) -> pd.DataFrame:
        """
        计算多个周期的对比数据

        Args:
            periods_data: {period_name: dataframe} 字典

        Returns:
            DataFrame: 各周期的关键指标对比
        """
        comparison = []

        for period_name, data in periods_data.items():
            if data.empty:
                continue

            comparison.append({
                '周期': period_name,
                '日人均会议数': self._calculate_daily_avg_meetings(data),
                '日人均会议时长(分钟)': self._calculate_daily_avg_duration(data),
                '即时会议占比(%)': self._calculate_instant_meeting_ratio(data),  # 已经是百分比
                '记录数': len(data)
            })

        return pd.DataFrame(comparison)


def test_calculator():
    """测试计算器"""
    print("=" * 60)
    print("测试指标计算器")
    print("=" * 60)

    from data_loader import MeetingDataLoader

    # 加载数据
    loader = MeetingDataLoader()
    loader.load_all_data()

    # 获取基线期和当前期数据
    baseline = loader.get_baseline_data()
    current = loader.get_recent_weeks_data(4)

    if baseline is None or current is None:
        print("❌ 数据加载失败")
        return

    print(f"\n✓ 基线期数据: {len(baseline)} 条记录")
    print(f"✓ 当前期数据: {len(current)} 条记录")

    # 创建计算器
    calculator = MeetingMetricsCalculator(baseline, current)

    # 计算所有KPI
    weekly_data = loader.get_data_by_period_type('weekly')
    all_kpis = calculator.calculate_all_kpis(weekly_data)

    # 显示结果
    print("\n" + "=" * 60)
    print("主要KPI指标")
    print("=" * 60)
    for kpi_name, kpi_data in all_kpis['主要KPI'].items():
        print(f"\n【{kpi_name}】")
        for key, value in kpi_data.items():
            if isinstance(value, bool):
                print(f"  {key}: {'✓ 是' if value else '✗ 否'}")
            elif isinstance(value, float):
                print(f"  {key}: {value:.2f}")
            else:
                print(f"  {key}: {value}")

    print("\n" + "=" * 60)
    print("次要KPI指标")
    print("=" * 60)
    for kpi_name, kpi_data in all_kpis['次要KPI'].items():
        print(f"\n【{kpi_name}】")
        for key, value in kpi_data.items():
            if isinstance(value, bool):
                print(f"  {key}: {'✓ 是' if value else '✗ 否'}")
            elif isinstance(value, float):
                print(f"  {key}: {value:.2f}")
            else:
                print(f"  {key}: {value}")

    print("\n" + "=" * 60)
    print("监控指标")
    print("=" * 60)
    for kpi_name, kpi_data in all_kpis['监控指标'].items():
        print(f"\n【{kpi_name}】")
        for key, value in kpi_data.items():
            if isinstance(value, bool):
                print(f"  {key}: {'✓ 是' if value else '✗ 否'}")
            elif isinstance(value, float):
                print(f"  {key}: {value:.2f}")
            else:
                print(f"  {key}: {value}")

    # 周期对比
    print("\n" + "=" * 60)
    print("周期对比")
    print("=" * 60)
    periods = {}
    for period in loader.get_period_list():
        period_name = period['period_name']
        periods[period_name] = loader.get_data_by_period(period_name)

    comparison_df = calculator.calculate_period_comparison(periods)
    print(comparison_df.to_string(index=False))


if __name__ == "__main__":
    test_calculator()
