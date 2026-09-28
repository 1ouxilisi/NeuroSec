"""注册第五轮新引擎（实战赋能系统）"""
filepath = r"E:\BaiduNetdiskDownload\yuanbao\PentestAI\pentestai\core\tool_init.py"

with open(filepath, "r", encoding="utf-8") as f:
    content = f.read()

if "lab_manager" in content:
    print("新引擎似乎已经注册过了，跳过")
else:
    old = "    registry.register(BlockchainSecurityEngineV4())\n\n    return registry"
    new = """    registry.register(BlockchainSecurityEngineV4())

    # 第五轮升级：实战赋能系统（补全短板）
    from pentestai.modules.utility.lab_manager import LabManager
    from pentestai.modules.utility.knowledge_base_engine import KnowledgeBaseEngine
    from pentestai.modules.utility.sop_engine import SOPEngine
    from pentestai.modules.automation.smart_orchestrator import SmartOrchestrator

    registry.register(LabManager())
    registry.register(KnowledgeBaseEngine())
    registry.register(SOPEngine())
    registry.register(SmartOrchestrator())

    return registry"""

    if old in content:
        content = content.replace(old, new)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print("4个实战赋能引擎注册完成")
    else:
        print("未找到目标字符串，需要手动检查")
