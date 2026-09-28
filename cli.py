"""PentestAI 命令行模式
用法:
  python cli.py --target http://example.com --mode full
  python cli.py --target 192.168.1.1 --mode recon
  python cli.py --list-tools
  python cli.py --tool port_scanner --target 192.168.1.1
"""
import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pentestai.utils.config import config
from pentestai.utils.logger import setup_logger, get_logger
from pentestai.core.tool_init import init_all_tools
from pentestai.core.agent import PentestAgent

logger = get_logger("cli")


def run_scan(target: str, mode: str = "full", depth: str = "standard", output: str = ""):
    """运行扫描"""
    print("=" * 60)
    print("PentestAI - AI驱动的全功能渗透测试平台")
    print("=" * 60)
    print(f"目标: {target}")
    print(f"模式: {mode}")
    print(f"深度: {depth}")
    print("=" * 60)

    registry = init_all_tools()
    agent = PentestAgent(registry)

    # 构建用户输入
    mode_map = {
        "full": f"全面扫描 {target}",
        "recon": f"信息收集 {target}",
        "web": f"Web漏洞扫描 {target}",
        "poc": f"PoC验证 {target}",
    }
    user_input = mode_map.get(mode, f"扫描 {target}")

    def on_progress(event_type, data):
        if event_type == "thinking":
            print(f"\n[思考] {data}")
        elif event_type == "plan":
            tools = [s["tool"] for s in data]
            print(f"[计划] {' → '.join(tools)}")
        elif event_type == "tool_start":
            print(f"\n[{data.get('index', '?')}/{data.get('total', '?')}] 执行: {data.get('tool', '')}")
        elif event_type == "tool_end":
            status = "成功" if data.get("success") else "失败"
            findings = data.get("findings_count", 0)
            print(f"[完成] {data.get('tool', '')} - {status}" + (f" (发现{findings}个问题)" if findings else ""))

    agent.set_callback(on_progress)

    print("\n开始扫描...\n")
    result = agent.run(user_input)

    # 输出结果
    print("\n" + "=" * 60)
    print("扫描完成")
    print("=" * 60)

    if result.get("success"):
        summary = result.get("summary", {})
        findings = result.get("findings", [])

        print(f"风险评分: {summary.get('risk_score', 0)}/100 ({summary.get('risk_rating', 'N/A')})")
        print(f"发现问题: {len(findings)} 个")
        counts = summary.get("severity_counts", {})
        print(f"  严重: {counts.get('critical', 0)}, 高危: {counts.get('high', 0)}, "
              f"中危: {counts.get('medium', 0)}, 低危: {counts.get('low', 0)}, 信息: {counts.get('info', 0)}")

        # 高危问题
        high = [f for f in findings if f.get("severity") in ["critical", "high"]]
        if high:
            print(f"\n高危问题:")
            for i, f in enumerate(high[:10], 1):
                print(f"  {i}. [{f.get('severity', '').upper()}] {f.get('title', '')}")

        # 生成报告
        if findings:
            from pentestai.modules.report.report_gen import ReportGenerator
            gen = ReportGenerator()
            report = gen.run(
                findings=findings,
                target=target,
                duration=result.get("duration", 0),
                tools_count=result.get("tools_executed", 0),
            )
            if report.success:
                print(f"\n报告: {report.data.get('report_path', '')}")

        # 输出JSON
        if output:
            os.makedirs(output, exist_ok=True)
            json_path = os.path.join(output, "scan_result.json")
            with open(json_path, "w", encoding="utf-8") as f:
                json.dump(result, f, ensure_ascii=False, indent=2, default=str)
            print(f"JSON结果: {json_path}")

        return 0
    else:
        print(f"扫描失败: {result.get('error', '未知错误')}")
        return 1


def list_tools():
    """列出所有工具"""
    registry = init_all_tools()
    tools = registry.list_tools()
    print("可用工具列表:")
    print("-" * 70)
    categories = {}
    for t in tools:
        categories.setdefault(t.get("category", "other"), []).append(t)
    for cat, tools in categories.items():
        print(f"\n[{cat}]")
        for t in tools:
            print(f"  {t['name']:<25} {t['description']}")
    print(f"\n共 {len(tools)} 个工具")


def run_single_tool(tool_name: str, target: str, **kwargs):
    """运行单个工具"""
    registry = init_all_tools()
    tool = registry.get(tool_name)
    if not tool:
        print(f"工具不存在: {tool_name}")
        return 1

    print(f"执行工具: {tool_name}")
    print(f"目标: {target}")
    print("-" * 50)

    params = {"target": target}
    params.update(kwargs)
    result = registry.execute(tool_name, **params)

    print(f"状态: {'成功' if result.success else '失败'}")
    print(f"耗时: {result.duration:.2f}s")
    if result.error:
        print(f"错误: {result.error}")
    print(f"\n输出:\n{result.output}")
    if result.findings:
        print(f"\n发现 {len(result.findings)} 个问题:")
        for i, f in enumerate(result.findings, 1):
            print(f"  {i}. [{f.get('severity', '').upper()}] {f.get('title', '')}")
    return 0 if result.success else 1


def main():
    parser = argparse.ArgumentParser(
        description="PentestAI - AI驱动的全功能渗透测试平台",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python cli.py --target http://example.com --mode full
  python cli.py --target 192.168.1.1 --mode recon
  python cli.py --target http://test.com --mode web --depth deep
  python cli.py --tool port_scanner --target 192.168.1.1
  python cli.py --list-tools
        """
    )
    parser.add_argument("--target", help="目标URL/域名/IP")
    parser.add_argument("--mode", choices=["full", "recon", "web", "poc"], default="full",
                        help="扫描模式 (默认: full)")
    parser.add_argument("--depth", choices=["basic", "standard", "deep"], default="standard",
                        help="扫描深度 (默认: standard)")
    parser.add_argument("--tool", help="运行单个工具")
    parser.add_argument("--list-tools", action="store_true", help="列出所有可用工具")
    parser.add_argument("--output", help="JSON结果输出目录")
    parser.add_argument("--config", default="config.yaml", help="配置文件路径")

    args = parser.parse_args()

    config.load(args.config)
    setup_logger(level="INFO")

    if args.list_tools:
        list_tools()
        return 0

    if args.tool:
        if not args.target:
            print("错误: 使用--tool时需要指定--target")
            return 1
        return run_single_tool(args.tool, args.target)

    if not args.target:
        parser.print_help()
        return 1

    return run_scan(args.target, args.mode, args.depth, args.output)


if __name__ == "__main__":
    sys.exit(main())
