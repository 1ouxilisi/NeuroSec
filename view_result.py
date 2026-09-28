import json
with open(r'E:\BaiduNetdiskDownload\yuanbao\PentestAI\真实靶场测试结果_JuiceShop.json', 'r', encoding='utf-8') as f:
    r = json.load(f)
print('=== 发现统计 ===')
print('总计: %s, 高危:%s, 中危:%s, 低危:%s, 信息:%s' % (
    r.get('findings_total'), r.get('findings_high'), r.get('findings_medium'),
    r.get('findings_low'), r.get('findings_info')))
print()
print('=== 所有发现 ===')
for i, f in enumerate(r.get('findings', [])):
    print('%d. [%s] %s' % (i+1, f.get('risk'), f.get('name')))
    print('   描述: %s' % f.get('description','')[:80])
    print('   工具: %s, 位置: %s' % (f.get('tool'), f.get('location')))
    if f.get('evidence'):
        print('   证据: %s' % str(f.get('evidence',''))[:100])
    print()
