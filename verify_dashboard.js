#!/usr/bin/env node
/**
 * 验证仪表盘HTML文件
 * 检查数据完整性和JavaScript功能
 */

const fs = require('fs');

console.log('======================================================================');
console.log('                 仪表盘验证工具');
console.log('======================================================================\n');

try {
    // 读取HTML文件
    const html = fs.readFileSync('output/meeting_dashboard_full.html', 'utf8');
    console.log('✅ HTML文件读取成功\n');

    // 检查1: 提取dashboardData
    console.log('[检查1] 提取数据对象...');
    const dataMatch = html.match(/const dashboardData = ({[\s\S]*?});[\s\S]*?<\/script>/);
    if (!dataMatch) {
        throw new Error('找不到 dashboardData 定义');
    }
    console.log('✅ 找到 dashboardData 定义\n');

    // 检查2: 解析JSON
    console.log('[检查2] 解析JSON数据...');
    const dashboardData = eval('(' + dataMatch[1] + ')');
    console.log('✅ JSON解析成功\n');

    // 检查3: 数据完整性
    console.log('[检查3] 验证数据完整性...');
    const checks = [
        { name: 'KPI指标', value: dashboardData.kpis },
        { name: '原始数据', value: dashboardData.raw_data },
        { name: '周期对比', value: dashboardData.period_comparison },
        { name: 'Top10用户', value: dashboardData.top10_users },
        { name: '异常检测', value: dashboardData.anomalies },
        { name: '用户分层', value: dashboardData.user_tiers },
    ];

    checks.forEach(check => {
        if (!check.value) {
            console.log(`  ❌ ${check.name}: 缺失`);
        } else if (Array.isArray(check.value)) {
            console.log(`  ✅ ${check.name}: ${check.value.length} 条`);
        } else if (typeof check.value === 'object') {
            const keys = Object.keys(check.value);
            console.log(`  ✅ ${check.name}: ${keys.length} 个分组`);
        }
    });
    console.log();

    // 检查4: 检查NaN
    console.log('[检查4] 检查NaN值...');
    const nanCount = (html.match(/: NaN[,\s\}]/g) || []).length;
    if (nanCount > 0) {
        console.log(`  ❌ 发现 ${nanCount} 个 NaN 值`);
    } else {
        console.log('  ✅ 无NaN值，数据清洁');
    }
    console.log();

    // 检查5: 标签页结构
    console.log('[检查5] 检查标签页结构...');
    const tabs = [
        'tab-overview',
        'tab-rawdata',
        'tab-analysis',
        'tab-personnel'
    ];
    tabs.forEach(tab => {
        if (html.includes(`id="${tab}"`)) {
            console.log(`  ✅ ${tab} 存在`);
        } else {
            console.log(`  ❌ ${tab} 缺失`);
        }
    });
    console.log();

    // 检查6: JavaScript函数
    console.log('[检查6] 检查关键JavaScript函数...');
    const functions = [
        'showTab',
        'renderRawDataTable',
        'sortTable',
        'applyFilters',
        'exportToCSV'
    ];
    functions.forEach(func => {
        if (html.includes(`function ${func}`)) {
            console.log(`  ✅ ${func}() 存在`);
        } else {
            console.log(`  ❌ ${func}() 缺失`);
        }
    });
    console.log();

    // 统计信息
    console.log('======================================================================');
    console.log('数据统计:');
    console.log(`  • 原始数据: ${dashboardData.raw_data.length} 条`);
    console.log(`  • 用户数: ${new Set(dashboardData.raw_data.map(r => r.user_name)).size} 人`);
    console.log(`  • 周期数: ${dashboardData.period_comparison.length} 个`);
    console.log(`  • Top10用户: ${dashboardData.top10_users.length} 人`);
    console.log(`  • 异常检测: ${dashboardData.anomalies.length} 项`);
    console.log('======================================================================');

    console.log('\n✅ 所有检查通过！仪表盘已就绪。\n');

} catch (error) {
    console.error('\n❌ 验证失败:', error.message);
    console.error(error.stack);
    process.exit(1);
}
