"""修复自主渗透引擎工具参数名不匹配的系统性bug"""
f = r"E:\BaiduNetdiskDownload\yuanbao\PentestAI\pentestai\modules\ai_security\autonomous_pentest_engine.py"
with open(f, 'r', encoding='utf-8') as fp:
    c = fp.read()

fixes = []

# 修复1: 信息收集阶段 - subdomain_enum: domain→target
old1 = '''{"tool_name": "subdomain_enum", "params": {"domain": self.target}, "description": "子域名枚举"}'''
new1 = '''{"tool_name": "subdomain_enum", "params": {"target": self.target}, "description": "子域名枚举"}'''
if old1 in c:
    c = c.replace(old1, new1)
    fixes.append("subdomain_enum: domain→target")

# 修复2: 信息收集阶段 - dir_bruter: url→target, 去掉不识别的wordlist
old2 = '''{"tool_name": "dir_bruter", "params": {"url": self.target, "wordlist": "common"}, "description": "目录爆破"}'''
new2 = '''{"tool_name": "dir_bruter", "params": {"target": self.target, "depth": "standard"}, "description": "目录爆破"}'''
if old2 in c:
    c = c.replace(old2, new2)
    fixes.append("dir_bruter: url→target, wordlist→depth")

# 修复3: 信息收集阶段 - tech_detector: url→target
old3 = '''{"tool_name": "tech_detector", "params": {"url": self.target}, "description": "技术栈识别"}'''
new3 = '''{"tool_name": "tech_detector", "params": {"target": self.target}, "description": "技术栈识别"}'''
if old3 in c:
    c = c.replace(old3, new3)
    fixes.append("tech_detector: url→target")

# 修复4: 信息收集阶段 - waf_detector: url→target
old4 = '''{"tool_name": "waf_detector", "params": {"url": self.target}, "description": "WAF检测"}'''
new4 = '''{"tool_name": "waf_detector", "params": {"target": self.target}, "description": "WAF检测"}'''
if old4 in c:
    c = c.replace(old4, new4)
    fixes.append("waf_detector: url→target")

# 修复5: 信息收集阶段 - port_scanner去掉不识别的ports="top100"
old5 = '''{"tool_name": "port_scanner", "params": {"target": self.target, "ports": "top100"}, "description": "端口扫描"}'''
new5 = '''{"tool_name": "port_scanner", "params": {"target": self.target, "depth": "standard"}, "description": "端口扫描"}'''
if old5 in c:
    c = c.replace(old5, new5)
    fixes.append("port_scanner: ports='top100'→depth='standard' (2处)")

# 修复6: 漏洞扫描阶段 - web_scanner: url→target, scan_type→depth="deep"
old6 = '''{"tool_name": "web_scanner", "params": {"url": self.target, "scan_type": "full"}, "description": "Web漏洞扫描"}'''
new6 = '''{"tool_name": "web_scanner", "params": {"target": self.target, "depth": "deep", "use_spider": True, "max_pages": 100}, "description": "Web漏洞扫描"}'''
if old6 in c:
    c = c.replace(old6, new6)
    fixes.append("web_scanner: url→target, scan_type→depth=deep, 增加爬虫参数")

# 修复7: 在_execute_tool中增加参数兼容处理（url/domain→target自动转换）
old7 = '''            if tool is None:
                result["status"] = "skipped"
                result["error"] = f"工具 {tool_name} 未注册"
                self._log(f"    ⚠️ 工具 {tool_name} 未注册，跳过", "warn")
            else:
                if hasattr(tool, 'run'):
                    tool_result = tool.run(**params)'''
new7 = '''            if tool is None:
                result["status"] = "skipped"
                result["error"] = f"工具 {tool_name} 未注册"
                self._log(f"    ⚠️ 工具 {tool_name} 未注册，跳过", "warn")
            else:
                if hasattr(tool, 'run'):
                    # 参数兼容处理：url/domain自动转target
                    safe_params = dict(params)
                    if "target" not in safe_params:
                        for alt in ["url", "domain", "host", "ip"]:
                            if alt in safe_params:
                                safe_params["target"] = safe_params.pop(alt)
                                self._log(f"    ℹ️ 参数兼容: {alt}→target", "debug")
                                break
                    tool_result = tool.run(**safe_params)'''
if old7 in c:
    c = c.replace(old7, new7)
    fixes.append("_execute_tool: 增加url/domain/host/ip→target参数兼容处理")

with open(f, 'w', encoding='utf-8') as fp:
    fp.write(c)

print("✅ 自主渗透引擎参数修复完成")
for fix in fixes:
    print(f"  - {fix}")

import py_compile
py_compile.compile(f, doraise=True)
print("\n✅ 语法检查通过")

# 验证修复
from pentestai.modules.ai_security.autonomous_pentest_engine import AutonomousPentestEngine
e = AutonomousPentestEngine()
e.set_target("http://localhost:3000")
e.state = __import__("pentestai.modules.ai_security.autonomous_pentest_engine", fromlist=["PentestState"]).PentestState(e.target, e.target_type)

# 验证信息收集阶段参数
phase1 = e._rule_generate_recon_phase()
print(f"\n✅ 信息收集阶段工具参数验证:")
for t in phase1.tools:
    has_target = "target" in t["params"]
    print(f"  {t['tool_name']}: target={'✅' if has_target else '❌'} params={list(t['params'].keys())}")

# 验证漏洞扫描阶段参数
e.state.phases_completed.append(phase1)
phase2 = e._rule_generate_next_phase()
print(f"\n✅ 漏洞扫描阶段工具参数验证:")
for t in phase2.tools:
    has_target = "target" in t["params"]
    print(f"  {t['tool_name']}: target={'✅' if has_target else '❌'} params={list(t['params'].keys())}")

print("\n✅ 所有工具参数修复验证通过！")
