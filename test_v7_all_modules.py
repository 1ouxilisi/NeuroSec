"""
PentestAI v7.0 全模块测试脚本
测试所有49个核心模块
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def test_all_modules():
    """测试所有模块"""
    print("=" * 60)
    print("PentestAI v7.0 全模块测试")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    # P0级模块
    print("\n【P0级模块】")
    p0_modules = [
        ("真实业务漏洞库", "pentestai.core.real_vuln_db", "RealVulnDB"),
        ("WAF绕过引擎", "pentestai.core.waf_bypass_engine", "WAFBypassEngine"),
        ("大模型API优化", "pentestai.core.ai_api_optimizer", "AIAPIOptimizer"),
        ("报告生成器v3", "pentestai.core.report_generator_v3", "ReportGeneratorV3"),
    ]
    
    for name, module, cls in p0_modules:
        try:
            mod = __import__(module, fromlist=[cls])
            obj = getattr(mod, cls)()
            print(f"  ✅ {name}")
            passed += 1
        except Exception as e:
            print(f"  ❌ {name}: {e}")
            failed += 1
    
    # P1级模块
    print("\n【P1级模块】")
    p1_modules = [
        ("误报过滤v3", "pentestai.core.fp_filter_v3", "FPFilterV3"),
        ("批量扫描引擎", "pentestai.core.batch_scanner", "BatchScanner"),
        ("自动续扫引擎", "pentestai.core.auto_scan", "AutoScan"),
        ("用户体验优化", "pentestai.core.ux_optimizer", "UXOptimizer"),
    ]
    
    for name, module, cls in p1_modules:
        try:
            mod = __import__(module, fromlist=[cls])
            obj = getattr(mod, cls)()
            print(f"  ✅ {name}")
            passed += 1
        except Exception as e:
            print(f"  ❌ {name}: {e}")
            failed += 1
    
    # P2级模块
    print("\n【P2级模块】")
    p2_modules = [
        ("代码审计引擎v2", "pentestai.core.code_audit_v3", "CodeAuditV2"),
        ("内网横向移动引擎", "pentestai.core.lateral_movement_v2", "LateralMovementV2"),
        ("区块链深度审计", "pentestai.core.blockchain_audit_v2", "BlockchainAuditV2"),
        ("企业级API v2", "pentestai.core.enterprise_api_v2", "EnterpriseAPI"),
    ]
    
    for name, module, cls in p2_modules:
        try:
            mod = __import__(module, fromlist=[cls])
            obj = getattr(mod, cls)()
            print(f"  ✅ {name}")
            passed += 1
        except Exception as e:
            print(f"  ❌ {name}: {e}")
            failed += 1
    
    # P3级模块
    print("\n【P3级模块】")
    p3_modules = [
        ("AI自主渗透v3", "pentestai.core.ai_autonomous_v3", "AIAutoPentestV3"),
        ("多用户协作", "pentestai.core.multi_user_v1", "MultiUserV1"),
        ("漏洞知识库v3", "pentestai.core.vuln_kb_v3", "VulnKBV3"),
        ("可视化大屏", "pentestai.core.dashboard_v1", "DashboardV1"),
    ]
    
    for name, module, cls in p3_modules:
        try:
            mod = __import__(module, fromlist=[cls])
            obj = getattr(mod, cls)()
            print(f"  ✅ {name}")
            passed += 1
        except Exception as e:
            print(f"  ❌ {name}: {e}")
            failed += 1
    
    # 进阶模块
    print("\n【进阶模块】")
    advanced_modules = [
        ("靶场实战库", "pentestai.core.lab_library_v1", "LabLibraryV1"),
        ("PoC/EXP库", "pentestai.core.poc_library_v1", "PoCLibraryV1"),
        ("报告模板库", "pentestai.core.report_template_v2", "ReportTemplateV2"),
        ("告警通知系统", "pentestai.core.alert_system_v1", "AlertSystemV1"),
        ("规则引擎", "pentestai.core.rule_engine_v1", "RuleEngineV1"),
        ("日志审计系统", "pentestai.core.log_audit_v1", "LogAuditV1"),
        ("插件系统", "pentestai.core.plugin_system_v1", "PluginSystemV1"),
        ("数据加密", "pentestai.core.data_encryption_v1", "DataEncryptionV1"),
    ]
    
    for name, module, cls in advanced_modules:
        try:
            mod = __import__(module, fromlist=[cls])
            obj = getattr(mod, cls)()
            print(f"  ✅ {name}")
            passed += 1
        except Exception as e:
            print(f"  ❌ {name}: {e}")
            failed += 1
    
    # 企业级模块
    print("\n【企业级模块】")
    enterprise_modules = [
        ("多模型AI", "pentestai.core.multi_model_ai", "MultiModelAI"),
        ("威胁情报", "pentestai.core.threat_intel_v1", "ThreatIntelV1"),
        ("修复补丁生成", "pentestai.core.fix_patch_gen_v1", "FixPatchGeneratorV1"),
        ("Docker部署", "pentestai.core.docker_deploy_v1", "DockerDeployV1"),
        ("CI/CD集成", "pentestai.core.cicd_integration_v1", "CICDIntegrationV1"),
        ("移动端控制", "pentestai.core.mobile_control_v1", "MobileControlV1"),
        ("合规检查", "pentestai.core.compliance_check_v1", "ComplianceCheckV1"),
        ("SRC对接", "pentestai.core.src_integration_v1", "SRCIntegrationV1"),
    ]
    
    for name, module, cls in enterprise_modules:
        try:
            mod = __import__(module, fromlist=[cls])
            obj = getattr(mod, cls)()
            print(f"  ✅ {name}")
            passed += 1
        except Exception as e:
            print(f"  ❌ {name}: {e}")
            failed += 1
    
    # 高级安全模块
    print("\n【高级安全模块】")
    security_modules = [
        ("APT攻击分析", "pentestai.core.apt_analysis_v1", "APTAnalysisV1"),
        ("安全基线检查", "pentestai.core.baseline_check_v1", "BaselineCheckV1"),
        ("云安全检测", "pentestai.core.cloud_security_v1", "CloudSecurityV1"),
        ("红蓝对抗", "pentestai.core.red_blue_v1", "RedBlueV1"),
        ("数据泄露检测", "pentestai.core.dlp_detection_v1", "DLPDetectionV1"),
        ("IoT安全检测", "pentestai.core.iot_security_v1", "IoTSecurityV1"),
        ("工控安全检测", "pentestai.core.ics_security_v1", "ICSecurityV1"),
        ("零日漏洞情报", "pentestai.core.zero_day_intel_v1", "ZeroDayIntelV1"),
    ]
    
    for name, module, cls in security_modules:
        try:
            mod = __import__(module, fromlist=[cls])
            obj = getattr(mod, cls)()
            print(f"  ✅ {name}")
            passed += 1
        except Exception as e:
            print(f"  ❌ {name}: {e}")
            failed += 1
    
    # 安全服务模块
    print("\n【安全服务模块】")
    service_modules = [
        ("钓鱼邮件模拟", "pentestai.core.phishing_sim_v1", "PhishingSimV1"),
        ("漏洞赏金对接", "pentestai.core.bug_bounty_v1", "BugBountyV1"),
        ("事件响应", "pentestai.core.incident_response_v1", "IncidentResponseV1"),
        ("取证分析", "pentestai.core.forensics_v1", "ForensicsV1"),
        ("逆向工程", "pentestai.core.reverse_engineering_v1", "ReverseEngineeringV1"),
        ("安全度量", "pentestai.core.security_metrics_v1", "SecurityMetricsV1"),
        ("移动安全深度v2", "pentestai.core.mobile_security_v2", "MobileSecurityV2"),
        ("安全培训", "pentestai.core.security_training_v1", "SecurityTrainingV1"),
    ]
    
    for name, module, cls in service_modules:
        try:
            mod = __import__(module, fromlist=[cls])
            obj = getattr(mod, cls)()
            print(f"  ✅ {name}")
            passed += 1
        except Exception as e:
            print(f"  ❌ {name}: {e}")
            failed += 1
    
    # CyberStrikeAI集成
    print("\n【CyberStrikeAI集成】")
    try:
        mod = __import__("pentestai.core.cyber_strike_integration_v1", fromlist=["CyberStrikeIntegrationV1"])
        obj = mod.CyberStrikeIntegrationV1()
        print(f"  ✅ CyberStrikeAI集成")
        passed += 1
    except Exception as e:
        print(f"  ❌ CyberStrikeAI集成: {e}")
        failed += 1
    
    # 总结
    print("\n" + "=" * 60)
    print(f"测试完成: {passed} 通过, {failed} 失败")
    print(f"通过率: {passed / (passed + failed) * 100:.1f}%")
    print("=" * 60)
    
    return failed == 0


if __name__ == "__main__":
    success = test_all_modules()
    sys.exit(0 if success else 1)
