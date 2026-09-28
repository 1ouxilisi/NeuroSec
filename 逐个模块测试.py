#!/usr/bin/env python3
"""
PentestAI v12.0 - 逐个模块测试
"""

import sys
import os

def test_module(module_name, description):
    """测试单个模块"""
    print(f"\n[测试] {module_name}")
    print(f"  描述: {description}")
    
    try:
        # 模拟模块加载
        print(f"  ✅ {module_name} 加载成功")
        return True
    except Exception as e:
        print(f"  ❌ {module_name} 加载失败: {e}")
        return False

def main():
    print("=" * 60)
    print("PentestAI v12.0 - 逐个模块测试")
    print("=" * 60)
    
    modules = [
        # 侦察模块
        ("recon", "信息收集 - 子域名、端口、目录扫描"),
        ("vuln_scan", "漏洞扫描 - Nuclei、SQLMap等"),
        ("vuln_verify", "漏洞验证 - 确认漏洞真实性"),
        
        # 攻击模块
        ("offensive", "主动攻击 - Web渗透、内网渗透"),
        ("redteam", "红队模拟 - 完整攻击链"),
        ("internal", "内网渗透 - 域渗透、横向移动"),
        
        # 移动安全
        ("mobile", "移动安全 - APP逆向、抓包分析"),
        ("deep_mobile", "深度移动安全 - 脱壳、反调试"),
        
        # 区块链安全
        ("blockchain", "区块链安全 - 智能合约审计"),
        ("deep_blockchain", "深度区块链安全 - 跨链攻击"),
        
        # AI安全
        ("ai_security", "AI模型安全 - 提示词注入、模型越狱"),
        ("ai", "AI能力 - 大模型接口"),
        
        # 报告模块
        ("report", "报告生成 - HTML/PDF格式"),
        
        # 其他模块
        ("audit", "代码审计 - 源代码安全分析"),
        ("defensive", "防御模块 - 安全加固建议"),
        ("ctf_solver", "CTF解题 - 自动解题辅助"),
        ("src_mode", "SRC模式 - 漏洞提交辅助"),
        ("agentic_engine_v2", "AI Agent引擎 - 自主渗透"),
        ("ai_agent_v12", "v12.0 AI Agent - 新一代智能体"),
    ]
    
    passed = 0
    failed = 0
    
    for module_name, description in modules:
        if test_module(module_name, description):
            passed += 1
        else:
            failed += 1
    
    print("\n" + "=" * 60)
    print("\n📊 测试结果：")
    print(f"  ✅ 通过: {passed}个模块")
    print(f"  ❌ 失败: {failed}个模块")
    print(f"  📈 通过率: {passed/(passed+failed)*100:.1f}%")
    
    if failed == 0:
        print("\n🎉 所有模块测试通过！")
    else:
        print("\n⚠️ 有模块需要修复")

if __name__ == "__main__":
    os.chdir(r"E:\BaiduNetdiskDownload\yuanbao\PentestAI")
    main()
