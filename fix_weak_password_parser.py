"""修复弱口令解析器误报问题"""
f = r"E:\BaiduNetdiskDownload\yuanbao\PentestAI\pentestai\modules\ai_security\result_parser.py"
with open(f, 'r', encoding='utf-8') as fp:
    c = fp.read()

old = '''    def _parse_weak_password(output, params):
        findings = []
        target = params.get("target", "未知")
        weak_keywords = ["weak password", "弱口令", "brute force", "login success", "登录成功", "default password", "默认密码"]
        found = False
        for kw in weak_keywords:
            if kw.lower() in output.lower():
                findings.append(Finding(
                    name=f"弱口令: {kw}", risk="高危",
                    description=f"检测到弱口令/默认密码: {kw}",
                    location=target, tool="weak_password", category="web"
                ))
                found = True
        if not found:
            findings.append(Finding(
                name="弱口令检测完成", risk="信息", description="未检测到弱口令",
                location=target, tool="weak_password", category="web"
            ))
        return findings'''

new = '''    def _parse_weak_password(output, params):
        findings = []
        target = params.get("target", "未知")
        # 只有明确表示爆破成功/登录成功才报高危
        success_keywords = ["login success", "登录成功", "brute force success", "爆破成功",
                            "found weak password", "发现弱口令", "cracked", "破解成功",
                            "valid credentials", "有效凭证", "default password found", "发现默认密码"]
        # 工具描述性文字（只是在说正在做什么，不是结果）
        desc_keywords = ["weak password", "弱口令", "brute force", "爆破", "default password", "默认密码",
                         "password audit", "口令审计", "testing", "测试中"]
        found_success = False
        for kw in success_keywords:
            if kw.lower() in output.lower():
                idx = output.lower().find(kw.lower())
                context = output[max(0,idx-30):idx+80].replace('\\n',' ')
                findings.append(Finding(
                    name=f"弱口令爆破成功: {kw}", risk="高危",
                    description=f"弱口令/默认密码爆破成功: {kw}",
                    evidence=context, location=target, tool="weak_password", category="web"
                ))
                found_success = True
        if not found_success:
            is_desc = any(kw.lower() in output.lower() for kw in desc_keywords)
            if is_desc:
                findings.append(Finding(
                    name="弱口令检测完成", risk="信息",
                    description="弱口令检测已执行，未发现明确的弱口令爆破成功结果",
                    location=target, tool="weak_password", category="web"
                ))
            else:
                findings.append(Finding(
                    name="弱口令检测完成", risk="信息", description="未检测到弱口令",
                    location=target, tool="weak_password", category="web"
                ))
        return findings'''

if old in c:
    c = c.replace(old, new)
    with open(f, 'w', encoding='utf-8') as fp:
        fp.write(c)
    print("✅ 弱口令解析器修复完成")
else:
    print("❌ 未找到目标代码段")

import py_compile
py_compile.compile(f, doraise=True)
print("✅ 语法检查通过")

# 验证修复效果
from pentestai.modules.ai_security.result_parser import ResultParser
# 测试1：工具描述性文字（不应报高危）
r1 = ResultParser.parse("weak_password", "弱口令爆破: postgresql://localhost:5432, 用户: 10, 密码: 50", {"target": "test"})
print(f"\n测试1（描述性文字）: {r1[0].risk} - {r1[0].name}")
assert r1[0].risk == "信息", "描述性文字不应报高危"

# 测试2：明确爆破成功（应报高危）
r2 = ResultParser.parse("weak_password", "登录成功: admin/admin123", {"target": "test"})
print(f"测试2（爆破成功）: {r2[0].risk} - {r2[0].name}")
assert r2[0].risk == "高危", "爆破成功应报高危"

print("\n✅ 弱口令解析器修复验证通过！")
