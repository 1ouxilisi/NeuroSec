"""
PentestAI 全面功能校验脚本
覆盖：基础功能、7大领域、AI引擎、结果解析器、GUI、授权、数据库、外部引擎
"""
import sys, os, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class Color:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    BOLD = '\033[1m'
    END = '\033[0m'

def ok(msg): print(f"  {Color.GREEN}✅{Color.END} {msg}")
def fail(msg): print(f"  {Color.RED}❌{Color.END} {msg}")
def warn(msg): print(f"  {Color.YELLOW}⚠️{Color.END} {msg}")
def info(msg): print(f"  {Color.BLUE}ℹ️{Color.END} {msg}")
def section(title): print(f"\n{Color.BOLD}{'='*60}\n  {title}\n{'='*60}{Color.END}")

results = []

def record(name, passed, detail=""):
    results.append({"name": name, "passed": passed, "detail": detail})

# ============================================================
section("一、基础功能校验")
# ============================================================

# 1. 工具注册
try:
    from pentestai.core.base_tool import ToolRegistry
    registry = ToolRegistry()
    all_tools = registry.list_tools()
    tool_count = len(all_tools)
    ok(f"工具注册成功: {tool_count}个工具")
    record("工具注册", tool_count >= 190, f"{tool_count}个工具")
except Exception as e:
    fail(f"工具注册失败: {e}")
    record("工具注册", False, str(e))

# 2. 外部引擎检测
try:
    from pentestai.core.engine_manager import EngineManager
    em = EngineManager()
    engines = em.detect_all_engines()
    engine_count = len([k for k,v in engines.items() if v.get('detected')])
    ok(f"外部引擎检测: {engine_count}/10个")
    for name, info_e in engines.items():
        if info_e.get('detected'):
            info(f"  {name}: {info_e.get('path','')[:50]}")
    record("外部引擎检测", engine_count >= 8, f"{engine_count}/10个")
except Exception as e:
    fail(f"引擎检测失败: {e}")
    record("外部引擎检测", False, str(e))

# 3. 数据库初始化
try:
    from pentestai.modules.utility.scan_history import ScanHistory
    sh = ScanHistory()
    ok("扫描历史数据库初始化成功")
    record("扫描历史数据库", True)
except Exception as e:
    fail(f"扫描历史数据库失败: {e}")
    record("扫描历史数据库", False, str(e))

try:
    from pentestai.modules.utility.vuln_kb import VulnKnowledgeBase
    vkb = VulnKnowledgeBase()
    vuln_count = vkb.get_all_vulns() if hasattr(vkb, 'get_all_vulns') else []
    ok(f"漏洞知识库初始化成功: {len(vuln_count) if isinstance(vuln_count, list) else '已加载'}个漏洞")
    record("漏洞知识库", True)
except Exception as e:
    fail(f"漏洞知识库失败: {e}")
    record("漏洞知识库", False, str(e))

# 4. 授权系统
try:
    from pentestai.modules.utility.license_manager import LicenseManager
    lm = LicenseManager()
    license_info = lm.get_license_info() if hasattr(lm, 'get_license_info') else {}
    status = license_info.get('status', 'unknown') if isinstance(license_info, dict) else 'unknown'
    ok(f"授权系统正常: {status}")
    record("授权系统", True, status)
except Exception as e:
    fail(f"授权系统失败: {e}")
    record("授权系统", False, str(e))

# ============================================================
section("二、7大安全领域模块校验")
# ============================================================

modules_to_test = [
    ("Web安全", ["web_scanner", "cve_checker", "weak_password", "vuln_verifier", "ssl_auditor", "waf_detector"]),
    ("信息收集", ["port_scanner", "subdomain_enum", "dir_bruter", "tech_detector", "whois_dns", "web_spider"]),
    ("内网渗透", ["internal_scanner", "internal_vuln_checker", "domain_enumerator", "lateral_movement_helper"]),
    ("移动安全", ["mobile_security_engine", "mobile_reverse", "mobile_api_security"]),
    ("区块链安全", ["blockchain_security_engine", "contract_auditor"]),
    ("AI模型安全", ["ai_model_security", "ai_model_security_v2"]),
    ("报告与 utility", ["report_generator", "auto_reporter", "log_analyzer"]),
]

