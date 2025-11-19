# 项目清理计划

生成时间: 2025-11-20

## 📋 清理目标

整理项目文件结构,删除临时文件、备份文件和冗余文件,保持项目目录清晰。

---

## 🔍 识别的文件分类

### 1️⃣ 需要删除的文件

#### 备份文件 (2个)
- `meeting_analysis/dashboard_generator.py.backup` - 备份文件
- `meeting_analysis/dashboard_generator.py.old` - 旧版本文件

#### Python缓存 (1个目录)
- `meeting_analysis/__pycache__/` - Python字节码缓存

#### 临时/测试文件
- `meeting_analysis/test_dashboard.py` - 测试文件(如已完成测试)
- `meeting_analysis/simple_dashboard_generator.py` - 简化版本(如已合并功能)

#### 临时文档文件
- `meeting_analysis/BEFORE_AFTER_COMPARISON.md` - 重构前后对比(已完成)
- `meeting_analysis/REFACTORING_REPORT.md` - 重构报告(已完成)
- `meeting_analysis/REFACTORING_SUMMARY.txt` - 重构摘要(已完成)
- `meeting_analysis/CARD_LAYOUT_GUIDE.md` - 卡片布局指南(可归档)
- `meeting_analysis/verify_refactoring.sh` - 验证脚本(已完成验证)

#### Output目录中的重复HTML
- `output/dashboard.html` - 旧版本
- `output/dashboard_v2.html` - v2版本
- `output/dashboard_clean.html` - 清理版本
- 保留: `output/interactive_dashboard.html` - 最新交互式版本

---

### 2️⃣ 需要保留的核心文件

#### 核心Python模块 (9个)
- `meeting_analysis/__init__.py`
- `meeting_analysis/data_loader.py`
- `meeting_analysis/calculator.py`
- `meeting_analysis/analyzer.py`
- `meeting_analysis/visualizer.py`
- `meeting_analysis/reporter.py`
- `meeting_analysis/dashboard_generator.py`
- `meeting_analysis/html_generator_v2.py`
- `meeting_analysis/main.py`

#### 文档文件
- `meeting_analysis/README.md` - 模块说明
- `使用指南.md` - 用户指南
- `可视化报表页面设计方案.md` - 设计方案
- `会议改善效果评估方案.md` - 评估方案
- `派生指标与统计分析表.md` - 指标说明
- `README_同步说明.md` - 同步说明

#### 工具脚本
- `generate_clean_dashboard.sh` - 生成脚本
- `generate_interactive_dashboard.py` - 交互式生成脚本
- `sync_new_tables.py` - 数据同步脚本

#### 数据文件 (input/)
- 所有CSV文件保留
- `.processed_tables.json` 保留

#### 输出文件 (output/)
- `interactive_dashboard.html` - 最新仪表盘
- `comparison.png` - 对比图
- `trend_meetings.png` - 趋势图
- `executive_summary.md` - 管理层摘要
- `detailed_report.md` - 详细报告
- `weekly_summary_*.md` - 周报
- `dashboard_summary.txt` - 文本摘要

---

## 🗑️ 清理操作清单

### 步骤1: 删除备份文件
```bash
rm meeting_analysis/dashboard_generator.py.backup
rm meeting_analysis/dashboard_generator.py.old
```

### 步骤2: 清理Python缓存
```bash
rm -rf meeting_analysis/__pycache__
```

### 步骤3: 删除临时文档
```bash
rm meeting_analysis/BEFORE_AFTER_COMPARISON.md
rm meeting_analysis/REFACTORING_REPORT.md
rm meeting_analysis/REFACTORING_SUMMARY.txt
rm meeting_analysis/CARD_LAYOUT_GUIDE.md
rm meeting_analysis/verify_refactoring.sh
```

### 步骤4: 清理测试文件
```bash
rm meeting_analysis/test_dashboard.py
rm meeting_analysis/simple_dashboard_generator.py
```

### 步骤5: 整理output目录
```bash
# 移动旧版本到归档目录
mkdir -p output/archived
mv output/dashboard.html output/archived/
mv output/dashboard_v2.html output/archived/
mv output/dashboard_clean.html output/archived/
```

### 步骤6: 清理空目录
```bash
find output -type d -empty -delete
```

---

## 📊 清理统计

### 删除前
- meeting_analysis Python文件: 12个
- 备份文件: 2个
- 临时文档: 6个
- output HTML文件: 4个

### 删除后预计
- meeting_analysis Python文件: 9个 (核心模块)
- 备份文件: 0个
- 临时文档: 0个
- output HTML文件: 1个 (最新版本)
- 归档文件: 3个

---

## ✅ 验证清单

- [ ] 备份文件已删除
- [ ] Python缓存已清理
- [ ] 临时文档已删除
- [ ] 测试文件已删除
- [ ] 旧版HTML已归档
- [ ] 核心功能正常运行
- [ ] 数据文件完整
- [ ] 输出目录整洁

---

## 🔄 清理后的项目结构

```
regular/
├── input/                          # 数据目录
│   ├── 9月会议详情.csv
│   ├── 10月会议详情.csv
│   └── ...
├── meeting_analysis/               # 核心模块
│   ├── __init__.py
│   ├── data_loader.py
│   ├── calculator.py
│   ├── analyzer.py
│   ├── visualizer.py
│   ├── reporter.py
│   ├── dashboard_generator.py
│   ├── html_generator_v2.py
│   ├── main.py
│   └── README.md
├── output/                         # 输出目录
│   ├── interactive_dashboard.html  # 最新仪表盘
│   ├── comparison.png
│   ├── trend_meetings.png
│   ├── executive_summary.md
│   ├── detailed_report.md
│   └── archived/                   # 归档目录
│       ├── dashboard.html
│       ├── dashboard_v2.html
│       └── dashboard_clean.html
├── 使用指南.md
├── 可视化报表页面设计方案.md
├── 会议改善效果评估方案.md
├── 派生指标与统计分析表.md
├── generate_clean_dashboard.sh
├── generate_interactive_dashboard.py
└── sync_new_tables.py
```

---

## 📝 注意事项

1. **执行前备份**: 清理前建议先备份整个项目
2. **逐步执行**: 按步骤执行,每步后验证
3. **保留归档**: 旧版HTML移到archived目录而非直接删除
4. **验证功能**: 清理后运行主程序验证功能正常

---

**执行建议**: 可以手动执行各步骤,或者使用自动化脚本
