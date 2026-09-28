"""修复结果解析器的3个问题"""
f = r"E:\BaiduNetdiskDownload\yuanbao\PentestAI\pentestai\modules\ai_security\result_parser.py"
with open(f, 'r', encoding='utf-8') as fp:
    c = fp.read()

fixes = []

# 修复1: 端口扫描解析器 - 支持port_scanner的实际输出格式
old_port = '''    @staticmethod
    def _parse_port_scanner(output, params):
        findings = []
        target = params.get("target", "未知")
        # 匹配开放端口: 80/tcp open http
        port_pattern = r'(\\d+)/tcp\\s+open\\s+(\\S+)'
        matches = re.findall(port_pattern, output)
        for port, service in matches:
            risk = "信息"
            desc = f"端口 {port}/{service} 开放"
            if service in ["ssh", "telnet", "ftp", "smb", "rdp", "mysql", "redis", "mongodb"]:
                risk = "低危"
                desc = f"端口 {port}/{service} 开放，可能存在弱口令风险"
            findings.append(Finding(
                name=f"开放端口: {port}/{service}", risk=risk,
                description=desc, location=f"{target}:{port}",
                tool="port_scanner", category="network"
            ))
        if not findings:
            findings.append(Finding(
                name="端口扫描完成", risk="信息",
                description="未发现明显开放端口或输出格式未识别",
                location=target, tool="port_scanner", category="network"
            ))
        return findings'''

new_port = '''    @staticmethod
    def _parse_port_scanner(output, params):
        findings = []
        target = params.get("target", "未知")
        # 格式1: nmap格式 "80/tcp open http"
        port_pattern1 = r'(\\d+)/tcp\\s+open\\s+(\\S+)'
        matches1 = re.findall(port_pattern1, output)
        # 格式2: port_scanner格式 "   3000  Node.js  banner..."
        port_pattern2 = r'^\\s*(\\d{2,5})\\s+([A-Za-z0-9._-]{2,30})'
        matches2 = re.findall(port_pattern2, output, re.MULTILINE)

        seen_ports = set()
        for port, service in matches1:
            if port in seen_ports:
                continue
            seen_ports.add(port)
            risk = "信息"
            desc = f"端口 {port}/{service} 开放"
            if service.lower() in ["ssh", "telnet", "ftp", "smb", "rdp", "mysql", "redis", "mongodb", "mssql", "postgresql"]:
                risk = "低危"
                desc = f"端口 {port}/{service} 开放，可能存在弱口令风险"
            findings.append(Finding(
                name=f"开放端口: {port}/{service}", risk=risk,
                description=desc, location=f"{target}:{port}",
                tool="port_scanner", category="network"
            ))
        for port, service in matches2:
            if port in seen_ports:
                continue
            # 跳过明显不是端口的行（如包含"扫描完成"的行）
            if any(kw in service.lower() for kw in ["扫描", "完成", "开放端口", "total"]):
                continue
            seen_ports.add(port)
            risk = "信息"
            desc = f"端口 {port}/{service} 开放"
            if service.lower() in ["ssh", "telnet", "ftp", "smb", "rdp", "mysql", "redis", "mongodb", "mssql", "postgresql"]:
                risk = "低危"
                desc = f"端口 {port}/{service} 开放，可能存在弱口令风险"
            findings.append(Finding(
                name=f"开放端口: {port}/{service}", risk=risk,
                description=desc, location=f"{target}:{port}",
                tool="port_scanner", category="network"
            ))
        if not findings:
            findings.append(Finding(
                name="端口扫描完成", risk="信息",
                description="未发现明显开放端口",
                location=target, tool="port_scanner", category="network"
            ))
        return findings'''

if old_port in c:
    c = c.replace(old_port, new_port)
    fixes.append("端口扫描解析器: 支持port_scanner实际输出格式(3000  Node.js)")
else:
    print("⚠️ 未找到端口扫描解析器代码段")

# 修复2: 弱口令解析器 - 检查"发现弱口令: 0"的情况
old_weak = '''        found_success = False
        for kw in success_keywords:
            if kw.lower() in output.lower():
                idx = output.lower().find(kw.lower())
                context = output[max(0,idx-30):idx+80].replace('\\n',' ')
                findings.append(Finding(
                    name=f"弱口令爆破成功: {kw}", risk="高危",
                    description=f"弱口令/默认密码爆破成功: {kw}",
                    evidence=context, location=target, tool="weak_password", category="web"
                ))
                found_success = True'''
