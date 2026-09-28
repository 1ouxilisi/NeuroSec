"""
PentestAI 实战测试 - 用测试数据跑完整扫描
直接导入工具类，绕过注册表
测试目标: www.baidu.com
"""
import sys, os, time, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def print_header(t):
    print("\n" + "=" * 70)
    print(f"  {t}")
    print("=" * 70)

def test_port_scanner():
    """实战1: PortScanner 端口扫描"""
    print_header("实战1: PortScanner 端口扫描")
    print("测试数据:")
    print("  目标: www.baidu.com")
    print("  端口: 80, 443, 22, 21, 3306, 3389")
    print("  深度: quick")
    print()
    
    try:
        from pentestai.modules.recon.port_scanner import PortScanner
        tool = PortScanner()
        print(f"✅ 工具实例化: {type(tool).__name__}")
        print(f"   名称: {getattr(tool, 'name', 'N/A')}")
        print(f"   分类: {getattr(tool, 'category', 'N/A')}")
        print()
        
        print("正在扫描（可能需要30-60秒）...")
        start = time.time()
        
        result = tool.run(
            target="www.baidu.com",
            depth="quick",
            ports=[80, 443, 22, 21, 3306, 3389]
        )
        
        elapsed = time.time() - start
        print(f"扫描完成，耗时: {elapsed:.1f}秒")
        print()
        
        # 解析结果
        if hasattr(result, 'success'):
            print(f"状态: {'✅ 成功' if result.success else '❌ 失败'}")
            if result.success and result.data:
                print("扫描结果:")
                print(json.dumps(result.data, ensure_ascii=False, indent=2, default=str)[:800])
            if not result.success and getattr(result, 'error', None):
                print(f"错误: {result.error}")
        else:
            print(f"结果类型: {type(result).__name__}")
            print(f"结果: {str(result)[:800]}")
        
        return result
    except Exception as e:
        print(f"❌ 异常: {e}")
        import traceback; traceback.print_exc()
        return None

def test_web_scanner():
    """实战2: WebScanner Web漏洞扫描"""
    print_header("实战2: WebScanner Web漏洞扫描")
    print("测试数据:")
    print("  目标: http://www.baidu.com")
    print("  深度: quick")
    print()
    
    try:
        from pentestai.modules.vuln_scan.web_scanner import WebScanner
        tool = WebScanner()
        print(f"✅ 工具实例化: {type(tool).__name__}")
        print(f"   名称: {getattr(tool, 'name', 'N/A')}")
        print(f"   分类: {getattr(tool, 'category', 'N/A')}")
        print()
        
        print("正在扫描（可能需要30-60秒）...")
        start = time.time()
        
        result = tool.run(
            target="http://www.baidu.com",
            depth="quick"
        )
        
        elapsed = time.time() - start
        print(f"扫描完成，耗时: {elapsed:.1f}秒")
        print()
        
        if hasattr(result, 'success'):
            print(f"状态: {'✅ 成功' if result.success else '❌ 失败'}")
            if result.success and result.data:
                print("扫描结果:")
                print(json.dumps(result.data, ensure_ascii=False, indent=2, default=str)[:800])
            if not result.success and getattr(result, 'error', None):
                print(f"错误: {result.error}")
        else:
            print(f"结果类型: {type(result).__name__}")
            print(f"结果: {str(result)[:800]}")
        
        return result
    except Exception as e:
        print(f"❌ 异常: {e}")
        import traceback; traceback.print_exc()
        return None

def test_subdomain_enum():
    """实战3: 子域名枚举"""
    print_header("实战3: 子域名枚举")
    print("测试数据:")
    print("  域名: baidu.com")
    print()
    
    try:
        from pentestai.modules.recon.subdomain_enum import SubdomainEnumerator
        tool = SubdomainEnumerator()
        print(f"✅ 工具实例化: {type(tool).__name__}")
        print()
        
        print("正在枚举（可能需要30秒）...")
        start = time.time()
        
        result = tool.run(domain="baidu.com")
        
        elapsed = time.time() - start
        print(f"完成，耗时: {elapsed:.1f}秒")
        print()
        
        if hasattr(result, 'success'):
            print(f"状态: {'✅ 成功' if result.success else '❌ 失败'}")
            if result.success and result.data:
                print("结果:")
                print(json.dumps(result.data, ensure_ascii=False, indent=2, default=str)[:500])
        else:
            print(f"结果: {str(result)[:500]}")
        
        return result
    except Exception as e:
        print(f"❌ 异常: {e}")
        import traceback; traceback.print_exc()
        return None

def generate_report(results):
    """生成测试报告"""
    print_header("测试报告生成")
    report = {
        "test_time": time.strftime('%Y-%m-%d %H:%M:%S'),
        "target": "www.baidu.com",
        "tools_tested": [],
        "summary": {}
    }
    
    for name, result in results.items():
        item = {"tool": name, "status": "unknown"}
        if result is None:
            item["status"] = "error"
        elif hasattr(result, 'success'):
            item["status"] = "success" if result.success else "failed"
            item["data"] = result.data if result.success else None
            item["error"] = result.error if not result.success else None
        report["tools_tested"].append(item)
    
    passed = sum(1 for i in report["tools_tested"] if i["status"] == "success")
    total = len(report["tools_tested"])
    report["summary"] = {"passed": passed, "total": total, "rate": f"{passed/total*100:.0f}%" if total else "0%"}
    
    # 保存报告
    report_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_report.json")
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2, default=str)
    
    print(f"✅ 测试报告已保存: {report_path}")
    print(f"   通过: {passed}/{total} ({report['summary']['rate']})")
    return report

def main():
    print("\n" + "🎯" * 25)
    print("  PentestAI 实战测试 - 测试数据驱动")
    print(f"  测试目标: www.baidu.com")
    print(f"  测试时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("🎯" * 25)
    
    results = {}
    
    # 实战1: 端口扫描
    results['port_scanner'] = test_port_scanner()
    
    # 实战2: Web扫描
    results['web_scanner'] = test_web_scanner()
    
    # 实战3: 子域名枚举
    results['subdomain_enum'] = test_subdomain_enum()
    
    # 生成报告
    report = generate_report(results)
    
    # 最终总结
    print_header("最终总结")
    print(f"测试工具: {len(report['tools_tested'])}个")
    print(f"通过: {report['summary']['passed']}/{report['summary']['total']}")
    print(f"通过率: {report['summary']['rate']}")
    print()
    for item in report['tools_tested']:
        icon = "✅" if item['status'] == 'success' else "❌"
        print(f"  {icon} {item['tool']}: {item['status']}")
    print("\n" + "=" * 70)
    
    return report['summary']['passed'] > 0

if __name__ == "__main__":
    sys.exit(0 if main() else 1)
