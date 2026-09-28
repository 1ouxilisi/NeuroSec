"""PentestAI 核心引擎测试框架 - 单元测试+集成测试"""
import sys
import os
import time
import json

sys.path.insert(0, r"E:\BaiduNetdiskDownload\yuanbao\PentestAI")


class TestRunner:
    """测试运行器"""

    def __init__(self):
        self.results = []
        self.passed = 0
        self.failed = 0
        self.skipped = 0

    def run_test(self, name, func, expected=True):
        """运行单个测试"""
        start = time.time()
        try:
            result = func()
            elapsed = round(time.time() - start, 3)
            if result == expected:
                self.passed += 1
                self.results.append({"name": name, "status": "PASS", "time": elapsed})
                return True
            else:
                self.failed += 1
                self.results.append({"name": name, "status": "FAIL", "time": elapsed,
                                    "error": f"expected {expected}, got {result}"})
                return False
        except Exception as e:
            elapsed = round(time.time() - start, 3)
            self.failed += 1
            self.results.append({"name": name, "status": "ERROR", "time": elapsed,
                                "error": str(e)[:200]})
            return False

    def summary(self):
        """输出测试摘要"""
        total = self.passed + self.failed + self.skipped
        print("\n" + "=" * 70)
        print("测试结果摘要")
        print("=" * 70)
        print(f"  总计: {total} | 通过: {self.passed} | 失败: {self.failed} | 跳过: {self.skipped}")
        print(f"  通过率: {round(self.passed/total*100,1)}%" if total > 0 else "  无测试")
        print("=" * 70)

        if self.failed > 0:
            print("\n失败的测试:")
            for r in self.results:
                if r["status"] in ["FAIL", "ERROR"]:
                    print(f"  [{r['status']}] {r['name']}: {r.get('error', '')}")

        print("\n详细结果:")
        for r in self.results:
            icon = "✓" if r["status"] == "PASS" else "✗"
            print(f"  {icon} {r['name']} ({r['time']}s)")

        return self.passed, self.failed


