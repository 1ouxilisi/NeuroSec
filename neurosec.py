#!/usr/bin/env python3
"""
NeuroSec CLI - AI Security Scanner
====================================
Usage:
    neurosec scan <text>           # 一站式安全扫描
    neurosec detect <text>         # 提示词注入检测
    neurosec leak <text>           # 数据泄露检测
    neurosec owasp <text>          # OWASP LLM Top 10检查
    neurosec report <text>         # 生成HTML报告
    neurosec web                   # 启动Web Demo
    neurosec version               # 显示版本
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

VERSION = "v48.4"


def cmd_scan(text: str):
    """一站式扫描"""
    from pentestai.modules.ai_security.orchestrator import SecurityOrchestrator
    orch = SecurityOrchestrator()
    result = orch.scan_input(text)

    print(f"风险评分: {result.risk_score:.1f} / 10")
    print(f"风险等级: {result.risk_level}")
    print(f"检测耗时: {result.scan_time_ms}ms")
    print(f"提示词注入: {'是' if result.injection_detected else '否'}")
    if result.injection_types:
        print(f"  类型: {', '.join(result.injection_types)}")
    print(f"数据泄露: {result.leak_count} 处")
    if result.owasp_findings:
        print(f"OWASP风险: {', '.join(f['id'] for f in result.owasp_findings)}")
    if result.suggestions:
        print(f"\n修复建议:")
        for s in result.suggestions:
            print(f"  - {s}")


def cmd_detect(text: str):
    from pentestai.modules.ai_security import PromptInjectionDetector
    d = PromptInjectionDetector()
    r = d.detect(text)
    print(f"注入: {'是' if r.is_injection else '否'} | 风险: {r.risk_level.value} | 置信度: {r.confidence:.0%}")


def cmd_leak(text: str):
    from pentestai.modules.ai_security import DataLeakageDetector
    d = DataLeakageDetector()
    safe, findings = d.sanitize(text)
    print(f"泄露: {len(findings)} 处")
    for f in findings:
        print(f"  [{f.severity}] {f.description}")


def cmd_owasp(text: str):
    from pentestai.modules.ai_security.owasp_llm_top10 import OWASLLMTop10Checker
    checker = OWASLLMTop10Checker()
    findings = checker.run_full_check(text)
    print(f"OWASP检查: {len(findings)} 个风险")
    for f in findings:
        print(f"  [{f.risk_id}] {f.risk_name}: {f.severity}")


def cmd_report(text: str):
    from pentestai.modules.ai_security.orchestrator import SecurityOrchestrator
    orch = SecurityOrchestrator()
    orch.scan_input(text)
    orch.generate_report("security_report.html")
    print("报告已生成: security_report.html")


def cmd_web():
    print("启动Web Demo... http://localhost:8000")
    os.system("python web/app.py")


def cmd_version():
    print(f"NeuroSec {VERSION}")
    print("AI-Driven Security Testing Platform")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(0)

    cmd = sys.argv[1]
    args = " ".join(sys.argv[2:])

    commands = {
        "scan": lambda: cmd_scan(args),
        "detect": lambda: cmd_detect(args),
        "leak": lambda: cmd_leak(args),
        "owasp": lambda: cmd_owasp(args),
        "report": lambda: cmd_report(args),
        "web": cmd_web,
        "version": cmd_version,
    }

    if cmd in commands:
        commands[cmd]()
    else:
        print(f"未知命令: {cmd}")
        print(__doc__)


if __name__ == "__main__":
    main()
