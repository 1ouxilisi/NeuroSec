"""
PentestAI 区块链安全深度测试
测试合约: VulnerableToken.sol (含10种常见漏洞)
"""
import sys, os, time, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

CONTRACT_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "test_contracts", "VulnerableToken.sol")

def print_header(t):
    print("\n" + "=" * 70)
    print(f"  {t}")
    print("=" * 70)

def main():
    print("\n" + "🔗" * 25)
    print("  PentestAI 区块链安全深度测试")
    print(f"  测试合约: {CONTRACT_PATH}")
    print(f"  时间: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    print("🔗" * 25)
    
    results = {}
    
    # 1. 智能合约审计
    print_header("1. 智能合约审计 (ContractAuditor)")
    try:
        from pentestai.modules.blockchain.contract_auditor import ContractAuditor
        tool = ContractAuditor()
        print(f"✅ 实例化: {type(tool).__name__}")
        print(f"合约路径: {CONTRACT_PATH}")
        print(f"文件存在: {os.path.exists(CONTRACT_PATH)}")
        
        if os.path.exists(CONTRACT_PATH):
            print("正在审计...")
            start = time.time()
            # 尝试多种调用方式
            result = None
            for kwargs in [
                {'contract_path': CONTRACT_PATH},
                {'file_path': CONTRACT_PATH},
                {'target': CONTRACT_PATH},
                {'contract': CONTRACT_PATH},
            ]:
                try:
                    result = tool.run(**kwargs)
                    break
                except TypeError:
                    continue
                except Exception as e:
                    print(f"调用异常: {str(e)[:100]}")
                    break
            
            elapsed = time.time() - start
            print(f"耗时: {elapsed:.1f}秒")
            
            if result and hasattr(result, 'success'):
                print(f"状态: {'✅ 成功' if result.success else '❌ 失败'}")
                if result.success and result.data:
                    print("审计结果:")
                    print(json.dumps(result.data, ensure_ascii=False, indent=2, default=str)[:800])
                    results['contract_audit'] = result.data
                if not result.success and getattr(result, 'error', None):
                    print(f"错误: {str(result.error)[:200]}")
            elif result:
                print(f"结果: {str(result)[:500]}")
                results['contract_audit'] = str(result)[:500]
        else:
            print("⚠️  合约文件不存在")
    except Exception as e:
        print(f"❌ 异常: {str(e)[:150]}")
        import traceback; traceback.print_exc()
    
    # 2. 区块链安全引擎
    print_header("2. 区块链安全引擎 (BlockchainSecurityEngine)")
    try:
        from pentestai.modules.blockchain.blockchain_security_engine import BlockchainSecurityEngine
        tool = BlockchainSecurityEngine()
        print(f"✅ 实例化: {type(tool).__name__}")
        print(f"名称: {getattr(tool, 'name', 'N/A')}")
        print(f"分类: {getattr(tool, 'category', 'N/A')}")
        results['blockchain_engine'] = "实例化成功"
    except Exception as e:
        print(f"❌ 异常: {str(e)[:150]}")
    
    # 3. 区块链安全引擎v4
    print_header("3. 区块链安全引擎v4 (BlockchainSecurityEngineV4)")
    try:
        from pentestai.modules.blockchain.blockchain_security_engine_v4 import BlockchainSecurityEngineV4
        tool = BlockchainSecurityEngineV4()
        print(f"✅ 实例化: {type(tool).__name__}")
        print(f"名称: {getattr(tool, 'name', 'N/A')}")
        results['blockchain_engine_v4'] = "实例化成功"
    except Exception as e:
        print(f"❌ 异常: {str(e)[:150]}")
    
    # 总结
    print_header("区块链安全测试总结")
    success_count = sum(1 for v in results.values() if v)
    print(f"测试模块: 3个")
    print(f"成功: {success_count}/3")
    print()
    
    # 预期漏洞清单（用于对比）
    print("测试合约预期包含的10种漏洞:")
    vulns = [
        "1. 整数溢出 (unchecked -= / +=)",
        "2. 重入攻击 (withdraw先转账后更新状态)",
        "3. 权限控制缺失 (mint无onlyOwner)",
        "4. 未检查返回值 (transferFrom未检查allowance)",
        "5. 时间戳依赖 (block.timestamp做随机数)",
        "6. 未初始化存储指针",
        "7. 可见性问题 (emergencyWithdraw为public)",
        "8. DoS无限循环 (distributeRewards)",
        "9. 短地址攻击 (setName未校验长度)",
        "10. 未处理外部调用返回值 (sendEther)",
    ]
    for v in vulns:
        print(f"  {v}")
    
    # 保存报告
    report = {
        "test_contract": CONTRACT_PATH,
        "scan_time": time.strftime('%Y-%m-%d %H:%M:%S'),
        "modules_tested": 3,
        "modules_success": success_count,
        "expected_vulnerabilities": 10,
        "vulnerability_list": vulns,
        "results": results
    }
    
    report_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "blockchain_security_report.json")
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, ensure_ascii=False, indent=2, default=str)
    print(f"\n报告已保存: {report_path}")
    print("\n" + "=" * 70)
    
    return success_count > 0

if __name__ == "__main__":
    sys.exit(0 if main() else 1)
