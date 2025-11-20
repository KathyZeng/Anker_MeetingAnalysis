# 会议改善效果评估系统

> 基于飞书会议数据的效果评估分析工具

---

## 🚀 快速开始

### 三步生成仪表盘

```bash
# 1️⃣ 放入新数据
cp 11月会议详情.csv input/

# 2️⃣ 生成仪表盘
python3 generate_full_dashboard.py

# 3️⃣ 查看结果
open output/meeting_dashboard_full.html
```

详细说明请查看: [docs/user-guides/使用指南.md](docs/user-guides/使用指南.md)

---

## 📚 文档导航

| 分类 | 路径 | 说明 |
|------|------|------|
| **用户指南** | [docs/user-guides/](docs/user-guides/) | 使用说明、快速更新指南 |
| **技术文档** | [docs/technical/](docs/technical/) | 业务方案、设计文档、指标定义 |
| **V2设计** | [docs/v2-design/](docs/v2-design/) | V2版本技术方案和升级计划 |
| **分析报告** | [docs/analysis-reports/](docs/analysis-reports/) | 历史分析报告和更新日志 |
| **归档文档** | [docs/archives/](docs/archives/) | 历史文档和临时记录 |

---

## 📊 核心功能

### 主要KPI指标

1. **日人均线上会议数（即时+日程）** - 不含1v1通话
2. **日人均线上会议时长（即时+日程）** - 不含1v1通话
3. **即时会议占比** - 反映会议计划性
4. **会议规模人均参会人数** - 会议效率指标

### 数据分析模块

- ✅ **概览页面**: KPI卡片、会议类型分布、趋势图
- ✅ **原始数据**: 全量数据表格、筛选、排序、分页
- ✅ **分析结果**: Top10用户、用户分层、异常检测
- ✅ **人员详情**: 单人详细指标和历史趋势

---

## 📂 项目结构

```
regular/
├── 📁 input/                        # 📥 CSV数据输入
│   ├── 9月会议详情.csv
│   ├── 10月会议详情.csv
│   └── 11.03-11.09会议详情.csv
│
├── 📁 output/                       # 📤 HTML仪表盘输出
│   ├── meeting_dashboard_full.html # ⭐ 主仪表盘
│   └── archived/                   # 历史版本
│
├── 📁 meeting_analysis/             # 🧮 核心分析模块
│   ├── data_loader.py              # 数据加载
│   ├── calculator.py               # KPI计算
│   ├── analyzer.py                 # 数据分析
│   ├── dashboard_generator.py      # 数据准备
│   └── full_dashboard_gen.py       # HTML生成
│
├── 📁 docs/                         # 📚 文档中心
│   ├── user-guides/                # 用户指南
│   ├── technical/                  # 技术文档
│   ├── v2-design/                  # V2设计
│   ├── analysis-reports/           # 分析报告
│   └── archives/                   # 归档文档
│
├── 📄 generate_full_dashboard.py    # 🚀 主生成脚本
├── 📄 README.md                     # 本文件
└── 📄 .gitignore                    # Git配置
```

---

## 🔧 系统要求

### 环境依赖

- **Python**: 3.7+
- **必需库**: Pandas, NumPy
- **浏览器**: Chrome, Firefox, Safari (支持ECharts)

### 安装依赖

```bash
pip install pandas numpy
```

---

## 📋 CSV数据格式

### 必需字段

| 字段名 | 类型 | 说明 |
|--------|------|------|
| `user_name` | 文本 | 用户名 |
| `日人均线上会议数-即时+日程` | 浮点 | 日均会议数（不含1v1） |
| `日人均线上会议时长(分钟)-即时+日程` | 浮点 | 日均时长（不含1v1） |
| `即时会议` | 整数 | 即时会议数量 |
| `日程会议` | 整数 | 日程会议数量 |
| `即时+日程会议` | 整数 | 即时+日程会议总数 |
| `1v1通话数` | 整数 | 1v1通话次数 |
| `人的会议数` | 整数 | 所有会议总数 |

详细字段说明: [docs/technical/派生指标与统计分析表.md](docs/technical/派生指标与统计分析表.md)

---

## 📈 使用示例

### 场景1: 新增一个月的数据

```bash
# 1. 将新CSV放入input目录
cp 12月会议详情.csv input/

# 2. 重新生成仪表盘
python3 generate_full_dashboard.py

# 3. 打开查看
open output/meeting_dashboard_full.html
```

### 场景2: 查看历史版本

```bash
# 查看归档的历史仪表盘
open output/archived/dashboard_2025-11-19.html
```

---

## 🎯 核心特性

### V1.0 当前版本

- ✅ **自动化处理**: 一键生成完整仪表盘
- ✅ **多周期对比**: 基线期（9-10月）vs 当前期（最近4周）
- ✅ **深度分析**: Top10用户、分层分析、异常检测
- ✅ **交互式图表**: ECharts可视化，支持筛选、排序
- ✅ **单文件输出**: HTML包含所有数据和代码，无需服务器

### V2.0 规划中

- 🔄 **Web界面上传**: 拖拽上传CSV，无需命令行
- 🔄 **灵活周期选择**: 用户自定义基线期和对比期
- 🔄 **实时生成**: 上传数据后立即生成报告
- 🔄 **数据管理**: 按周组织数据，便于管理和删除

详细V2方案: [docs/v2-design/V2_简化技术方案.md](docs/v2-design/V2_简化技术方案.md)

---

## 💡 常见问题

### Q: CSV文件命名有要求吗？

A: 支持两种格式:
- **月度**: `9月会议详情.csv`
- **周度**: `11.03-11.09会议详情.csv`

### Q: 生成失败怎么办？

A: 检查以下几点:
1. CSV文件编码是否为UTF-8
2. 必需字段是否完整
3. 数值字段是否为纯数字

### Q: 如何修改基线期定义？

A: 当前版本基线期硬编码为9月+10月，V2版本将支持动态选择。

更多问题: [docs/user-guides/使用指南.md](docs/user-guides/使用指南.md)

---

## 📞 更多帮助

- **快速更新指南**: [docs/user-guides/快速更新指南.md](docs/user-guides/快速更新指南.md)
- **数据更新操作**: [docs/user-guides/数据更新操作指南.md](docs/user-guides/数据更新操作指南.md)
- **仪表盘使用**: [docs/user-guides/仪表盘使用说明.md](docs/user-guides/仪表盘使用说明.md)
- **技术架构**: [docs/technical/可视化报表页面设计方案.md](docs/technical/可视化报表页面设计方案.md)

---

## 📅 版本历史

- **2025-11-20**: V1.0 完成，文档结构优化
- **2025-11-19**: 修复即时会议占比显示问题
- **2025-11-19**: 添加用户分层和异常检测
- **2025-11-16**: 完成完整交互式仪表盘

详细更新日志: [docs/analysis-reports/](docs/analysis-reports/)

---

## 📝 许可证

内部使用项目

---

**开始使用**: `python3 generate_full_dashboard.py` 🚀
