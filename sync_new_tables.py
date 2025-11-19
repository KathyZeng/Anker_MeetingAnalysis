#!/usr/bin/env python3
"""
飞书多维表格增量同步脚本
自动检测并同步新增的表格,避免重复处理
"""

import json
import os
from datetime import datetime

# 配置文件路径
CONFIG_FILE = "input/.processed_tables.json"
WIKI_URL = "https://anker-in.feishu.cn/wiki/FybQw1XSzi3AWgk2ps1cQUJPnVg"

def load_config():
    """加载配置文件"""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    return {
        "last_sync_time": None,
        "processed_tables": [],
        "source_info": {
            "app_token": "Hioab1CEpa3R8SszroPcMkYin4c",
            "wiki_url": WIKI_URL
        }
    }

def save_config(config):
    """保存配置文件"""
    config["last_sync_time"] = datetime.now().isoformat()
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f, ensure_ascii=False, indent=2)

def get_new_tables(all_tables, processed_tables):
    """
    识别新增的表格

    Args:
        all_tables: 所有表格列表
        processed_tables: 已处理的表格列表

    Returns:
        新增表格列表
    """
    processed_set = set(processed_tables)
    new_tables = [table for table in all_tables if table not in processed_set]
    return new_tables

def validate_table_name(table_name):
    """
    验证表格名称格式
    支持的格式:
    - "X月会议详情" (如: 9月会议详情, 10月会议详情)
    - "MM.DD-MM.DD会议详情" (如: 10.20-10.26会议详情)

    Returns:
        bool: 是否符合格式
    """
    import re

    # 格式1: X月会议详情
    pattern1 = r'^\d{1,2}月会议详情$'

    # 格式2: MM.DD-MM.DD会议详情
    pattern2 = r'^\d{1,2}\.\d{1,2}-\d{1,2}\.\d{1,2}会议详情$'

    return bool(re.match(pattern1, table_name) or re.match(pattern2, table_name))

def main():
    """主函数 - 这是一个示例,实际使用时需要通过Claude Code调用飞书API"""

    print("=" * 60)
    print("飞书多维表格增量同步工具")
    print("=" * 60)

    # 加载配置
    config = load_config()
    print(f"\n📋 已处理的表格数量: {len(config['processed_tables'])}")
    print(f"⏰ 上次同步时间: {config.get('last_sync_time', '从未同步')}")

    print("\n" + "=" * 60)
    print("使用说明:")
    print("=" * 60)
    print("""
1. 本脚本用于追踪已处理的表格,避免重复读取
2. 表格名称格式要求:
   - 格式1: "X月会议详情" (如: 11月会议详情, 12月会议详情)
   - 格式2: "MM.DD-MM.DD会议详情" (如: 11.17-11.23会议详情)

3. 使用方法:
   方法A (推荐): 直接告诉Claude Code
   -----------------------------------------------
   "请同步飞书表格中的新增数据表到/input目录"

   方法B: 手动指定
   -----------------------------------------------
   "请读取飞书表格,只处理这些新表格:[表格名1, 表格名2]"

4. Claude Code会:
   ✓ 自动读取飞书表格列表
   ✓ 对比 .processed_tables.json 找出新表格
   ✓ 只处理新表格并保存到 /input/
   ✓ 更新配置文件记录已处理表格
    """)

    print("\n当前已处理的表格:")
    print("-" * 60)
    for i, table in enumerate(config['processed_tables'], 1):
        print(f"  {i}. {table}")

    print("\n" + "=" * 60)
    print("准备就绪!等待Claude Code处理新增表格...")
    print("=" * 60)

if __name__ == "__main__":
    main()
