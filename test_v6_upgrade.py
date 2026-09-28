"""PentestAI v6.0 全模块测试脚本

测试所有升级模块是否正常工作
"""
import sys
import os
import time
import json

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_module_imports():
    """测试所有模块导入"""
    print("=" * 60)
    print("测试1: 模块导入测试")
    print("=" * 60)

    modules = [
        ("pentestai.core.multi_agent", "MultiAgentOrchestrator"),
        ("pentestai.core.api_server_v6", "APIRouter"),
        ("pentestai.core.attack_path_analyzer_v2", "AttackPathAnalyzer"),
        ("pentestai.core.task_scheduler", "TaskScheduler"),
        ("pentestai.core.fix_advisor_v2", "FixAdvisorEngine"),
        ("pentestai.core.code_audit_v2", "CodeAuditEngine"),
        ("pentestai.core.memory_compressor", "MemoryCompressor"),
        ("pentestai.core.browser_automation_v2", "BrowserAutomationEngine"),
        ("pentestai.core.proxy_v2", "ProxyServer"),
        ("pentestai.core.playbook_v2", "PlaybookEngine"),
        ("pentestai.core.v6_integration", "PentestAIV6"),
    ]

    passed = 0
    failed = 0

    for module_path, class_name in modules:
        try:
            module = __import__(module_path, fromlist=[class_name])
            cls = getattr(module, class_name)
            print(f"  ✅ {module_path}.{class_name}")
            passed += 1
        except Exception as e:
            print(f"  ❌ {module_path}.{class_name}: {e}")
            failed += 1

    print(f"\n结果: {passed} 通过, {failed} 失败")
    return failed == 0


def test_multi_agent():
    """测试多Agent架构"""
    print("\n" + "=" * 60)
    print("测试2: 多Agent架构")
    print("=" * 60)

    try:
        from pentestai.core.multi_agent import MultiAgentOrchestrator, run_multi_agent_pentest

        orchestrator = MultiAgentOrchestrator()
        print(f"  ✅ MultiAgentOrchestrator 创建成功")
        print(f"     - Agents: {list(orchestrator.agents.keys())}")

        # 测试同步运行（空registry，不会实际执行工具）
        print(f"  ℹ️  跳过实际扫描测试（需要工具注册表）")
        print(f"  ✅ 多Agent架构模块正常")
        return True
    except Exception as e:
        print(f"  ❌ 失败: {e}")
        return False


def test_api_server():
    """测试REST API"""
    print("\n" + "=" * 60)
    print("测试3: REST API 服务器")
    print("=" * 60)

    try:
        from pentestai.core.api_server_v6 import APIRouter, ScanTaskManager

        # 测试任务管理器
        manager = ScanTaskManager()
        task = manager.create_task("http://example.com")
        print(f"  ✅ 任务创建: {task.task_id}")

        # 测试路由
        router = APIRouter()
        result = router.handle_request("GET", "/api/health")
        print(f"  ✅ 健康检查: {result.get('status')}")

        result = router.handle_request("GET", "/api/tools")
        print(f"  ✅ 工具列表: {result.get('total', 0)} 个工具")

        print(f"  ✅ REST API 模块正常")
        return True
    except Exception as e:
        print(f"  ❌ 失败: {e}")
        return False


