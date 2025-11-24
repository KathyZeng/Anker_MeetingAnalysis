# 会议改善效果评估系统

一个用于分析和可视化会议数据的完整解决方案,支持KPI计算、趋势分析和交互式仪表盘生成。

---

## 📁 项目结构

```
regular/
├── input/                          # 数据输入目录
│   ├── 9月会议详情.csv
│   ├── 10月会议详情.csv
│   └── ...                        # 其他周期数据
│
├── meeting_analysis/               # 核心分析模块
│   ├── __init__.py
│   ├── data_loader.py             # 数据加载器
│   ├── calculator.py              # KPI计算器
│   ├── analyzer.py                # 数据分析器
│   ├── visualizer.py              # 可视化生成器
│   ├── reporter.py                # 报告生成器
│   ├── dashboard_generator.py     # 仪表盘生成器
│   ├── html_generator_v2.py       # HTML生成器
│   └── main.py                    # 主执行脚本
│
├── output/                         # 输出结果目录
│   ├── interactive_dashboard.html # 交互式仪表盘
│   ├── comparison.png             # 对比图表
│   ├── trend_meetings.png         # 趋势图表
│   ├── executive_summary.md       # 管理层摘要
│   ├── detailed_report.md         # 详细报告
│   └── archived/                  # 旧版本归档
│
├── 使用指南.md                     # 系统使用指南
├── 可视化报表页面设计方案.md       # 仪表盘设计方案
├── 会议改善效果评估方案.md         # 评估方法说明
├── 派生指标与统计分析表.md         # 指标定义
├── generate_interactive_dashboard.py  # 快速生成脚本
└── sync_new_tables.py             # 数据同步工具
```

---

## 🚀 快速开始

### 1. 准备数据
将会议数据CSV文件放入 `input/` 目录:
- 文件命名格式: `{周期}会议详情.csv`
- 例如: `9月会议详情.csv`, `10.20-10.26会议详情.csv`

### 2. 运行分析
```bash
# 完整分析(生成所有报告和仪表盘)
python3 meeting_analysis/main.py

# 快速摘要(仅显示关键指标)
python3 meeting_analysis/main.py --mode quick

# 生成交互式仪表盘
python3 generate_interactive_dashboard.py
```

### 3. 查看结果
在浏览器中打开:
```bash
open output/interactive_dashboard.html
```

---

## 📊 功能特性

### 数据分析
- ✅ 多周期数据加载和处理
- ✅ 基线期与当前期对比
- ✅ KPI指标自动计算
- ✅ 趋势分析和异常检测
- ✅ Top用户识别

### 可视化
- ✅ 交互式HTML仪表盘
- ✅ KPI卡片展示
- ✅ ECharts动态图表
- ✅ 对比和趋势图
- ✅ 响应式设计

### 报告生成
- ✅ 管理层摘要报告
- ✅ 详细分析报告
- ✅ 周度数据摘要
- ✅ 文本和图表导出

---

## 📈 主要KPI指标

1. **KPI-01**: 日人均会议数减少率 (目标: ≥15%)
2. **KPI-02**: 日人均会议时长减少率 (目标: ≥15%)
3. **KPI-03**: 即时会议占比降低 (目标: ≤25%)
4. **KPI-04**: 1v1通话占比降低 (目标: ≤25%)

详见: `派生指标与统计分析表.md`

---

## 📖 文档说明

- **使用指南.md** - 系统使用说明和命令行选项
- **可视化报表页面设计方案.md** - 仪表盘UI/UX设计方案
- **会议改善效果评估方案.md** - 评估方法和指标定义
- **派生指标与统计分析表.md** - 所有指标的计算方法
- **PROJECT_CLEANUP_REPORT.md** - 项目清理记录

---

## 🔧 依赖环境

```bash
# Python 3.7+
pip install pandas numpy matplotlib
```

---

## 📝 数据格式要求

CSV文件需包含以下字段:
- `user_name`: 用户姓名
- `period_name`: 周期名称
- `日人均线上会议数`: 日均会议次数
- `日人均线上会议时长(分钟)`: 日均时长
- `即时会议数`, `日程会议数`, `1v1通话数`: 会议类型统计

---

## 🎯 下一步计划

- [ ] 完善交互式仪表盘(按设计方案)
- [ ] 增加数据筛选和导出功能
- [ ] 支持更多可视化图表类型
- [ ] 添加单元测试

---

## 📧 联系方式

如有问题或建议,请参考 `使用指南.md` 或查看项目文档。

---

**版本**: 1.0
**最后更新**: 2025-11-20
**状态**: 生产就绪 ✅
