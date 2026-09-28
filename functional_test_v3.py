"""
PentestAI 真实功能测试 v3 - 用确切工具名
"""
import sys, os, time, json, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

TARGET = "www.baidu.com"

def print_header(t):
    print("\n" + "=" * 70)
    print(f"  {t}")
    print("=" * 70)

def get_tool(registry, name):
    """按确切名称获取并实例化工具"""
    if not hasattr(registry, '_registry'):
        return None
    entry = registry._registry.get(name)
    if not entry:
        return None
    if isinstance(entry, dict):
        for k in ['class', 'tool_class', 'cls']:
            v = entry.get(k)
            if v and callable(v):
                return v()
        if 'instance' in entry:
            return entry['instance']
    elif callable(entry):
        return entry()
    else:
        return entry
    return None

def test_port_scanner():
    """测试1: port_scanner (Nmap端口扫描)"""
    print_header("测试1: port_scanner 端口扫描 (Nmap引擎)")
    print(f"目标: {TARGET}")
    print()
    try:
        from pentestai.core.tool_init import init_all_tools
        # 预热两次确保所有工具注册完成
        init_all_tools()
        registry = init_all_tools()
        
        tool = get_tool(registry, 'port_scanner')
        if not tool:
            print("❌ 未找到port_scanner工具")
            # 列出所有可用工具名
            if hasattr(registry, '_registry'):
                print("可用工具:", sorted(registry._registry.keys())[:30])
            return False
        
        print(f"✅ 工具实例化成功: {type(tool).__name__}")
        print(f"方法: {[m for m in dir(tool) if not m.startswith('_') and callable(getattr(tool,m))][:8]}")
        print()
        print("正在扫描（80,443端口，可能需要30秒）...")
        start = time.time()
        
        # 尝试多种调用方式
        result = None
        last_err = None
        for kwargs in [
            {'target': TARGET, 'scan_type': 'quick'},
            {'target': TARGET, 'ports': '80,443'},
            {'target': TARGET},
            {'host': TARGET},
        ]:
            try:
                result = tool.run(**kwargs)
                last_err = None
                break
            except TypeError as e:
                last_err = e
                continue
            except Exception as e:
                last_err = e
                break
        
        elapsed = time.time() - start
        print(f"调用完成，耗时: {elapsed:.1f}秒")
        
        if last_err and result is None:
            print(f"❌ 调用失败: {last_err}")
            return False
        
        # 解析结果
        if hasattr(result, 'success'):
            print(f"状态: {'✅ 成功' if result.success else '❌ 失败'}")
            if result.success and result.data:
                print(f"结果: {json.dumps(result.data, ensure_ascii=False, indent=2, default=str)[:500]}")
            if not result.success and getattr(result, 'error', None):
                print(f"错误: {result.error}")
        elif result is not None:
            print(f"结果类型: {type(result).__name__}")
            print(f"结果: {str(result)[:500]}")
        return True
    except Exception as e:
        print(f"❌ 异常: {e}")
        import traceback; traceback.print_exc()
        return False

def test_web_scanner():
    """测试2: web_scanner (Web漏洞扫描)"""
    print_header("测试2: web_scanner Web扫描")
    print(f"目标: http://{TARGET}")
    print()
    try:
        from pentestai.core.tool_init import init_all_tools
        init_all_tools()
        registry = init_all_tools()
        
        tool = get_tool(registry, 'web_scanner')
        if not tool:
            print("❌ 未找到web_scanner工具")
            return False
        
        print(f"✅ 工具实例化成功: {type(tool).__name__}")
        print("正在扫描（可能需要30-60秒）...")
        start = time.time()
        
        result = None
        last_err = None
        for kwargs in [
            {'target': f'http://{TARGET}', 'scan_type': 'quick'},
            {'url': f'http://{TARGET}'},
            {'target': TARGET},
        ]:
            try:
                result = tool.run(**kwargs)
                last_err = None
                break
            except TypeError as e:
                last_err = e; continue
            except Exception as e:
                last_err = e; break
        
        elapsed = time.time() - start
        print(f"完成，耗时: {elapsed:.1f}秒")
        
        if last_err and result is None:
            print(f"❌ 调用失败: {last_err}")
            return False
        
        if hasattr(result, 'success'):
            print(f"状态: {'✅ 成功' if result.success else '❌ 失败'}")
            if result.success and result.data:
                print(f"结果: {json.dumps(result.data, ensure_ascii=False, indent=2, default=str)[:500]}")
        elif result is not None:
            print(f"结果: {str(result)[:500]}")
        return True
    except Exception as e:
        print(f"❌ 异常: {e}")
        import traceback; traceback.print_exc()
        return False

def test_nmap_engine_direct():
    """测试3: 直接调用Nmap引擎"""
    print_header("测试3: Nmap引擎直接调用验证")
    print(f"目标: {TARGET} (80,443端口)")
    print()
    try:
        nmap_path = r"C:\Program Files (x86)\Nmap\nmap.exe"
        if not os.path.exists(nmap_path):
            print("⚠️  Nmap未安装"); return None
        
        print(f"引擎路径: {nmap_path}")
        print("正在扫描...")
        start = time.time()
        r = subprocess.run([nmap_path, '-p', '80,443', '-T4', '--host-timeout', '30s', TARGET],
                          capture_output=True, text=True, timeout=45)
        elapsed = time.time() - start
        print(f"完成，耗时: {elapsed:.1f}秒，退出码: {r.returncode}")
        print()
        print("=== Nmap输出 ===")
        print(r.stdout[:600] if r.stdout else "(无输出)")
        if r.stderr:
            print(f"STDERR: {r.stderr[:200]}")
        
        has_open = 'open' in (r.stdout or '').lower()
        if r.returncode == 0:
            print(f"\n✅ Nmap引擎工作正常{'，发现开放端口' if has_open else ''}")
            return True
        return False
    except subprocess.TimeoutExpired:
        print("❌ 超时"); return False
    except Exception as e:
        print(f"❌ 异常: {e}"); return False

def main():
    print("\n" + "🔥" * 25)
    print("  PentestAI 真实功能测试 v3")
    print(f"  靶场: {TARGET}")
    print(f"  时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("🔥" * 25)
    
    results = {}
    results['port_scanner'] = test_port_scanner()
    results['web_scanner'] = test_web_scanner()
    results['nmap_engine'] = test_nmap_engine_direct()
    
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
    sys.exit(0 if main() else 1)
