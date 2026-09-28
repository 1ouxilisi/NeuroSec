import json
with open('统一端到端测试报告.json', 'r', encoding='utf-8') as f:
    report = json.load(f)
print('失败项:')
for r in report['详细结果']:
    if not r['passed']:
        print(f"  - {r['name']}: {r['detail']}")
print()
print('全部结果:')
for r in report['详细结果']:
    s = '✅' if r['passed'] else '❌'
    print(f"  {s} {r['name']}: {r['detail']}")
