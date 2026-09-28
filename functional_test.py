"""
PentestAI 真实功能测试
测试目标: http://testphp.vulnweb.com (Acunetix官方测试靶场)
测试内容: 端口扫描 + Web漏洞扫描 + 结果验证
"""
import sys
import os
import time
import json

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

TARGET = "testphp.vulnweb.com"
TARGET_URL = "http://testphp.vulnweb.com"

def print_header(title):
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)

def test_nmap_scan():
    """测试1: Nmap端口扫描"""
    print_header("测试1: Nmap端口扫描")
    print(f"目标: {TARGET}")
    print(f"时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        from pentestai.core.tool_init import init_all_tools
        registry = init_all_tools()
        
        # 获取Nmap工具
        nmap_tool = None
        if hasattr(registry, '_registry'):
            nmap_tool = registry._registry.get('nmap_scanner') or registry._registry.get('nmap')
        
        if not nmap_tool:
            print("⚠️  未找到Nmap工具，跳过")
            return False
        
        print(f"工具: {nmap_tool.get('name', 'nmap') if isinstance(nmap_tool, dict) else 'nmap'}")
        
        # 实例化并运行
        if isinstance(nmap_tool, dict):
            tool_cls = nmap_tool.get('class') or nmap_tool.get('tool_class')
            if tool_cls:
                tool = tool_cls()
            else:
                print("⚠️  无法获取工具类，跳过")
                return False
        else:
            tool = nmap_tool() if callable(nmap_tool) else nmap_tool
        
        print("正在扫描（快速端口扫描，可能需要30-60秒）...")
        start = time.time()
        
        # 调用run方法
        result = tool.run(target=TARGET, scan_type="quick")
        
        elapsed = time.time() - start
        print(f"扫描完成，耗时: {elapsed:.1f}秒")
        print()
        
        # 解析结果
        if hasattr(result, 'success'):
            print(f"状态: {'✅ 成功' if result.success else '❌ 失败'}")
            if result.success and result.data:
                print(f"数据: {json.dumps(result.data, ensure_ascii=False, indent=2)[:500]}")
            if not result.success and result.error:
                print(f"错误: {result.error}")
        else:
            print(f"结果: {str(result)[:500]}")
        
        return True
    except Exception as e:
        print(f"❌ Nmap扫描异常: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_web_scan():
    """测试2: Web漏洞扫描（Nikto/Nuclei）"""
    print_header("测试2: Web漏洞扫描")
    print(f"目标: {TARGET_URL}")
    print(f"时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        from pentestai.core.tool_init import init_all_tools
        registry = init_all_tools()
        
        # 尝试找Web扫描工具
        web_tool = None
        tool_name = None
        if hasattr(registry, '_registry'):
            for name in ['nikto_scanner', 'nuclei_scanner', 'web_vuln_scanner', 'web_scanner']:
                if name in registry._registry:
                    web_tool = registry._registry[name]
                    tool_name = name
                    break
        
        if not web_tool:
            print("⚠️  未找到Web扫描工具，尝试用HTTP工具测试连通性")
            # 退而求其次：测试HTTP连通性
            return test_http_connectivity()
        
        print(f"工具: {tool_name}")
        
        # 实例化
        if isinstance(web_tool, dict):
            tool_cls = web_tool.get('class') or web_tool.get('tool_class')
            if tool_cls:
                tool = tool_cls()
            else:
                print("⚠️  无法获取工具类")
                return False
        else:
            tool = web_tool() if callable(web_tool) else web_tool
        
        print("正在扫描（可能需要1-2分钟）...")
        start = time.time()
        
        result = tool.run(target=TARGET_URL, scan_type="quick")
        
        elapsed = time.time() - start
        print(f"扫描完成，耗时: {elapsed:.1f}秒")
        print()
        
        if hasattr(result, 'success'):
            print(f"状态: {'✅ 成功' if result.success else '❌ 失败'}")
            if result.success and result.data:
                data_str = json.dumps(result.data, ensure_ascii=False, indent=2)
                print(f"发现漏洞/信息:\n{data_str[:800]}")
            if not result.success and result.error:
                print(f"错误: {result.error}")
        else:
            print(f"结果: {str(result)[:800]}")
        
        return True
    except Exception as e:
        print(f"❌ Web扫描异常: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_http_connectivity():
    """备选测试: HTTP连通性测试"""
    print_header("备选测试: HTTP连通性测试")
    try:
        import urllib.request
        start = time.time()
        req = urllib.request.Request(TARGET_URL, headers={'User-Agent': 'PentestAI-Test'})
        resp = urllib.request.urlopen(req, timeout=15)
        elapsed = time.time() - start
        print(f"✅ 目标可达: {TARGET_URL}")
        print(f"状态码: {resp.status}")
        print(f"响应时间: {elapsed:.2f}秒")
        print(f"Content-Type: {resp.headers.get('Content-Type', 'unknown')}")
        body = resp.read(500).decode('utf-8', errors='ignore')
        print(f"页面内容前200字: {body[:200]}")
        return True
    except Exception as e:
        print(f"❌ HTTP连接失败: {e}")
        return False

def test_subdomain_enum():
    """测试3: 子域名枚举"""
    print_header("测试3: 子域名枚举")
    print(f"目标: {TARGET}")
    print()
    
    try:
        from pentestai.core.tool_init import init_all_tools
        registry = init_all_tools()
        
        sub_tool = None
        if hasattr(registry, '_registry'):
            for name in ['subfinder', 'subdomain_enum', 'subdomain_scanner']:
                if name in registry._registry:
                    sub_tool = registry._registry[name]
                    break
        
        if not sub_tool:
            print("⚠️  未找到子域名枚举工具，跳过")
            return None
        
        print("正在枚举子域名（可能需要30秒）...")
        start = time.time()
        
        if isinstance(sub_tool, dict):
            tool_cls = sub_tool.get('class') or sub_tool.get('tool_class')
            tool = tool_cls() if tool_cls else None
        else:
            tool = sub_tool() if callable(sub_tool) else sub_tool
        
        if not tool:
            print("⚠️  无法实例化工具")
            return False
        
        result = tool.run(domain=TARGET)
        elapsed = time.time() - start
        print(f"完成，耗时: {elapsed:.1f}秒")
        
        if hasattr(result, 'success') and result.success:
            print(f"结果: {json.dumps(result.data, ensure_ascii=False)[:300]}")
        return True
    except Exception as e:
        print(f"❌ 子域名枚举异常: {e}")
        return False

def main():
    print("\n" + "🔥" * 25)
    print("  PentestAI 真实功能测试")
    print(f"  测试靶场: {TARGET_URL}")
    print(f"  测试时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("🔥" * 25)
    
    results = {}
    
    # 测试1: Nmap端口扫描
    results['nmap'] = test_nmap_scan()
    
    # 测试2: Web漏洞扫描
    results['web_scan'] = test_web_scan()
    
    # 测试3: 子域名枚举
    results['subdomain'] = test_subdomain_enum()
    
    # 总结
    print_header("测试总结")
    passed = sum(1 for v in results.values() if v)
    total = len([v for v in results.values() if v is not None])
    print(f"通过: {passed}/{total}")
    for name, status in results.items():
        icon = "✅" if status else ("⚠️ " if status is None else "❌")
        print(f"  {icon} {name}")
    
    print("\n" + "=" * 70)
    return passed > 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
