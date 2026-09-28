"""v2.1规则模式完整流程模拟验证（不实际执行扫描，只验证决策逻辑）"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pentestai.modules.ai_security.autonomous_pentest_engine import AutonomousPentestEngine, PentestPhase, PentestState
from pentestai.modules.ai_security.result_parser import ResultParser, Finding

def simulate_full_flow():
    print("=" * 70)
    print("  v2.1规则模式完整流程模拟验证")
    print("=" * 70)

    engine = AutonomousPentestEngine()
    engine.set_target("http://juiceshop.local:3000")
    # 手动初始化state（模拟run_autonomous中的state创建）
    engine.state = PentestState(engine.target, engine.target_type)
    print(f"\n🎯 目标: {engine.target} ({engine.target_type})")
    print(f"🤖 引擎版本: v{engine.version}")
    print(f"📋 模式: 规则降级模式（未配置AI API key）")

    # 模拟逐阶段决策
    print("\n" + "─" * 70)
    print("  阶段1: 信息收集（recon）")
    print("─" * 70)
    phase1 = engine._rule_generate_recon_phase()
    print(f"  阶段名: {phase1.name}")
    print(f"  阶段类型: {phase1.phase_type}")
    print(f"  工具数: {len(phase1.tools)}")
    for t in phase1.tools:
        print(f"    - {t['tool_name']}: {t['description']}")

    # 模拟阶段1执行结果
    phase1.results = [
        {"tool_name": "port_scanner", "status": "success", "output": "3000/tcp open http\n22/tcp open ssh", "params": {"target": "juiceshop.local"}},
        {"tool_name": "tech_detector", "status": "success", "output": "Node.js Express Angular", "params": {"url": "http://juiceshop.local:3000"}},
        {"tool_name": "dir_bruter", "status": "success", "output": "/api 200\n/admin 200\n/.git 403", "params": {"url": "http://juiceshop.local:3000"}},
        {"tool_name": "bad_tool", "status": "failed", "error": "工具未找到或执行超时", "params": {}},
    ]
    # 模拟自动解析
    parsed = 0
    for r in phase1.results:
        if r["status"] == "success":
            findings = ResultParser.parse(r["tool_name"], r["output"], r["params"])
            engine.state.parsed_findings.extend(findings)
            parsed += len(findings)
        else:
            engine.state.add_failed_tool(r["tool_name"], r["error"])
    engine.state.phases_completed.append(phase1)
    print(f"\n  ✅ 阶段1完成，自动解析提取{parsed}个发现")
    print(f"  ⚠️  失败工具: {[f['tool'] for f in engine.state.failed_tools]}")

    print("\n" + "─" * 70)
    print("  阶段2: 漏洞扫描（vuln_scan）")
    print("─" * 70)
    phase2 = engine._rule_generate_next_phase()
    print(f"  阶段名: {phase2.name}")
    print(f"  阶段类型: {phase2.phase_type}")
    print(f"  工具数: {len(phase2.tools)}")
    for t in phase2.tools:
        print(f"    - {t['tool_name']}: {t['description']}")

    # 模拟阶段2执行结果
    phase2.results = [
        {"tool_name": "web_scanner", "status": "success", "output": "发现SQL注入漏洞在 /rest/user/login\n检测到XSS漏洞在 /search\n发现文件上传漏洞在 /file-upload", "params": {"url": "http://juiceshop.local:3000"}},
        {"tool_name": "cve_checker", "status": "success", "output": "CVE-2021-23424 可能存在", "params": {"target": "juiceshop.local"}},
    ]
    parsed2 = 0
    for r in phase2.results:
        if r["status"] == "success":
            findings = ResultParser.parse(r["tool_name"], r["output"], r["params"])
            engine.state.parsed_findings.extend(findings)
            parsed2 += len(findings)
    engine.state.phases_completed.append(phase2)
    print(f"\n  ✅ 阶段2完成，自动解析提取{parsed2}个发现")

    print("\n" + "─" * 70)
    print("  阶段3: 漏洞验证（vuln_verify）")
    print("─" * 70)
    phase3 = engine._rule_generate_next_phase()
    print(f"  阶段名: {phase3.name}")
    print(f"  阶段类型: {phase3.phase_type}")
    print(f"  工具数: {len(phase3.tools)}")
    for t in phase3.tools:
        print(f"    - {t['tool_name']}: {t['description']}")

    phase3.results = [
        {"tool_name": "vuln_verifier", "status": "success", "output": "SQL注入已验证，确认真实存在，可获取用户数据", "params": {"target": "http://juiceshop.local:3000"}},
    ]
    parsed3 = 0
    for r in phase3.results:
        if r["status"] == "success":
            findings = ResultParser.parse(r["tool_name"], r["output"], r["params"])
            engine.state.parsed_findings.extend(findings)
            parsed3 += len(findings)
    engine.state.phases_completed.append(phase3)
    print(f"\n  ✅ 阶段3完成，自动解析提取{parsed3}个发现")

    print("\n" + "─" * 70)
    print("  阶段4: 报告生成（report）")
    print("─" * 70)
    phase4 = engine._rule_generate_next_phase()
    print(f"  阶段名: {phase4.name}")
    print(f"  阶段类型: {phase4.phase_type}")
    print(f"  工具数: {len(phase4.tools)}")
    engine.state.phases_completed.append(phase4)

    print("\n" + "─" * 70)
    print("  阶段5: AI决策停止")
    print("─" * 70)
    phase5 = engine._rule_generate_next_phase()
    if phase5 is None:
        print(f"  ✅ 规则模式正确返回None（停止渗透）")
        print(f"  停止原因: {engine.state.stop_reason}")
    else:
        print(f"  ❌ 错误：应该停止但返回了阶段")

    # 最终统计
    print("\n" + "=" * 70)
    print("  最终验证结果")
    print("=" * 70)
    all_findings = engine.state.parsed_findings
    high = sum(1 for f in all_findings if f.risk == "高危")
    medium = sum(1 for f in all_findings if f.risk == "中危")
    low = sum(1 for f in all_findings if f.risk == "低危")
    info = sum(1 for f in all_findings if f.risk == "信息")

    print(f"\n  📊 发现统计:")
    print(f"    总计: {len(all_findings)}个")
    print(f"    高危: {high}个")
    print(f"    中危: {medium}个")
    print(f"    低危: {low}个")
    print(f"    信息: {info}个")

    print(f"\n  🔍 发现详情（按风险排序）:")
    sorted_findings = sorted(all_findings, key=lambda x: {"高危":0,"中危":1,"低危":2,"信息":3}.get(x.risk, 4))
    for i, f in enumerate(sorted_findings[:10]):
        print(f"    {i+1}. [{f.risk}] {f.name} - {f.description[:50]}")

    print(f"\n  ⚠️  失败工具记录: {[f['tool'] for f in engine.state.failed_tools]}")
    print(f"  📋 完成阶段数: {len(engine.state.phases_completed)}")
    print(f"  🛑 停止原因: {engine.state.stop_reason}")

    # 验证检查
    print("\n" + "=" * 70)
    print("  验证检查清单")
    print("=" * 70)
    checks = [
        ("逐阶段决策正确（4阶段+停止）", len(engine.state.phases_completed) == 4 and phase5 is None),
        ("阶段类型正确（recon→vuln_scan→vuln_verify→report）",
         engine.state.phases_completed[0].phase_type == "recon" and
         engine.state.phases_completed[1].phase_type == "vuln_scan" and
         engine.state.phases_completed[2].phase_type == "vuln_verify" and
         engine.state.phases_completed[3].phase_type == "report"),
        ("自动发现提取工作", len(all_findings) > 0),
        ("发现包含高危漏洞", high > 0),
        ("发现包含中危漏洞", medium > 0),
        ("错误恢复机制（失败工具记录）", len(engine.state.failed_tools) > 0),
        ("发现统计正确", high + medium + low + info == len(all_findings)),
        ("发现按风险排序", sorted_findings[0].risk == "高危"),
        ("停止原因正确", "4个阶段" in engine.state.stop_reason),
    ]
    all_pass = True
    for name, result in checks:
        status = "✅" if result else "❌"
        if not result:
            all_pass = False
        print(f"  {status} {name}")

    print(f"\n  {'🎉 全部验证通过！v2.1规则模式完整流程验证成功！' if all_pass else '❌ 存在验证失败项'}")
    return all_pass

if __name__ == "__main__":
    success = simulate_full_flow()
    sys.exit(0 if success else 1)
