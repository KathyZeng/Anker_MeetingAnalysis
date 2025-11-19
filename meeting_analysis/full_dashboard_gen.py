#!/usr/bin/env python3
"""
完整仪表盘生成器 - 按照《可视化报表页面设计方案.md》
实现四大模块:
1. 概览页面 (Dashboard Overview)
2. 原始数据页面 (Raw Data)
3. 分析结果页面 (Analysis Results)
4. 人员详情页面 (Personnel Details)
"""

import json
import pandas as pd
import numpy as np
from datetime import datetime
from typing import Dict, List
from pathlib import Path


class NumpyEncoder(json.JSONEncoder):
    """自定义JSON编码器"""
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, np.bool_):
            return bool(obj)
        elif pd.isna(obj):
            return None
        return super().default(obj)


class FullDashboardGenerator:
    """完整仪表盘生成器"""

    def __init__(self, output_dir="output"):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def generate(self, data: Dict) -> str:
        """生成完整的交互式仪表盘HTML"""
        html = self._generate_html_structure(data)

        output_file = self.output_dir / "meeting_dashboard_full.html"
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)

        return str(output_file)

    def _generate_html_structure(self, data: Dict) -> str:
        """生成HTML结构"""
        # 将数据转换为JSON字符串
        data_json = json.dumps(data, cls=NumpyEncoder, ensure_ascii=False, indent=2)

        html = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>会议改善效果评估仪表盘</title>
    <script src="https://cdn.jsdelivr.net/npm/echarts@5.4.3/dist/echarts.min.js"></script>

    <style>
{self._generate_css()}
    </style>
</head>
<body>
    <!-- 顶部标题 -->
    <div class="header">
        <h1>🎯 会议改善效果评估仪表盘</h1>
        <div class="subtitle">Meeting Analysis Dashboard</div>
        <div class="metadata">
            <span>📅 数据周期: 2025-09-01 ~ 2025-11-16</span>
        </div>
    </div>

    <!-- 导航标签页 -->
    <div class="nav-tabs">
        <button class="nav-tab active" onclick="showTab('overview', event)">
            <span class="tab-icon">🏠</span> 概览
        </button>
        <button class="nav-tab" onclick="showTab('rawdata', event)">
            <span class="tab-icon">📊</span> 原始数据
        </button>
        <button class="nav-tab" onclick="showTab('analysis', event)">
            <span class="tab-icon">📈</span> 分析结果
        </button>
        <button class="nav-tab" onclick="showTab('personnel', event)">
            <span class="tab-icon">👥</span> 人员详情
        </button>
    </div>

    <div class="container">
        <!-- 模块1: 概览页面 -->
        <div id="tab-overview" class="tab-content active">
{self._generate_overview_module()}
        </div>

        <!-- 模块2: 原始数据页面 -->
        <div id="tab-rawdata" class="tab-content">
{self._generate_rawdata_module()}
        </div>

        <!-- 模块3: 分析结果页面 -->
        <div id="tab-analysis" class="tab-content">
{self._generate_analysis_module()}
        </div>

        <!-- 模块4: 人员详情页面 -->
        <div id="tab-personnel" class="tab-content">
{self._generate_personnel_module()}
        </div>
    </div>

    <!-- 个人详情弹窗 -->
    <div id="user-modal" class="modal">
        <div class="modal-content">
            <span class="close" onclick="closeUserModal()">&times;</span>
            <h2 id="modal-user-name"></h2>
            <div id="modal-user-content"></div>
        </div>
    </div>

    <script>
        // 数据注入
        const dashboardData = {data_json};

{self._generate_javascript()}
    </script>
</body>
</html>'''

        return html

    def _generate_css(self) -> str:
        """生成CSS样式"""
        return '''
/* 全局样式 */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC',
                 'Hiragino Sans GB', 'Microsoft YaHei', sans-serif;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
    padding: 20px;
    line-height: 1.6;
}

.container {
    max-width: 1400px;
    margin: 0 auto;
}

/* 顶部标题 */
.header {
    background: white;
    padding: 30px;
    border-radius: 15px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    margin-bottom: 20px;
    text-align: center;
}

.header h1 {
    font-size: 32px;
    color: #2d3748;
    margin-bottom: 10px;
}

.header .subtitle {
    color: #718096;
    font-size: 16px;
    margin-bottom: 15px;
}

.header .metadata {
    font-size: 14px;
    color: #4a5568;
}

.header .divider {
    margin: 0 10px;
    color: #cbd5e0;
}

/* 导航标签页 */
.nav-tabs {
    background: white;
    padding: 10px;
    border-radius: 10px;
    margin-bottom: 20px;
    display: flex;
    gap: 10px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    flex-wrap: wrap;
}

.nav-tab {
    flex: 1;
    min-width: 140px;
    padding: 15px 20px;
    background: #f7fafc;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-size: 16px;
    font-weight: 500;
    color: #4a5568;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
}

.nav-tab:hover {
    background: #edf2f7;
    transform: translateY(-2px);
}

.nav-tab.active {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

.tab-icon {
    font-size: 18px;
}

/* 标签页内容 */
.tab-content {
    display: none;
    animation: fadeIn 0.5s ease;
}

.tab-content.active {
    display: block;
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

/* KPI卡片网格 */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 20px;
    margin-bottom: 30px;
}

.kpi-card {
    background: white;
    padding: 25px;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    transition: all 0.3s ease;
    cursor: pointer;
    position: relative;
}

.kpi-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 25px rgba(0,0,0,0.15);
}

.kpi-card::before {
    content: '';
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    width: 5px;
    border-radius: 12px 0 0 12px;
}