def run_all_tests():
    """运行所有测试"""
    runner = TestRunner()

    print("=" * 70)
    print("PentestAI 核心引擎测试框架")
    print("=" * 70)

    # ========== 1. 工具注册测试 ==========
    print("\n[1/6] 工具注册测试...")

    def test_registry_init():
        from pentestai.core.tool_init import get_registry
        r = get_registry()
        return len(r.list_tools()) > 100

    runner.run_test("注册表初始化", test_registry_init)

    def test_registry_count():
        from pentestai.core.tool_init import get_registry
        r = get_registry()
        return len(r.list_tools()) >= 195

    runner.run_test("工具数量>=195", test_registry_count)

    def test_core_engines():
        from pentestai.core.tool_init import get_registry
        r = get_registry()
        core = ["nmap_engine", "nuclei_engine", "sqlmap_engine", "auto_pentest_pro",
                "pro_report_generator", "project_manager", "ai_vuln_analyzer",
                "false_positive_filter", "vuln_prioritizer", "self_vuln_verifier"]
        return all(r.get(name) for name in core)

    runner.run_test("核心引擎全部注册", test_core_engines)

    # ========== 2. 基础工具类测试 ==========
    print("\n[2/6] 基础工具类测试...")

    def test_base_tool():
        from pentestai.core.base_tool import BaseTool, ToolResult
        result = ToolResult(success=True, tool_name="test", output="ok")
        return result.success and result.tool_name == "test"

    runner.run_test("ToolResult基础功能", test_base_tool)

    def test_tool_registry():
        from pentestai.core.base_tool import ToolRegistry, BaseTool
        reg = ToolRegistry()

        class TestTool(BaseTool):
            name = "test_tool"
            description = "test"
            category = "test"
            def run(self, **kwargs):
                from pentestai.core.base_tool import ToolResult
                return ToolResult(success=True, tool_name=self.name, output="test")

        reg.register(TestTool())
        return reg.get("test_tool") is not None and len(reg.list_tools()) == 1

    runner.run_test("ToolRegistry注册/获取", test_tool_registry)

    # ========== 3. 误报过滤引擎测试 ==========
    print("\n[3/6] 误报过滤引擎测试...")

    def test_fp_filter_init():
        from pentestai.modules.ai.false_positive_filter import FalsePositiveFilter
        fp = FalsePositiveFilter()
        return fp.name == "false_positive_filter"

    runner.run_test("误报过滤引擎初始化", test_fp_filter_init)

    def test_fp_dedup():
        from pentestai.modules.ai.false_positive_filter import FalsePositiveFilter
        fp = FalsePositiveFilter()
        findings = [
            {"title": "SQL注入漏洞", "target": "http://test.com", "severity": "high"},
            {"title": "SQL注入漏洞", "target": "http://test.com", "severity": "high"},
            {"title": "XSS漏洞", "target": "http://test.com", "severity": "medium"},
        ]
        result = fp.run(action="deduplicate", findings=findings)
        return result.success and len(result.data.get("findings", [])) == 2

    runner.run_test("漏洞去重功能", test_fp_dedup)

    def test_fp_confidence():
        from pentestai.modules.ai.false_positive_filter import FalsePositiveFilter
        fp = FalsePositiveFilter()
        findings = [
            {"title": "SQL注入", "severity": "high", "evidence": "payload: ' OR 1=1, response: SQL syntax error", "verified": True},
            {"title": "安全头缺失", "severity": "low", "evidence": ""},
        ]
        result = fp.run(action="score_confidence", findings=findings)
        if result.success:
            scored = result.data.get("findings", [])
            return len(scored) == 2 and scored[0].get("confidence", 0) > scored[1].get("confidence", 0)
        return False

    runner.run_test("置信度评分功能", test_fp_confidence)

    # ========== 4. 漏洞优先级引擎测试 ==========
    print("\n[4/6] 漏洞优先级引擎测试...")

    def test_prio_init():
        from pentestai.modules.ai.vuln_prioritizer import VulnerabilityPrioritizer
        p = VulnerabilityPrioritizer()
        return p.name == "vuln_prioritizer"

    runner.run_test("优先级引擎初始化", test_prio_init)

    def test_prio_scoring():
        from pentestai.modules.ai.vuln_prioritizer import VulnerabilityPrioritizer
        p = VulnerabilityPrioritizer()
        vulns = [
            {"title": "SQL注入", "severity": "critical", "has_exploit": True, "in_the_wild": True},
            {"title": "安全头缺失", "severity": "low"},
        ]
        result = p.run(action="prioritize", vulnerabilities=vulns)
        if result.success:
            scored = result.data.get("vulnerabilities", [])
            return len(scored) == 2 and scored[0].get("priority") == "P0"
        return False

    runner.run_test("P0-P4优先级分级", test_prio_scoring)

    def test_prio_matrix():
        from pentestai.modules.ai.vuln_prioritizer import VulnerabilityPrioritizer
        p = VulnerabilityPrioritizer()
        result = p.run(action="get_matrix")
        return result.success and "P0" in result.data and "P4" in result.data

    runner.run_test("优先级矩阵查询", test_prio_matrix)

    # ========== 5. 自研漏洞验证引擎测试 ==========
    print("\n[5/6] 自研漏洞验证引擎测试...")

    def test_self_verifier_init():
        from pentestai.modules.vuln_verify.self_vuln_verifier import SelfVulnerabilityVerifier
        v = SelfVulnerabilityVerifier()
        return v.name == "self_vuln_verifier"

    runner.run_test("自研验证引擎初始化", test_self_verifier_init)

    def test_self_verifier_methods():
        from pentestai.modules.vuln_verify.self_vuln_verifier import SelfVulnerabilityVerifier
        v = SelfVulnerabilityVerifier()
        # 测试静态方法
        title = v._extract_title("<html><head><title>Test Page</title></head></html>")
        diff = v._content_difference("a\nb\nc", "a\nb\nd")
        return title == "Test Page" and 0 < diff <= 1

    runner.run_test("自研引擎辅助方法", test_self_verifier_methods)

    def test_self_verifier_payloads():
        from pentestai.modules.vuln_verify.self_vuln_verifier import SelfVulnerabilityVerifier
        v = SelfVulnerabilityVerifier()
        return (len(v.SQLI_PAYLOADS) >= 4 and len(v.XSS_PAYLOADS) >= 3 and
                len(v.CMDI_PAYLOADS) >= 4 and len(v.LFI_PAYLOADS) >= 2)

    runner.run_test("Payload库完整性", test_self_verifier_payloads)

    # ========== 6. LLM客户端测试 ==========
    print("\n[6/6] LLM客户端测试...")

    def test_llm_client():
        from pentestai.llm.client import LLMClient
        client = LLMClient()
        return hasattr(client, 'chat') and hasattr(client, 'is_configured')

    runner.run_test("LLM客户端初始化", test_llm_client)

    def test_llm_ollama_detection():
        from pentestai.llm.client import LLMClient
        client = LLMClient()
        return hasattr(client, 'is_ollama_available') and hasattr(client, 'list_local_models')

    runner.run_test("Ollama本地模型支持", test_llm_ollama_detection)

    def test_llm_parse_json():
        from pentestai.llm.client import LLMClient
        client = LLMClient()
        result = client.parse_json('```json\n{"key": "value"}\n```')
        return result and result.get("key") == "value"

    runner.run_test("JSON解析功能", test_llm_parse_json)

    # ========== 汇总 ==========
    passed, failed = runner.summary()

    # 保存测试报告
    report = {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "total": passed + failed,
        "passed": passed,
        "failed": failed,
        "pass_rate": f"{round(passed/(passed+failed)*100,1)}%" if (passed+failed) > 0 else "0%",
        "results": runner.results,
    }

    report_dir = r"E:\BaiduNetdiskDownload\yuanbao\PentestAI\pentestai\data\test_reports"
    os.makedirs(report_dir, exist_ok=True)
    report_path = os.path.join(report_dir, f"test_report_{time.strftime('%Y%m%d_%H%M%S')}.json")
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(f"\n测试报告已保存: {report_path}")

    return failed == 0


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
