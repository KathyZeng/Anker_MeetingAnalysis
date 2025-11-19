# 会议改善效果评估分析工具包

## 📋 概述

这是一个完整的Python分析工具包,用于评估研发团队会议改善措施(如固定会议窗口)的实施效果。

## 🎯 核心功能

### 1. 数据加载 (data_loader.py)
- 自动加载所有CSV数据文件
- 识别月度和周度数据格式
- 提取基线期(9-10月)和当前期(最近4周)数据
- 支持按周期、类型筛选数据

### 2. 指标计算 (calculator.py)
计算8个核心KPI指标:

**主要KPI (3个)**
- 日人均会议数减少率 (目标: ≥15%)
- 日人均会议时长减少率 (目标: ≥20%)
- 即时会议占比下降 (目标: ≥10百分点)

**次要KPI (3个)**
- 会议时长效率提升 (目标: ≥10%)
- 1v1通话替代率 (目标: ≥5%)
- 团队会议负担分布均衡度 (目标: 变异系数下降≥10%)

**监控指标 (2个)**
- 周度波动性 (目标: <0.15)
- Top 10重度会议用户改善率 (目标: ≥20%)

### 3. 统计分析 (analyzer.py)
- 趋势分析 (线性回归、R²拟合度)
- 异常检测 (Z-score方法)
- 分布分析 (均值、中位数、分位数等)
- 相关性分析 (皮尔逊、斯皮尔曼相关系数)
- 环比变化计算
- Top N用户识别

### 4. 可视化 (visualizer.py)
- 趋势折线图
- 对比柱状图
- 堆叠柱状图
- 热力图
- 饼图
- 箱线图
- 仪表盘文本摘要
- 支持matplotlib图形和文本模式双输出

### 5. 报告生成 (reporter.py)
生成4类Markdown格式报告:
- **管理层摘要报告** - 核心结论和达标情况
- **详细分析报告** - 完整的KPI、趋势、异常分析
- **个人健康报告** - 个人会议负担分析和建议
- **周报** - 每周数据概览

## 🚀 快速开始

### 安装依赖

```bash
# 核心依赖
pip install pandas numpy scipy

# 可选依赖 (用于图表生成)
pip install matplotlib seaborn
```

### 基础使用

#### 方式1: 使用主脚本 (推荐)

```bash
# 完整分析 (数据加载 → KPI计算 → 统计分析 → 可视化 → 报告生成)
python3 main.py

# 快速摘要模式 (仅显示关键KPI)
python3 main.py --mode quick

# 指定数据和输出目录
python3 main.py --data-dir /path/to/data --output-dir /path/to/output

# 静默模式
python3 main.py --quiet
```

#### 方式2: 作为Python模块使用

```python
from meeting_analysis import (
    MeetingDataLoader,
    MeetingMetricsCalculator,
    MeetingDataAnalyzer,
    MeetingVisualizer,
    MeetingReportGenerator
)

# 1. 加载数据
loader = MeetingDataLoader('input')
all_data = loader.load_all_data()
baseline = loader.get_baseline_data()
current = loader.get_recent_weeks_data(4)

# 2. 计算KPI
calculator = MeetingMetricsCalculator(baseline, current)
kpi_results = calculator.calculate_all_kpis()

# 3. 统计分析
analyzer = MeetingDataAnalyzer(all_data)
trend = analyzer.analyze_trend('日人均线上会议数')
anomalies = analyzer.detect_anomalies('日人均线上会议数')

# 4. 可视化
visualizer = MeetingVisualizer('output')
visualizer.create_dashboard_summary(kpi_results)

# 5. 生成报告
reporter = MeetingReportGenerator('output')
reporter.generate_executive_summary(kpi_results)
```

## 📂 目录结构

```
meeting_analysis/
├── __init__.py              # 模块初始化
├── data_loader.py           # 数据加载
├── calculator.py            # KPI指标计算
├── analyzer.py              # 统计分析
├── visualizer.py            # 可视化
├── reporter.py              # 报告生成
├── main.py                  # 主执行脚本
└── README.md                # 本文档

input/                       # 数据输入目录
├── 9月会议详情.csv
├── 10月会议详情.csv
├── 10.20-10.26会议详情.csv
├── ...
└── .processed_tables.json   # 已处理表格记录

output/                      # 分析输出目录
├── executive_summary.md     # 管理层摘要
├── detailed_report.md       # 详细报告
├── dashboard_summary.txt    # 仪表盘文本
├── trend_meetings.png       # 趋势图
├── comparison.png           # 对比图
└── weekly_summary_*.md      # 周报
```