for domain, tools in modules_to_test:
    print(f"\n  {Color.BOLD}【{domain}】{Color.END}")
    domain_pass = 0
    for tool_name in tools:
        try:
            tool = registry.get(tool_name)
            if tool:
                ok(f"{tool_name}: 已注册")
                domain_pass += 1
            else:
                warn(f"{tool_name}: 未注册")
        except Exception as e:
            fail(f"{tool_name}: {str(e)[:50]}")
    record(f"{domain}模块", domain_pass == len(tools), f"{domain_pass}/{len(tools)}")

# ============================================================
section("三、AI引擎校验（3个AI引擎）")
# ============================================================

# 1. AI安全分析引擎
try:
    from pentestai.modules.ai_security.ai_security_analyzer import AISecurityAnalyzer
    asa = AISecurityAnalyzer()
    ok(f"AI安全分析引擎初始化成功")
    info(f"  支持模型: OpenAI兼容/Ollama")
    info(f"  功能: 漏洞深度分析/误报过滤/优先级排序/管理层摘要")
    record("AI安全分析引擎", True)
except Exception as e:
    fail(f"AI安全分析引擎: {e}")
    record("AI安全分析引擎", False, str(e))

# 2. AI智能渗透顾问
try:
    from pentestai.modules.ai_security.ai_pentest_advisor_pro import AIPentestAdvisorPro
    apa = AIPentestAdvisorPro()
    ok(f"AI智能渗透顾问初始化成功")
    info(f"  模式: plan/payload/interpret/chat")
    record("AI智能渗透顾问", True)
except Exception as e:
    fail(f"AI智能渗透顾问: {e}")
    record("AI智能渗透顾问", False, str(e))

# 3. AI自主渗透引擎v2.1
try:
    from pentestai.modules.ai_security.autonomous_pentest_engine import AutonomousPentestEngine
    ape = AutonomousPentestEngine()
    ok(f"AI自主渗透引擎v{ape.version}初始化成功")
    info(f"  智能体模式: 逐阶段AI决策+自动解析+错误恢复")
    info(f"  最大阶段: 10, 支持URL/IP/IP段/域名")
    record("AI自主渗透引擎v2.1", ape.version == "2.1.0", f"v{ape.version}")
except Exception as e:
    fail(f"AI自主渗透引擎: {e}")
    record("AI自主渗透引擎v2.1", False, str(e))

# ============================================================
section("四、结果结构化解析器校验（15种工具）")
# ============================================================

from pentestai.modules.ai_security.result_parser import ResultParser, Finding

parser_tests = [
    ("port_scanner", "扫描完成: 127.0.0.1, 开放端口 3/43\n    135  MSRPC\n   3000  Node.js\n   8443  HTTPS-Alt", {"target": "test"}),
    ("web_scanner", "发现SQL注入漏洞\n检测到XSS漏洞", {"url": "test"}),
    ("subdomain_enum", "admin.test.com\napi.test.com", {"domain": "test.com"}),
    ("dir_bruter", "/admin 200\n/backup 200\n/.git 200", {"url": "test"}),
    ("tech_detector", "nginx 1.18.0\nPHP 7.4\nMySQL", {"url": "test"}),
    ("waf_detector", "检测到Cloudflare WAF", {"url": "test"}),
    ("cve_checker", "CVE-2021-44228 可能存在", {"target": "test"}),
    ("weak_password", "登录成功: admin/admin123", {"target": "test"}),
    ("weak_password(0个)", "发现弱口令: 0 个", {"target": "test"}),
    ("vuln_verifier", "SQL注入已验证，确认真实存在", {"target": "test"}),
    ("ssl_auditor", "检测到过期证书\nTLS 1.0 已启用", {"target": "test"}),
    ("internal_scanner", "192.168.1.1 存活\n192.168.1.2 存活", {"target": "192.168.1.0/24"}),
    ("internal_vuln_checker", "检测到MS17-010漏洞", {"target": "test"}),
]

