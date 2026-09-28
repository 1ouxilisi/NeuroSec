"""
PentestAI DVWA靶场实战扫描
目标: http://localhost:8080
覆盖: 端口扫描/Web爬虫/技术指纹/WAF检测/Web漏洞扫描/目录爆破
"""
import sys, os, time, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

TARGET = "http://localhost:8082"
HOST = "localhost"

def print_header(t):
    print("\n" + "=" * 70)
    print(f"  {t}")
    print("=" * 70)

def run_tool(name, import_path, class_name, target, **kwargs):
    """运行工具并返回结果"""
    print(f"\n--- {name} ---")
    try:
        module = __import__(import_path, fromlist=[class_name])
        cls = getattr(module, class_name)
        tool = cls()
        print(f"  ✅ 实例化: {type(tool).__name__}")
        print(f"  目标: {target}")
        print(f"  正在扫描...")
        start = time.time()
        result = tool.run(target=target, **kwargs)
        elapsed = time.time() - start
        print(f"  耗时: {elapsed:.1f}秒")
        if hasattr(result, 'success'):
            print(f"  状态: {'✅ 成功' if result.success else '❌ 失败'}")
            if result.success and result.data:
                return result.data
            if not result.success and getattr(result, 'error', None):
                print(f"  错误: {str(result.error)[:200]}")
        return None
    except Exception as e:
        print(f"  ❌ 异常: {str(e)[:150]}")
        return None

def main():
    print("\n" + "🎯" * 25)
    print("  PentestAI DVWA靶场实战扫描")
    print(f"  目标: {TARGET}")
    print(f"  时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("🎯" * 25)
    
    all_results = {}
    
    # 1. 端口扫描
    print_header("1. 端口扫描")
    all_results['port_scan'] = run_tool(
        "端口扫描", "pentestai.modules.recon.port_scanner", "PortScanner",
        HOST, ports=[8082, 80, 443, 22, 3306, 21], depth="quick"
    )
    
    # 2. 技术指纹识别
    print_header("2. 技术指纹识别")
    all_results['tech_detect'] = run_tool(
        "技术指纹", "pentestai.modules.recon.tech_detector", "TechDetector",
        TARGET
    )
    
    # 3. WAF检测
    print_header("3. WAF检测")
    all_results['waf_detect'] = run_tool(
        "WAF检测", "pentestai.modules.recon.waf_detector", "WAFDetector",
        TARGET
    )
    
    # 4. Web爬虫
    print_header("4. Web爬虫")
    all_results['web_spider'] = run_tool(
        "Web爬虫", "pentestai.modules.recon.web_spider", "WebSpider",
        TARGET
    )
    
    # 5. 目录爆破
    print_header("5. 目录爆破")
    all_results['dir_brute'] = run_tool(
        "目录爆破", "pentestai.modules.recon.dir_bruter", "DirBruter",
        TARGET
    )
    
    # 6. Web漏洞扫描（核心）
    print_header("6. Web漏洞扫描（核心）")
    all_results['web_vuln'] = run_tool(
        "Web漏洞扫描", "pentestai.modules.vuln_scan.web_scanner", "WebScanner",
        TARGET, depth="quick"
    )
    
    # 总结
    print_header("DVWA实战扫描总结")
    success_count = sum(1 for v in all_results.values() if v is not None)
    print(f"扫描模块: {len(all_results)}个")
    print(f"成功: {success_count}/{len(all_results)}")
    print()
    
    # 统计漏洞
    vuln_count = 0
    if all_results.get('web_vuln'):
        vuln_data = all_results['web_vuln']
        if isinstance(vuln_data, dict):
            if 'vulnerabilities' in vuln_data:
                vuln_count = len(vuln_data['vulnerabilities'])
            elif 'findings' in vuln_data:
                vuln_count = len(vuln_data['findings'])
    
    print(f"发现漏洞: {vuln_count}个")
    print()
    
    # 保存完整报告
    report = {
        "target": TARGET,
        "scan_time": time.strftime('%Y-%m-%d %H:%M:%S'),
        "modules_tested": len(all_results),
        "modules_success": success_count,
        "vulnerabilities_found": vuln_count,
        "detailed_results": {k: v for k, v in all_results.items() if v}
    }
    
    report_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dvwa_scan_report.json")
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2, default=str)
    print(f"完整报告已保存: {report_path}")
    print("\n" + "=" * 70)
    
    return success_count > 0

if __name__ == "__main__":
    sys.exit(0 if main() else 1)