## 📊 数据格式要求

### 输入CSV文件要求

1. **文件命名格式**:
   - 月度: `X月会议详情.csv` (如: 9月会议详情.csv)
   - 周度: `MM.DD-MM.DD会议详情.csv` (如: 10.20-10.26会议详情.csv)

2. **必需字段**:
   - `user_name`: 用户姓名
   - `日人均线上会议数`: 日均会议数
   - `日人均线上会议时长(分钟)`: 日均会议时长
   - `即时会议`: 即时会议数量
   - `日程会议`: 日程会议数量
   - `1v1通话数`: 1对1通话数量
   - `人的会议数`: 总会议数

3. **可选字段**:
   - `即时+日程会议`: 即时和日程会议总数
   - 其他业务字段

## 🔍 模块详解

### data_loader.py

```python
class MeetingDataLoader:
    def __init__(self, data_dir="input"):
        """初始化数据加载器"""

    def load_all_data(self):
        """加载所有CSV文件并合并"""

    def get_baseline_data(self):
        """获取基线期数据 (9月和10月)"""

    def get_recent_weeks_data(self, n_weeks=4):
        """获取最近N周的数据"""

    def get_data_by_period(self, period_name):
        """获取指定周期的数据"""

    def get_period_list(self):
        """获取所有周期列表"""
```

### calculator.py

```python
class MeetingMetricsCalculator:
    def __init__(self, baseline_data, current_data):
        """初始化计算器"""

    def calculate_primary_kpis(self):
        """计算3个主要KPI"""

    def calculate_meeting_efficiency(self):
        """计算会议时长效率提升"""

    def calculate_1v1_substitution_rate(self):
        """计算1v1通话替代率"""

    def calculate_burden_distribution(self):
        """计算团队负担分布均衡度"""

    def calculate_all_kpis(self, weekly_data=None):
        """计算所有KPI指标"""
```

### analyzer.py

```python
class MeetingDataAnalyzer:
    def __init__(self, data):
        """初始化分析器"""

    def analyze_trend(self, metric):
        """趋势分析 - 线性回归"""

    def detect_anomalies(self, metric, threshold=2.0):
        """异常检测 - Z-score方法"""

    def analyze_distribution(self, metric):
        """分布分析"""

    def compare_periods(self, metric, period1, period2):
        """周期对比分析 - t检验"""

    def identify_top_users(self, metric, n=10):
        """识别Top N用户"""

    def analyze_correlation(self, metric1, metric2):
        """相关性分析"""
```

### visualizer.py

```python
class MeetingVisualizer:
    def __init__(self, output_dir="output"):
        """初始化可视化器"""

    def plot_trend_line(self, data, x_col, y_col, ...):
        """绘制趋势折线图"""

    def plot_comparison_bar(self, categories, baseline, current, ...):
        """绘制对比柱状图"""

    def plot_stacked_bar(self, data, x_col, y_cols, ...):
        """绘制堆叠柱状图"""

    def create_dashboard_summary(self, kpi_results):
        """创建仪表盘文本摘要"""
```

### reporter.py

```python
class MeetingReportGenerator:
    def __init__(self, output_dir="output"):
        """初始化报告生成器"""

    def generate_executive_summary(self, kpi_results):
        """生成管理层摘要报告"""

    def generate_detailed_report(self, kpi_results, trend_analysis, ...):
        """生成详细分析报告"""

    def generate_personal_report(self, user_data, user_name, team_avg):
        """生成个人会议健康报告"""

    def generate_weekly_summary(self, week_data, week_name):
        """生成周报"""
```

## 🧪 测试

每个模块都包含独立的测试函数:

```bash
# 测试数据加载
python3 data_loader.py

# 测试指标计算
python3 calculator.py

# 测试统计分析
python3 analyzer.py

# 测试可视化
python3 visualizer.py

# 测试报告生成
python3 reporter.py
```

## 📈 使用示例

### 示例1: 生成管理层周报

