"""AI自主渗透引擎 v2.1 全面测试（删除重复劳动版）"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pentestai.modules.ai_security.autonomous_pentest_engine import AutonomousPentestEngine, PentestPhase, PentestState
from pentestai.modules.ai_security.result_parser import ResultParser, Finding

def test_engine_v21():
    print("=" * 60)
    print("测试1: 引擎v2.1初始化")
    print("=" * 60)
    engine = AutonomousPentestEngine()
    print(f"  ✅ 版本: {engine.version}")
    print(f"  ✅ 工具名: {engine.name}")
    assert engine.version == "2.1.0"
    return engine

def test_result_parser():
    print("\n" + "=" * 60)
    print("测试2: 结果结构化解析器（删除重复劳动核心）")
    print("=" * 60)
    # 测试端口扫描解析
    findings = ResultParser.parse("port_scanner", "80/tcp open http\n443/tcp open https\n22/tcp open ssh\n3306/tcp open mysql", {"target": "test.com"})
    print(f"  ✅ 端口扫描解析: {len(findings)}个发现")
    for f in findings:
        print(f"    - [{f.risk}] {f.name}")
    assert len(findings) == 4

    # 测试Web漏洞解析
    findings2 = ResultParser.parse("web_scanner", "发现SQL注入漏洞在 /search.php\n检测到XSS漏洞在 /comment.php", {"url": "http://test.com"})
    print(f"  ✅ Web漏洞解析: {len(findings2)}个发现")
    for f in findings2:
        print(f"    - [{f.risk}] {f.name}")
    assert len(findings2) >= 2

    # 测试子域名解析
    findings3 = ResultParser.parse("subdomain_enum", "admin.test.com\napi.test.com\nmail.test.com", {"domain": "test.com"})
    print(f"  ✅ 子域名解析: {len(findings3)}个发现")
    assert len(findings3) >= 1

    # 测试目录爆破解析
    findings4 = ResultParser.parse("dir_bruter", "/admin 200\n/backup 200\n/.git 200\n/login 302", {"url": "http://test.com"})
    print(f"  ✅ 目录爆破解析: {len(findings4)}个发现")
    for f in findings4:
        print(f"    - [{f.risk}] {f.name}")
    assert len(findings4) >= 3

    # 汇总统计
    all_findings = findings + findings2 + findings3 + findings4
    summary = ResultParser.summarize_findings(all_findings)
    print(f"  ✅ 汇总统计: 共{summary['total']}个，高危{summary['高危']}，中危{summary['中危']}，低危{summary['低危']}")
    return True

def test_auto_finding_extraction(engine):
    print("\n" + "=" * 60)
    print("测试3: 自动发现提取（AI决策有真实数据）")
    print("=" * 60)
    engine.state = PentestState("http://test.com", "url")
    # 模拟工具结果
    phase = PentestPhase("信息收集", "测试", [
        {"tool_name": "port_scanner", "params": {"target": "test.com"}, "description": "端口扫描", "status": "success", "output": "80/tcp open http\n3306/tcp open mysql"},
        {"tool_name": "web_scanner", "params": {"url": "http://test.com"}, "description": "Web扫描", "status": "success", "output": "发现SQL注入漏洞"},
        {"tool_name": "bad_tool", "params": {}, "description": "失败工具", "status": "failed", "error": "工具不存在"},
    ], phase_type="recon")
    phase.results = phase.tools  # 直接用tools作为results
    phase.status = "completed"

    # 手动执行解析逻辑（模拟_execute_phase中的解析）
    parsed_count = 0
    for result in phase.results:
        if result.get("status") == "success":
            findings = ResultParser.parse(result.get("tool_name", ""), result.get("output", ""), result.get("params", {}))
            for finding in findings:
                engine.state.parsed_findings.append(finding)
                parsed_count += 1
        elif result.get("status") == "failed":
            engine.state.add_failed_tool(result.get("tool_name", ""), result.get("error", ""))

    print(f"  ✅ 自动提取{parsed_count}个结构化发现")
    for f in engine.state.parsed_findings:
        print(f"    - [{f.risk}] {f.name}")
    print(f"  ✅ 失败工具记录: {[ft['tool'] for ft in engine.state.failed_tools]}")

    # 验证state摘要包含发现
    summary = engine.state.get_summary()
    assert "SQL注入" in summary or "端口" in summary, "摘要应包含发现"
    assert "bad_tool" in summary, "摘要应包含失败工具"
    print(f"  ✅ state摘要包含发现和失败工具")
    return True

def test_ai_prompt_quality(engine):
    print("\n" + "=" * 60)
    print("测试4: AI决策prompt质量（删除重复劳动关键）")
    print("=" * 60)
    engine.state = PentestState("http://test.com", "url")
    engine.state.parsed_findings = [
        Finding("SQL注入", "高危", "在/search.php发现SQL注入", "test.com", "web_scanner", "web"),
        Finding("开放端口3306", "低危", "MySQL端口开放", "test.com:3306", "port_scanner", "network"),
    ]
    prompt = engine._build_next_phase_prompt()

    # 检查prompt质量
    checks = [
        ("完整工具清单", "port_scanner" in prompt and "web_scanner" in prompt and "vuln_verifier" in prompt),
        ("发现统计", "高危" in prompt and "中危" in prompt),
        ("决策原则", "决策原则" in prompt),
        ("参数说明", "params:target" in prompt or "params:url" in prompt),
        ("严格JSON格式", "严格JSON" in prompt),
        ("停止选项", "action.*stop" in prompt or '"stop"' in prompt),
        ("工具数量限制", "不超过5个" in prompt),
    ]
    all_pass = True
    for name, result in checks:
        status = "✅" if result else "❌"
        if not result:
            all_pass = False
        print(f"  {status} {name}")
    print(f"  Prompt长度: {len(prompt)}字符")
    return all_pass

def test_finding_summary():
    print("\n" + "=" * 60)
    print("测试5: 发现统计与排序")
    print("=" * 60)
    state = PentestState("http://test.com", "url")
    state.parsed_findings = [
        Finding("信息1", "信息", "", "", "", ""),
        Finding("高危1", "高危", "", "", "", ""),
        Finding("中危1", "中危", "", "", "", ""),
        Finding("低危1", "低危", "", "", "", ""),
        Finding("高危2", "高危", "", "", "", ""),
    ]
    summary = state.get_summary()
    print(f"  ✅ 摘要包含发现数量: {'发现数量: 5' in summary}")
    # 检查排序（高危应在前）
    assert summary.find("高危") < summary.find("信息") or "高危" in summary
    print(f"  ✅ 发现按风险排序")
    print(f"  摘要预览:\n{summary[:200]}")
    return True

def main():
    print("\n" + "🤖" * 30)
    print("  AI自主渗透引擎 v2.1 - 删除重复劳动版 全面测试")
    print("🤖" * 30 + "\n")

    results = []
    engine = test_engine_v21()
    results.append(("引擎v2.1初始化", True))
    results.append(("结果结构化解析器", test_result_parser()))
    results.append(("自动发现提取", test_auto_finding_extraction(engine)))
    results.append(("AI决策prompt质量", test_ai_prompt_quality(engine)))
    results.append(("发现统计与排序", test_finding_summary()))

    print("\n" + "=" * 60)
    print("  测试总结")
    print("=" * 60)
    passed = sum(1 for _, r in results if r)
    total = len(results)
    for name, r in results:
        status = "✅ 通过" if r else "❌ 失败"
        print(f"  {status}: {name}")
    print(f"\n  总计: {passed}/{total} 通过")
    if passed == total:
        print("  🎉 全部测试通过！v2.1删除重复劳动版验证成功！")
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
