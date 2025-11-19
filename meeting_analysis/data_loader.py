#!/usr/bin/env python3
"""
数据加载与清洗模块
负责从CSV文件加载数据并进行标准化处理
"""

import pandas as pd
import glob
import os
from datetime import datetime
import re

class MeetingDataLoader:
    """会议数据加载器"""

    def __init__(self, data_dir="input"):
        """
        初始化数据加载器

        Args:
            data_dir: 数据文件目录
        """
        self.data_dir = data_dir
        self.all_data = None

    def parse_period_from_filename(self, filename):
        """
        从文件名解析时间周期

        Args:
            filename: 文件名

        Returns:
            dict: 包含period_type, period_name, sort_key等信息
        """
        basename = os.path.basename(filename).replace('.csv', '')

        # 格式1: X月会议详情
        month_pattern = r'(\d{1,2})月会议详情'
        month_match = re.match(month_pattern, basename)
        if month_match:
            month = int(month_match.group(1))
            return {
                'period_type': 'monthly',
                'period_name': basename,
                'month': month,
                'sort_key': f"2024-{month:02d}-01"  # 假设是2024年
            }

        # 格式2: MM.DD-MM.DD会议详情
        week_pattern = r'(\d{1,2})\.(\d{1,2})-(\d{1,2})\.(\d{1,2})会议详情'
        week_match = re.match(week_pattern, basename)
        if week_match:
            start_month = int(week_match.group(1))
            start_day = int(week_match.group(2))
            end_month = int(week_match.group(3))
            end_day = int(week_match.group(4))
            return {
                'period_type': 'weekly',
                'period_name': basename,
                'start_month': start_month,
                'start_day': start_day,
                'end_month': end_month,
                'end_day': end_day,
                'sort_key': f"2024-{start_month:02d}-{start_day:02d}"
            }

        return {
            'period_type': 'unknown',
            'period_name': basename,
            'sort_key': basename
        }

    def load_single_file(self, filepath):
        """
        加载单个CSV文件

        Args:
            filepath: 文件路径

        Returns:
            DataFrame: 加载的数据
        """
        try:
            df = pd.read_csv(filepath, encoding='utf-8')

            # 添加周期信息
            period_info = self.parse_period_from_filename(filepath)
            for key, value in period_info.items():
                df[key] = value

            # 添加文件路径信息
            df['source_file'] = os.path.basename(filepath)

            return df
        except Exception as e:
            print(f"❌ 加载文件失败: {filepath}")
            print(f"   错误: {str(e)}")
            return None

    def load_all_data(self):
        """
        加载所有CSV文件

        Returns:
            DataFrame: 合并后的所有数据
        """
        csv_files = glob.glob(os.path.join(self.data_dir, "*.csv"))

        if not csv_files:
            print(f"❌ 在 {self.data_dir} 目录下未找到CSV文件")
            return None

        print(f"📂 找到 {len(csv_files)} 个CSV文件")

        dfs = []
        for filepath in csv_files:
            df = self.load_single_file(filepath)
            if df is not None:
                print(f"   ✓ {os.path.basename(filepath)}: {len(df)} 条记录")
                dfs.append(df)

        if not dfs:
            print("❌ 没有成功加载任何数据")
            return None

        # 合并所有数据
        self.all_data = pd.concat(dfs, ignore_index=True)

        # 按时间排序
        self.all_data = self.all_data.sort_values('sort_key')

        print(f"\n✅ 数据加载完成: 总计 {len(self.all_data)} 条记录")
        return self.all_data

    def get_period_list(self):
        """获取所有周期列表"""
        if self.all_data is None:
            return []

        periods = self.all_data[['period_name', 'period_type', 'sort_key']].drop_duplicates()
        periods = periods.sort_values('sort_key')
        return periods.to_dict('records')

    def get_data_by_period(self, period_name):
        """
        获取指定周期的数据

        Args:
            period_name: 周期名称

        Returns:
            DataFrame: 该周期的数据
        """
        if self.all_data is None:
            return None

        return self.all_data[self.all_data['period_name'] == period_name].copy()

    def get_data_by_period_type(self, period_type):
        """
        按周期类型获取数据

        Args:
            period_type: 'monthly' 或 'weekly'

        Returns:
            DataFrame: 该类型的所有数据
        """
        if self.all_data is None:
            return None

        return self.all_data[self.all_data['period_type'] == period_type].copy()

    def get_baseline_data(self):
        """
        获取基线期数据 (9月和10月)

        Returns:
            DataFrame: 基线期数据
        """
        if self.all_data is None:
            return None

        monthly_data = self.get_data_by_period_type('monthly')
        if monthly_data is None or monthly_data.empty:
            return None

        # 选择9月和10月的数据
        baseline = monthly_data[monthly_data['month'].isin([9, 10])].copy()
        return baseline

    def get_recent_weeks_data(self, n_weeks=4):
        """
        获取最近N周的数据

        Args:
            n_weeks: 周数

        Returns:
            DataFrame: 最近N周的数据
        """
        if self.all_data is None:
            return None

        weekly_data = self.get_data_by_period_type('weekly')
        if weekly_data is None or weekly_data.empty:
            return None

        # 获取最近的N周
        periods = weekly_data['period_name'].unique()
        recent_periods = sorted(set(periods), key=lambda x: weekly_data[weekly_data['period_name']==x]['sort_key'].iloc[0], reverse=True)[:n_weeks]

        return weekly_data[weekly_data['period_name'].isin(recent_periods)].copy()


def test_loader():
    """测试数据加载器"""
    print("=" * 60)
    print("测试数据加载器")
    print("=" * 60)

    loader = MeetingDataLoader()
    data = loader.load_all_data()

    if data is not None:
        print("\n" + "=" * 60)
        print("数据概览")
        print("=" * 60)
        print(data.head())

        print("\n" + "=" * 60)
        print("周期列表")
        print("=" * 60)
        periods = loader.get_period_list()
        for i, p in enumerate(periods, 1):
            print(f"{i}. {p['period_name']} ({p['period_type']})")

        print("\n" + "=" * 60)
        print("基线期数据")
        print("=" * 60)
        baseline = loader.get_baseline_data()
        if baseline is not None:
            print(f"记录数: {len(baseline)}")
            print(f"周期: {baseline['period_name'].unique()}")

        print("\n" + "=" * 60)
        print("最近4周数据")
        print("=" * 60)
        recent = loader.get_recent_weeks_data(4)
        if recent is not None:
            print(f"记录数: {len(recent)}")
            print(f"周期: {recent['period_name'].unique()}")


if __name__ == "__main__":
    test_loader()
