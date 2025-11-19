#!/usr/bin/env python3
"""
HTML仪表盘生成器 V2
每个指标都包含计算讲解和计算结果两部分
"""

import os
import base64
from datetime import datetime
from typing import Dict
import json


class HTMLDashboardGeneratorV2:
    """HTML仪表盘生成器 V2"""

    def __init__(self, output_dir: str = "output"):
        """
        初始化生成器

        Args:
            output_dir: 输出目录
        """
        self.output_dir = output_dir

        # 定义KPI元数据(包含计算说明)
        self.kpi_metadata = {
            '日人均会议数减少率': {
                'icon': '📊',
                'definition': '衡量团队日均会议数量的变化',
                'formula': '减少率(%) = (基线期均值 - 当前期均值) / 基线期均值 × 100%',
                'data_source': '会议数 = 即时会议 + 日程会议 + 1v1通话',
                'calculation_steps': [
                    '1. 计算基线期(9-10月)的日人均会议数均值',
                    '2. 计算当前期(最近4周)的日人均会议数均值',
                    '3. 使用公式计算减少率',
                    '4. 正值表示减少,负值表示增加'
                ],
                'target': '≥15%',
                'meaning': '会议数量减少15%以上表示改善措施有效'
            },
            '日人均会议时长减少率': {
                'icon': '⏱️',
                'definition': '衡量团队日均会议时长的变化',
                'formula': '减少率(%) = (基线期时长 - 当前期时长) / 基线期时长 × 100%',
                'data_source': '会议时长(分钟) = 所有在线会议的时长总和',
                'calculation_steps': [
                    '1. 计算基线期的日人均会议时长均值',
                    '2. 计算当前期的日人均会议时长均值',
                    '3. 使用公式计算减少率',
                    '4. 正值表示时长减少,负值表示时长增加'
                ],
                'target': '≥20%',
                'meaning': '会议时长减少20%以上表示时间利用效率提升'
            },
            '即时会议占比下降': {
                'icon': '⚡',
                'definition': '衡量即时会议(临时会议)相对于总会议数的占比变化',
                'formula': '下降幅度 = 基线期即时会议占比 - 当前期即时会议占比',
                'data_source': '即时会议占比 = 即时会议数 / 日人均线上会议数',
                'calculation_steps': [
                    '1. 计算基线期即时会议占比 = 即时会议数 / 日人均线上会议数',
                    '2. 计算当前期即时会议占比 = 即时会议数 / 日人均线上会议数',
                    '3. 计算两者差值(百分点)',
                    '4. 正值表示即时会议占比下降,负值表示上升'
                ],
                'target': '≥10百分点',
                'meaning': '即时会议占比下降表示会议计划性提升'
            },
            '会议时长效率提升': {
                'icon': '⚙️',
                'definition': '衡量日人均会议时长的变化',
                'formula': '效率提升(%) = (基线期时长 - 当前期时长) / 基线期时长 × 100%',
                'data_source': '使用字段: 日人均线上会议时长(分钟)',
                'calculation_steps': [
                    '1. 计算基线期日人均线上会议时长的均值',
                    '2. 计算当前期日人均线上会议时长的均值',
                    '3. 使用公式计算效率提升率',
                    '4. 正值表示时长缩短(效率提升)'
                ],
                'target': '≥10%',
                'meaning': '会议时长缩短表示会议效率提升'
            },
            '1v1通话替代率': {
                'icon': '📞',
                'definition': '衡量1v1通话占比的下降程度',
                'formula': '替代率(%) = (基线期1v1占比 - 当前期1v1占比) / 基线期1v1占比 × 100%',
                'data_source': '1v1占比 = 1v1通话数 / 人的会议数',
                'calculation_steps': [
                    '1. 计算基线期1v1通话占比',
                    '2. 计算当前期1v1通话占比',
                    '3. 计算占比下降的相对比率',
                    '4. 正值表示1v1被其他沟通方式替代'
                ],
                'target': '≥5%',
                'meaning': '1v1通话减少表示异步沟通工具使用增加'
            },
            '团队会议负担分布均衡度': {
                'icon': '⚖️',
                'definition': '衡量团队成员会议负担的均衡程度',
                'formula': '均衡度改善(%) = (基线期变异系数 - 当前期变异系数) / 基线期变异系数 × 100%',
                'data_source': '变异系数(CV) = 标准差 / 均值',
                'calculation_steps': [
                    '1. 计算基线期各成员会议数的变异系数',
                    '2. 计算当前期各成员会议数的变异系数',
                    '3. 计算变异系数的下降率',
                    '4. 变异系数越小,分布越均衡'
                ],
                'target': '变异系数下降≥10%',
                'meaning': '变异系数下降表示会议负担更加均衡'
            },
            'Top10重度用户改善率': {
                'icon': '👥',
                'definition': '衡量会议最多的Top10用户的改善情况',
                'formula': '改善率(%) = (基线期Top10均值 - 当前期Top10均值) / 基线期Top10均值 × 100%',
                'data_source': 'Top10用户 = 基线期会议数最多的10位成员',
                'calculation_steps': [
                    '1. 识别基线期会议数最多的10位用户',
                    '2. 计算这10位用户在基线期的平均会议数',
                    '3. 计算这10位用户在当前期的平均会议数',
                    '4. 计算改善率'
                ],
                'target': '≥20%',
                'meaning': '重度用户改善表示针对性措施有效'
            },
            '周度波动性': {
                'icon': '📉',
                'definition': '衡量每周会议数的稳定性',
                'formula': '波动系数 = 周度标准差 / 平均值',
                'data_source': '按周统计的日人均会议数',
                'calculation_steps': [
                    '1. 计算每周的日人均会议数',
                    '2. 计算周度数据的标准差',
                    '3. 计算周度数据的均值',
                    '4. 计算波动系数'
                ],
                'target': '<0.15',
                'meaning': '波动系数越小,会议数越稳定'
            }
        }

    def image_to_base64(self, image_path: str) -> str:
        """将图片转换为base64编码"""
        if not os.path.exists(image_path):
            return ""

        with open(image_path, 'rb') as f:
            image_data = f.read()
            return base64.b64encode(image_data).decode('utf-8')

    def generate_kpi_card_html(self, kpi_name: str, kpi_data: Dict, category: str = 'primary') -> str:
        """
        生成KPI卡片HTML

        Args:
            kpi_name: KPI名称
            kpi_data: KPI数据
            category: 类别(primary/secondary/monitoring)

        Returns:
            str: HTML代码
        """
        metadata = self.kpi_metadata.get(kpi_name, {})
        达标 = kpi_data.get('达标', False)

        # 提取数值
        values_html = ""
        for key, value in kpi_data.items():
            if key == '达标':
                continue
            if isinstance(value, float):
                value_str = f"{value:.2f}"
            else:
                value_str = str(value)

            values_html += f"""
                <div class="result-item">
                    <span class="result-label">{key}</span>
                    <span class="result-value">{value_str}</span>
                </div>
"""

        html = f"""
        <div class="kpi-card {'kpi-passed' if 达标 else 'kpi-failed'}">
            <div class="kpi-header">
                <div class="kpi-title">
                    <span class="kpi-icon">{metadata.get('icon', '📊')}</span>
                    <span>{kpi_name}</span>
                </div>
                <span class="status-badge {'badge-success' if 达标 else 'badge-danger'}">
                    {'✅ 达标' if 达标 else '❌ 未达标'}
                </span>
            </div>

            <!-- 计算讲解部分 -->
            <div class="calculation-section">
                <h4 class="section-subtitle">📖 计算讲解</h4>

                <div class="calc-item">
                    <div class="calc-label">定义</div>
                    <div class="calc-content">{metadata.get('definition', '')}</div>
                </div>

                <div class="calc-item">
                    <div class="calc-label">计算公式</div>
                    <div class="calc-formula">{metadata.get('formula', '')}</div>
                </div>

                <div class="calc-item">
                    <div class="calc-label">数据来源</div>
                    <div class="calc-content">{metadata.get('data_source', '')}</div>
                </div>

                <div class="calc-item">
                    <div class="calc-label">计算步骤</div>
                    <div class="calc-steps">
"""

        for step in metadata.get('calculation_steps', []):
            html += f'                        <div class="step-item">{step}</div>\n'

        html += f"""
                    </div>
                </div>

                <div class="calc-item">
                    <div class="calc-label">目标值</div>
                    <div class="calc-target">{metadata.get('target', '')}</div>
                </div>

                <div class="calc-item">
                    <div class="calc-label">指标意义</div>
                    <div class="calc-content">{metadata.get('meaning', '')}</div>
                </div>
            </div>

            <!-- 计算结果部分 -->
            <div class="result-section">
                <h4 class="section-subtitle">📊 计算结果</h4>
                <div class="result-grid">
{values_html}
                </div>
            </div>
        </div>
"""
        return html

    def generate_dashboard(self, kpi_results: Dict, trend_analysis: Dict,
                          anomalies_count: int = 0, top_users_count: int = 0) -> str:
        """生成HTML仪表盘"""

        # 读取图片
        trend_img = self.image_to_base64(os.path.join(self.output_dir, 'trend_meetings.png'))
        comparison_img = self.image_to_base64(os.path.join(self.output_dir, 'comparison.png'))

        # 提取KPI数据
        primary_kpis = kpi_results.get('主要KPI', {})
        secondary_kpis = kpi_results.get('次要KPI', {})
        monitoring = kpi_results.get('监控指标', {})

        # 计算达标率
        primary_passed = sum(1 for kpi in primary_kpis.values() if kpi.get('达标', False))
        primary_total = len(primary_kpis)
        pass_rate = (primary_passed / primary_total * 100) if primary_total > 0 else 0

        html_content = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>会议改善效果评估仪表盘 V2</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, "PingFang SC", "Microsoft YaHei", sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            color: #333;
            line-height: 1.6;
        }}

        .container {{
            max-width: 1600px;
            margin: 0 auto;
        }}

        .header {{
            background: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 10px 40px rgba(0,0,0,0.2);
            margin-bottom: 30px;
            text-align: center;
        }}

        .header h1 {{
            font-size: 2.8em;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 15px;
        }}

        .header .subtitle {{
            font-size: 1.2em;
            color: #666;
            margin-bottom: 10px;
        }}

        .header .timestamp {{
            font-size: 0.95em;
            color: #999;
        }}

        .summary-cards {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
            gap: 25px;
            margin-bottom: 30px;
        }}

        .summary-card {{
            background: white;
            padding: 30px;
            border-radius: 20px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            transition: all 0.3s;
        }}

        .summary-card:hover {{
            transform: translateY(-5px);
            box-shadow: 0 15px 35px rgba(0,0,0,0.15);
        }}

        .card-title {{
            font-size: 0.9em;
            color: #666;
            text-transform: uppercase;
            letter-spacing: 1.5px;
            margin-bottom: 15px;
        }}

        .card-value {{
            font-size: 3em;
            font-weight: bold;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 10px;
        }}

        .progress-bar {{
            width: 100%;
            height: 8px;
            background: #e5e7eb;
            border-radius: 10px;
            overflow: hidden;
            margin: 15px 0;
        }}

        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
            transition: width 1.5s cubic-bezier(0.4, 0, 0.2, 1);
        }}

        .section {{
            background: white;
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            margin-bottom: 30px;
        }}

        .section-title {{
            font-size: 2em;
            color: #667eea;
            margin-bottom: 30px;
            padding-bottom: 15px;
            border-bottom: 3px solid #667eea;
        }}

        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(500px, 1fr));
            gap: 30px;
        }}

        .kpi-card {{
            border-radius: 15px;
            padding: 30px;
            background: #fafafa;
            border: 2px solid #e5e7eb;
            transition: all 0.3s;
        }}

        .kpi-card:hover {{
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
            transform: translateY(-2px);
        }}

        .kpi-passed {{
            border-left: 6px solid #10b981;
            background: linear-gradient(135deg, #f0fdf4 0%, #ffffff 100%);
        }}

        .kpi-failed {{
            border-left: 6px solid #ef4444;
            background: linear-gradient(135deg, #fef2f2 0%, #ffffff 100%);
        }}

        .kpi-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 25px;
            padding-bottom: 15px;
            border-bottom: 2px solid #e5e7eb;
        }}

        .kpi-title {{
            font-size: 1.3em;
            font-weight: bold;
            color: #1f2937;
            display: flex;
            align-items: center;
            gap: 10px;
        }}

        .kpi-icon {{
            font-size: 1.4em;
        }}

        .status-badge {{
            padding: 8px 20px;
            border-radius: 25px;
            font-size: 0.9em;
            font-weight: bold;
        }}

        .badge-success {{
            background: #10b981;
            color: white;
        }}

        .badge-danger {{
            background: #ef4444;
            color: white;
        }}

        .calculation-section {{
            background: white;
            border-radius: 12px;
            padding: 25px;
            margin-bottom: 20px;
            border: 1px solid #e5e7eb;
        }}

        .result-section {{
            background: white;
            border-radius: 12px;
            padding: 25px;
            border: 1px solid #e5e7eb;
        }}

        .section-subtitle {{
            font-size: 1.15em;
            color: #667eea;
            margin-bottom: 20px;
            font-weight: bold;
        }}

        .calc-item {{
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 1px dashed #e5e7eb;
        }}

        .calc-item:last-child {{
            border-bottom: none;
            margin-bottom: 0;
        }}

        .calc-label {{
            font-weight: bold;
            color: #4b5563;
            margin-bottom: 8px;
            font-size: 0.95em;
        }}

        .calc-content {{
            color: #6b7280;
            font-size: 0.95em;
            line-height: 1.7;
        }}

        .calc-formula {{
            background: #f3f4f6;
            padding: 12px 15px;
            border-radius: 8px;
            font-family: 'Courier New', monospace;
            color: #1f2937;
            font-size: 0.9em;
            border-left: 3px solid #667eea;
        }}

        .calc-steps {{
            color: #6b7280;
            font-size: 0.9em;
        }}

        .step-item {{
            padding: 8px 0;
            padding-left: 20px;
            position: relative;
        }}

        .step-item:before {{
            content: "▶";
            position: absolute;
            left: 0;
            color: #667eea;
            font-size: 0.8em;
        }}

        .calc-target {{
            background: #fef3c7;
            padding: 10px 15px;
            border-radius: 8px;
            color: #92400e;
            font-weight: bold;
            border-left: 3px solid #f59e0b;
        }}

        .result-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
        }}

        .result-item {{
            background: #f9fafb;
            padding: 15px;
            border-radius: 10px;
            border: 1px solid #e5e7eb;
        }}

        .result-label {{
            display: block;
            font-size: 0.85em;
            color: #6b7280;
            margin-bottom: 5px;
        }}

        .result-value {{
            display: block;
            font-size: 1.3em;
            font-weight: bold;
            color: #1f2937;
        }}

        .charts-section {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(600px, 1fr));
            gap: 30px;
            margin-bottom: 30px;
        }}

        .chart-card {{
            background: white;
            padding: 35px;
            border-radius: 20px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
        }}

        .chart-title {{
            font-size: 1.6em;
            color: #667eea;
            margin-bottom: 25px;
            text-align: center;
            font-weight: bold;
        }}

        .chart-image {{
            width: 100%;
            border-radius: 15px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.05);
        }}

        .footer {{
            background: white;
            padding: 25px;
            border-radius: 20px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            text-align: center;
            color: #6b7280;
            font-size: 0.9em;
        }}

        @media (max-width: 768px) {{
            .kpi-grid {{
                grid-template-columns: 1fr;
            }}

            .charts-section {{
                grid-template-columns: 1fr;
            }}

            .header h1 {{
                font-size: 2em;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <!-- Header -->
        <div class="header">
            <h1>📊 会议改善效果评估仪表盘 V2</h1>
            <div class="subtitle">Meeting Improvement Evaluation Dashboard - Enhanced Edition</div>
            <div class="timestamp">报告生成时间: {datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}</div>
        </div>

        <!-- Summary Cards -->
        <div class="summary-cards">
            <div class="summary-card">
                <div class="card-title">主要KPI达标率</div>
                <div class="card-value">{primary_passed}/{primary_total}</div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {pass_rate}%"></div>
                </div>
            </div>

            <div class="summary-card">
                <div class="card-title">数据记录总数</div>
                <div class="card-value">264</div>
                <div class="card-title" style="margin-top: 10px; font-size: 0.8em;">基线期: 97 | 当前期: 167</div>
            </div>

            <div class="summary-card">
                <div class="card-title">检测到异常</div>
                <div class="card-value">{anomalies_count}</div>
            </div>

            <div class="summary-card">
                <div class="card-title">Top用户数</div>
                <div class="card-value">{top_users_count}</div>
            </div>
        </div>

        <!-- Charts -->
        <div class="charts-section">
            <div class="chart-card">
                <h3 class="chart-title">📈 会议数趋势分析</h3>
"""

        if trend_img:
            html_content += f'                <img src="data:image/png;base64,{trend_img}" alt="趋势图" class="chart-image">\n'
        else:
            html_content += '                <p style="text-align: center; color: #999;">图表文件未找到</p>\n'

        html_content += """
            </div>

            <div class="chart-card">
                <h3 class="chart-title">📊 基线期 vs 当前期对比</h3>
"""

        if comparison_img:
            html_content += f'                <img src="data:image/png;base64,{comparison_img}" alt="对比图" class="chart-image">\n'
        else:
            html_content += '                <p style="text-align: center; color: #999;">图表文件未找到</p>\n'

        html_content += """
            </div>
        </div>

        <!-- Primary KPIs -->
        <div class="section">
            <h2 class="section-title">🎯 主要KPI指标</h2>
            <div class="kpi-grid">
"""

        # 生成主要KPI卡片
        for kpi_name, kpi_data in primary_kpis.items():
            html_content += self.generate_kpi_card_html(kpi_name, kpi_data, 'primary')

        html_content += """
            </div>
        </div>

        <!-- Secondary KPIs -->
        <div class="section">
            <h2 class="section-title">📈 次要KPI指标</h2>
            <div class="kpi-grid">
"""

        # 生成次要KPI卡片
        for kpi_name, kpi_data in secondary_kpis.items():
            html_content += self.generate_kpi_card_html(kpi_name, kpi_data, 'secondary')

        html_content += """
            </div>
        </div>

        <!-- Monitoring Indicators -->
        <div class="section">
            <h2 class="section-title">🔍 监控指标</h2>
            <div class="kpi-grid">
"""

        # 生成监控指标卡片
        for indicator_name, indicator_data in monitoring.items():
            html_content += self.generate_kpi_card_html(indicator_name, indicator_data, 'monitoring')

        html_content += f"""
            </div>
        </div>

        <!-- Footer -->
        <div class="footer">
            <p><strong>会议改善效果评估系统 V2</strong> - 每个指标包含完整的计算讲解和结果展示</p>
            <p>数据来源: /Users/admin/Desktop/regular/input/</p>
            <p>技术支持: Claude Code + Python分析工具包</p>
        </div>
    </div>

    <script>
        // 添加加载动画
        window.addEventListener('load', function() {{
            const progressBars = document.querySelectorAll('.progress-fill');
            progressBars.forEach(bar => {{
                const width = bar.style.width;
                bar.style.width = '0%';
                setTimeout(() => {{
                    bar.style.width = width;
                }}, 100);
            }});
        }});
    </script>
</body>
</html>
"""

        # 保存HTML文件
        filepath = os.path.join(self.output_dir, 'dashboard_v2.html')
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(html_content)

        return filepath


if __name__ == "__main__":
    from data_loader import MeetingDataLoader
    from calculator import MeetingMetricsCalculator
    from analyzer import MeetingDataAnalyzer

    print("=" * 60)
    print("生成增强版HTML仪表盘")
    print("=" * 60)

    # 加载数据
    loader = MeetingDataLoader('../input')
    all_data = loader.load_all_data()

    if all_data is None:
        print("❌ 数据加载失败")
        exit(1)

    baseline = loader.get_baseline_data()
    current = loader.get_recent_weeks_data(4)

    # 计算KPI
    calculator = MeetingMetricsCalculator(baseline, current)
    weekly_data = loader.get_data_by_period_type('weekly')
    kpi_results = calculator.calculate_all_kpis(weekly_data)

    # 分析
    analyzer = MeetingDataAnalyzer(all_data)
    trend_analysis = {
        '日人均线上会议数': analyzer.analyze_trend('日人均线上会议数'),
        '日人均线上会议时长': analyzer.analyze_trend('日人均线上会议时长(分钟)')
    }

    anomalies = analyzer.detect_anomalies('日人均线上会议数', threshold=2.0)
    top_users = analyzer.identify_top_users('日人均线上会议数', n=10)

    # 生成HTML
    generator = HTMLDashboardGeneratorV2('../output')
    filepath = generator.generate_dashboard(
        kpi_results,
        trend_analysis,
        len(anomalies),
        len(top_users)
    )

    print(f"\n✅ 增强版HTML仪表盘已生成: {filepath}")
    print(f"\n打开方式: open {filepath}")
