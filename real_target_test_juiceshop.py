"""真实靶场测试：AI自主渗透引擎v2.1在JuiceShop上跑完整流程"""
import sys, os, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pentestai.modules.ai_security.autonomous_pentest_engine import AutonomousPentestEngine

def main():
    print("=" * 70)
    print("  🔥 真实靶场测试：AI自主渗透引擎v2.1")
    print("  目标: OWASP Juice Shop (http://localhost:3000)")
    print("=" * 70)

    # 初始化引擎
    engine = AutonomousPentestEngine()
    print(f"\n🤖 引擎版本: v{engine.version}")
    print(f"📋 AI启用: {engine.ai_enabled}")
    if not engine.ai_enabled:
        print("⚠️  未配置AI API key，使用规则降级模式")
    print(f"🔧 工具总数: 197")

    # 设置目标
    target = "http://localhost:3000"
    print(f"\n🎯 设置目标: {target}")
    engine.set_target(target)

    # 运行自主渗透
    print("\n" + "─" * 70)
    print("  🚀 开始自主渗透测试...")
    print("─" * 70)

    start_time = time.time()
    try:
        result = engine.run_autonomous(mode="auto")
    except Exception as e:
        print(f"\n❌ 执行异常: {str(e)[:200]}")
        import traceback
        traceback.print_exc()
        return False

    elapsed = time.time() - start_time

    # 输出结果
    print("\n" + "=" * 70)
    print("  📊 测试结果")
    print("=" * 70)

    print(f"\n⏱️  耗时: {elapsed:.1f}秒")
    print(f"🎯 目标: {result.get('target')}")
    print(f"📋 模式: {result.get('mode')}")
    print(f"🤖 AI启用: {result.get('ai_enabled')}")
    print(f"🔄 智能体模式: {result.get('agent_mode')}")
    print(f"📝 完成阶段: {result.get('phases_completed')}")
    print(f"🛑 停止原因: {result.get('stop_reason')}")

    # 工具执行统计
    total_tools = result.get("total_tools", 0)
    successful = result.get("successful_tools", 0)
    failed = result.get("failed_tools", 0)
    print(f"\n🔧 工具执行: 总计{total_tools}个 (成功{successful}/失败{failed})")

    # 发现统计
    print(f"\n🔍 发现统计:")
    print(f"  总计: {result.get('findings_total', 0)}个")
    print(f"  高危: {result.get('findings_high', 0)}个")
    print(f"  中危: {result.get('findings_medium', 0)}个")
    print(f"  低危: {result.get('findings_low', 0)}个")
    print(f"  信息: {result.get('findings_info', 0)}个")

    # 发现详情
    findings = result.get("findings", [])
    if findings:
        print(f"\n📋 发现详情（前10个）:")
        for i, f in enumerate(findings[:10]):
            print(f"  {i+1}. [{f.get('risk','?')}] {f.get('name','?')}")
            if f.get('description'):
                print(f"     {f['description'][:60]}")

    # 阶段详情
    phases = result.get("phases", [])
    if phases:
        print(f"\n📈 阶段执行详情:")
        for i, p in enumerate(phases):
            print(f"  阶段{i+1}: {p.get('name','?')} ({p.get('phase_type','?')})")
            print(f"    工具: {len(p.get('tools',[]))}个, 状态: {p.get('status','?')}")
            if p.get('ai_decision'):
                print(f"    AI决策: {p['ai_decision'][:80]}")

    # 保存结果
    output_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), "真实靶场测试结果_JuiceShop.json")
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(result, f, ensure_ascii=False, indent=2, default=str)
    print(f"\n💾 完整结果已保存: {output_file}")

    # 验证检查
    print("\n" + "=" * 70)
    print("  ✅ 验证检查")
    print("=" * 70)
    checks = [
        ("引擎成功执行", result.get("status") == "completed" or result.get("phases_completed", 0) > 0),
        ("完成至少1个阶段", result.get("phases_completed", 0) >= 1),
        ("执行了工具", total_tools > 0),
        ("有发现统计字段", "findings_total" in result),
        ("有阶段详情", len(phases) > 0),
        ("结果已保存", os.path.exists(output_file)),
    ]
    all_pass = True
    for name, r in checks:
        status = "✅" if r else "❌"
        if not r:
            all_pass = False
        print(f"  {status} {name}")

    print(f"\n{'🎉 真实靶场测试完成！' if all_pass else '⚠️  测试完成，部分检查未通过'}")
    return all_pass

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