.kpi-card.达标::before { background: #48bb78; }
.kpi-card.未达标::before { background: #f56565; }
.kpi-card.需关注::before { background: #ed8936; }
.kpi-card.接近达标::before { background: #ecc94b; }

.kpi-title {
    font-size: 14px;
    color: #718096;
    margin-bottom: 15px;
    font-weight: 500;
}

.kpi-value {
    font-size: 36px;
    font-weight: bold;
    color: #2d3748;
    margin-bottom: 10px;
}

.kpi-change {
    font-size: 18px;
    font-weight: 600;
}

.kpi-change.positive { color: #48bb78; }
.kpi-change.negative { color: #f56565; }

.kpi-status {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 12px;
    font-size: 12px;
    font-weight: 600;
    margin-top: 10px;
}

.kpi-status.达标 {
    background: #c6f6d5;
    color: #22543d;
}

.kpi-status.未达标 {
    background: #fed7d7;
    color: #742a2a;
}

.kpi-status.需关注 {
    background: #feebc8;
    color: #7c2d12;
}

.kpi-status.接近达标 {
    background: #fefcbf;
    color: #744210;
}

/* 图表容器 */
.chart-container {
    background: white;
    padding: 25px;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    margin-bottom: 20px;
}

.chart-title {
    font-size: 18px;
    font-weight: 600;
    color: #2d3748;
    margin-bottom: 20px;
    display: flex;
    align-items: center;
    gap: 10px;
}

.chart {
    width: 100%;
    height: 400px;
}

/* 快速洞察卡片 */
.insight-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 20px;
    margin-bottom: 30px;
}

.insight-card {
    background: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    cursor: pointer;
    transition: all 0.3s ease;
}

.insight-card:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 20px rgba(0,0,0,0.15);
}

.insight-title {
    font-size: 14px;
    color: #718096;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 8px;
}

.insight-value {
    font-size: 28px;
    font-weight: bold;
    color: #2d3748;
    margin-bottom: 8px;
}

.insight-desc {
    font-size: 13px;
    color: #4a5568;
    margin-bottom: 10px;
}

.insight-link {
    color: #667eea;
    font-size: 13px;
    text-decoration: none;
    font-weight: 500;
}

.insight-link:hover {
    text-decoration: underline;
}

/* 数据表格 */
.table-controls {
    background: white;
    padding: 20px;
    border-radius: 12px;
    margin-bottom: 20px;
    display: flex;
    gap: 15px;
    flex-wrap: wrap;
    align-items: center;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
}

.control-group {
    display: flex;
    align-items: center;
    gap: 10px;
}

.control-group label {
    font-size: 14px;
    color: #4a5568;
    font-weight: 500;
}

.control-group select,
.control-group input {
    padding: 8px 12px;
    border: 1px solid #cbd5e0;
    border-radius: 6px;
    font-size: 14px;
    min-width: 150px;
}

.btn {
    padding: 8px 16px;
    border: none;
    border-radius: 6px;
    cursor: pointer;
    font-size: 14px;
    font-weight: 500;
    transition: all 0.3s ease;
}

.btn-primary {
    background: #667eea;
    color: white;
}

.btn-primary:hover {
    background: #5568d3;
}

.btn-secondary {
    background: #e2e8f0;
    color: #4a5568;
}

.btn-secondary:hover {
    background: #cbd5e0;
}

/* 数据表格 */
.data-table-container {
    background: white;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    overflow: hidden;
}

.table-header {
    padding: 20px;
    background: #f7fafc;
    border-bottom: 2px solid #e2e8f0;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.table-header h3 {
    font-size: 18px;
    color: #2d3748;
}

.export-btns {
    display: flex;
    gap: 10px;
}

table {
    width: 100%;
    border-collapse: collapse;
}

thead {
    background: #f7fafc;
    position: sticky;
    top: 0;
    z-index: 10;
}

th {
    padding: 15px;
    text-align: left;
    font-size: 13px;
    font-weight: 600;
    color: #4a5568;
    border-bottom: 2px solid #e2e8f0;
    cursor: pointer;
    user-select: none;
}

th:hover {
    background: #edf2f7;
}

td {
    padding: 12px 15px;
    font-size: 14px;
    color: #2d3748;
    border-bottom: 1px solid #e2e8f0;
}

tr:hover {
    background: #f7fafc;
}

.btn-detail {
    padding: 4px 12px;
    background: #667eea;
    color: white;
    border: none;
    border-radius: 4px;
    font-size: 12px;
    cursor: pointer;
    transition: all 0.3s ease;
}

.btn-detail:hover {
    background: #5568d3;
}

/* Top10 用户卡片 */
.top10-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
    gap: 20px;
    margin-bottom: 30px;
}

.user-card {
    background: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    cursor: pointer;
    transition: all 0.3s ease;
    position: relative;
}

.user-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 8px 25px rgba(0,0,0,0.15);
}

.user-rank {
    position: absolute;
    top: 15px;
    right: 15px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
    font-weight: bold;
    font-size: 16px;
}

.user-name {
    font-size: 18px;
    font-weight: 600;
    color: #2d3748;
    margin-bottom: 15px;
}

.user-metrics {
    display: flex;
    justify-content: space-between;
    margin-bottom: 10px;
    font-size: 14px;
}

.metric-change {
    font-size: 20px;
    font-weight: bold;
    margin: 10px 0;
}

.user-status {
    display: inline-block;
    padding: 4px 12px;
    border-radius: 12px;
    font-size: 12px;
    font-weight: 600;
}

.user-status.改善 {
    background: #c6f6d5;
    color: #22543d;
}

.user-status.增加 {
    background: #fed7d7;
    color: #742a2a;
}

/* 弹窗 */
.modal {
    display: none;
    position: fixed;
    z-index: 1000;
    left: 0;
    top: 0;
    width: 100%;
    height: 100%;
    background-color: rgba(0,0,0,0.5);
    animation: fadeIn 0.3s ease;
}

.modal-content {
    background: white;
    margin: 50px auto;
    padding: 30px;
    width: 90%;
    max-width: 900px;
    border-radius: 15px;
    box-shadow: 0 10px 40px rgba(0,0,0,0.3);
    max-height: 80vh;
    overflow-y: auto;
    position: relative;
}

.close {
    position: absolute;
    right: 20px;
    top: 20px;
    font-size: 28px;
    font-weight: bold;
    color: #718096;
    cursor: pointer;
    transition: color 0.3s ease;
}

.close:hover {
    color: #2d3748;
}

/* 响应式设计 */
@media (max-width: 768px) {
    body {
        padding: 10px;
    }

    .header {
        padding: 20px;
    }

    .header h1 {
        font-size: 24px;
    }

    .nav-tabs {
        flex-direction: column;
    }

    .nav-tab {
        width: 100%;
    }

    .kpi-grid,
    .insight-grid,
    .top10-grid {
        grid-template-columns: 1fr;
    }

    .chart {
        height: 300px;
    }

    .table-controls {
        flex-direction: column;
        align-items: stretch;
    }

    .control-group {
        flex-direction: column;
        align-items: stretch;
    }

    .control-group select,
    .control-group input {
        width: 100%;
    }

    table {
        font-size: 12px;
    }

    th, td {
        padding: 8px;
    }
}

/* 状态徽章 */
.badge {
    display: inline-block;
    padding: 2px 8px;
    border-radius: 10px;
    font-size: 11px;
    font-weight: 600;
}

.badge-success {
    background: #c6f6d5;
    color: #22543d;
}

.badge-warning {
    background: #feebc8;
    color: #7c2d12;
}

.badge-danger {
    background: #fed7d7;
    color: #742a2a;
}

.badge-info {
    background: #bee3f8;
    color: #2c5282;
}

/* 分页 */
.pagination {
    display: flex;
    justify-content: center;
    align-items: center;
    gap: 10px;
    padding: 20px;
    background: white;
    border-top: 1px solid #e2e8f0;
}

.pagination button {
    padding: 6px 12px;
    border: 1px solid #cbd5e0;
    background: white;
    border-radius: 4px;
    cursor: pointer;
    font-size: 14px;
    transition: all 0.3s ease;
}

.pagination button:hover:not(:disabled) {
    background: #f7fafc;
    border-color: #667eea;
}

.pagination button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

.pagination .page-info {
    font-size: 14px;
    color: #4a5568;
}
'''

    def _generate_overview_module(self) -> str:
        """生成概览模块HTML"""
        return '''
            <div class="module-title">
                <h2>📊 核心指标概览</h2>
            </div>

            <!-- KPI卡片区 -->
            <div class="kpi-grid" id="kpi-cards"></div>

            <!-- 趋势图区 -->
            <div class="chart-container">
                <div class="chart-title">
                    <span>📈</span>
                    <span>趋势分析</span>
                </div>
                <div id="overview-trend-chart" class="chart"></div>
            </div>

            <!-- 会议类型分布（与分析结果页面保持一致） -->
            <div class="chart-container">
                <div class="chart-title">
                    <span>📊</span>
                    <span>会议类型分布变化分析</span>
                </div>

                <!-- 饼图对比区域 -->
                <div style="background: #f7fafc; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
                    <h4 style="margin: 0 0 15px 0; color: #2d3748;">基线期 vs 当前期对比</h4>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 30px;">
                        <div>
                            <div id="overview-type-baseline" class="chart" style="height: 350px;"></div>
                        </div>
                        <div>
                            <div id="overview-type-current" class="chart" style="height: 350px;"></div>
                        </div>
                    </div>
                </div>

                <!-- 详细数据表格 -->
                <div>
                    <h4 style="margin: 0 0 15px 0; color: #2d3748;">📊 数据详情表</h4>
                    <table style="width: 100%; border-collapse: collapse;">
                        <thead>
                            <tr style="background: #edf2f7;">
                                <th style="padding: 12px; text-align: left; border: 1px solid #e2e8f0;">会议类型</th>
                                <th style="padding: 12px; text-align: right; border: 1px solid #e2e8f0;">基线期数量</th>
                                <th style="padding: 12px; text-align: right; border: 1px solid #e2e8f0;">当前期数量</th>
                                <th style="padding: 12px; text-align: right; border: 1px solid #e2e8f0;">数量变化</th>
                                <th style="padding: 12px; text-align: right; border: 1px solid #e2e8f0;">基线占比</th>
                                <th style="padding: 12px; text-align: right; border: 1px solid #e2e8f0;">当前占比</th>
                                <th style="padding: 12px; text-align: center; border: 1px solid #e2e8f0;">占比变化</th>
                                <th style="padding: 12px; text-align: center; border: 1px solid #e2e8f0;">趋势</th>
                            </tr>
                        </thead>
                        <tbody id="overview-type-table" style="font-size: 14px;"></tbody>
                    </table>
                </div>

                <!-- 关键洞察 -->
                <div id="overview-type-insights" style="margin-top: 20px; padding: 15px; background: #fffaf0; border-left: 4px solid #ed8936; border-radius: 4px;">
                    <div style="font-weight: 600; margin-bottom: 8px; color: #2d3748;">💡 关键洞察</div>
                    <div id="overview-type-insights-content" style="color: #4a5568; font-size: 14px; line-height: 1.6;"></div>
                </div>
            </div>

            <!-- 快速洞察卡片区 -->
            <div class="insight-grid" id="insight-cards"></div>
'''

    def _generate_rawdata_module(self) -> str:
        """生成原始数据模块HTML"""
        return '''
            <!-- 数据筛选器 -->
            <div class="table-controls">
                <div class="control-group">
                    <label>时间段:</label>
                    <select id="period-filter">
                        <option value="all">全部</option>
                    </select>
                </div>
                <div class="control-group">
                    <label>人员搜索:</label>
                    <input type="text" id="user-search" placeholder="输入姓名搜索">
                </div>
                <div class="control-group">
                    <button class="btn btn-primary" onclick="applyFilters()">应用筛选</button>
                    <button class="btn btn-secondary" onclick="resetFilters()">重置</button>
                </div>
                <span id="filter-result" style="margin-left: auto; color: #4a5568;"></span>
            </div>

            <!-- 原始数据表格 -->
            <div class="data-table-container">
                <div class="table-header">
                    <h3>原始会议数据详情</h3>
                    <div class="export-btns">
                        <button class="btn btn-secondary" onclick="exportToCSV()">导出 CSV</button>
                        <button class="btn btn-secondary" onclick="exportToJSON()">导出 JSON</button>
                    </div>
                </div>
                <div style="overflow-x: auto;">
                    <table id="raw-data-table">
                        <thead>
                            <tr>
                                <th onclick="sortTable('user_name')">姓名 ↕</th>
                                <th onclick="sortTable('period_name')">周期 ↕</th>
                                <th onclick="sortTable('日人均线上会议数')">日均会议数 ↕</th>
                                <th onclick="sortTable('日人均线上会议时长(分钟)')">日均时长(分) ↕</th>
                                <th onclick="sortTable('即时会议数')">即时会议 ↕</th>
                                <th onclick="sortTable('日程会议数')">日程会议 ↕</th>
                                <th onclick="sortTable('1v1通话数')">1v1通话 ↕</th>
                                <th>操作</th>
                            </tr>
                        </thead>
                        <tbody id="raw-data-tbody"></tbody>
                    </table>
                </div>
                <div class="pagination" id="raw-data-pagination"></div>
            </div>
'''

    def _generate_analysis_module(self) -> str:
        """生成分析结果模块HTML"""
        return '''
            <div class="module-title">
                <h2>📈 会议改善效果评估分析</h2>
            </div>

            <!-- 分析方法说明 -->
            <div class="chart-container" style="margin-bottom: 30px;">
                <div class="chart-title">
                    <span>📋</span>
                    <span>评估方法说明</span>
                </div>
                <div style="padding: 20px; line-height: 1.8; color: #4a5568;">
                    <h3 style="color: #2d3748; margin-top: 0;">📊 评估框架</h3>
                    <p><strong>核心目标：</strong>验证"固定会议窗口"措施是否有效降低会议负担，识别改善趋势，为持续优化提供依据。</p>

                    <h3 style="color: #2d3748; margin-top: 20px;">📅 数据基础</h3>
                    <ul style="margin: 10px 0;">
                        <li><strong>基线期：</strong>9月 + 10月会议详情（措施实施前）</li>
                        <li><strong>当前期：</strong>最近4周周度数据（10.20-10.26、10.27-11.2、11.03-11.09、11.10-11.16）</li>
                        <li><strong>数据维度：</strong>日人均线上会议数、日人均会议时长、会议类型（即时/日程/1v1）</li>
                    </ul>

                    <h3 style="color: #2d3748; margin-top: 20px;">🎯 核心评估指标（Primary KPIs）</h3>
                    <div style="margin-left: 20px;">
                        <p><strong>1. 日人均会议数减少率</strong></p>
                        <ul style="margin: 5px 0 15px 20px;">
                            <li>计算公式：(基线期均值 - 当前期均值) / 基线期均值 × 100%</li>
                            <li>评估标准：减少 ≥10% 为达标，≥20% 为优秀</li>
                            <li>意义：综合评估所有会议类型的整体负担变化</li>
                        </ul>

                        <p><strong>2. 日人均会议时长减少率</strong></p>
                        <ul style="margin: 5px 0 15px 20px;">
                            <li>计算公式：(基线期均值 - 当前期均值) / 基线期均值 × 100%</li>
                            <li>评估标准：减少 ≥10% 为达标，减少 ≥30分钟/天为优秀</li>
                            <li>意义：评估会议总时长负担的变化</li>
                        </ul>

                        <p><strong>3. 即时会议占比下降</strong></p>
                        <ul style="margin: 5px 0 15px 20px;">
                            <li>计算公式：基线期占比 - 当前期占比（百分点）</li>
                            <li>评估标准：下降 ≥10个百分点为达标</li>
                            <li>意义：反映会议计划性提升程度，即时会议减少说明会议更有序</li>
                        </ul>
                    </div>

                    <h3 style="color: #2d3748; margin-top: 20px;">📈 分析维度</h3>
                    <ul style="margin: 10px 0;">
                        <li><strong>周期趋势分析：</strong>观察6个周期的会议数变化趋势</li>
                        <li><strong>会议类型分布：</strong>对比基线期和当前期各类型会议的数量和占比</li>
                        <li><strong>人员分层统计：</strong>识别高频（≥5次/天）、中频（2-5次/天）、低频（<2次/天）用户</li>
                        <li><strong>异常检测：</strong>基于Z-score（阈值1.5）识别异常数据点</li>
                    </ul>
                </div>
            </div>

            <div class="module-title">
                <h2>📊 主要KPI详细分析</h2>
            </div>

            <!-- KPI详细展开 -->
            <div id="kpi-details"></div>

            <!-- 统计分析结果 -->
            <div class="chart-container">
                <div class="chart-title">
                    <span>📊</span>
                    <span>描述性统计对比</span>
                </div>
                <div style="display: grid; grid-template-columns: 2fr 1fr; gap: 20px;">
                    <div id="stats-comparison-chart" class="chart" style="min-height: 400px;"></div>
                    <div>
                        <h4 style="margin-top: 0; color: #2d3748; font-size: 16px;">📈 数值详情</h4>
                        <table style="width: 100%; font-size: 14px;">
                            <thead>
                                <tr style="background: #f7fafc;">
                                    <th style="padding: 10px; text-align: left;">指标</th>
                                    <th style="padding: 10px; text-align: right;">基线期</th>
                                    <th style="padding: 10px; text-align: right;">当前期</th>
                                    <th style="padding: 10px; text-align: right;">变化</th>
                                </tr>
                            </thead>
                            <tbody id="stats-details-table"></tbody>
                        </table>
                    </div>
                </div>
            </div>

            <!-- 会议类型详细分析 -->
            <div class="chart-container">
                <div class="chart-title">
                    <span>📊</span>
                    <span>会议类型分布变化分析</span>
                </div>

                <!-- 饼图对比区域 -->
                <div style="background: #f7fafc; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
                    <h4 style="margin: 0 0 15px 0; color: #2d3748;">基线期 vs 当前期对比</h4>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 30px;">
                        <div>
                            <div id="meeting-type-baseline" class="chart" style="height: 350px;"></div>
                        </div>
                        <div>
                            <div id="meeting-type-current" class="chart" style="height: 350px;"></div>
                        </div>
                    </div>
                </div>

                <!-- 详细数据表格 -->
                <div>
                    <h4 style="margin: 0 0 15px 0; color: #2d3748;">📊 数据详情表</h4>
                    <table style="width: 100%; border-collapse: collapse;">
                        <thead>
                            <tr style="background: #edf2f7;">
                                <th style="padding: 12px; text-align: left; border: 1px solid #e2e8f0;">会议类型</th>
                                <th style="padding: 12px; text-align: right; border: 1px solid #e2e8f0;">基线期数量</th>
                                <th style="padding: 12px; text-align: right; border: 1px solid #e2e8f0;">当前期数量</th>
                                <th style="padding: 12px; text-align: right; border: 1px solid #e2e8f0;">数量变化</th>
                                <th style="padding: 12px; text-align: right; border: 1px solid #e2e8f0;">基线占比</th>
                                <th style="padding: 12px; text-align: right; border: 1px solid #e2e8f0;">当前占比</th>
                                <th style="padding: 12px; text-align: center; border: 1px solid #e2e8f0;">占比变化</th>
                                <th style="padding: 12px; text-align: center; border: 1px solid #e2e8f0;">趋势</th>
                            </tr>
                        </thead>
                        <tbody id="meeting-type-table" style="font-size: 14px;"></tbody>
                    </table>
                </div>

                <!-- 关键洞察 -->
                <div id="meeting-type-insights" style="margin-top: 20px; padding: 15px; background: #fffaf0; border-left: 4px solid #ed8936; border-radius: 4px;">
                    <div style="font-weight: 600; margin-bottom: 8px; color: #2d3748;">💡 关键洞察</div>
                    <div id="meeting-type-insights-content" style="color: #4a5568; font-size: 14px; line-height: 1.6;"></div>
                </div>
            </div>
'''

    def _generate_personnel_module(self) -> str:
        """生成人员详情模块HTML"""
        return '''
            <div class="module-title">
                <h2>🏆 Top 10 重度会议用户</h2>
            </div>

            <!-- Top10用户卡片 -->
            <div class="top10-grid" id="top10-users"></div>

            <!-- 人员分层统计 -->
            <div class="chart-container">
                <div class="chart-title">
                    <span>📊</span>
                    <span>人员分层分析</span>
                </div>
                <div id="user-tier-chart" class="chart"></div>
            </div>

            <!-- 异常用户列表 -->
            <div class="data-table-container" style="margin-top: 20px;">
                <div class="table-header">
                    <h3>⚠️ 异常检测结果</h3>
                </div>
                <div style="overflow-x: auto;">
                    <table>
                        <thead>
                            <tr>
                                <th>序号</th>
                                <th>姓名</th>
                                <th>异常指标</th>
                                <th>当前值</th>
                                <th>整体均值</th>
                                <th>Z-score</th>
                                <th>类型</th>
                            </tr>
                        </thead>
                        <tbody id="anomaly-tbody"></tbody>
                    </table>
                </div>
            </div>
'''

    def _generate_javascript(self) -> str:
        """生成JavaScript代码"""
        return '''
        // ==================== 全局变量 ====================
        let currentPage = 1;
        let pageSize = 50;
        let filteredData = [];
        let sortColumn = '';
        let sortOrder = 'asc';

        // ==================== 初始化 ====================
        document.addEventListener('DOMContentLoaded', function() {
            console.log('Dashboard loaded', dashboardData);

            // 初始化各个模块
            initOverview();
            initRawData();
            initAnalysis();
            initPersonnel();

            // 设置默认激活的标签页
            showTab('overview');
        });

        // ==================== 标签页切换 ====================
        function showTab(tabName, event) {
            // 隐藏所有标签页
            const tabs = document.querySelectorAll('.tab-content');
            tabs.forEach(tab => tab.classList.remove('active'));

            // 移除所有按钮的激活状态
            const buttons = document.querySelectorAll('.nav-tab');
            buttons.forEach(btn => btn.classList.remove('active'));

            // 显示选中的标签页
            document.getElementById('tab-' + tabName).classList.add('active');

            // 激活对应的按钮
            if (event && event.target) {
                event.target.classList.add('active');
            } else {
                // 如果没有event,根据tabName找到对应按钮
                const targetBtn = Array.from(buttons).find(btn =>
                    btn.getAttribute('onclick').includes(tabName)
                );
                if (targetBtn) {
                    targetBtn.classList.add('active');
                }
            }

            // 调整图表大小
            setTimeout(() => {
                const charts = document.querySelectorAll('.chart');
                charts.forEach(chart => {
                    const instance = echarts.getInstanceByDom(chart);
                    if (instance) {
                        instance.resize();
                    }
                });
            }, 100);
        }

        // ==================== 模块1: 概览页面 ====================
        function initOverview() {
            renderKPICards();
            renderOverviewTrendChart();
            renderOverviewTypeChart();
            renderInsightCards();
        }

        function renderKPICards() {
            const container = document.getElementById('kpi-cards');
            if (!container || !dashboardData.kpis) return;

            const kpis = dashboardData.kpis['主要KPI'] || {};
            let html = '';

            Object.entries(kpis).forEach(([name, data]) => {
                const status = data['达标'] ? '达标' : '未达标';

                // 根据KPI名称获取正确的变化率字段
                let changeRate = 0;
                if (name === '日人均会议数减少率') {
                    changeRate = data['减少率(%)'] || 0;
                } else if (name === '日人均会议时长减少率') {
                    changeRate = data['减少率(%)'] || 0;
                } else if (name === '即时会议占比下降') {
                    changeRate = data['下降幅度(百分点)'] || 0;
                }

                const changeClass = changeRate > 0 ? 'positive' : 'negative';
                const changeIcon = changeRate > 0 ? '📉' : '📈';

                html += `
                <div class="kpi-card ${status === '达标' ? 'status-good' : 'status-bad'}" onclick="showTab('analysis', event)">
                    <div class="kpi-title">${name}</div>
                    <div class="kpi-value">${Math.abs(changeRate).toFixed(2)}%</div>
                    <div class="kpi-change ${changeClass}">
                        ${changeIcon} ${changeRate > 0 ? '改善' : '恶化'} ${Math.abs(changeRate).toFixed(2)}%
                    </div>
                    <div class="kpi-status ${status === '达标' ? 'status-good' : 'status-bad'}">${status}</div>
                </div>
                `;
            });

            container.innerHTML = html;
        }

        function renderOverviewTrendChart() {
            const chart = echarts.init(document.getElementById('overview-trend-chart'));

            // 准备数据
            const periods = dashboardData.period_comparison || [];
            const xData = periods.map(p => p['周期'] || p.period_name);
            const yData = periods.map(p => p['日人均会议数'] || p['日人均线上会议数'] || 0);

            const option = {
                tooltip: { trigger: 'axis' },
                xAxis: {
                    type: 'category',
                    data: xData,
                    axisLabel: { rotate: 45 }
                },
                yAxis: {
                    type: 'value',
                    name: '日人均会议数'
                },
                series: [{
                    name: '会议数',
                    data: yData,
                    type: 'line',
                    smooth: true,
                    itemStyle: { color: '#667eea' },
                    areaStyle: {
                        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
                            { offset: 0, color: 'rgba(102, 126, 234, 0.3)' },
                            { offset: 1, color: 'rgba(102, 126, 234, 0)' }
                        ])
                    }
                }]
            };

            chart.setOption(option);
        }

        function renderOverviewTypeChart() {
            // 使用与分析结果页面相同的完整会议类型分析逻辑
            const baseline = dashboardData.baseline_stats || {};
            const current = dashboardData.current_stats || {};

            // 提取会议类型数据
            const baselineInstant = parseFloat(baseline['即时会议数']) || 0;
            const baselineScheduled = parseFloat(baseline['日程会议数']) || 0;
            const baseline1v1 = parseFloat(baseline['1v1通话数']) || 0;

            const currentInstant = parseFloat(current['即时会议数']) || 0;
            const currentScheduled = parseFloat(current['日程会议数']) || 0;
            const current1v1 = parseFloat(current['1v1通话数']) || 0;

            // 基线期饼图
            const baselineChart = echarts.init(document.getElementById('overview-type-baseline'));
            const baselineTotal = baselineInstant + baselineScheduled + baseline1v1;

            baselineChart.setOption({
                title: {
                    text: '基线期会议类型分布',
                    left: 'center',
                    top: 10,
                    textStyle: { fontSize: 16, fontWeight: 'bold' }
                },
                tooltip: {
                    trigger: 'item',
                    formatter: function(params) {
                        return `${params.name}<br/>数量: ${params.value.toFixed(2)}<br/>占比: ${params.percent.toFixed(1)}%`;
                    }
                },
                legend: {
                    orient: 'horizontal',
                    bottom: 10,
                    left: 'center'
                },
                series: [{
                    type: 'pie',
                    radius: ['35%', '65%'],
                    center: ['50%', '50%'],
                    label: {
                        show: true,
                        position: 'outside',
                        formatter: function(params) {
                            return `${params.name}\n${params.value.toFixed(1)}\n${params.percent.toFixed(1)}%`;
                        },
                        fontSize: 12
                    },
                    labelLine: { show: true, length: 15, length2: 10 },
                    itemStyle: {
                        borderRadius: 8,
                        shadowBlur: 10,
                        shadowColor: 'rgba(0, 0, 0, 0.2)'
                    },
                    data: [
                        { value: baselineInstant, name: '即时会议', itemStyle: { color: '#f56565' } },
                        { value: baselineScheduled, name: '日程会议', itemStyle: { color: '#48bb78' } },
                        { value: baseline1v1, name: '1v1通话', itemStyle: { color: '#4299e1' } }
                    ]
                }]
            });

            // 当前期饼图
            const currentChart = echarts.init(document.getElementById('overview-type-current'));
            const currentTotal = currentInstant + currentScheduled + current1v1;

            currentChart.setOption({
                title: {
                    text: '当前期会议类型分布',
                    left: 'center',
                    top: 10,
                    textStyle: { fontSize: 16, fontWeight: 'bold' }
                },
                tooltip: {
                    trigger: 'item',
                    formatter: function(params) {
                        return `${params.name}<br/>数量: ${params.value.toFixed(2)}<br/>占比: ${params.percent.toFixed(1)}%`;
                    }
                },
                legend: {
                    orient: 'horizontal',
                    bottom: 10,
                    left: 'center'
                },
                series: [{
                    type: 'pie',
                    radius: ['35%', '65%'],
                    center: ['50%', '50%'],
                    label: {
                        show: true,
                        position: 'outside',
                        formatter: function(params) {
                            return `${params.name}\n${params.value.toFixed(1)}\n${params.percent.toFixed(1)}%`;
                        },
                        fontSize: 12
                    },
                    labelLine: { show: true, length: 15, length2: 10 },
                    itemStyle: {
                        borderRadius: 8,
                        shadowBlur: 10,
                        shadowColor: 'rgba(0, 0, 0, 0.2)'
                    },
                    data: [
                        { value: currentInstant, name: '即时会议', itemStyle: { color: '#f56565' } },
                        { value: currentScheduled, name: '日程会议', itemStyle: { color: '#48bb78' } },
                        { value: current1v1, name: '1v1通话', itemStyle: { color: '#4299e1' } }
                    ]
                }]
            });

            // 填充数据表格
            const tableBody = document.getElementById('overview-type-table');
            const types = [
                { name: '即时会议', baseline: baselineInstant, current: currentInstant, icon: '⚡', color: '#f56565' },
                { name: '日程会议', baseline: baselineScheduled, current: currentScheduled, icon: '📅', color: '#48bb78' },
                { name: '1v1通话', baseline: baseline1v1, current: current1v1, icon: '📞', color: '#4299e1' }
            ];

            let html = '';
            const insights = [];

            types.forEach(type => {
                const baselineCount = type.baseline;
                const currentCount = type.current;
                const countChange = currentCount - baselineCount;
                const countChangePercent = baselineCount > 0 ? ((countChange / baselineCount) * 100) : 0;

                const baselinePercent = baselineTotal > 0 ? (baselineCount / baselineTotal * 100) : 0;
                const currentPercent = currentTotal > 0 ? (currentCount / currentTotal * 100) : 0;
                const percentChange = currentPercent - baselinePercent;

                const trendValue = percentChange;
                const trendIcon = trendValue > 5 ? '⬆️' : trendValue < -5 ? '⬇️' : '➡️';
                const trendColor = trendValue > 5 ? '#e53e3e' : trendValue < -5 ? '#38a169' : '#718096';
                const trendText = trendValue > 5 ? '增加' : trendValue < -5 ? '下降' : '稳定';

                // 生成洞察
                if (type.name === '即时会议' && trendValue < -5) {
                    insights.push(`✅ 即时会议占比下降 ${Math.abs(trendValue).toFixed(1)} 个百分点，说明会议计划性显著提升`);
                } else if (type.name === '即时会议' && trendValue > 5) {
                    insights.push(`⚠️ 即时会议占比上升 ${trendValue.toFixed(1)} 个百分点，建议加强会议规划`);
                }

                if (type.name === '日程会议' && trendValue > 5) {
                    insights.push(`✅ 日程会议占比提升 ${trendValue.toFixed(1)} 个百分点，会议规范性改善明显`);
                }

                if (type.name === '1v1通话' && Math.abs(trendValue) > 8) {
                    insights.push(`📞 1v1通话占比变化 ${trendValue.toFixed(1)} 个百分点，${trendValue > 0 ? '沟通更加聚焦' : '团队协作模式转变'}`);
                }

                const bgColor = type.name === '即时会议' ? '#fff5f5' : type.name === '日程会议' ? '#f0fff4' : '#ebf8ff';

                html += `
                <tr style="background: ${bgColor};">
                    <td style="padding: 10px; border: 1px solid #e2e8f0;"><strong style="color: ${type.color};">${type.icon} ${type.name}</strong></td>
                    <td style="padding: 10px; border: 1px solid #e2e8f0; text-align: right;">${baselineCount.toFixed(2)}</td>
                    <td style="padding: 10px; border: 1px solid #e2e8f0; text-align: right;">${currentCount.toFixed(2)}</td>
                    <td style="padding: 10px; border: 1px solid #e2e8f0; text-align: right;">
                        ${countChange.toFixed(2)}<br/>
                        <span style="font-size: 12px; color: ${countChange > 0 ? '#e53e3e' : '#38a169'};">(${countChangePercent > 0 ? '+' : ''}${countChangePercent.toFixed(1)}%)</span>
                    </td>
                    <td style="padding: 10px; border: 1px solid #e2e8f0; text-align: right;">${baselinePercent.toFixed(1)}%</td>
                    <td style="padding: 10px; border: 1px solid #e2e8f0; text-align: right;">${currentPercent.toFixed(1)}%</td>
                    <td style="padding: 10px; border: 1px solid #e2e8f0; text-align: center;">
                        <span style="color: ${trendColor}; font-weight: 600;">${percentChange > 0 ? '+' : ''}${percentChange.toFixed(1)}pp</span>
                    </td>
                    <td style="padding: 10px; border: 1px solid #e2e8f0; text-align: center;">
                        <span style="color: ${trendColor}; font-weight: 600;">${trendIcon} ${trendText}</span>
                    </td>
                </tr>
                `;
            });

            // 添加总计行
            html += `
            <tr style="background: #edf2f7; font-weight: bold;">
                <td style="padding: 10px; border: 1px solid #e2e8f0;">📊 总计</td>
                <td style="padding: 10px; border: 1px solid #e2e8f0; text-align: right;">${baselineTotal.toFixed(2)}</td>
                <td style="padding: 10px; border: 1px solid #e2e8f0; text-align: right;">${currentTotal.toFixed(2)}</td>
                <td style="padding: 10px; border: 1px solid #e2e8f0; text-align: right;">${(currentTotal - baselineTotal).toFixed(2)}</td>
                <td style="padding: 10px; border: 1px solid #e2e8f0; text-align: right;">100.0%</td>
                <td style="padding: 10px; border: 1px solid #e2e8f0; text-align: right;">100.0%</td>
                <td style="padding: 10px; border: 1px solid #e2e8f0; text-align: center;">-</td>
                <td style="padding: 10px; border: 1px solid #e2e8f0; text-align: center;">-</td>
            </tr>
            `;

            tableBody.innerHTML = html;

            // 填充关键洞察
            const insightsContent = document.getElementById('overview-type-insights-content');
            if (insights.length > 0) {
                insightsContent.innerHTML = insights.map(i => `<div>• ${i}</div>`).join('');
            } else {
                insightsContent.innerHTML = '<div>• 各类型会议占比变化不显著，保持相对稳定</div>';
            }
        }

        function renderInsightCards() {
            const container = document.getElementById('insight-cards');
            if (!container) return;

            const top10Count = dashboardData.top10_users?.length || 0;
            const anomalyCount = dashboardData.anomalies?.length || 0;
            const userTiers = dashboardData.user_tiers || {};
            const highFreq = userTiers.high?.length || 0;

            const cv = dashboardData.current_stats?.cv || 0;

            container.innerHTML = `
                <div class="insight-card" onclick="showTab('personnel')">
                    <div class="insight-title">🏆 Top10用户</div>
                    <div class="insight-value">${top10Count}</div>
                    <div class="insight-desc">重度会议用户</div>
                    <a href="#" class="insight-link">查看详情 →</a>
                </div>

                <div class="insight-card" onclick="showTab('personnel')">
                    <div class="insight-title">⚠️ 异常检测</div>
                    <div class="insight-value">${anomalyCount}</div>
                    <div class="insight-desc">发现异常数据点</div>
                    <a href="#" class="insight-link">查看列表 →</a>
                </div>

                <div class="insight-card">
                    <div class="insight-title">📊 团队均衡度</div>
                    <div class="insight-value">${cv.toFixed(2)}</div>
                    <div class="insight-desc">变异系数 (CV)</div>
                    <span class="badge badge-success">良好</span>
                </div>

                <div class="insight-card" onclick="showTab('personnel')">
                    <div class="insight-title">👥 高频用户</div>
                    <div class="insight-value">${highFreq}</div>
                    <div class="insight-desc">≥5次/天的用户</div>
                    <a href="#" class="insight-link">查看分布 →</a>
                </div>
            `;
        }

        // ==================== 模块2: 原始数据 ====================
        function initRawData() {
            // 填充周期筛选器
            const periodFilter = document.getElementById('period-filter');
            if (periodFilter) {
                const periods = [...new Set(dashboardData.raw_data.map(r => r.period_name))];
                periods.forEach(period => {
                    const option = document.createElement('option');
                    option.value = period;
                    option.textContent = period;
                    periodFilter.appendChild(option);
                });
            }

            // 初始化数据
            filteredData = dashboardData.raw_data || [];
            renderRawDataTable();
        }

        function renderRawDataTable() {
            const tbody = document.getElementById('raw-data-tbody');
            if (!tbody) return;

            // 分页
            const start = (currentPage - 1) * pageSize;
            const end = start + pageSize;
            const pageData = filteredData.slice(start, end);

            let html = '';
            pageData.forEach(row => {
                html += `
                <tr>
                    <td>${row.user_name || ''}</td>
                    <td>${row.period_name || ''}</td>
                    <td>${(row['日人均线上会议数'] || 0).toFixed(2)}</td>
                    <td>${(row['日人均线上会议时长(分钟)'] || 0).toFixed(0)}</td>
                    <td>${row['即时会议数'] || 0}</td>
                    <td>${row['日程会议数'] || 0}</td>
                    <td>${row['1v1通话数'] || 0}</td>
                    <td><button class="btn-detail" onclick="showUserDetail('${row.user_name}')">详情</button></td>
                </tr>
                `;
            });

            tbody.innerHTML = html;
            renderPagination();
        }

        function renderPagination() {
            const container = document.getElementById('raw-data-pagination');
            if (!container) return;

            const totalPages = Math.ceil(filteredData.length / pageSize);

            container.innerHTML = `
                <button onclick="changePage(-1)" ${currentPage === 1 ? 'disabled' : ''}>上一页</button>
                <span class="page-info">第 ${currentPage} / ${totalPages} 页 (共 ${filteredData.length} 条)</span>
                <button onclick="changePage(1)" ${currentPage === totalPages ? 'disabled' : ''}>下一页</button>
            `;
        }

        function changePage(delta) {
            currentPage += delta;
            renderRawDataTable();
        }

        function applyFilters() {
            const period = document.getElementById('period-filter')?.value;
            const search = document.getElementById('user-search')?.value.toLowerCase() || '';

            filteredData = dashboardData.raw_data.filter(row => {
                const matchPeriod = !period || period === 'all' || row.period_name === period;
                const matchSearch = !search || row.user_name.toLowerCase().includes(search);
                return matchPeriod && matchSearch;
            });

            currentPage = 1;
            renderRawDataTable();

            const result = document.getElementById('filter-result');
            if (result) {
                result.textContent = `找到 ${filteredData.length} 条记录`;
            }
        }

        function resetFilters() {
            document.getElementById('period-filter').value = 'all';
            document.getElementById('user-search').value = '';
            filteredData = dashboardData.raw_data;
            currentPage = 1;
            renderRawDataTable();

            const result = document.getElementById('filter-result');
            if (result) {
                result.textContent = '';
            }
        }

        function sortTable(column) {
            if (sortColumn === column) {
                sortOrder = sortOrder === 'asc' ? 'desc' : 'asc';
            } else {
                sortColumn = column;
                sortOrder = 'asc';
            }

            filteredData.sort((a, b) => {
                let aVal = a[column];
                let bVal = b[column];

                if (typeof aVal === 'string') {
                    return sortOrder === 'asc' ?
                        aVal.localeCompare(bVal) : bVal.localeCompare(aVal);
                } else {
                    return sortOrder === 'asc' ? aVal - bVal : bVal - aVal;
                }
            });

            renderRawDataTable();
        }

        // ==================== 模块3: 分析结果 ====================
        function initAnalysis() {
            renderKPIDetails();
            renderStatsComparison();
            renderMeetingTypeAnalysis();
        }

        function renderKPIDetails() {
            const container = document.getElementById('kpi-details');
            if (!container || !dashboardData.kpis) return;

            const kpis = dashboardData.kpis['主要KPI'] || {};
            let html = '';

            Object.entries(kpis).forEach(([name, data]) => {
                const status = data['达标'] ? '达标' : '未达标';
                const statusBadge = data['达标'] ? 'badge-success' : 'badge-danger';

                // 根据KPI名称提取正确的字段
                let baselineValue = 0;
                let currentValue = 0;
                let changeRate = 0;
                let target = '';
                let unit = '';

                if (name === '日人均会议数减少率') {
                    baselineValue = data['基线期均值'] || 0;
                    currentValue = data['当前期均值'] || 0;
                    changeRate = data['减少率(%)'] || 0;
                    target = data['目标'] || '≥10%';
                    unit = '次';
                } else if (name === '日人均会议时长减少率') {
                    baselineValue = data['基线期均值(分钟)'] || 0;
                    currentValue = data['当前期均值(分钟)'] || 0;
                    changeRate = data['减少率(%)'] || 0;
                    target = data['目标'] || '≥10%';
                    unit = '分钟';
                } else if (name === '即时会议占比下降') {
                    baselineValue = data['基线期占比(%)'] || 0;
                    currentValue = data['当前期占比(%)'] || 0;
                    changeRate = data['下降幅度(百分点)'] || 0;
                    target = data['目标'] || '≥10个百分点';
                    unit = '%';
                }

                const changeColor = changeRate > 0 ? '#48bb78' : '#f56565';
                const changeText = changeRate > 0 ? '改善' : '恶化';

                html += `
                <div class="chart-container" style="margin-bottom: 20px;">
                    <div class="chart-title">
                        <span>${name}</span>
                        <span class="badge ${statusBadge}">${status}</span>
                    </div>
                    <div style="padding: 20px;">
                        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 15px; margin-bottom: 15px;">
                            <div style="background: #edf2f7; padding: 15px; border-radius: 8px;">
                                <div style="color: #718096; font-size: 14px; margin-bottom: 5px;">📊 基线期均值</div>
                                <div style="font-size: 24px; font-weight: bold; color: #2d3748;">${baselineValue.toFixed(2)} ${unit}</div>
                            </div>
                            <div style="background: #e6fffa; padding: 15px; border-radius: 8px;">
                                <div style="color: #718096; font-size: 14px; margin-bottom: 5px;">📈 当前期均值</div>
                                <div style="font-size: 24px; font-weight: bold; color: #2d3748;">${currentValue.toFixed(2)} ${unit}</div>
                            </div>
                            <div style="background: ${changeRate > 0 ? '#f0fff4' : '#fff5f5'}; padding: 15px; border-radius: 8px;">
                                <div style="color: #718096; font-size: 14px; margin-bottom: 5px;">${changeRate > 0 ? '✅' : '⚠️'} ${name.includes('占比') ? '下降幅度' : '减少率'}</div>
                                <div style="font-size: 24px; font-weight: bold; color: ${changeColor};">
                                    ${changeText} ${Math.abs(changeRate).toFixed(2)}${name.includes('占比') ? '个百分点' : '%'}
                                </div>
                            </div>
                            <div style="background: #fef5e7; padding: 15px; border-radius: 8px;">
                                <div style="color: #718096; font-size: 14px; margin-bottom: 5px;">🎯 目标</div>
                                <div style="font-size: 18px; font-weight: bold; color: #2d3748;">${target}</div>
                            </div>
                        </div>
                        <div style="background: #f7fafc; padding: 15px; border-radius: 8px; border-left: 4px solid ${data['达标'] ? '#48bb78' : '#f56565'};">
                            <div style="font-weight: 600; margin-bottom: 8px; color: #2d3748;">
                                💡 评估说明
                            </div>
                            <div style="color: #4a5568; font-size: 14px; line-height: 1.6;">
                                ${name === '日人均会议数减少率' ?
                                    `基线期日人均会议数为 <strong>${baselineValue.toFixed(2)}</strong> 次，当前期为 <strong>${currentValue.toFixed(2)}</strong> 次，${changeText} <strong>${Math.abs(changeRate).toFixed(2)}%</strong>。${data['达标'] ? '已达标 ✅' : '未达标 ❌'} (目标: ${target})` :
                                  name === '日人均会议时长减少率' ?
                                    `基线期日人均会议时长为 <strong>${baselineValue.toFixed(2)}</strong> 分钟，当前期为 <strong>${currentValue.toFixed(2)}</strong> 分钟，${changeText} <strong>${Math.abs(changeRate).toFixed(2)}%</strong>，相当于每天${changeRate > 0 ? '节省' : '增加'}约 <strong>${Math.abs(baselineValue - currentValue).toFixed(0)}</strong> 分钟。${data['达标'] ? '已达标 ✅' : '未达标 ❌'} (目标: ${target})` :
                                    `基线期即时会议占比为 <strong>${baselineValue.toFixed(2)}%</strong>，当前期为 <strong>${currentValue.toFixed(2)}%</strong>，${changeRate > 0 ? '下降' : '上升'} <strong>${Math.abs(changeRate).toFixed(2)}</strong> 个百分点。即时会议占比${changeRate > 0 ? '降低' : '升高'}说明会议计划性${changeRate > 0 ? '提升' : '下降'}。${data['达标'] ? '已达标 ✅' : '未达标 ❌'} (目标: ${target})`
                                }
                            </div>
                        </div>
                    </div>
                </div>
                `;
            });

            container.innerHTML = html;
        }

        function renderStatsComparison() {
            const chart = echarts.init(document.getElementById('stats-comparison-chart'));

            const baseline = dashboardData.baseline_stats || {};
            const current = dashboardData.current_stats || {};

            // 提取数据
            const baselineMean = baseline['mean'] || 0;
            const currentMean = current['mean'] || 0;
            const baselineStd = baseline['std'] || 0;
            const currentStd = current['std'] || 0;
            const baselineCv = baseline['cv'] || 0;
            const currentCv = current['cv'] || 0;
            const baselineMax = baseline['max'] || 0;
            const currentMax = current['max'] || 0;
            const baselineMin = baseline['min'] || 0;
            const currentMin = current['min'] || 0;

            // 动态计算最大值
            const maxMean = Math.max(baselineMean, currentMean) * 1.2 || 10;
            const maxStd = Math.max(baselineStd, currentStd) * 1.2 || 5;
            const maxCv = Math.max(baselineCv, currentCv) * 1.2 || 1;
            const maxMax = Math.max(baselineMax, currentMax) * 1.2 || 15;
            const maxMin = Math.max(baselineMin, currentMin) * 1.2 || 5;

            const option = {
                tooltip: {
                    trigger: 'axis',
                    formatter: function(params) {
                        let result = '';
                        params.forEach(item => {
                            result += `${item.seriesName}<br/>`;
                            result += `${item.name}: ${item.value}<br/>`;
                        });
                        return result;
                    }
                },
                legend: { data: ['基线期', '当前期'], top: 20 },
                radar: {
                    indicator: [
                        { name: '均值', max: maxMean },
                        { name: '标准差', max: maxStd },
                        { name: '变异系数', max: maxCv },
                        { name: '最大值', max: maxMax },
                        { name: '最小值', max: maxMin }
                    ]
                },
                series: [{
                    type: 'radar',
                    data: [
                        {
                            value: [baselineMean, baselineStd, baselineCv, baselineMax, baselineMin],
                            name: '基线期',
                            areaStyle: {
                                color: 'rgba(102, 126, 234, 0.3)'
                            },
                            lineStyle: { color: '#667eea' }
                        },
                        {
                            value: [currentMean, currentStd, currentCv, currentMax, currentMin],
                            name: '当前期',
                            areaStyle: {
                                color: 'rgba(72, 187, 120, 0.3)'
                            },
                            lineStyle: { color: '#48bb78' }
                        }
                    ]
                }]
            };

            chart.setOption(option);

            // 填充数值详情表格
            const statsTable = document.getElementById('stats-details-table');
            if (statsTable) {
                const stats = [
                    { name: '均值', baseline: baselineMean, current: currentMean, unit: '次' },
                    { name: '标准差', baseline: baselineStd, current: currentStd, unit: '' },
                    { name: '变异系数', baseline: baselineCv, current: currentCv, unit: '' },
                    { name: '最大值', baseline: baselineMax, current: currentMax, unit: '次' },
                    { name: '最小值', baseline: baselineMin, current: currentMin, unit: '次' }
                ];

                let tableHtml = '';
                stats.forEach(stat => {
                    const change = ((stat.current - stat.baseline) / stat.baseline * 100).toFixed(2);
                    const changeColor = change > 0 ? '#f56565' : '#48bb78';
                    const changeIcon = change > 0 ? '↑' : '↓';
                    const changeText = Math.abs(change);

                    tableHtml += `
                    <tr style="border-bottom: 1px solid #e2e8f0;">
                        <td style="padding: 10px; font-weight: 500;">${stat.name}</td>
                        <td style="padding: 10px; text-align: right;">${stat.baseline.toFixed(2)}${stat.unit}</td>
                        <td style="padding: 10px; text-align: right;">${stat.current.toFixed(2)}${stat.unit}</td>
                        <td style="padding: 10px; text-align: right; color: ${changeColor}; font-weight: 600;">
                            ${changeIcon} ${changeText}%
                        </td>
                    </tr>
                    `;
                });

                statsTable.innerHTML = tableHtml;
            }

            // 调试信息
            console.log('描述性统计数据:', {
                baseline: { mean: baselineMean, std: baselineStd, cv: baselineCv, max: baselineMax, min: baselineMin },
                current: { mean: currentMean, std: currentStd, cv: currentCv, max: currentMax, min: currentMin }
            });
        }

        function renderMeetingTypeAnalysis() {
            const baseline = dashboardData.baseline_stats || {};
            const current = dashboardData.current_stats || {};

            // 提取会议类型数据
            const baselineInstant = parseFloat(baseline['即时会议数']) || 0;
            const baselineScheduled = parseFloat(baseline['日程会议数']) || 0;
            const baseline1v1 = parseFloat(baseline['1v1通话数']) || 0;

            const currentInstant = parseFloat(current['即时会议数']) || 0;
            const currentScheduled = parseFloat(current['日程会议数']) || 0;
            const current1v1 = parseFloat(current['1v1通话数']) || 0;

            // 调试信息
            console.log('会议类型数据:', {
                baseline: { 即时: baselineInstant, 日程: baselineScheduled, 通话: baseline1v1 },
                current: { 即时: currentInstant, 日程: currentScheduled, 通话: current1v1 },
                baselineTotal: baselineInstant + baselineScheduled + baseline1v1,
                currentTotal: currentInstant + currentScheduled + current1v1
            });

            // 检查数据有效性
            if (baselineInstant === 0 && baselineScheduled === 0 && baseline1v1 === 0) {
                console.warn('基线期会议类型数据全部为0');
            }
            if (currentInstant === 0 && currentScheduled === 0 && current1v1 === 0) {
                console.warn('当前期会议类型数据全部为0');
            }

            // 基线期饼图
            const baselineChart = echarts.init(document.getElementById('meeting-type-baseline'));
            const baselineTotal = baselineInstant + baselineScheduled + baseline1v1;

            baselineChart.setOption({
                title: {
                    text: '基线期会议类型分布',
                    left: 'center',
                    top: 10,
                    textStyle: { fontSize: 16, fontWeight: 'bold' }
                },
                tooltip: {
                    trigger: 'item',
                    formatter: function(params) {
                        return `${params.name}<br/>数量: ${params.value.toFixed(2)}<br/>占比: ${params.percent.toFixed(1)}%`;
                    }
                },
                legend: {
                    orient: 'horizontal',
                    bottom: 10,
                    left: 'center'
                },
                series: [{
                    type: 'pie',
                    radius: ['35%', '65%'],
                    center: ['50%', '55%'],
                    avoidLabelOverlap: true,
                    itemStyle: {
                        borderRadius: 5,
                        borderColor: '#fff',
                        borderWidth: 2
                    },
                    label: {
                        show: true,
                        position: 'outside',
                        formatter: function(params) {
                            return `${params.name}\n${params.value.toFixed(1)}\n${params.percent.toFixed(1)}%`;
                        },
                        fontSize: 12
                    },
                    labelLine: {
                        show: true,
                        length: 15,
                        length2: 10
                    },
                    data: [
                        { value: baselineInstant, name: '即时会议', itemStyle: { color: '#f56565' } },
                        { value: baselineScheduled, name: '日程会议', itemStyle: { color: '#48bb78' } },
                        { value: baseline1v1, name: '1v1通话', itemStyle: { color: '#4299e1' } }
                    ],
                    emphasis: {
                        itemStyle: {
                            shadowBlur: 10,
                            shadowOffsetX: 0,
                            shadowColor: 'rgba(0, 0, 0, 0.5)'
                        }
                    }
                }]
            });

            // 当前期饼图
            const currentChart = echarts.init(document.getElementById('meeting-type-current'));
            const currentTotal = currentInstant + currentScheduled + current1v1;

            currentChart.setOption({
                title: {
                    text: '当前期会议类型分布',
                    left: 'center',
                    top: 10,
                    textStyle: { fontSize: 16, fontWeight: 'bold' }
                },
                tooltip: {
                    trigger: 'item',
                    formatter: function(params) {
                        return `${params.name}<br/>数量: ${params.value.toFixed(2)}<br/>占比: ${params.percent.toFixed(1)}%`;
                    }
                },
                legend: {
                    orient: 'horizontal',
                    bottom: 10,
                    left: 'center'
                },
                series: [{
                    type: 'pie',
                    radius: ['35%', '65%'],
                    center: ['50%', '55%'],
                    avoidLabelOverlap: true,
                    itemStyle: {
                        borderRadius: 5,
                        borderColor: '#fff',
                        borderWidth: 2
                    },
                    label: {
                        show: true,
                        position: 'outside',
                        formatter: function(params) {
                            return `${params.name}\n${params.value.toFixed(1)}\n${params.percent.toFixed(1)}%`;
                        },
                        fontSize: 12
                    },
                    labelLine: {
                        show: true,
                        length: 15,
                        length2: 10
                    },
                    data: [
                        { value: currentInstant, name: '即时会议', itemStyle: { color: '#f56565' } },
                        { value: currentScheduled, name: '日程会议', itemStyle: { color: '#48bb78' } },
                        { value: current1v1, name: '1v1通话', itemStyle: { color: '#4299e1' } }
                    ],
                    emphasis: {
                        itemStyle: {
                            shadowBlur: 10,
                            shadowOffsetX: 0,
                            shadowColor: 'rgba(0, 0, 0, 0.5)'
                        }
                    }
                }]
            });

            // 填充表格
            const tbody = document.getElementById('meeting-type-table');
            if (tbody) {
                const types = [
                    { name: '即时会议', baseline: baselineInstant, current: currentInstant, icon: '⚡', color: '#f56565' },
                    { name: '日程会议', baseline: baselineScheduled, current: currentScheduled, icon: '📅', color: '#48bb78' },
                    { name: '1v1通话', baseline: baseline1v1, current: current1v1, icon: '📞', color: '#4299e1' }
                ];

                let html = '';
                let insights = [];

                // 添加总计行的数据
                let totalBaselineCount = 0;
                let totalCurrentCount = 0;

                types.forEach(type => {
                    const baselineCount = type.baseline;
                    const currentCount = type.current;

                    totalBaselineCount += baselineCount;
                    totalCurrentCount += currentCount;

                    // 数量变化
                    const countChange = currentCount - baselineCount;
                    const countChangePercent = baselineCount > 0 ? ((countChange / baselineCount) * 100) : 0;

                    // 占比计算
                    const baselinePercent = baselineTotal > 0 ? (baselineCount / baselineTotal * 100) : 0;
                    const currentPercent = currentTotal > 0 ? (currentCount / currentTotal * 100) : 0;
                    const percentChange = currentPercent - baselinePercent;

                    // 趋势判断
                    const trendValue = percentChange;
                    let trend = '→ 持平';
                    let trendColor = '#718096';

                    if (Math.abs(trendValue) < 0.5) {
                        trend = '→ 持平';
                        trendColor = '#718096';
                    } else if (trendValue > 0) {
                        trend = '↑ 上升';
                        trendColor = type.name === '即时会议' ? '#f56565' : '#48bb78';
                    } else {
                        trend = '↓ 下降';
                        trendColor = type.name === '即时会议' ? '#48bb78' : '#f56565';
                    }

                    // 收集洞察信息
                    if (type.name === '即时会议') {
                        if (trendValue < -5) {
                            insights.push(`✅ <strong>即时会议占比下降 ${Math.abs(trendValue).toFixed(1)} 个百分点</strong>，说明会议计划性显著提升，团队规范性改善明显。`);
                        } else if (trendValue > 5) {
                            insights.push(`⚠️ <strong>即时会议占比上升 ${trendValue.toFixed(1)} 个百分点</strong>，建议加强会议预约规划，减少临时会议干扰。`);
                        } else if (Math.abs(trendValue) <= 5 && Math.abs(trendValue) >= 2) {
                            insights.push(`即时会议占比${trendValue > 0 ? '略有上升' : '略有下降'} ${Math.abs(trendValue).toFixed(1)} 个百分点，整体保持稳定。`);
                        }
                    }

                    if (type.name === '日程会议' && trendValue > 5) {
                        insights.push(`✅ <strong>日程会议占比上升 ${trendValue.toFixed(1)} 个百分点</strong>，预约会议习惯培养成效显著。`);
                    }

                    if (type.name === '1v1通话' && Math.abs(trendValue) > 8) {
                        insights.push(`${trendValue > 0 ? '⚠️' : '📊'} <strong>1v1通话占比${trendValue > 0 ? '上升' : '下降'} ${Math.abs(trendValue).toFixed(1)} 个百分点</strong>，${trendValue > 0 ? '一对一沟通增多' : '一对一沟通减少'}。`);
                    }

                    html += `
                    <tr style="background: ${type.name === '即时会议' ? '#fff5f5' : type.name === '日程会议' ? '#f0fff4' : '#eff6ff'};">
                        <td style="padding: 12px; border: 1px solid #e2e8f0;">
                            <strong style="color: ${type.color};">${type.icon} ${type.name}</strong>
                        </td>
                        <td style="padding: 12px; text-align: right; border: 1px solid #e2e8f0; font-weight: 500;">
                            ${baselineCount.toFixed(2)}
                        </td>
                        <td style="padding: 12px; text-align: right; border: 1px solid #e2e8f0; font-weight: 500;">
                            ${currentCount.toFixed(2)}
                        </td>
                        <td style="padding: 12px; text-align: right; border: 1px solid #e2e8f0; font-weight: 600; ${countChange >= 0 ? 'color: #e53e3e;' : 'color: #38a169;'}">
                            ${countChange >= 0 ? '+' : ''}${countChange.toFixed(2)}<br/>
                            <span style="font-size: 12px;">(${countChange >= 0 ? '+' : ''}${countChangePercent.toFixed(1)}%)</span>
                        </td>
                        <td style="padding: 12px; text-align: right; border: 1px solid #e2e8f0;">
                            ${baselinePercent.toFixed(1)}%
                        </td>
                        <td style="padding: 12px; text-align: right; border: 1px solid #e2e8f0;">
                            ${currentPercent.toFixed(1)}%
                        </td>
                        <td style="padding: 12px; text-align: center; border: 1px solid #e2e8f0; font-weight: 700; font-size: 15px; color: ${trendColor};">
                            ${percentChange >= 0 ? '+' : ''}${percentChange.toFixed(1)}<br/>
                            <span style="font-size: 11px;">个百分点</span>
                        </td>
                        <td style="padding: 12px; text-align: center; border: 1px solid #e2e8f0; color: ${trendColor}; font-weight: bold; font-size: 14px;">
                            ${trend}
                        </td>
                    </tr>
                    `;
                });

                // 添加总计行
                html += `
                <tr style="background: #edf2f7; font-weight: bold;">
                    <td style="padding: 12px; border: 1px solid #e2e8f0;">📊 总计</td>
                    <td style="padding: 12px; text-align: right; border: 1px solid #e2e8f0;">${totalBaselineCount.toFixed(2)}</td>
                    <td style="padding: 12px; text-align: right; border: 1px solid #e2e8f0;">${totalCurrentCount.toFixed(2)}</td>
                    <td style="padding: 12px; text-align: right; border: 1px solid #e2e8f0;">
                        ${(totalCurrentCount - totalBaselineCount >= 0 ? '+' : '')}${(totalCurrentCount - totalBaselineCount).toFixed(2)}
                    </td>
                    <td style="padding: 12px; text-align: right; border: 1px solid #e2e8f0;">100.0%</td>
                    <td style="padding: 12px; text-align: right; border: 1px solid #e2e8f0;">100.0%</td>
                    <td style="padding: 12px; text-align: center; border: 1px solid #e2e8f0;">-</td>
                    <td style="padding: 12px; text-align: center; border: 1px solid #e2e8f0;">-</td>
                </tr>
                `;

                tbody.innerHTML = html;

                // 填充洞察内容
                const insightsContent = document.getElementById('meeting-type-insights-content');
                if (insightsContent) {
                    if (insights.length > 0) {
                        insightsContent.innerHTML = insights.join('<br/><br/>');
                    } else {
                        insightsContent.innerHTML = '📊 各类型会议占比变化较小（±2个百分点以内），整体保持稳定。团队会议结构合理，继续保持当前会议管理策略。';
                    }
                }
            }
        }

        // ==================== 模块4: 人员详情 ====================
        function initPersonnel() {
            renderTop10Users();
            renderUserTierChart();
            renderAnomalies();
        }

        function renderTop10Users() {
            const container = document.getElementById('top10-users');
            if (!container || !dashboardData.top10_users) return;

            let html = '';
            dashboardData.top10_users.forEach(user => {
                const statusClass = user.status === '改善' ? '改善' : '增加';
                const changeIcon = user.change_rate < 0 ? '📉' : '📈';

                html += `
                <div class="user-card" onclick="showUserDetail('${user.user_name}')">
                    <div class="user-rank">#${user.rank}</div>
                    <div class="user-name">${user.user_name}</div>
                    <div class="user-metrics">
                        <span style="color: #718096;">基线: ${user.baseline_meetings}</span>
                        <span style="color: #718096;">当前: ${user.current_meetings}</span>
                    </div>
                    <div class="metric-change" style="color: ${user.change_rate < 0 ? '#48bb78' : '#f56565'};">
                        ${changeIcon} ${user.change_rate}%
                    </div>
                    <span class="user-status ${statusClass}">${user.status}</span>
                </div>
                `;
            });

            container.innerHTML = html;
        }

        function renderUserTierChart() {
            const chart = echarts.init(document.getElementById('user-tier-chart'));

            const tiers = dashboardData.user_tiers || {};
            const highCount = tiers.high?.length || 0;
            const mediumCount = tiers.medium?.length || 0;
            const lowCount = tiers.low?.length || 0;

            const option = {
                tooltip: { trigger: 'axis' },
                xAxis: {
                    type: 'category',
                    data: ['高频(≥5次)', '中频(2-5次)', '低频(<2次)']
                },
                yAxis: { type: 'value', name: '人数' },
                series: [{
                    data: [highCount, mediumCount, lowCount],
                    type: 'bar',
                    itemStyle: {
                        color: function(params) {
                            const colors = ['#f56565', '#ed8936', '#48bb78'];
                            return colors[params.dataIndex];
                        }
                    },
                    label: {
                        show: true,
                        position: 'top',
                        formatter: '{c}人'
                    }
                }]
            };

            chart.setOption(option);
        }

        function renderAnomalies() {
            const tbody = document.getElementById('anomaly-tbody');
            if (!tbody || !dashboardData.anomalies) return;

            let html = '';
            dashboardData.anomalies.forEach((anomaly, index) => {
                html += `
                <tr>
                    <td>${index + 1}</td>
                    <td>${anomaly.user_name}</td>
                    <td>${anomaly.metric}</td>
                    <td>${anomaly.value}</td>
                    <td>${anomaly.mean}</td>
                    <td>${anomaly.z_score}</td>
                    <td><span class="badge ${anomaly.type === '高于平均' ? 'badge-warning' : 'badge-info'}">${anomaly.type}</span></td>
                </tr>
                `;
            });

            tbody.innerHTML = html;
        }

        // ==================== 用户详情弹窗 ====================
        function showUserDetail(userName) {
            const modal = document.getElementById('user-modal');
            const modalName = document.getElementById('modal-user-name');
            const modalContent = document.getElementById('modal-user-content');

            if (!modal) return;

            // 查找用户数据
            const userTop10 = dashboardData.top10_users?.find(u => u.user_name === userName);
            const userHistory = dashboardData.raw_data.filter(r => r.user_name === userName);

            if (!userHistory.length) {
                alert('未找到该用户数据');
                return;
            }

            modalName.textContent = userName + ' - 个人会议数据详情';

            // 构建详情内容
            let html = '<div style="margin: 20px 0;">';

            if (userTop10) {
                html += `
                <div style="background: #f7fafc; padding: 20px; border-radius: 8px; margin-bottom: 20px;">
                    <h3 style="margin-bottom: 15px;">基本信息</h3>
                    <div style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px;">
                        <div>
                            <div style="color: #718096; font-size: 14px;">排名</div>
                            <div style="font-size: 20px; font-weight: bold;">#${userTop10.rank}</div>
                        </div>
                        <div>
                            <div style="color: #718096; font-size: 14px;">变化率</div>
                            <div style="font-size: 20px; font-weight: bold; color: ${userTop10.change_rate < 0 ? '#48bb78' : '#f56565'};">
                                ${userTop10.change_rate}%
                            </div>
                        </div>
                        <div>
                            <div style="color: #718096; font-size: 14px;">基线期会议数</div>
                            <div style="font-size: 20px; font-weight: bold;">${userTop10.baseline_meetings}次/天</div>
                        </div>
                        <div>
                            <div style="color: #718096; font-size: 14px;">当前期会议数</div>
                            <div style="font-size: 20px; font-weight: bold;">${userTop10.current_meetings}次/天</div>
                        </div>
                    </div>
                </div>
                `;
            }

            html += `
                <h3 style="margin-bottom: 15px;">全部周期数据</h3>
                <table style="width: 100%;">
                    <thead>
                        <tr>
                            <th>周期</th>
                            <th>日均会议数</th>
                            <th>日均时长(分)</th>
                            <th>即时会议</th>
                            <th>日程会议</th>
                            <th>1v1通话</th>
                        </tr>
                    </thead>
                    <tbody>
            `;

            userHistory.forEach(record => {
                html += `
                <tr>
                    <td>${record.period_name}</td>
                    <td>${(record['日人均线上会议数'] || 0).toFixed(2)}</td>
                    <td>${(record['日人均线上会议时长(分钟)'] || 0).toFixed(0)}</td>
                    <td>${record['即时会议数'] || 0}</td>
                    <td>${record['日程会议数'] || 0}</td>
                    <td>${record['1v1通话数'] || 0}</td>
                </tr>
                `;
            });

            html += '</tbody></table></div>';

            modalContent.innerHTML = html;
            modal.style.display = 'block';
        }

        function closeUserModal() {
            const modal = document.getElementById('user-modal');
            if (modal) {
                modal.style.display = 'none';
            }
        }

        // 点击模态框外部关闭
        window.onclick = function(event) {
            const modal = document.getElementById('user-modal');
            if (event.target === modal) {
                modal.style.display = 'none';
            }
        }

        // ==================== 导出功能 ====================
        function exportToCSV() {
            const headers = ['姓名', '周期', '日均会议数', '日均时长(分)', '即时会议', '日程会议', '1v1通话'];
            let csv = headers.join(',') + '\\n';

            filteredData.forEach(row => {
                csv += [
                    row.user_name || '',
                    row.period_name || '',
                    (row['日人均线上会议数'] || 0).toFixed(2),
                    (row['日人均线上会议时长(分钟)'] || 0).toFixed(0),
                    row['即时会议数'] || 0,
                    row['日程会议数'] || 0,
                    row['1v1通话数'] || 0
                ].join(',') + '\\n';
            });

            downloadFile(csv, 'meeting_data.csv', 'text/csv');
        }

        function exportToJSON() {
            const json = JSON.stringify(filteredData, null, 2);
            downloadFile(json, 'meeting_data.json', 'application/json');
        }

        function downloadFile(content, filename, type) {
            const blob = new Blob([content], { type: type });
            const url = URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = filename;
            a.click();
            URL.revokeObjectURL(url);
        }

        // ==================== 响应式处理 ====================
        window.addEventListener('resize', function() {
            const charts = document.querySelectorAll('.chart');
            charts.forEach(chart => {
                const instance = echarts.getInstanceByDom(chart);
                if (instance) {
                    instance.resize();
                }
            });
        });

        function showKPIDetail(kpiName) {
            // 切换到分析结果页面
            showTab('analysis');
        }
'''


if __name__ == "__main__":
    # 测试代码
    gen = FullDashboardGenerator()
    print("Full Dashboard Generator ready!")