```python
from meeting_analysis import MeetingDataLoader, MeetingMetricsCalculator, MeetingReportGenerator

# 加载数据
loader = MeetingDataLoader()
loader.load_all_data()
baseline = loader.get_baseline_data()
current = loader.get_recent_weeks_data(4)

# 计算KPI
calculator = MeetingMetricsCalculator(baseline, current)
kpi_results = calculator.calculate_all_kpis()

# 生成报告
reporter = MeetingReportGenerator()
report_path = reporter.generate_executive_summary(kpi_results)
print(f"报告已生成: {report_path}")
```

### 示例2: 分析特定用户

```python
from meeting_analysis import MeetingDataLoader, MeetingReportGenerator

loader = MeetingDataLoader()
all_data = loader.load_all_data()

# 获取特定用户数据
user_name = "张三"
user_data = all_data[all_data['user_name'] == user_name]

# 计算团队平均值
team_avg = {
    '日人均线上会议数': all_data['日人均线上会议数'].mean(),
    '日人均线上会议时长(分钟)': all_data['日人均线上会议时长(分钟)'].mean()
}

# 生成个人报告
reporter = MeetingReportGenerator()
report_path = reporter.generate_personal_report(user_data, user_name, team_avg)
print(f"个人报告已生成: {report_path}")
```

### 示例3: 趋势监控

```python
from meeting_analysis import MeetingDataLoader, MeetingDataAnalyzer

loader = MeetingDataLoader()
all_data = loader.load_all_data()

analyzer = MeetingDataAnalyzer(all_data)

# 分析会议数趋势
trend = analyzer.analyze_trend('日人均线上会议数')
print(f"趋势方向: {trend['direction']}")
print(f"变化率: {trend['change_rate']:.2f}%")
print(f"R²拟合度: {trend['r_squared']:.4f}")

# 检测异常
anomalies = analyzer.detect_anomalies('日人均线上会议数', threshold=2.0)
if not anomalies.empty:
    print(f"检测到 {len(anomalies)} 个异常数据点")
```

## 🔧 高级配置

### 自定义KPI目标值

修改 `calculator.py` 中的目标值:

```python
# 在 calculate_primary_kpis() 方法中
'日人均会议数减少率': {
    ...
    '目标': '≥15%',  # 修改此处
    '达标': meeting_reduction_rate >= 15  # 修改此处
}
```

### 自定义基线期

修改 `data_loader.py` 中的基线期定义:

```python
def get_baseline_data(self):
    # 选择其他月份作为基线
    baseline = monthly_data[monthly_data['month'].isin([8, 9])].copy()
    return baseline
```

### 自定义异常检测阈值

```python
# Z-score阈值越高,检测越严格
anomalies = analyzer.detect_anomalies('日人均线上会议数', threshold=3.0)
```

## 📝 输出报告示例

### 管理层摘要报告结构

```markdown
# 会议改善效果评估 - 管理层摘要报告

## 📊 核心结论
**主要KPI达标情况**: 3/3 项达标
✅ 评估结论: 会议改善措施效果显著,所有主要KPI均已达标!

## 🎯 主要KPI指标
### ✅ 日人均会议数减少率
| 指标 | 数值 |
|------|------|
| 基线期均值 | 4.50 |
| 当前期均值 | 3.60 |
| 减少率(%) | 20.00 |
| 目标 | ≥15% |

...

## 💡 行动建议
1. 巩固成果: 继续保持当前的会议管理机制
2. 经验总结: 总结固定会议窗口等有效措施
3. 持续监控: 保持每周监控,关注波动性指标
```

## ⚙️ 故障排查

### 问题1: 找不到数据文件

**解决**: 确保CSV文件在 `input/` 目录下,且命名格式正确

### 问题2: 缺少必需字段

**错误**: `KeyError: '日人均线上会议数'`

**解决**: 检查CSV文件是否包含所有必需字段

### 问题3: matplotlib未安装

**解决**: 系统会自动切换到文本模式,或安装matplotlib:
```bash
pip install matplotlib
```

### 问题4: 基线期或当前期数据为空

**解决**: 确保input目录下至少包含:
- 9月和10月的月度数据
- 最近4周的周度数据

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交Issue和Pull Request

## 📧 联系方式

如有问题,请通过以下方式联系:
- 提交GitHub Issue
- 发送邮件至项目负责人

---

**版本**: v1.0.0
**最后更新**: 2025-11-19
