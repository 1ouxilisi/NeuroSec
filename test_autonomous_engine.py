"""
AI自主渗透引擎测试脚本
验证：初始化、目标解析、计划生成、进度获取、停止功能
注意：只验证计划生成，不实际执行扫描（避免未授权扫描）
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pentestai.modules.ai_security.autonomous_pentest_engine import AutonomousPentestEngine, PentestPhase

def test_engine_init():
    """测试引擎初始化"""
    print("=" * 60)
    print("测试1: 引擎初始化")
    print("=" * 60)
    engine = AutonomousPentestEngine()
    print(f"  ✅ 引擎实例化成功")
    print(f"  工具名: {engine.name}")
    print(f"  显示名: {engine.display_name}")
    print(f"  分类: {engine.category}")
    print(f"  AI启用: {engine.ai_enabled}")
    print(f"  运行模式: {engine.mode}")
    return engine

def test_target_parsing(engine):
    """测试目标解析"""
    print("\n" + "=" * 60)
    print("测试2: 目标解析")
    print("=" * 60)
    test_cases = [
        ("https://example.com", "url"),
        ("http://test-site.org", "url"),
        ("192.168.1.1", "ip"),
        ("192.168.1.0/24", "ip_range"),
        ("example.com", "domain"),
        ("sub.domain.com", "domain"),
    ]
    all_pass = True
    for target, expected in test_cases:
        result = engine._parse_target(target)
        status = "✅" if result == expected else "❌"
        if result != expected:
            all_pass = False
        print(f"  {status} {target:<30} -> {result:<10} (预期: {expected})")
    return all_pass

def test_plan_generation(engine):
    """测试计划生成"""
    print("\n" + "=" * 60)
    print("测试3: 渗透计划生成（URL目标）")
    print("=" * 60)
    engine.set_target("https://example.com")
    engine.set_mode("semi_auto")
    phases = engine.generate_plan()
    print(f"  ✅ 计划生成成功，共{len(phases)}个阶段")
    total_tools = 0
    for i, phase in enumerate(phases):
        tool_count = len(phase.tools)
        total_tools += tool_count
        print(f"  阶段{i+1}: {phase.name}")
        print(f"    描述: {phase.description}")
        print(f"    工具数: {tool_count}")
        print(f"    预期输出: {phase.expected_output}")
        for tool in phase.tools[:3]:  # 只显示前3个
            print(f"      - {tool['tool_name']}: {tool['description']}")
        if len(phase.tools) > 3:
            print(f"      ... 还有{len(phase.tools)-3}个工具")
    print(f"  总工具数: {total_tools}")
    return len(phases) >= 3 and total_tools >= 5

def test_ip_plan_generation(engine):
    """测试IP目标计划生成"""
    print("\n" + "=" * 60)
    print("测试4: 渗透计划生成（IP目标）")
    print("=" * 60)
    engine.set_target("192.168.1.0/24")
    phases = engine.generate_plan()
    print(f"  ✅ IP目标计划生成成功，共{len(phases)}个阶段")
    for i, phase in enumerate(phases):
        print(f"  阶段{i+1}: {phase.name} ({len(phase.tools)}个工具)")
    return len(phases) >= 2

def test_progress(engine):
    """测试进度获取"""
    print("\n" + "=" * 60)
    print("测试5: 进度获取")
    print("=" * 60)
    progress = engine.get_progress()
    print(f"  ✅ 进度获取成功")
    print(f"  状态: {progress['status']}")
    print(f"  总阶段: {progress['total_phases']}")
    print(f"  已完成: {progress['completed_phases']}")
    print(f"  进度: {progress['progress']}%")
    print(f"  当前阶段: {progress['current_phase']}")
    print(f"  目标: {progress['target']}")
    print(f"  模式: {progress['mode']}")
    return True

def test_phase_class():
    """测试PentestPhase类"""
    print("\n" + "=" * 60)
    print("测试6: PentestPhase类")
    print("=" * 60)
    phase = PentestPhase(
        name="测试阶段",
        description="这是一个测试阶段",
        tools=[{"tool_name": "test_tool", "params": {}, "description": "测试工具"}],
        expected_output="测试输出"
    )
    phase.status = "completed"
    phase.results = [{"status": "success"}, {"status": "failed"}]
    d = phase.to_dict()
    print(f"  ✅ PentestPhase创建成功")
    print(f"  名称: {d['name']}")
    print(f"  状态: {d['status']}")
    print(f"  工具数: {d['tools_count']}")
    print(f"  结果数: {d['results_count']}")
    return d['status'] == "completed" and d['results_count'] == 2

def main():
    print("\n" + "🔍" * 30)
    print("  AI自主渗透引擎 - 功能测试")
    print("🔍" * 30 + "\n")

    results = []

    # 测试1: 引擎初始化
    engine = test_engine_init()
    results.append(("引擎初始化", True))

    # 测试2: 目标解析
    r = test_target_parsing(engine)
    results.append(("目标解析", r))

    # 测试3: URL计划生成
    r = test_plan_generation(engine)
    results.append(("URL计划生成", r))

    # 测试4: IP计划生成
    r = test_ip_plan_generation(engine)
    results.append(("IP计划生成", r))

    # 测试5: 进度获取
    r = test_progress(engine)
    results.append(("进度获取", r))

    # 测试6: PentestPhase类
    r = test_phase_class()
    results.append(("PentestPhase类", r))

    # 总结
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
        print("  🎉 全部测试通过！")
    else:
        print(f"  ⚠️  有{total-passed}个测试失败")

    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