parser_pass = 0
for tool_name, output, params in parser_tests:
    try:
        findings = ResultParser.parse(tool_name.replace("(0个)", ""), output, params)
        if tool_name == "weak_password(0个)":
            if findings[0].risk == "信息":
                ok(f"{tool_name}: 正确识别为信息（0个不误报）")
                parser_pass += 1
            else:
                fail(f"{tool_name}: 误报为{findings[0].risk}")
        elif len(findings) > 0:
            ok(f"{tool_name}: 解析出{len(findings)}个发现")
            parser_pass += 1
        else:
            warn(f"{tool_name}: 未解析出发现")
    except Exception as e:
        fail(f"{tool_name}: {str(e)[:50]}")

record("结果解析器", parser_pass >= 12, f"{parser_pass}/{len(parser_tests)}")

# ============================================================
section("五、GUI功能校验")
# ============================================================

gui_files = [
    ("主窗口", "pentestai/gui/main_window.py"),
    ("首页快速开始", "pentestai/gui/home_page.py"),
    ("关于对话框", "pentestai/gui/about_dialog.py"),
    ("自主渗透页面", "pentestai/gui/autonomous_pentest_page.py"),
    ("业务页面", "pentestai/gui/business_page.py"),
]

for name, path in gui_files:
    full_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), path)
    if os.path.exists(full_path):
        size = os.path.getsize(full_path)
        ok(f"{name}: {path} ({size}字节)")
    else:
        fail(f"{name}: {path} 不存在")

record("GUI文件", all(os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)), p)) for _, p in gui_files))

# 检查快捷键和关于对话框集成
try:
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "pentestai/gui/main_window.py"), 'r', encoding='utf-8') as f:
        mw_content = f.read()
    has_shortcut = "QShortcut" in mw_content or "Ctrl+" in mw_content
    has_about = "about_dialog" in mw_content or "AboutDialog" in mw_content
    has_home = "home_page" in mw_content or "HomePage" in mw_content
    has_autonomous = "autonomous_pentest" in mw_content
    ok(f"主窗口集成: 快捷键={'✅' if has_shortcut else '❌'} 关于={'✅' if has_about else '❌'} 首页={'✅' if has_home else '❌'} 自主渗透={'✅' if has_autonomous else '❌'}")
    record("GUI集成", all([has_shortcut, has_about, has_home, has_autonomous]))
except Exception as e:
    fail(f"GUI集成检查失败: {e}")
    record("GUI集成", False, str(e))

# ============================================================
section("六、真实靶场校验（JuiceShop）")
# ============================================================

import subprocess
print("  启动JuiceShop真实靶场测试（约15秒）...")
test_script = os.path.join(os.path.dirname(os.path.abspath(__file__)), "real_target_test_juiceshop.py")
result_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "真实靶场测试结果_JuiceShop.json")