new_weak = '''        found_success = False
        for kw in success_keywords:
            if kw.lower() in output.lower():
                idx = output.lower().find(kw.lower())
                context = output[max(0,idx-30):idx+80].replace('\\n',' ')
                # 检查是否是"发现弱口令: 0"这种情况（0个不算成功）
                after_kw = output[idx+len(kw):idx+len(kw)+20]
                if re.search(r'[:：]\\s*0\\b', after_kw):
                    continue
                findings.append(Finding(
                    name=f"弱口令爆破成功: {kw}", risk="高危",
                    description=f"弱口令/默认密码爆破成功: {kw}",
                    evidence=context, location=target, tool="weak_password", category="web"
                ))
                found_success = True'''
if old_weak in c:
    c = c.replace(old_weak, new_weak)
    fixes.append("弱口令解析器: 排除'发现弱口令: 0'的误报")
else:
    print("⚠️ 未找到弱口令解析器代码段")

# 修复3: Web扫描解析器 - 去重（xss和XSS是同一个问题）
old_web = '''        for keyword, risk in vuln_keywords.items():
            if keyword.lower() in output.lower():
                # 提取相关上下文
                idx = output.lower().find(keyword.lower())
                context = output[max(0, idx-50):idx+100].replace('\\n', ' ')
                findings.append(Finding(
                    name=f"Web漏洞: {keyword}", risk=risk,
                    description=f"检测到{keyword}漏洞", evidence=context,
                    location=target, tool="web_scanner", category="web"
                ))'''
new_web = '''        seen_vulns = set()
        for keyword, risk in vuln_keywords.items():
            kw_lower = keyword.lower()
            if kw_lower in output.lower():
                # 去重：xss和XSS是同一个问题，统一用小写
                if kw_lower in seen_vulns:
                    continue
                seen_vulns.add(kw_lower)
                # 提取相关上下文
                idx = output.lower().find(kw_lower)
                context = output[max(0, idx-50):idx+100].replace('\\n', ' ')
                findings.append(Finding(
                    name=f"Web漏洞: {keyword}", risk=risk,
                    description=f"检测到{keyword}漏洞", evidence=context,
                    location=target, tool="web_scanner", category="web"
                ))'''
if old_web in c:
    c = c.replace(old_web, new_web)
    fixes.append("Web扫描解析器: 去重(xss/XSS统一)")
else:
    print("⚠️ 未找到Web扫描解析器代码段")

with open(f, 'w', encoding='utf-8') as fp:
    fp.write(c)

print("✅ 结果解析器修复完成")
for fix in fixes:
    print(f"  - {fix}")

import py_compile
py_compile.compile(f, doraise=True)
print("\n✅ 语法检查通过")

# 验证修复
from pentestai.modules.ai_security.result_parser import ResultParser

# 测试端口扫描解析（port_scanner实际格式）
port_output = """扫描完成: 127.0.0.1, 开放端口 3/43
    135  MSRPC
   3000  Node.js
   8443  HTTPS-Alt            HTTP/1.0 400 Bad Request"""
r1 = ResultParser.parse("port_scanner", port_output, {"target": "127.0.0.1"})
print(f"\n✅ 端口扫描解析: 发现{len(r1)}个开放端口")
for f in r1:
    print(f"  - [{f.risk}] {f.name}")
assert len(r1) == 3, "应该发现3个开放端口"
assert any("3000" in f.name for f in r1), "应该包含3000端口"

# 测试弱口令"0个"不误报
weak_output = """弱口令爆破: postgresql://localhost:5432
  尝试次数: 500
  发现弱口令: 0 个"""
r2 = ResultParser.parse("weak_password", weak_output, {"target": "test"})
print(f"\n✅ 弱口令解析(0个): {r2[0].risk} - {r2[0].name}")
assert r2[0].risk == "信息", "0个弱口令不应报高危"

# 测试弱口令真的成功
weak_success = """弱口令爆破: postgresql://localhost:5432
  尝试次数: 500
  登录成功: admin/admin123"""
r3 = ResultParser.parse("weak_password", weak_success, {"target": "test"})
print(f"✅ 弱口令解析(成功): {r3[0].risk} - {r3[0].name}")
assert r3[0].risk == "高危", "登录成功应报高危"

# 测试Web扫描去重
web_output = "检测到xss漏洞\n检测到XSS漏洞\n检测到SQL注入"
r4 = ResultParser.parse("web_scanner", web_output, {"url": "test"})
print(f"\n✅ Web扫描解析(去重): 发现{len(r4)}个漏洞")
for f in r4:
    print(f"  - [{f.risk}] {f.name}")
xss_count = sum(1 for f in r4 if "xss" in f.name.lower())
assert xss_count == 1, "XSS应该只报1次（去重）"

print("\n🎉 所有解析器修复验证通过！")
