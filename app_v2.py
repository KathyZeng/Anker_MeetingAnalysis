#!/usr/bin/env python3
"""
会议分析系统 - Streamlit Web应用 V2
提供完整的数据分析和可视化界面
"""

import streamlit as st
import pandas as pd
import numpy as np
import os
import json
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import sys

# 不使用meeting_analysis模块，直接在这里实现需要的功能
import re
from datetime import datetime

# 设置页面配置
st.set_page_config(
    page_title="会议改善效果评估系统",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 自定义CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        padding: 1rem 0;
    }
    .kpi-card {
        padding: 1.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        color: white;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .kpi-value {
        font-size: 2.5rem;
        font-weight: bold;
        margin: 0.5rem 0;
    }
    .kpi-label {
        font-size: 1rem;
        opacity: 0.9;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #2c3e50;
        padding: 0.5rem 0;
        border-bottom: 2px solid #3498db;
        margin-top: 1rem;
    }
    .info-box {
        padding: 1rem;
        background-color: #d1ecf1;
        border-left: 4px solid #17a2b8;
        border-radius: 4px;
        margin: 1rem 0;
    }
    .warning-box {
        padding: 1rem;
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
        border-radius: 4px;
        margin: 1rem 0;
    }
    .success-box {
        padding: 1rem;
        background-color: #d4edda;
        border-left: 4px solid #28a745;
        border-radius: 4px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# 目录配置
INPUT_DIR = "input"
CONFIG_DIR = "config"
OUTPUT_DIR = "output"
CONFIG_FILE = os.path.join(CONFIG_DIR, "responsible_persons.json")
DATA_CONFIG_FILE = os.path.join(CONFIG_DIR, "data_config.json")

# 确保目录存在
os.makedirs(INPUT_DIR, exist_ok=True)
os.makedirs(CONFIG_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)


# ==================== 配置管理函数 ====================

def save_data_config(baseline_files, current_files):
    """保存数据配置"""
    config = {
        'baseline_files': baseline_files,
        'current_files': current_files,
        'last_updated': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    try:
        with open(DATA_CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, ensure_ascii=False, indent=2)
        return True
    except Exception as e:
        st.error(f"保存配置失败: {str(e)}")
        return False


def load_data_config():
    """加载数据配置"""
    if os.path.exists(DATA_CONFIG_FILE):
        try:
            with open(DATA_CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
            return config.get('baseline_files', []), config.get('current_files', [])
        except Exception as e:
            st.warning(f"加载配置失败: {str(e)}")
            return [], []
    return [], []


# ==================== 数据加载和分析函数 ====================

def parse_period_from_filename(filename):
    """从文件名解析周期"""
    # 月度数据: 9月会议详情.csv
    month_match = re.search(r'(\d+)月', filename)
    if month_match:
        return f"{month_match.group(1)}月"

    # 周度数据: 11.03-11.09会议详情.csv
    week_match = re.search(r'(\d+\.\d+-\d+\.\d+)', filename)
    if week_match:
        return week_match.group(1)

    return filename.replace('.csv', '')


def load_single_csv(file_path, filename):
    """加载单个CSV文件"""
    try:
        # 读取第一行检查是否是"表格 1"
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            first_line = f.readline().strip()

        # 如果第一行是"表格 1"或类似的标题，跳过它
        if '表格' in first_line and first_line.count(',') == 0:
            df = pd.read_csv(file_path, encoding='utf-8-sig', skiprows=1)
        else:
            df = pd.read_csv(file_path, encoding='utf-8-sig')

        # 删除Unnamed列（这些是CSV中的空列）
        unnamed_cols = [col for col in df.columns if col.startswith('Unnamed')]
        if unnamed_cols:
            df = df.drop(columns=unnamed_cols)

        # 删除所有值都为空的列
        df = df.dropna(axis=1, how='all')

        # 添加周期和文件名信息
        df['period'] = parse_period_from_filename(filename)
        df['file_name'] = filename

        return df
    except Exception as e:
        st.error(f"读取文件失败 {filename}: {str(e)}")
        return None


def load_all_csvs():
    """加载所有CSV文件"""
    all_dfs = []

    for filename in get_csv_files():
        file_path = os.path.join(INPUT_DIR, filename)
        df = load_single_csv(file_path, filename)

        if df is not None:
            all_dfs.append(df)

    if all_dfs:
        return pd.concat(all_dfs, ignore_index=True)
    else:
        return pd.DataFrame()


def calculate_period_kpis(df):
    """计算某个周期的KPI"""
    if df is None or df.empty:
        return {}

    # 使用fillna(0)确保没有NaN值
    kpis = {
        '日人均线上会议数-即时+日程': df['日人均线上会议数-即时+日程'].fillna(0).mean(),
        '日人均线上会议时长(分钟)-即时+日程': df['日人均线上会议时长(分钟)-即时+日程'].fillna(0).mean(),
        '即时会议': df['即时会议'].fillna(0).sum(),
        '日程会议': df['日程会议'].fillna(0).sum(),
        '即时+日程会议': df['即时+日程会议'].fillna(0).sum(),
        '1v1通话数': df['1v1通话数'].fillna(0).sum(),
    }

    return kpis


def get_top_users(df, n=10):
    """获取Top N用户"""
    if df is None or df.empty:
        return pd.DataFrame()

    top_users = df.nlargest(n, '日人均线上会议数-即时+日程')[
        ['user_name', '日人均线上会议数-即时+日程', '日人均线上会议时长(分钟)-即时+日程', 'period']
    ].copy()

    return top_users


def tier_users(df):
    """用户分层"""
    if df is None or df.empty:
        return {'high': {'count': 0, 'avg': 0}, 'medium': {'count': 0, 'avg': 0}, 'low': {'count': 0, 'avg': 0}}

    high = df[df['日人均线上会议数-即时+日程'] >= 5]
    medium = df[(df['日人均线上会议数-即时+日程'] >= 2) & (df['日人均线上会议数-即时+日程'] < 5)]
    low = df[df['日人均线上会议数-即时+日程'] < 2]

    return {
        'high': {
            'count': len(high),
            'avg': high['日人均线上会议数-即时+日程'].mean() if not high.empty else 0
        },
        'medium': {
            'count': len(medium),
            'avg': medium['日人均线上会议数-即时+日程'].mean() if not medium.empty else 0
        },
        'low': {
            'count': len(low),
            'avg': low['日人均线上会议数-即时+日程'].mean() if not low.empty else 0
        }
    }


def sort_periods(periods):
    """按时间顺序排序周期列表"""
    def period_sort_key(period):
        # 处理非字符串类型
        if not isinstance(period, str):
            return (999, 999, str(period))

        # 提取月份（如"9月", "10月"）
        month_match = re.search(r'(\d+)月', period)
        if month_match:
            return (int(month_match.group(1)), 0, '')

        # 提取周期范围（如"10.20-10.26"）
        week_match = re.search(r'(\d+)\.(\d+)-(\d+)\.(\d+)', period)
        if week_match:
            month1 = int(week_match.group(1))
            day1 = int(week_match.group(2))
            return (month1, 1, f"{month1:02d}{day1:02d}")

        # 其他情况按原样排序
        return (999, 999, str(period))

    return sorted(periods, key=period_sort_key)


# ==================== 工具函数 ====================

def get_csv_files():
    """获取input目录中的CSV文件"""
    if not os.path.exists(INPUT_DIR):
        return []
    return sorted([f for f in os.listdir(INPUT_DIR) if f.endswith('.csv')])


def load_config():
    """加载主责人员配置"""
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
                config = json.load(f)
                # 过滤示例数据
                config['responsible_persons'] = [
                    p for p in config.get('responsible_persons', [])
                    if not p.get('name', '').startswith('示例人员')
                ]
                return config
        except:
            pass

    return {
        "version": "1.1",
        "responsible_persons": []
    }


def save_config(config):
    """保存主责人员配置"""
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)


def load_data_with_selection(baseline_files, current_files):
    """根据用户选择加载数据"""
    # 加载所有数据
    all_data = load_all_csvs()

    if all_data.empty:
        return None, None, None

    # 根据选择分类数据
    baseline_data = all_data[all_data['file_name'].isin(baseline_files)].copy()
    current_data = all_data[all_data['file_name'].isin(current_files)].copy()

    # 标记周期类型
    all_data['period_type'] = all_data['file_name'].apply(
        lambda x: 'baseline' if x in baseline_files else ('current' if x in current_files else 'other')
    )
    baseline_data['period_type'] = 'baseline'
    current_data['period_type'] = 'current'

    return all_data, baseline_data, current_data


def get_users_from_data(df):
    """从数据中获取用户列表"""
    if df is None or df.empty:
        return []
    return sorted(df['user_name'].dropna().unique().tolist())


# ==================== Session State 初始化 ====================

# 初始化session_state，并尝试加载上次的配置
if 'baseline_files' not in st.session_state:
    saved_baseline, saved_current = load_data_config()
    st.session_state.baseline_files = saved_baseline
    st.session_state.current_files = saved_current
    st.session_state.config_loaded = True if (saved_baseline or saved_current) else False
else:
    if 'config_loaded' not in st.session_state:
        st.session_state.config_loaded = False

if 'current_files' not in st.session_state:
    st.session_state.current_files = []
if 'data_loaded' not in st.session_state:
    st.session_state.data_loaded = False
if 'all_data' not in st.session_state:
    st.session_state.all_data = None
if 'baseline_data' not in st.session_state:
    st.session_state.baseline_data = None
if 'current_data' not in st.session_state:
    st.session_state.current_data = None
if 'auto_load_attempted' not in st.session_state:
    st.session_state.auto_load_attempted = False


# ==================== 主界面 ====================

st.markdown('''
<h1 style="text-align: center; color: #1f77b4; margin-bottom: 0;">
📊 会议改善效果评估系统
</h1>
<p style="text-align: center; font-size: 0.9rem; color: #666; margin-top: 0;">
V2 | 作者: Elva.Zeng
</p>
''', unsafe_allow_html=True)

# 侧边栏导航
st.sidebar.title("📋 导航")

csv_files = get_csv_files()
data_ready = st.session_state.data_loaded and st.session_state.all_data is not None

# 固定的页面列表
pages = [
    "📁 数据管理",
    "📊 概览",
    "📄 原始数据",
    "📈 分析结果",
    "👥 人员详情"
]

page = st.sidebar.radio("选择功能", pages)

# 显示数据状态
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 数据状态")
if data_ready:
    st.sidebar.success("✅ 数据已加载")
    st.sidebar.info(f"📦 总记录: {len(st.session_state.all_data)}")
    st.sidebar.info(f"📅 基线期: {len(st.session_state.baseline_data)} 条")
    st.sidebar.info(f"📅 当前期: {len(st.session_state.current_data)} 条")
else:
    st.sidebar.warning("⚠️ 请先加载数据")


# ==================== 页面1: 数据管理 ====================

if page == "📁 数据管理":
    # 自动加载上次的配置
    if st.session_state.config_loaded and not st.session_state.auto_load_attempted and csv_files:
        if st.session_state.baseline_files and st.session_state.current_files:
            # 验证文件是否存在
            valid_baseline = [f for f in st.session_state.baseline_files if f in csv_files]
            valid_current = [f for f in st.session_state.current_files if f in csv_files]

            if valid_baseline and valid_current:
                with st.spinner("正在自动加载上次的配置..."):
                    all_data, baseline_data, current_data = load_data_with_selection(
                        valid_baseline, valid_current
                    )

                    if all_data is not None and not all_data.empty:
                        st.session_state.all_data = all_data
                        st.session_state.baseline_data = baseline_data
                        st.session_state.current_data = current_data
                        st.session_state.baseline_files = valid_baseline
                        st.session_state.current_files = valid_current
                        st.session_state.data_loaded = True
                        st.success("✅ 已自动加载上次的配置和数据")

                st.session_state.auto_load_attempted = True

    # ==== 第一部分：数据周期选择（放在最上面）====
    st.markdown("## 📅 选择数据周期")

    if not csv_files:
        st.warning("⚠️ 暂无CSV文件，请先上传数据")
    else:
        # 显示上次配置时间
        if os.path.exists(DATA_CONFIG_FILE):
            try:
                with open(DATA_CONFIG_FILE, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                    last_updated = config.get('last_updated', '未知')
                    st.info(f"💾 上次配置时间: {last_updated}")
            except:
                pass

        st.markdown("""
        <div class="info-box">
            <b>💡 说明：</b><br>
            • <b>基线期</b>：措施实施前的数据（通常是9月+10月）<br>
            • <b>当前期</b>：措施实施后的数据（最近几周）<br>
            • 系统将对比两个周期的差异，计算改善效果<br>
            • <b>配置会自动保存</b>，下次启动应用会自动加载
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### 📊 基线期数据")
            baseline_files = st.multiselect(
                "选择基线期文件（措施实施前）",
                csv_files,
                default=st.session_state.baseline_files,
                key="baseline_select",
                help="选择作为基线期的CSV文件"
            )

        with col2:
            st.markdown("#### 📈 当前期数据")
            # 排除已选为基线期的文件
            available_files = [f for f in csv_files if f not in baseline_files]
            current_files = st.multiselect(
                "选择当前期文件（措施实施后）",
                available_files,
                default=[f for f in st.session_state.current_files if f in available_files],
                key="current_select",
                help="选择作为当前期的CSV文件"
            )

        # 加载数据按钮
        if st.button("🚀 加载数据并开始分析", type="primary", use_container_width=True):
            if not baseline_files:
                st.error("❌ 请至少选择一个基线期文件")
            elif not current_files:
                st.error("❌ 请至少选择一个当前期文件")
            else:
                with st.spinner("正在加载数据..."):
                    all_data, baseline_data, current_data = load_data_with_selection(
                        baseline_files, current_files
                    )

                if all_data is not None and not all_data.empty:
                    try:
                        st.session_state.all_data = all_data
                        st.session_state.baseline_data = baseline_data
                        st.session_state.current_data = current_data
                        st.session_state.baseline_files = baseline_files
                        st.session_state.current_files = current_files
                        st.session_state.data_loaded = True

                        # 保存配置到文件
                        save_data_config(baseline_files, current_files)

                        st.success(f"""
                        ✅ 数据加载成功！配置已自动保存
                        - 总记录数: {len(all_data)}
                        - 基线期: {len(baseline_data)} 条
                        - 当前期: {len(current_data)} 条
                        """)
                        st.info("💡 现在可以切换到其他页面查看分析结果")

                    except Exception as e:
                        st.error(f"❌ 保存数据时出错: {str(e)}")
                        import traceback
                        st.code(traceback.format_exc())
                else:
                    st.error("❌ 数据加载失败，请检查CSV文件格式")

    # ==== 第二部分：文件管理 ====
    st.markdown("---")
    st.markdown("## 📤 上传CSV文件")
    uploaded_files = st.file_uploader(
        "选择CSV文件",
        type=['csv'],
        accept_multiple_files=True,
        help="支持拖拽上传多个CSV文件"
    )

    if uploaded_files:
        success_count = 0
        for uploaded_file in uploaded_files:
            try:
                file_path = os.path.join(INPUT_DIR, uploaded_file.name)
                with open(file_path, 'wb') as f:
                    f.write(uploaded_file.getbuffer())
                success_count += 1
            except Exception as e:
                st.error(f"❌ 上传失败: {uploaded_file.name} - {str(e)}")

        if success_count > 0:
            st.success(f"✅ 成功上传 {success_count} 个文件")
            st.rerun()

    # 显示已有文件
    st.markdown("---")
    st.markdown("### 📂 已上传的文件")

    if not csv_files:
        st.info("📭 暂无CSV文件，请先上传数据")
    else:
        st.success(f"✅ 共有 {len(csv_files)} 个CSV文件")

        # 文件列表
        for idx, file in enumerate(csv_files):
            file_path = os.path.join(INPUT_DIR, file)
            file_size = os.path.getsize(file_path) / 1024  # KB

            col1, col2, col3 = st.columns([3, 1, 1])
            with col1:
                st.text(f"📄 {file}")
            with col2:
                st.text(f"{file_size:.1f} KB")
            with col3:
                if st.button("🗑️", key=f"del_{idx}", help=f"删除 {file}"):
                    os.remove(file_path)
                    st.success(f"✅ 已删除: {file}")
                    st.rerun()


# ==================== 页面2: 概览 ====================

elif page == "📊 概览":
    st.markdown('<div class="section-header">📊 数据概览</div>', unsafe_allow_html=True)

    if not data_ready:
        st.warning("⚠️ 请先在'数据管理'页面加载数据")
    else:
        # 检查数据有效性
        if st.session_state.baseline_data is None or st.session_state.baseline_data.empty:
            st.warning("⚠️ 基线期数据为空，请在'数据管理'页面选择基线期数据")
            baseline_kpis = {}
        else:
            baseline_kpis = calculate_period_kpis(st.session_state.baseline_data)

        if st.session_state.current_data is None or st.session_state.current_data.empty:
            st.warning("⚠️ 当前期数据为空，请在'数据管理'页面选择当前期数据")
            current_kpis = {}
        else:
            current_kpis = calculate_period_kpis(st.session_state.current_data)

        # KPI卡片
        st.markdown("### 📊 核心KPI指标")

        col1, col2, col3 = st.columns(3)

        with col1:
            baseline_meetings = baseline_kpis.get('日人均线上会议数-即时+日程', 0)
            current_meetings = current_kpis.get('日人均线上会议数-即时+日程', 0)
            change = ((current_meetings - baseline_meetings) / baseline_meetings * 100) if baseline_meetings > 0 else 0

            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">日人均会议数</div>
                <div class="kpi-value">{current_meetings:.2f}</div>
                <div class="kpi-label">
                    基线期: {baseline_meetings:.2f} |
                    变化: {change:+.1f}%
                </div>
            </div>
            """, unsafe_allow_html=True)

            with st.expander("💡 计算说明", expanded=False):
                st.markdown("""
                **计算方式**:
                - 取所有记录的 `日人均线上会议数-即时+日程` 字段的**平均值**

                **数据源字段**:
                - `日人均线上会议数-即时+日程`

                **含义**:
                - 平均每人每天参加的线上会议次数（包含即时会议和日程会议，不含1v1通话）

                **计算示例**:
                - 基线期: {len(st.session_state.baseline_data)}条记录 → 平均值 {baseline_meetings:.2f}
                - 当前期: {len(st.session_state.current_data)}条记录 → 平均值 {current_meetings:.2f}
                """)

        with col2:
            baseline_duration = baseline_kpis.get('日人均线上会议时长(分钟)-即时+日程', 0)
            current_duration = current_kpis.get('日人均线上会议时长(分钟)-即时+日程', 0)
            change = ((current_duration - baseline_duration) / baseline_duration * 100) if baseline_duration > 0 else 0

            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">日人均会议时长（分钟）</div>
                <div class="kpi-value">{current_duration:.1f}</div>
                <div class="kpi-label">
                    基线期: {baseline_duration:.1f} |
                    变化: {change:+.1f}%
                </div>
            </div>
            """, unsafe_allow_html=True)

            with st.expander("💡 计算说明", expanded=False):
                st.markdown("""
                **计算方式**:
                - 取所有记录的 `日人均线上会议时长(分钟)-即时+日程` 字段的**平均值**

                **数据源字段**:
                - `日人均线上会议时长(分钟)-即时+日程`

                **含义**:
                - 平均每人每天在线上会议中的总时长（分钟）

                **计算示例**:
                - 基线期: {len(st.session_state.baseline_data)}条记录 → 平均值 {baseline_duration:.1f}分钟
                - 当前期: {len(st.session_state.current_data)}条记录 → 平均值 {current_duration:.1f}分钟
                """)

        with col3:
            baseline_instant = baseline_kpis.get('即时会议', 0)
            baseline_total = baseline_kpis.get('即时+日程会议', 1)
            current_instant = current_kpis.get('即时会议', 0)
            current_total = current_kpis.get('即时+日程会议', 1)

            baseline_ratio = (baseline_instant / baseline_total * 100) if baseline_total > 0 else 0
            current_ratio = (current_instant / current_total * 100) if current_total > 0 else 0
            change = current_ratio - baseline_ratio

            st.markdown(f"""
            <div class="kpi-card">
                <div class="kpi-label">即时会议占比</div>
                <div class="kpi-value">{current_ratio:.1f}%</div>
                <div class="kpi-label">
                    基线期: {baseline_ratio:.1f}% |
                    变化: {change:+.1f}pp
                </div>
            </div>
            """, unsafe_allow_html=True)

            with st.expander("💡 计算说明", expanded=False):
                st.markdown(f"""
                **计算方式**:
                - 即时会议占比 = (即时会议总数 ÷ 即时+日程会议总数) × 100%

                **数据源字段**:
                - `即时会议` (求和)
                - `即时+日程会议` (求和)

                **含义**:
                - 在所有线上会议中，即时发起的会议所占的比例

                **计算示例**:
                - 基线期: {baseline_instant}个即时会议 ÷ {baseline_total}个总会议 = {baseline_ratio:.1f}%
                - 当前期: {current_instant}个即时会议 ÷ {current_total}个总会议 = {current_ratio:.1f}%
                """)

        # 趋势图
        st.markdown("---")
        st.markdown("### 📈 趋势分析")

        # 按周期统计
        period_stats = st.session_state.all_data.groupby('period').agg({
            '日人均线上会议数-即时+日程': 'mean',
            '日人均线上会议时长(分钟)-即时+日程': 'mean'
        }).reset_index()

        # 对周期进行排序
        period_stats['period'] = pd.Categorical(
            period_stats['period'],
            categories=sort_periods(period_stats['period'].tolist()),
            ordered=True
        )
        period_stats = period_stats.sort_values('period')

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=period_stats['period'],
            y=period_stats['日人均线上会议数-即时+日程'],
            mode='lines+markers',
            name='日人均会议数',
            line=dict(color='#667eea', width=3)
        ))

        fig.update_layout(
            title="会议数趋势",
            xaxis_title="周期",
            yaxis_title="日人均会议数",
            height=400,
            hovermode='x unified'
        )

        st.plotly_chart(fig, width='stretch')

        # 会议类型分布
        st.markdown("---")
        st.markdown("### 📊 会议类型分布")

        col1, col2 = st.columns(2)

        with col1:
            baseline_types = {
                '即时会议': baseline_kpis.get('即时会议', 0),
                '日程会议': baseline_kpis.get('日程会议', 0),
                '1v1通话': baseline_kpis.get('1v1通话数', 0)
            }

            fig = px.pie(
                values=list(baseline_types.values()),
                names=list(baseline_types.keys()),
                title="基线期会议类型分布"
            )
            st.plotly_chart(fig, width='stretch')

        with col2:
            current_types = {
                '即时会议': current_kpis.get('即时会议', 0),
                '日程会议': current_kpis.get('日程会议', 0),
                '1v1通话': current_kpis.get('1v1通话数', 0)
            }

            fig = px.pie(
                values=list(current_types.values()),
                names=list(current_types.keys()),
                title="当前期会议类型分布"
            )
            st.plotly_chart(fig, width='stretch')


# ==================== 页面3: 原始数据 ====================

elif page == "📄 原始数据":
    st.markdown('<div class="section-header">📄 原始数据</div>', unsafe_allow_html=True)

    if not data_ready:
        st.warning("⚠️ 请先在'数据管理'页面加载数据")
    else:
        st.markdown(f"### 📊 全部数据（共 {len(st.session_state.all_data)} 条记录）")

        # 筛选选项
        col1, col2 = st.columns(2)

        with col1:
            # 获取所有周期并排序
            all_periods = sort_periods(st.session_state.all_data['period'].unique().tolist())
            period_filter = st.multiselect(
                "选择周期",
                all_periods,
                default=all_periods
            )

        with col2:
            search_user = st.text_input("搜索用户", placeholder="输入用户名（留空显示全部）")

        # 应用筛选
        filtered_data = st.session_state.all_data[
            st.session_state.all_data['period'].isin(period_filter)
        ].copy()

        if search_user:
            filtered_data = filtered_data[
                filtered_data['user_name'].str.contains(search_user, case=False, na=False)
            ]

        st.info(f"📊 筛选后: {len(filtered_data)} 条记录")

        # 准备显示的数据 - 重新排列列顺序，确保周期在前面，详情在最后
        display_columns = ['user_name', 'period', '日人均线上会议数-即时+日程', '日人均线上会议时长(分钟)-即时+日程',
                          '即时会议', '日程会议', '即时+日程会议', '1v1通话数']

        # 只保留存在的列
        display_columns = [col for col in display_columns if col in filtered_data.columns]

        # 添加其他列
        other_columns = [col for col in filtered_data.columns if col not in display_columns and col != 'period_type']
        display_data = filtered_data[display_columns + other_columns]

        # 显示数据表
        st.dataframe(
            display_data,
            use_container_width=True,
            height=600
        )

        # 详情按钮说明
        st.markdown("---")
        st.markdown("### 👤 查看用户详情")

        # 用户选择器
        col1, col2 = st.columns([3, 1])
        with col1:
            selected_user = st.selectbox(
                "选择用户查看详细信息",
                options=[''] + sorted(filtered_data['user_name'].unique().tolist()),
                format_func=lambda x: '请选择用户...' if x == '' else x
            )

        with col2:
            st.markdown("<br>", unsafe_allow_html=True)
            if st.button("📊 查看详情", disabled=(selected_user == '')):
                st.session_state.selected_detail_user = selected_user
                st.rerun()

        # 如果已选择用户，显示详情
        if selected_user and selected_user != '':
            st.markdown(f"#### 📋 {selected_user} 的会议数据")

            user_data = st.session_state.all_data[
                st.session_state.all_data['user_name'] == selected_user
            ].copy()

            # 按周期排序
            user_data['period'] = pd.Categorical(
                user_data['period'],
                categories=sort_periods(user_data['period'].tolist()),
                ordered=True
            )
            user_data = user_data.sort_values('period')

            # 统计卡片
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("总周期数", len(user_data))

            with col2:
                avg_meetings = user_data['日人均线上会议数-即时+日程'].mean()
                st.metric("平均日均会议数", f"{avg_meetings:.2f}")

            with col3:
                avg_duration = user_data['日人均线上会议时长(分钟)-即时+日程'].mean()
                st.metric("平均日均时长", f"{avg_duration:.1f}分钟")

            with col4:
                total_meetings = user_data['即时+日程会议'].sum()
                st.metric("总会议数", int(total_meetings))

            # 趋势图
            st.markdown("##### 📈 会议数趋势")
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=user_data['period'],
                y=user_data['日人均线上会议数-即时+日程'],
                mode='lines+markers',
                name='日人均会议数',
                line=dict(color='#667eea', width=2),
                marker=dict(size=8)
            ))
            fig.update_layout(
                xaxis_title="周期",
                yaxis_title="日人均会议数",
                height=300,
                showlegend=False
            )
            st.plotly_chart(fig, width='stretch')

            # 详细数据表
            st.markdown("##### 📊 详细数据")
            st.dataframe(user_data[display_columns], use_container_width=True)

        # 下载按钮
        st.markdown("---")
        csv = filtered_data.to_csv(index=False, encoding='utf-8-sig')
        st.download_button(
            label="📥 下载筛选数据（CSV）",
            data=csv,
            file_name="filtered_meeting_data.csv",
            mime="text/csv"
        )


# ==================== 页面4: 分析结果 ====================

elif page == "📈 分析结果":
    st.markdown('<div class="section-header">📈 深度分析结果</div>', unsafe_allow_html=True)

    if not data_ready:
        st.warning("⚠️ 请先在'数据管理'页面加载数据")
    else:
        # 检查当前期数据是否存在
        if st.session_state.current_data is None or st.session_state.current_data.empty:
            st.warning("⚠️ 当前期数据为空，请在'数据管理'页面选择当前期数据")
        else:
            # Top10用户
            st.markdown("### 🏆 Top10 高频会议用户")
            top10_data = get_top_users(st.session_state.current_data, 10)

            if not top10_data.empty:
                fig = px.bar(
                    top10_data,
                    x='user_name',
                    y='日人均线上会议数-即时+日程',
                    title="Top10 用户日均会议数",
                    labels={'日人均线上会议数-即时+日程': '日均会议数', 'user_name': '用户'},
                    color='日人均线上会议数-即时+日程',
                    color_continuous_scale='Reds'
                )
                fig.update_layout(height=400)
                st.plotly_chart(fig, width='stretch')

                # 显示表格
                st.dataframe(top10_data, use_container_width=True)
            else:
                st.info("ℹ️ 当前期数据中没有足够的用户数据")

            # 用户分层
            st.markdown("---")
            st.markdown("### 📊 用户分层统计")

            tiers = tier_users(st.session_state.current_data)

            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "🔴 高频用户（≥5次/天）",
                    f"{tiers['high']['count']} 人",
                    f"平均 {tiers['high']['avg']:.2f} 次/天"
                )

            with col2:
                st.metric(
                    "🟡 中频用户（2-5次/天）",
                    f"{tiers['medium']['count']} 人",
                    f"平均 {tiers['medium']['avg']:.2f} 次/天"
                )

            with col3:
                st.metric(
                    "🟢 低频用户（<2次/天）",
                    f"{tiers['low']['count']} 人",
                    f"平均 {tiers['low']['avg']:.2f} 次/天"
                )

            # 主责人员统计
            st.markdown("---")
            st.markdown("### 👔 主责人员统计")

            config = load_config()
            responsible_persons = config.get('responsible_persons', [])

            if not responsible_persons:
                st.info("ℹ️ 暂未配置主责人员，请在'配置'页面添加")
            else:
                rp_names = [p['name'] for p in responsible_persons]
                rp_data = st.session_state.current_data[
                    st.session_state.current_data['user_name'].isin(rp_names)
                ]

                if not rp_data.empty:
                    rp_stats = rp_data.groupby('user_name').agg({
                        '日人均线上会议数-即时+日程': 'mean',
                        '日人均线上会议时长(分钟)-即时+日程': 'mean'
                    }).reset_index()

                    st.dataframe(
                        rp_stats.style.format({
                            '日人均线上会议数-即时+日程': '{:.2f}',
                            '日人均线上会议时长(分钟)-即时+日程': '{:.1f}'
                        }),
                        use_container_width=True
                    )
                else:
                    st.warning("⚠️ 在当前期数据中未找到主责人员的记录")


# ==================== 页面5: 人员详情 ====================

elif page == "👥 人员详情":
    st.markdown('<div class="section-header">👥 人员详细分析</div>', unsafe_allow_html=True)

    if not data_ready:
        st.warning("⚠️ 请先在'数据管理'页面加载数据")
    else:
        # 用户选择
        users = get_users_from_data(st.session_state.all_data)
        selected_user = st.selectbox("选择用户", users)

        if selected_user:
            user_data = st.session_state.all_data[
                st.session_state.all_data['user_name'] == selected_user
            ]

            st.markdown(f"### 📊 {selected_user} 的详细数据")

            # 统计卡片
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                total_periods = len(user_data)
                st.metric("数据周期数", total_periods)

            with col2:
                avg_meetings = user_data['日人均线上会议数-即时+日程'].mean()
                st.metric("平均会议数/天", f"{avg_meetings:.2f}")

            with col3:
                avg_duration = user_data['日人均线上会议时长(分钟)-即时+日程'].mean()
                st.metric("平均时长/天", f"{avg_duration:.1f}分")

            with col4:
                instant_ratio = (user_data['即时会议'].sum() / user_data['即时+日程会议'].sum() * 100) if user_data['即时+日程会议'].sum() > 0 else 0
                st.metric("即时会议占比", f"{instant_ratio:.1f}%")

            # 趋势图
            st.markdown("---")
            st.markdown("### 📈 历史趋势")

            # 对周期排序
            user_data_sorted = user_data.copy()
            user_data_sorted['period'] = pd.Categorical(
                user_data_sorted['period'],
                categories=sort_periods(user_data_sorted['period'].tolist()),
                ordered=True
            )
            user_data_sorted = user_data_sorted.sort_values('period')

            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=user_data_sorted['period'],
                y=user_data_sorted['日人均线上会议数-即时+日程'],
                mode='lines+markers',
                name='会议数',
                line=dict(color='#667eea', width=2)
            ))

            fig.update_layout(
                title=f"{selected_user} 的会议数趋势",
                xaxis_title="周期",
                yaxis_title="日均会议数",
                height=400
            )

            st.plotly_chart(fig, width='stretch')

            # 详细数据表
            st.markdown("---")
            st.markdown("### 📄 详细数据")
            st.dataframe(user_data_sorted, use_container_width=True)


# ==================== 页面6: 配置 ====================

elif page == "⚙️ 配置":
    st.markdown('<div class="section-header">⚙️ 系统配置</div>', unsafe_allow_html=True)

    # 主责人员配置
    st.markdown("### 👔 主责人员配置")

    config = load_config()
    responsible_persons = config.get('responsible_persons', [])

    # 显示已配置人员
    if responsible_persons:
        st.success(f"✅ 当前已配置 {len(responsible_persons)} 名主责人员")

        # 显示列表
        for idx, person in enumerate(responsible_persons):
            col1, col2, col3 = st.columns([2, 3, 1])
            with col1:
                st.text(f"👤 {person['name']}")
            with col2:
                st.text(person.get('note', '-'))
            with col3:
                if st.button("🗑️", key=f"del_rp_{idx}"):
                    responsible_persons.pop(idx)
                    config['responsible_persons'] = responsible_persons
                    save_config(config)
                    st.rerun()
    else:
        st.info("ℹ️ 暂未配置主责人员")

    # 添加新人员
    st.markdown("---")
    st.markdown("#### ➕ 添加主责人员")

    # 获取用户列表
    if data_ready:
        users = get_users_from_data(st.session_state.all_data)
    else:
        users = []

    if users:
        selected_names = st.multiselect(
            "选择主责人员（可多选）",
            users,
            help="从数据中选择主责人员"
        )

        note = st.text_area(
            "备注（可选）",
            placeholder="例如：项目核心负责人",
            height=80
        )

        if st.button("➕ 添加", type="primary"):
            if selected_names:
                added = 0
                for name in selected_names:
                    if not any(p['name'] == name for p in responsible_persons):
                        responsible_persons.append({
                            'name': name,
                            'note': note if note else '主责人员'
                        })
                        added += 1

                if added > 0:
                    config['responsible_persons'] = responsible_persons
                    save_config(config)
                    st.success(f"✅ 成功添加 {added} 名主责人员")
                    st.rerun()
                else:
                    st.warning("⚠️ 所有选择的人员已存在")
            else:
                st.error("❌ 请至少选择一个人员")
    else:
        st.warning("⚠️ 请先在'数据管理'页面加载数据，以便选择主责人员")
