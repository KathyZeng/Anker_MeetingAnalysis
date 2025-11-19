#!/usr/bin/env python3
"""
可视化模块
负责生成各类图表,支持matplotlib和文本图表两种模式
"""

import pandas as pd
import numpy as np
from typing import List, Dict, Optional
import os


class MeetingVisualizer:
    """会议数据可视化器"""

    def __init__(self, output_dir: str = "output"):
        """
        初始化可视化器

        Args:
            output_dir: 输出目录
        """
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

        # 尝试导入matplotlib
        try:
            import matplotlib.pyplot as plt
            import matplotlib
            matplotlib.use('Agg')  # 使用非交互式后端
            self.has_matplotlib = True
            self.plt = plt
            # 设置中文字体
            plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
            plt.rcParams['axes.unicode_minus'] = False
        except ImportError:
            self.has_matplotlib = False
            print("⚠️  matplotlib未安装,将使用文本模式生成图表")

    def plot_trend_line(self, data: pd.DataFrame, x_col: str, y_col: str,
                       title: str, xlabel: str, ylabel: str,
                       filename: str = "trend.png") -> str:
        """
        绘制趋势折线图

        Args:
            data: 数据DataFrame
            x_col: x轴列名
            y_col: y轴列名
            title: 图表标题
            xlabel: x轴标签
            ylabel: y轴标签
            filename: 保存文件名

        Returns:
            str: 保存的文件路径
        """
        if not self.has_matplotlib:
            return self._plot_text_trend(data, x_col, y_col, title)

        fig, ax = self.plt.subplots(figsize=(12, 6))

        # 绘制折线
        ax.plot(data[x_col], data[y_col], marker='o', linewidth=2, markersize=8)

        # 添加数值标签
        for i, (x, y) in enumerate(zip(data[x_col], data[y_col])):
            ax.text(i, y, f'{y:.2f}', ha='center', va='bottom', fontsize=9)

        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xlabel(xlabel, fontsize=12)
        ax.set_ylabel(ylabel, fontsize=12)
        ax.grid(True, alpha=0.3)
        ax.tick_params(axis='x', rotation=45)

        self.plt.tight_layout()
        filepath = os.path.join(self.output_dir, filename)
        self.plt.savefig(filepath, dpi=300, bbox_inches='tight')
        self.plt.close()

        return filepath

    def plot_comparison_bar(self, categories: List[str], baseline: List[float],
                           current: List[float], title: str, ylabel: str,
                           filename: str = "comparison.png") -> str:
        """
        绘制对比柱状图

        Args:
            categories: 类别列表
            baseline: 基线期数据
            current: 当前期数据
            title: 图表标题
            ylabel: y轴标签
            filename: 文件名

        Returns:
            str: 保存的文件路径
        """
        if not self.has_matplotlib:
            return self._plot_text_comparison(categories, baseline, current, title)

        fig, ax = self.plt.subplots(figsize=(10, 6))

        x = np.arange(len(categories))
        width = 0.35

        bars1 = ax.bar(x - width/2, baseline, width, label='基线期', alpha=0.8)
        bars2 = ax.bar(x + width/2, current, width, label='当前期', alpha=0.8)

        # 添加数值标签
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                ax.text(bar.get_x() + bar.get_width()/2., height,
                       f'{height:.2f}', ha='center', va='bottom', fontsize=9)

        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_ylabel(ylabel, fontsize=12)
        ax.set_xticks(x)
        ax.set_xticklabels(categories)
        ax.legend()
        ax.grid(True, axis='y', alpha=0.3)

        self.plt.tight_layout()
        filepath = os.path.join(self.output_dir, filename)
        self.plt.savefig(filepath, dpi=300, bbox_inches='tight')
        self.plt.close()

        return filepath

    def plot_stacked_bar(self, data: pd.DataFrame, x_col: str, y_cols: List[str],
                        title: str, xlabel: str, ylabel: str,
                        filename: str = "stacked.png") -> str:
        """
        绘制堆叠柱状图

        Args:
            data: 数据DataFrame
            x_col: x轴列名
            y_cols: y轴数据列名列表
            title: 标题
            xlabel: x轴标签
            ylabel: y轴标签
            filename: 文件名

        Returns:
            str: 文件路径
        """
        if not self.has_matplotlib:
            return self._plot_text_stacked(data, x_col, y_cols, title)

        fig, ax = self.plt.subplots(figsize=(12, 6))

        # 绘制堆叠柱状图
        bottom = np.zeros(len(data))
        for col in y_cols:
            ax.bar(data[x_col], data[col], label=col, bottom=bottom, alpha=0.8)
            bottom += data[col].values

        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_xlabel(xlabel, fontsize=12)
        ax.set_ylabel(ylabel, fontsize=12)
        ax.legend()
        ax.grid(True, axis='y', alpha=0.3)
        ax.tick_params(axis='x', rotation=45)

        self.plt.tight_layout()
        filepath = os.path.join(self.output_dir, filename)
        self.plt.savefig(filepath, dpi=300, bbox_inches='tight')
        self.plt.close()

        return filepath

    def plot_heatmap(self, data: pd.DataFrame, title: str,
                    filename: str = "heatmap.png") -> str:
        """
        绘制热力图

        Args:
            data: 数据DataFrame (二维数据)
            title: 标题
            filename: 文件名

        Returns:
            str: 文件路径
        """
        if not self.has_matplotlib:
            return self._plot_text_heatmap(data, title)

        try:
            import seaborn as sns
            fig, ax = self.plt.subplots(figsize=(10, 8))
            sns.heatmap(data, annot=True, fmt='.2f', cmap='YlOrRd', ax=ax)
            ax.set_title(title, fontsize=14, fontweight='bold')
            self.plt.tight_layout()
            filepath = os.path.join(self.output_dir, filename)
            self.plt.savefig(filepath, dpi=300, bbox_inches='tight')
            self.plt.close()
            return filepath
        except ImportError:
            return self._plot_text_heatmap(data, title)

    def plot_pie_chart(self, labels: List[str], sizes: List[float], title: str,
                      filename: str = "pie.png") -> str:
        """
        绘制饼图

        Args:
            labels: 标签列表
            sizes: 数值列表
            title: 标题
            filename: 文件名

        Returns:
            str: 文件路径
        """
        if not self.has_matplotlib:
            return self._plot_text_pie(labels, sizes, title)

        fig, ax = self.plt.subplots(figsize=(8, 8))
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.axis('equal')

        self.plt.tight_layout()
        filepath = os.path.join(self.output_dir, filename)
        self.plt.savefig(filepath, dpi=300, bbox_inches='tight')
        self.plt.close()

        return filepath

    def plot_box_plot(self, data: pd.DataFrame, columns: List[str], title: str,
                     filename: str = "boxplot.png") -> str:
        """
        绘制箱线图

        Args:
            data: 数据DataFrame
            columns: 要绘制的列
            title: 标题
            filename: 文件名

        Returns:
            str: 文件路径
        """
        if not self.has_matplotlib:
            return self._plot_text_boxplot(data, columns, title)

        fig, ax = self.plt.subplots(figsize=(10, 6))
        data[columns].boxplot(ax=ax)
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.set_ylabel('数值', fontsize=12)
        ax.grid(True, alpha=0.3)

        self.plt.tight_layout()
        filepath = os.path.join(self.output_dir, filename)
        self.plt.savefig(filepath, dpi=300, bbox_inches='tight')
        self.plt.close()

        return filepath

    # ==================== 文本模式绘图方法 ====================

    def _plot_text_trend(self, data: pd.DataFrame, x_col: str, y_col: str, title: str) -> str:
        """文本模式趋势图"""
        output = [f"\n{'=' * 60}", f"{title}", f"{'=' * 60}\n"]

        max_val = data[y_col].max()
        min_val = data[y_col].min()
        range_val = max_val - min_val if max_val != min_val else 1

        for _, row in data.iterrows():
            period = str(row[x_col])
            value = row[y_col]
            # 归一化到0-40个字符
            bar_length = int(((value - min_val) / range_val) * 40)
            bar = '█' * bar_length
            output.append(f"{period:20s} {bar} {value:.2f}")

        result = '\n'.join(output)
        print(result)
        return "text_mode"

    def _plot_text_comparison(self, categories: List[str], baseline: List[float],
                             current: List[float], title: str) -> str:
        """文本模式对比图"""
        output = [f"\n{'=' * 60}", f"{title}", f"{'=' * 60}\n"]

        max_val = max(max(baseline), max(current))
        for i, cat in enumerate(categories):
            base = baseline[i]
            curr = current[i]
            base_bar = '█' * int((base / max_val) * 30)
            curr_bar = '█' * int((curr / max_val) * 30)
            output.append(f"\n{cat}")
            output.append(f"  基线期: {base_bar} {base:.2f}")
            output.append(f"  当前期: {curr_bar} {curr:.2f}")
            change = ((curr - base) / base * 100) if base != 0 else 0
            output.append(f"  变化率: {change:+.1f}%")

        result = '\n'.join(output)
        print(result)
        return "text_mode"

    def _plot_text_stacked(self, data: pd.DataFrame, x_col: str,
                          y_cols: List[str], title: str) -> str:
        """文本模式堆叠图"""
        output = [f"\n{'=' * 60}", f"{title}", f"{'=' * 60}\n"]

        for _, row in data.iterrows():
            period = str(row[x_col])
            output.append(f"\n{period}:")
            for col in y_cols:
                value = row[col]
                bar = '█' * int(value / 2)  # 简单缩放
                output.append(f"  {col:30s} {bar} {value:.2f}")

        result = '\n'.join(output)
        print(result)
        return "text_mode"

    def _plot_text_heatmap(self, data: pd.DataFrame, title: str) -> str:
        """文本模式热力图"""
        output = [f"\n{'=' * 60}", f"{title}", f"{'=' * 60}\n"]
        output.append(data.to_string())

        result = '\n'.join(output)
        print(result)
        return "text_mode"

    def _plot_text_pie(self, labels: List[str], sizes: List[float], title: str) -> str:
        """文本模式饼图"""
        output = [f"\n{'=' * 60}", f"{title}", f"{'=' * 60}\n"]

        total = sum(sizes)
        for label, size in zip(labels, sizes):
            percentage = (size / total * 100) if total > 0 else 0
            bar = '█' * int(percentage / 2)
            output.append(f"{label:30s} {bar} {percentage:.1f}%")

        result = '\n'.join(output)
        print(result)
        return "text_mode"

    def _plot_text_boxplot(self, data: pd.DataFrame, columns: List[str], title: str) -> str:
        """文本模式箱线图"""
        output = [f"\n{'=' * 60}", f"{title}", f"{'=' * 60}\n"]

        for col in columns:
            values = data[col].dropna()
            q1 = values.quantile(0.25)
            q2 = values.quantile(0.50)
            q3 = values.quantile(0.75)
            min_val = values.min()
            max_val = values.max()

            output.append(f"\n{col}:")
            output.append(f"  Min:  {min_val:.2f}")
            output.append(f"  Q1:   {q1:.2f}")
            output.append(f"  Med:  {q2:.2f}")
            output.append(f"  Q3:   {q3:.2f}")
            output.append(f"  Max:  {max_val:.2f}")

        result = '\n'.join(output)
        print(result)
        return "text_mode"

    def create_dashboard_summary(self, kpi_results: Dict) -> str:
        """
        创建仪表盘文本摘要

        Args:
            kpi_results: KPI计算结果

        Returns:
            str: 仪表盘摘要文本
        """
        output = []
        output.append("\n" + "=" * 80)
        output.append("会议改善效果评估 - 仪表盘摘要")
        output.append("=" * 80)

        # 主要KPI
        output.append("\n【主要KPI】")
        output.append("-" * 80)
        for kpi_name, kpi_data in kpi_results.get('主要KPI', {}).items():
            达标 = kpi_data.get('达标', False)
            status = '✓ 达标' if 达标 else '✗ 未达标'
            output.append(f"\n{kpi_name}: {status}")
            for key, value in kpi_data.items():
                if key != '达标' and not isinstance(value, bool):
                    if isinstance(value, float):
                        output.append(f"  {key}: {value:.2f}")
                    else:
                        output.append(f"  {key}: {value}")

        # 次要KPI
        output.append("\n【次要KPI】")
        output.append("-" * 80)
        for kpi_name, kpi_data in kpi_results.get('次要KPI', {}).items():
            达标 = kpi_data.get('达标', False)
            status = '✓ 达标' if 达标 else '✗ 未达标'
            output.append(f"\n{kpi_name}: {status}")
            for key, value in kpi_data.items():
                if key != '达标' and not isinstance(value, bool):
                    if isinstance(value, float):
                        output.append(f"  {key}: {value:.2f}")
                    else:
                        output.append(f"  {key}: {value}")

        # 监控指标
        output.append("\n【监控指标】")
        output.append("-" * 80)
        for kpi_name, kpi_data in kpi_results.get('监控指标', {}).items():
            output.append(f"\n{kpi_name}:")
            for key, value in kpi_data.items():
                if isinstance(value, bool):
                    output.append(f"  {key}: {'✓ 是' if value else '✗ 否'}")
                elif isinstance(value, float):
                    output.append(f"  {key}: {value:.2f}")
                else:
                    output.append(f"  {key}: {value}")

        output.append("\n" + "=" * 80)

        result = '\n'.join(output)
        print(result)

        # 保存到文件
        filepath = os.path.join(self.output_dir, "dashboard_summary.txt")
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(result)

        return filepath


