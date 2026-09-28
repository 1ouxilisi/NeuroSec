"""AI自主渗透引擎 v2.0 智能体功能测试"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pentestai.modules.ai_security.autonomous_pentest_engine import AutonomousPentestEngine, PentestPhase, PentestState

def test_engine_init():
    print("=" * 60)
    print("测试1: 引擎v2.0初始化")
    print("=" * 60)
    engine = AutonomousPentestEngine()
    print(f"  ✅ 引擎实例化成功")
    print(f"  版本: {engine.version}")
    print(f"  工具名: {engine.name}")
    print(f"  显示名: {engine.display_name}")
    print(f"  AI启用: {engine.ai_enabled}")
    print(f"  描述: {engine.description[:60]}...")
    assert engine.version == "2.0.0", "版本号应为2.0.0"
    assert "智能体" in engine.description, "描述应包含智能体"
    return engine

def test_state_class():
    print("\n" + "=" * 60)
    print("测试2: PentestState状态类")
    print("=" * 60)
    state = PentestState("https://example.com", "url")
    print(f"  ✅ 状态创建成功")
    print(f"  目标: {state.target}")
    print(f"  目标类型: {state.target_type}")
    print(f"  最大阶段: {state.max_phases}")
    state.add_finding({"name": "SQL注入", "risk": "高危"})
    print(f"  发现数: {len(state.findings)}")
    summary = state.get_summary()
    print(f"  状态摘要长度: {len(summary)}字符")
    assert "SQL注入" in summary, "摘要应包含发现"
    return True

def test_phase_class():
    print("\n" + "=" * 60)
    print("测试3: PentestPhase阶段类（v2.0新增字段）")
    print("=" * 60)
    phase = PentestPhase(
        name="AI生成阶段", description="测试阶段",
        tools=[{"tool_name": "test", "params": {}, "description": "测试"}],
        expected_output="测试输出", phase_type="vuln_scan"
    )
    phase.ai_decision = "因为发现了SQL注入，需要深入验证"
    phase.status = "completed"
    phase.results = [{"status": "success"}, {"status": "failed"}]
    d = phase.to_dict()
    print(f"  ✅ 阶段创建成功")
    print(f"  名称: {d['name']}")
    print(f"  类型: {d['phase_type']}")
    print(f"  AI决策: {d['ai_decision']}")
    print(f"  状态: {d['status']}")
    print(f"  结果数: {d['results_count']}")
    assert d['phase_type'] == "vuln_scan", "应有phase_type字段"
    assert d['ai_decision'] != "", "应有ai_decision字段"
    return True

def test_target_parsing(engine):
    print("\n" + "=" * 60)
    print("测试4: 目标解析")
    print("=" * 60)
    test_cases = [
        ("https://example.com", "url"),
        ("192.168.1.1", "ip"),
        ("192.168.1.0/24", "ip_range"),
        ("example.com", "domain"),
    ]
    all_pass = True
    for target, expected in test_cases:
        result = engine._parse_target(target)
        status = "✅" if result == expected else "❌"
        if result != expected:
            all_pass = False
        print(f"  {status} {target:<25} -> {result:<10} (预期: {expected})")
    return all_pass

def test_rule_first_phase(engine):
    print("\n" + "=" * 60)
    print("测试5: 规则模式-第一阶段生成（信息收集）")
    print("=" * 60)
    engine.set_target("https://example.com")
    phase = engine._rule_generate_recon_phase()
    print(f"  ✅ 第一阶段生成成功")
    print(f"  名称: {phase.name}")
    print(f"  类型: {phase.phase_type}")
    print(f"  工具数: {len(phase.tools)}")
    print(f"  预期输出: {phase.expected_output}")
    for tool in phase.tools:
        print(f"    - {tool['tool_name']}: {tool['description']}")
    assert phase.phase_type == "recon", "第一阶段应为recon类型"
    assert len(phase.tools) >= 3, "至少3个工具"
    return True

def test_rule_next_phases(engine):
    print("\n" + "=" * 60)
    print("测试6: 规则模式-后续阶段生成（动态决策）")
    print("=" * 60)
    engine.state = PentestState("https://example.com", "url")
    phases_generated = []
    for i in range(5):
        phase = engine._rule_generate_next_phase()
        if phase is None:
            print(f"  阶段{i+1}: AI决策停止（返回None）")
            break
        phases_generated.append(phase)
        engine.state.phases_completed.append(phase)
        print(f"  阶段{i+1}: {phase.name} (类型: {phase.phase_type}, 工具: {len(phase.tools)})")
    print(f"  ✅ 共生成{len(phases_generated)}个阶段后停止")
    print(f"  停止原因: {engine.state.stop_reason}")
    assert len(phases_generated) == 4, "规则模式应生成4个阶段"
    assert phases_generated[0].phase_type == "recon"
    assert phases_generated[1].phase_type == "vuln_scan"
    assert phases_generated[2].phase_type == "vuln_verify"
    assert phases_generated[3].phase_type == "report"
    return True

def test_progress(engine):
    print("\n" + "=" * 60)
    print("测试7: 进度获取（v2.0智能体模式）")
    print("=" * 60)
    engine.state = PentestState("https://example.com", "url")
    engine.state.phases_completed = [PentestPhase("测试", "", [], phase_type="recon")]
    progress = engine.get_progress()
    print(f"  ✅ 进度获取成功")
    print(f"  状态: {progress['status']}")
    print(f"  总阶段: {progress['total_phases']}")
    print(f"  已完成: {progress['completed_phases']}")
    print(f"  进度: {progress['progress']}%")
    print(f"  智能体模式: {progress.get('agent_mode', False)}")
    assert progress.get('agent_mode') == True, "应标记为智能体模式"
    return True

def main():
    print("\n" + "🤖" * 30)
    print("  AI自主渗透引擎 v2.0 - 智能体功能测试")
    print("🤖" * 30 + "\n")

    results = []
    engine = test_engine_init()
    results.append(("引擎v2.0初始化", True))
    results.append(("PentestState状态类", test_state_class()))
    results.append(("PentestPhase阶段类", test_phase_class()))
    results.append(("目标解析", test_target_parsing(engine)))
    results.append(("规则第一阶段生成", test_rule_first_phase(engine)))
    results.append(("规则后续阶段动态决策", test_rule_next_phases(engine)))
    results.append(("进度获取(智能体模式)", test_progress(engine)))

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
        print("  🎉 全部测试通过！v2.0智能体架构验证成功！")
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
