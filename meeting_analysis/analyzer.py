#!/usr/bin/env python3
"""
统计分析模块
提供趋势分析、异常检测、相关性分析等功能
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Tuple
from scipy import stats


class MeetingDataAnalyzer:
    """会议数据分析器"""

    def __init__(self, data: pd.DataFrame):
        """
        初始化分析器

        Args:
            data: 会议数据DataFrame
        """
        self.data = data

    def analyze_trend(self, metric: str, period_col: str = 'period_name') -> Dict:
        """
        趋势分析

        Args:
            metric: 要分析的指标名称
            period_col: 周期列名

        Returns:
            dict: 趋势分析结果
        """
        if metric not in self.data.columns or period_col not in self.data.columns:
            return {'error': f'列 {metric} 或 {period_col} 不存在'}

        # 按周期分组计算均值
        trend_data = self.data.groupby(period_col)[metric].mean().reset_index()

        # 如果有sort_key列,添加到trend_data中用于排序
        if 'sort_key' in self.data.columns:
            sort_keys = self.data[[period_col, 'sort_key']].drop_duplicates()
            trend_data = trend_data.merge(sort_keys, on=period_col, how='left')
            trend_data = trend_data.sort_values('sort_key')
        else:
            trend_data = trend_data.sort_values(period_col)

        values = trend_data[metric].values

        # 计算趋势方向
        if len(values) < 2:
            return {
                'trend_data': trend_data,
                'direction': 'insufficient_data',
                'change_rate': 0.0
            }

        # 线性回归计算趋势
        x = np.arange(len(values))
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, values)

        # 整体变化率
        first_value = values[0]
        last_value = values[-1]
        change_rate = (last_value - first_value) / first_value * 100 if first_value != 0 else 0

        # 判断趋势方向
        if abs(slope) < 0.01:
            direction = 'stable'
        elif slope > 0:
            direction = 'increasing'
        else:
            direction = 'decreasing'

        return {
            'trend_data': trend_data,
            'direction': direction,
            'slope': slope,
            'r_squared': r_value ** 2,
            'p_value': p_value,
            'change_rate': change_rate,
            'first_value': first_value,
            'last_value': last_value
        }

    def detect_anomalies(self, metric: str, threshold: float = 2.0) -> pd.DataFrame:
        """
        异常检测 (使用Z-score方法)

        Args:
            metric: 要检测的指标
            threshold: Z-score阈值,默认2.0 (约95%置信区间)

        Returns:
            DataFrame: 包含异常记录的数据
        """
        if metric not in self.data.columns:
            return pd.DataFrame()

        # 计算Z-score
        mean = self.data[metric].mean()
        std = self.data[metric].std()

        if std == 0:
            return pd.DataFrame()

        self.data['z_score'] = (self.data[metric] - mean) / std

        # 识别异常值
        anomalies = self.data[abs(self.data['z_score']) > threshold].copy()

        # 添加异常类型
        anomalies['anomaly_type'] = anomalies['z_score'].apply(
            lambda x: 'high' if x > threshold else 'low'
        )

        return anomalies[['user_name', 'period_name', metric, 'z_score', 'anomaly_type']].sort_values(
            'z_score', ascending=False
        )

    def analyze_distribution(self, metric: str) -> Dict:
        """
        分布分析

        Args:
            metric: 要分析的指标

        Returns:
            dict: 分布统计信息
        """
        if metric not in self.data.columns:
            return {'error': f'列 {metric} 不存在'}

        values = self.data[metric].dropna()

        return {
            'count': len(values),
            'mean': values.mean(),
            'median': values.median(),
            'std': values.std(),
            'min': values.min(),
            'max': values.max(),
            'q25': values.quantile(0.25),
            'q75': values.quantile(0.75),
            'skewness': values.skew(),
            'kurtosis': values.kurtosis()
        }

    def compare_periods(self, metric: str, period1: str, period2: str) -> Dict:
        """
        周期对比分析

        Args:
            metric: 对比指标
            period1: 周期1
            period2: 周期2

        Returns:
            dict: 对比结果
        """
        if metric not in self.data.columns or 'period_name' not in self.data.columns:
            return {'error': '缺少必要字段'}

        data1 = self.data[self.data['period_name'] == period1][metric]
        data2 = self.data[self.data['period_name'] == period2][metric]

        if len(data1) == 0 or len(data2) == 0:
            return {'error': '周期数据为空'}

        # 基本统计
        mean1 = data1.mean()
        mean2 = data2.mean()
        change = (mean2 - mean1) / mean1 * 100 if mean1 != 0 else 0

        # t检验 (检验两组均值是否有显著差异)
        t_stat, p_value = stats.ttest_ind(data1, data2)

        return {
            'period1': period1,
            'period2': period2,
            'mean1': mean1,
            'mean2': mean2,
            'change_rate': change,
            't_statistic': t_stat,
            'p_value': p_value,
            'significant': p_value < 0.05
        }

    def identify_top_users(self, metric: str, n: int = 10, ascending: bool = False) -> pd.DataFrame:
        """
        识别Top N用户

        Args:
            metric: 排序指标
            n: Top N数量
            ascending: 是否升序 (False表示降序,取最大值)

        Returns:
            DataFrame: Top N用户数据
        """
        if metric not in self.data.columns or 'user_name' not in self.data.columns:
            return pd.DataFrame()

        # 按用户聚合
        user_stats = self.data.groupby('user_name')[metric].agg(['mean', 'sum', 'count']).reset_index()
        user_stats.columns = ['user_name', f'{metric}_avg', f'{metric}_sum', 'data_points']

        # 排序并取Top N
        top_users = user_stats.nlargest(n, f'{metric}_avg') if not ascending else user_stats.nsmallest(n, f'{metric}_avg')

        return top_users

    def analyze_correlation(self, metric1: str, metric2: str) -> Dict:
        """
        相关性分析

        Args:
            metric1: 指标1
            metric2: 指标2

        Returns:
            dict: 相关性分析结果
        """
        if metric1 not in self.data.columns or metric2 not in self.data.columns:
            return {'error': '指标不存在'}

        # 去除缺失值
        valid_data = self.data[[metric1, metric2]].dropna()

        if len(valid_data) < 3:
            return {'error': '有效数据点不足'}

        # 皮尔逊相关系数
        pearson_corr, pearson_p = stats.pearsonr(valid_data[metric1], valid_data[metric2])

        # 斯皮尔曼相关系数 (用于非线性关系)
        spearman_corr, spearman_p = stats.spearmanr(valid_data[metric1], valid_data[metric2])

        return {
            'metric1': metric1,
            'metric2': metric2,
            'pearson_correlation': pearson_corr,
            'pearson_p_value': pearson_p,
            'spearman_correlation': spearman_corr,
            'spearman_p_value': spearman_p,
            'sample_size': len(valid_data)
        }

    def analyze_improvement_by_group(self, metric: str, group_col: str,
                                    baseline_periods: List[str],
                                    current_periods: List[str]) -> pd.DataFrame:
        """
        分组改善分析

        Args:
            metric: 分析指标
            group_col: 分组列
            baseline_periods: 基线期列表
            current_periods: 当前期列表

        Returns:
            DataFrame: 各组改善情况
        """
        if metric not in self.data.columns or group_col not in self.data.columns:
            return pd.DataFrame()

        # 基线期数据
        baseline = self.data[self.data['period_name'].isin(baseline_periods)]
        baseline_stats = baseline.groupby(group_col)[metric].mean()

        # 当前期数据
        current = self.data[self.data['period_name'].isin(current_periods)]
        current_stats = current.groupby(group_col)[metric].mean()

        # 合并并计算改善率
        comparison = pd.DataFrame({
            'baseline': baseline_stats,
            'current': current_stats
        })
        comparison['improvement_rate'] = (
            (comparison['baseline'] - comparison['current']) / comparison['baseline'] * 100
        )
        comparison['improved'] = comparison['improvement_rate'] > 0

        return comparison.reset_index().sort_values('improvement_rate', ascending=False)

    def calculate_week_over_week_change(self, metric: str) -> pd.DataFrame:
        """
        计算环比变化

        Args:
            metric: 分析指标

        Returns:
            DataFrame: 各周期环比数据
        """
        if metric not in self.data.columns or 'period_name' not in self.data.columns:
            return pd.DataFrame()

        # 按周期计算均值
        period_data = self.data.groupby('period_name')[metric].mean().reset_index()

        # 按时间排序
        if 'sort_key' in self.data.columns:
            period_order = self.data[['period_name', 'sort_key']].drop_duplicates().sort_values('sort_key')
            period_data = period_data.merge(period_order, on='period_name')
            period_data = period_data.sort_values('sort_key')

        # 计算环比
        period_data['previous_value'] = period_data[metric].shift(1)
        period_data['wow_change'] = period_data[metric] - period_data['previous_value']
        period_data['wow_change_rate'] = (
            period_data['wow_change'] / period_data['previous_value'] * 100
        ).fillna(0)

        return period_data[['period_name', metric, 'previous_value', 'wow_change', 'wow_change_rate']]

    def generate_summary_report(self, metrics: List[str]) -> Dict:
        """
        生成汇总分析报告

        Args:
            metrics: 要分析的指标列表

        Returns:
            dict: 汇总报告
        """
        report = {}

        for metric in metrics:
            if metric not in self.data.columns:
                continue

            metric_report = {
                'distribution': self.analyze_distribution(metric),
                'trend': self.analyze_trend(metric),
                'top10_users': self.identify_top_users(metric, n=10),
                'anomalies': self.detect_anomalies(metric)
            }

            report[metric] = metric_report

        return report


def test_analyzer():
    """测试分析器"""
    print("=" * 60)
    print("测试数据分析器")
    print("=" * 60)

    from data_loader import MeetingDataLoader

    # 加载数据
    loader = MeetingDataLoader()
    data = loader.load_all_data()

    if data is None:
        print("❌ 数据加载失败")
        return

    # 创建分析器
    analyzer = MeetingDataAnalyzer(data)

    # 1. 趋势分析
    print("\n" + "=" * 60)
    print("趋势分析: 日人均线上会议数")
    print("=" * 60)
    trend = analyzer.analyze_trend('日人均线上会议数')
    if 'error' not in trend:
        print(f"趋势方向: {trend['direction']}")
        print(f"变化率: {trend['change_rate']:.2f}%")
        print(f"R²: {trend['r_squared']:.4f}")
        print(f"起始值: {trend['first_value']:.2f}")
        print(f"结束值: {trend['last_value']:.2f}")

    # 2. 分布分析
    print("\n" + "=" * 60)
    print("分布分析: 日人均线上会议时长(分钟)")
    print("=" * 60)
    dist = analyzer.analyze_distribution('日人均线上会议时长(分钟)')
    if 'error' not in dist:
        for key, value in dist.items():
            print(f"{key}: {value:.2f}")

    # 3. Top 10用户
    print("\n" + "=" * 60)
    print("Top 10会议最多的用户")
    print("=" * 60)
    top10 = analyzer.identify_top_users('日人均线上会议数', n=10)
    if not top10.empty:
        print(top10.to_string(index=False))

    # 4. 异常检测
    print("\n" + "=" * 60)
    print("异常检测: 日人均线上会议数")
    print("=" * 60)
    anomalies = analyzer.detect_anomalies('日人均线上会议数', threshold=2.0)
    if not anomalies.empty:
        print(f"检测到 {len(anomalies)} 个异常值:")
        print(anomalies.head(10).to_string(index=False))
    else:
        print("未检测到异常值")

    # 5. 环比变化
    print("\n" + "=" * 60)
    print("环比变化: 日人均线上会议数")
    print("=" * 60)
    wow = analyzer.calculate_week_over_week_change('日人均线上会议数')
    if not wow.empty:
        print(wow.to_string(index=False))

    # 6. 相关性分析
    print("\n" + "=" * 60)
    print("相关性分析: 会议数 vs 会议时长")
    print("=" * 60)
    corr = analyzer.analyze_correlation('日人均线上会议数', '日人均线上会议时长(分钟)')
    if 'error' not in corr:
        print(f"皮尔逊相关系数: {corr['pearson_correlation']:.4f} (p={corr['pearson_p_value']:.4f})")
        print(f"斯皮尔曼相关系数: {corr['spearman_correlation']:.4f} (p={corr['spearman_p_value']:.4f})")


if __name__ == "__main__":
    test_analyzer()
