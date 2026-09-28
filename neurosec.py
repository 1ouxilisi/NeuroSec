#!/usr/bin/env python3
"""
NeuroSec CLI
=============
AI驱动的安全测试平台命令行工具

Usage:
    neurosec scan <target>          # 扫描目标
    neurosec detect <text>          # 提示词注入检测
    neurosec leak <text>            # 数据泄露检测
    neurosec version               # 显示版本
    neurosec help                  # 显示帮助
"""
import sys
import os
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

VERSION = "v48.2"


def cmd_version():
    print(f"NeuroSec {VERSION}")
    print("AI-Driven Security Testing Platform")


def cmd_detect(text: str):
    """提示词注入检测"""
    from pentestai.modules.ai_security.prompt_injection_detector import PromptInjectionDetector
    detector = PromptInjectionDetector()
    result = detector.detect(text)

    print(f"输入: {text}")
    print(f"是否注入: {'是' if result.is_injection else '否'}")
    print(f"风险等级: {result.risk_level.value}")
    print(f"置信度: {result.confidence:.1%}")
    if result.injection_types:
        print(f"攻击类型: {', '.join(t.value for t in result.injection_types)}")
    if result.matched_patterns:
        print(f"匹配模式: {', '.join(result.matched_patterns[:5])}")


def cmd_leak(text: str):
    """数据泄露检测"""
    from pentestai.modules.ai_security.data_leakage_detector import DataLeakageDetector
    detector = DataLeakageDetector()
    safe, findings = detector.sanitize(text)

    print(f"发现泄露: {len(findings)} 处")
    for f in findings:
        print(f"  [{f.severity}] {f.description}: {f.matched_content[:30]}")
    print(f"\n脱敏后: {safe[:200]}")


def cmd_scan(target: str):
    """扫描目标（示例）"""
    print(f"[!] 扫描目标: {target}")
    print(f"[!] 此功能需要完整GUI版本，CLI仅做AI安全检测")
    print(f"[!] 运行 python main.py 启动完整GUI")


def cmd_help():
    print(__doc__)


def main():
    if len(sys.argv) < 2:
        cmd_help()
        sys.exit(0)

    command = sys.argv[1]
    args = sys.argv[2:]

    commands = {
        "version": cmd_version,
        "detect": lambda: cmd_detect(" ".join(args)) if args else print("用法: neurosec detect <text>"),
        "leak": lambda: cmd_leak(" ".join(args)) if args else print("用法: neurosec leak <text>"),
        "scan": lambda: cmd_scan(args[0]) if args else print("用法: neurosec scan <target>"),
        "help": cmd_help,
    }

    if command in commands:
        commands[command]()
    else:
        print(f"未知命令: {command}")
        cmd_help()


if __name__ == "__main__":
    main()
