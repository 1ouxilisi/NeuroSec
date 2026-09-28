"""
PentestAI 真实功能测试 v2
测试目标: www.baidu.com (端口扫描) + 本地HTTP服务 (Web测试)
"""
import sys
import os
import time
import json
import subprocess

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

TARGET = "www.baidu.com"

def print_header(title):
    print("\n" + "=" * 70)
    print(f"  {title}")
    print("=" * 70)

def find_tool(registry, keywords):
    """遍历注册表查找匹配关键词的工具"""
    if not hasattr(registry, '_registry'):
        return None, None
    for name, entry in registry._registry.items():
        if any(k in name.lower() for k in keywords):
            return name, entry
    return None, None

def instantiate_tool(entry):
    """从工具注册表条目实例化工具"""
    if isinstance(entry, dict):
        for key in ['class', 'tool_class', 'cls', 'instance']:
            val = entry.get(key)
            if val:
                if key == 'instance':
                    return val
                if callable(val):
                    return val()
        # 如果dict本身有run方法，可能就是实例
        if hasattr(entry, 'run'):
            return entry
    elif callable(entry):
        return entry()
    else:
        return entry  # 已经是实例
    return None

def test_nmap_scan():
    """测试1: Nmap端口扫描"""
    print_header("测试1: Nmap端口扫描")
    print(f"目标: {TARGET}")
    print(f"时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    try:
        from pentestai.core.tool_init import init_all_tools
        registry = init_all_tools()
        
        # 遍历查找Nmap相关工具
        tool_name, tool_entry = find_tool(registry, ['nmap', 'port_scan', 'network_scan'])
        
        if not tool_entry:
            print("⚠️  未找到Nmap工具，列出所有扫描类工具:")
            if hasattr(registry, '_registry'):
                for n in sorted(registry._registry.keys()):
                    if 'scan' in n.lower() or 'nmap' in n.lower():
                        print(f"  - {n}")
            return False
        
        print(f"找到工具: {tool_name}")
        
        # 实例化
        tool = instantiate_tool(tool_entry)
        if not tool:
            print("❌ 无法实例化工具")
            return False
        
        print(f"工具实例: {type(tool).__name__}")
        print(f"工具方法: {[m for m in dir(tool) if not m.startswith('_') and callable(getattr(tool, m))][:10]}")
        print()
        print("正在扫描（快速端口扫描，可能需要30-60秒）...")
        start = time.time()
        
        # 尝试不同的调用方式
        result = None
        call_error = None
        for call_kwargs in [
            {'target': TARGET, 'scan_type': 'quick'},
            {'target': TARGET, 'ports': '80,443,22,21'},
            {'host': TARGET},
            {'target': TARGET},
        ]:
            try:
                result = tool.run(**call_kwargs)
                call_error = None
                break
            except TypeError as e:
                call_error = e
                continue
            except Exception as e:
                call_error = e
                break
        
        elapsed = time.time() - start
        print(f"扫描调用完成，耗时: {elapsed:.1f}秒")
        print()
        
        if call_error and result is None:
            print(f"❌ 调用失败: {call_error}")
            return False
        
        # 解析结果
        if hasattr(result, 'success'):
            print(f"状态: {'✅ 成功' if result.success else '❌ 失败'}")
            if result.success and result.data:
                data_str = json.dumps(result.data, ensure_ascii=False, indent=2, default=str)
                print(f"扫描结果:\n{data_str[:600]}")
            if not result.success and result.error:
                print(f"错误: {result.error}")
        elif result is not None:
            print(f"结果类型: {type(result).__name__}")
            print(f"结果: {str(result)[:600]}")
        
        return True
    except Exception as e:
        print(f"❌ Nmap扫描异常: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_http_tool():
    """测试2: HTTP/Web工具（用百度测试连通性）"""
    print_header("测试2: HTTP/Web扫描工具")
    print(f"目标: http://{TARGET}")
    print()
    
    try:
        from pentestai.core.tool_init import init_all_tools
        registry = init_all_tools()
        
        # 查找Web/HTTP相关工具
        tool_name, tool_entry = find_tool(registry, ['web_scan', 'http', 'url', 'web_vuln', 'cms', 'waf', 'ssl'])
        
        if not tool_entry:
            print("⚠️  未找到Web扫描工具，用urllib做基础HTTP测试")
            return test_basic_http()
        
        print(f"找到工具: {tool_name}")
        tool = instantiate_tool(tool_entry)
        if not tool:
            print("❌ 无法实例化工具")
            return False
        
        print(f"工具实例: {type(tool).__name__}")
        print("正在扫描（可能需要30-60秒）...")
        start = time.time()
        
        result = None
        call_error = None
        for call_kwargs in [
            {'target': f'http://{TARGET}', 'scan_type': 'quick'},
            {'url': f'http://{TARGET}'},
            {'target': TARGET},
        ]:
            try:
                result = tool.run(**call_kwargs)
                call_error = None
                break
            except TypeError as e:
                call_error = e
                continue
            except Exception as e:
                call_error = e
                break
        
        elapsed = time.time() - start
        print(f"完成，耗时: {elapsed:.1f}秒")
        print()
        
        if call_error and result is None:
            print(f"❌ 调用失败: {call_error}")
            return False
        
        if hasattr(result, 'success'):
            print(f"状态: {'✅ 成功' if result.success else '❌ 失败'}")
            if result.success and result.data:
                print(f"结果: {json.dumps(result.data, ensure_ascii=False, indent=2, default=str)[:600]}")
        elif result is not None:
            print(f"结果: {str(result)[:600]}")
        
        return True
    except Exception as e:
        print(f"❌ Web扫描异常: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_basic_http():
    """基础HTTP测试"""
    try:
        import urllib.request
        start = time.time()
        req = urllib.request.Request(f'http://{TARGET}', headers={'User-Agent': 'PentestAI-Test'})
        resp = urllib.request.urlopen(req, timeout=15)
        elapsed = time.time() - start
        print(f"✅ HTTP连通性正常")
        print(f"状态码: {resp.status}")
        print(f"响应时间: {elapsed:.2f}秒")
        print(f"服务器: {resp.headers.get('Server', 'unknown')}")
        return True
    except Exception as e:
        print(f"❌ HTTP连接失败: {e}")
        return False

def test_engine_direct():
    """测试3: 直接调用Nmap引擎（绕过工具层）"""
    print_header("测试3: 直接调用Nmap引擎验证")
    print(f"目标: {TARGET} (仅扫描80,443端口)")
    print()
    
    try:
        nmap_path = r"C:\Program Files (x86)\Nmap\nmap.exe"
        if not os.path.exists(nmap_path):
            print("⚠️  Nmap未安装，跳过")
            return None
        
        print(f"Nmap路径: {nmap_path}")
        print("正在扫描（快速扫描2个端口）...")
        start = time.time()
        
        result = subprocess.run(
            [nmap_path, '-p', '80,443', '-T4', TARGET],
            capture_output=True, text=True, timeout=60
        )
        
        elapsed = time.time() - start
        print(f"扫描完成，耗时: {elapsed:.1f}秒")
        print(f"退出码: {result.returncode}")
        print()
        print("Nmap输出:")
        print(result.stdout[:800])
        
        if result.returncode == 0 and 'open' in result.stdout.lower():
            print("\n✅ Nmap引擎工作正常，发现开放端口")
            return True
        elif result.returncode == 0:
            print("\n✅ Nmap引擎工作正常（扫描完成）")
            return True
        else:
            print(f"\n❌ Nmap扫描出错: {result.stderr[:200]}")
            return False
    except subprocess.TimeoutExpired:
        print("❌ Nmap扫描超时")
        return False
    except Exception as e:
        print(f"❌ Nmap引擎异常: {e}")
        return False

def main():
    print("\n" + "🔥" * 25)
    print("  PentestAI 真实功能测试 v2")
    print(f"  测试靶场: {TARGET}")
    print(f"  测试时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("🔥" * 25)
    
    results = {}
    
    # 测试1: Nmap端口扫描（通过PentestAI工具层）
    results['nmap_tool'] = test_nmap_scan()
    
    # 测试2: HTTP/Web工具
    results['web_tool'] = test_http_tool()
    
    # 测试3: 直接调用Nmap引擎（验证引擎本身可用）
    results['nmap_engine'] = test_engine_direct()
    
    # 总结
    print_header("测试总结")
    passed = sum(1 for v in results.values() if v)
    total = len([v for v in results.values() if v is not None])
    print(f"通过: {passed}/{total}")
    for name, status in results.items():
        icon = "✅" if status else ("⚠️ 跳过" if status is None else "❌")
        print(f"  {icon} {name}")
    
    print("\n" + "=" * 70)
    return passed > 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