def test_attack_path():
    """测试攻击路径分析"""
    print("\n" + "=" * 60)
    print("测试4: 攻击路径关联分析")
    print("=" * 60)

    try:
        from pentestai.core.attack_path_analyzer_v2 import AttackPathAnalyzer, analyze_attack_paths

        # 模拟测试数据
        test_findings = [
            {"type": "sql_injection", "severity": "high", "name": "SQL注入漏洞"},
            {"type": "weak_password", "severity": "critical", "name": "弱口令"},
            {"type": "xss", "severity": "medium", "name": "存储型XSS"},
            {"type": "file_upload", "severity": "high", "name": "文件上传"},
        ]

        analyzer = AttackPathAnalyzer()
        result = analyzer.analyze(test_findings)

        print(f"  ✅ 分析完成")
        print(f"     - 总发现: {result['total_findings']}")
        print(f"     - 攻击节点: {result['attack_nodes']}")
        print(f"     - 攻击链: {result['attack_chains']}")
        print(f"     - 攻击路径: {result['attack_paths']}")
        print(f"     - 耗时: {result['duration']}s")

        return True
    except Exception as e:
        print(f"  ❌ 失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_task_scheduler():
    """测试定时任务调度"""
    print("\n" + "=" * 60)
    print("测试5: 定时任务调度")
    print("=" * 60)

    try:
        from pentestai.core.task_scheduler import TaskScheduler, TaskType, add_daily_task

        scheduler = TaskScheduler()
        task = scheduler.add_task(
            name="测试任务",
            task_type=TaskType.DAILY,
            target="http://example.com",
            schedule_time="08:00"
        )

        print(f"  ✅ 任务创建: {task.task_id}")
        print(f"     - 名称: {task.name}")
        print(f"     - 类型: {task.task_type.value}")
        print(f"     - 下次运行: {task.next_run}")

        tasks = scheduler.list_tasks()
        print(f"  ✅ 任务列表: {len(tasks)} 个任务")

        return True
    except Exception as e:
        print(f"  ❌ 失败: {e}")
        return False


def test_fix_advisor():
    """测试自动修复建议"""
    print("\n" + "=" * 60)
    print("测试6: 自动修复建议引擎")
    print("=" * 60)

    try:
        from pentestai.core.fix_advisor_v2 import FixAdvisorEngine, generate_fix_suggestions

        engine = FixAdvisorEngine()

        # 测试单个修复建议
        suggestion = engine.generate_fix("sql_injection", "python", "high")
        print(f"  ✅ SQL注入修复建议生成")
        print(f"     - 标题: {suggestion.title}")
        print(f"     - 步骤: {len(suggestion.fix_steps)} 步")
        print(f"     - 参考: {len(suggestion.references)} 个链接")

        # 测试批量生成
        test_findings = [
            {"type": "sql_injection", "severity": "high"},
            {"type": "xss", "severity": "medium"},
            {"type": "weak_password", "severity": "critical"},
        ]
        result = engine.generate_batch_fix(test_findings, "python")

        print(f"  ✅ 批量修复建议: {result['total_suggestions']} 个建议")
        print(f"     - 耗时: {result['duration']}s")

        return True
    except Exception as e:
        print(f"  ❌ 失败: {e}")
        return False


def test_memory_compressor():
    """测试记忆压缩"""
    print("\n" + "=" * 60)
    print("测试7: 记忆压缩与长任务支持")
    print("=" * 60)

    try:
        from pentestai.core.memory_compressor import MemoryCompressor, LongTaskManager

        compressor = MemoryCompressor(max_entries=10)

        # 添加记忆条目
        for i in range(15):
            compressor.add_entry(
                entry_type="observation",
                content=f"测试观察 {i}",
                importance=1 if i < 10 else 3
            )

        print(f"  ✅ 记忆条目添加: {len(compressor.entries)} 个保留")

        # 测试获取上下文
        context = compressor.get_context()
        print(f"  ✅ 上下文生成: {len(context)} 字符")

        # 测试长任务管理器
        manager = LongTaskManager(storage_dir=None)
        manager.save_task(
            task_id="test123",
            target="http://example.com",
            current_stage="scanning",
            progress=0.5
        )
        print(f"  ✅ 任务状态保存成功")

        task = manager.load_task("test123")
        print(f"  ✅ 任务状态加载: {task.current_stage}")

        return True
    except Exception as e:
        print(f"  ❌ 失败: {e}")
        return False


def test_playbook():
    """测试技能系统"""
    print("\n" + "=" * 60)
    print("测试8: 技能系统 (Playbook)")
    print("=" * 60)

    try:
        from pentestai.core.playbook_v2 import PlaybookEngine

        engine = PlaybookEngine()

        playbooks = engine.list_playbooks()
        print(f"  ✅ 预设剧本: {len(playbooks)} 个")

        for pb in playbooks:
            print(f"     - {pb['name']}: {pb['steps_count']} 步")

        return True
    except Exception as e:
        print(f"  ❌ 失败: {e}")
        return False


def test_v6_integration():
    """测试v6.0统一集成"""
    print("\n" + "=" * 60)
    print("测试9: v6.0 统一集成入口")
    print("=" * 60)

    try:
        from pentestai.core.v6_integration import PentestAIV6

        v6 = PentestAIV6()
        status = v6.get_status()

        print(f"  ✅ v6.0 初始化成功")
        print(f"     - 版本: {status['version']}")
        print(f"     - 模块数: {status['modules_count']}")
        print(f"     - 模块: {', '.join(status['modules_loaded'])}")

        features = v6.list_features()
        available = sum(1 for f in features if f['status'] == 'available')
        print(f"  ✅ 功能列表: {available}/{len(features)} 可用")

        return True
    except Exception as e:
        print(f"  ❌ 失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """运行所有测试"""
    print("\n" + "=" * 60)
    print("PentestAI v6.0 全模块测试")
    print("=" * 60)
    print()

    tests = [
        ("模块导入", test_module_imports),
        ("多Agent架构", test_multi_agent),
        ("REST API", test_api_server),
        ("攻击路径分析", test_attack_path),
        ("定时任务调度", test_task_scheduler),
        ("自动修复建议", test_fix_advisor),
        ("记忆压缩", test_memory_compressor),
        ("技能系统", test_playbook),
        ("v6.0集成", test_v6_integration),
    ]

    results = {}
    total_start = time.time()

    for name, test_func in tests:
        try:
            passed = test_func()
            results[name] = "✅ 通过" if passed else "❌ 失败"
        except Exception as e:
            results[name] = f"❌ 异常: {e}"

    total_duration = time.time() - total_start

    # 汇总
    print("\n" + "=" * 60)
    print("测试汇总")
    print("=" * 60)

    passed_count = sum(1 for r in results.values() if "✅" in r)
    failed_count = len(results) - passed_count

    for name, result in results.items():
        print(f"  {result} {name}")

    print(f"\n总计: {passed_count} 通过, {failed_count} 失败")
    print(f"总耗时: {round(total_duration, 2)}s")
    print()

    if failed_count == 0:
        print("🎉 所有测试通过！PentestAI v6.0 升级成功！")
    else:
        print(f"⚠️  {failed_count} 个测试失败，需要检查")

    return failed_count == 0


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