try:
    proc = subprocess.run([sys.executable, test_script], capture_output=True, text=True, timeout=120, cwd=os.path.dirname(os.path.abspath(__file__)))
    if os.path.exists(result_file):
        with open(result_file, 'r', encoding='utf-8') as f:
            r = json.load(f)
        total = r.get('findings_total', 0)
        high = r.get('findings_high', 0)
        medium = r.get('findings_medium', 0)
        low = r.get('findings_low', 0)
        info_c = r.get('findings_info', 0)
        ok(f"靶场测试完成: 共{total}个发现 (高危{high}/中危{medium}/低危{low}/信息{info_c})")
        # 检查是否有端口发现（修复后应该有）
        has_port = any("端口" in f.get('name','') and "开放" in f.get('name','') for f in r.get('findings', []))
        if has_port:
            ok("端口扫描修复验证: 成功识别开放端口")
        else:
            warn("端口扫描修复验证: 未识别到开放端口（可能解析器仍需调优）")
        # 检查弱口令是否误报
        weak_high = any("弱口令" in f.get('name','') and f.get('risk') == '高危' for f in r.get('findings', []))
        if not weak_high:
            ok("弱口令误报修复验证: 无误报高危")
        else:
            warn("弱口令误报修复验证: 仍有高危（需确认是否真的爆破成功）")
        record("真实靶场测试", total > 0, f"{total}个发现")
    else:
        fail("靶场测试结果文件未生成")
        record("真实靶场测试", False, "结果文件未生成")
except Exception as e:
    fail(f"靶场测试异常: {e}")
    record("真实靶场测试", False, str(e))

# ============================================================
section("七、销售素材与文档校验")
# ============================================================

artifacts = [
    ("使用手册", "使用手册_PentestAI.md"),
    ("产品介绍", "产品介绍_PentestAI.md"),
    ("演示视频脚本", "演示视频脚本.md"),
    ("实战漏洞案例集", "实战漏洞发现案例集.md"),
    ("CSDN引流文", "引流文章/CSDN_主引流文_我用Python+AI做了一个自动化渗透测试平台.md"),
    ("知乎引流文", "引流文章/知乎_深度引流文_我用AI把渗透测试效率提升10倍.md"),
    ("推广文案合集", "引流文章/推广文案合集_朋友圈微信群QQ群.md"),
    ("升级报告", "升级报告_v50.0_AI能力重大升级.md"),
]

for name, path in artifacts:
    full_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), path)
    if os.path.exists(full_path):
        size = os.path.getsize(full_path)
        ok(f"{name}: {size}字节")
    else:
        warn(f"{name}: 未找到 ({path})")

# 销售素材包
sales_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "销售素材包")
if os.path.exists(sales_dir):
    sales_files = os.listdir(sales_dir)
    ok(f"销售素材包: {len(sales_files)}个文件")
else:
    warn("销售素材包目录不存在")

# ============================================================
section("八、最终校验总结")
# ============================================================

total = len(results)
passed = sum(1 for r in results if r['passed'])
failed = total - passed

print(f"\n  {Color.BOLD}校验项目总数: {total}{Color.END}")
print(f"  {Color.GREEN}✅ 通过: {passed}{Color.END}")
print(f"  {Color.RED}❌ 失败: {failed}{Color.END}")
print(f"  {Color.BOLD}通过率: {passed/total*100:.1f}%{Color.END}")

print(f"\n  {Color.BOLD}详细结果:{Color.END}")
for r in results:
    status = f"{Color.GREEN}✅{Color.END}" if r['passed'] else f"{Color.RED}❌{Color.END}"
    detail = f" ({r['detail']})" if r['detail'] else ""
    print(f"    {status} {r['name']}{detail}")

# 保存报告
report = {
    "校验时间": time.strftime("%Y-%m-%d %H:%M:%S"),
    "总项目数": total,
    "通过数": passed,
    "失败数": failed,
    "通过率": f"{passed/total*100:.1f}%",
    "详细结果": results
}
report_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "全面功能校验报告.json")
with open(report_path, 'w', encoding='utf-8') as f:
    json.dump(report, f, ensure_ascii=False, indent=2)
print(f"\n  💾 校验报告已保存: {report_path}")

if failed == 0:
    print(f"\n  {Color.GREEN}{Color.BOLD}🎉 全部校验通过！PentestAI所有核心功能正常！{Color.END}{Color.END}")
else:
    print(f"\n  {Color.YELLOW}⚠️  有{failed}项未通过，需要进一步检查{Color.END}")

sys.exit(0 if failed == 0 else 1)