def test_visualizer():
    """测试可视化器"""
    print("=" * 60)
    print("测试可视化器")
    print("=" * 60)

    from data_loader import MeetingDataLoader
    from calculator import MeetingMetricsCalculator

    # 加载数据
    loader = MeetingDataLoader()
    data = loader.load_all_data()

    if data is None:
        print("❌ 数据加载失败")
        return

    # 创建可视化器
    viz = MeetingVisualizer()

    # 1. 趋势图
    print("\n生成趋势图...")
    period_data = data.groupby('period_name')['日人均线上会议数'].mean().reset_index()
    viz.plot_trend_line(
        period_data,
        'period_name',
        '日人均线上会议数',
        '日人均会议数趋势',
        '周期',
        '日人均会议数',
        'trend_meetings.png'
    )

    # 2. 对比图
    print("\n生成对比图...")
    baseline = loader.get_baseline_data()
    current = loader.get_recent_weeks_data(4)

    if baseline is not None and current is not None:
        categories = ['日人均会议数', '日人均会议时长']
        baseline_vals = [
            baseline['日人均线上会议数'].mean(),
            baseline['日人均线上会议时长(分钟)'].mean()
        ]
        current_vals = [
            current['日人均线上会议数'].mean(),
            current['日人均线上会议时长(分钟)'].mean()
        ]
        viz.plot_comparison_bar(
            categories,
            baseline_vals,
            current_vals,
            '基线期 vs 当前期对比',
            '数值',
            'comparison.png'
        )

    # 3. 仪表盘摘要
    print("\n生成仪表盘摘要...")
    calculator = MeetingMetricsCalculator(baseline, current)
    kpi_results = calculator.calculate_all_kpis(loader.get_data_by_period_type('weekly'))
    viz.create_dashboard_summary(kpi_results)

    print("\n✅ 可视化测试完成")


if __name__ == "__main__":
    test_visualizer()
