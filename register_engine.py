"""注册自主渗透引擎到工具表"""
f = r"E:\BaiduNetdiskDownload\yuanbao\PentestAI\pentestai\core\tool_init.py"
with open(f, 'r', encoding='utf-8') as fp:
    c = fp.read()

# 1. 添加导入（在AIPentestAdvisorPro导入之后）
if "autonomous_pentest_engine" not in c:
    c = c.replace(
        "from pentestai.modules.ai_security.ai_pentest_advisor_pro import AIPentestAdvisorPro",
        "from pentestai.modules.ai_security.ai_pentest_advisor_pro import AIPentestAdvisorPro\n    from pentestai.modules.ai_security.autonomous_pentest_engine import AutonomousPentestEngine"
    )

# 2. 添加注册（在AIPentestAdvisorPro注册之后）
if "AutonomousPentestEngine()" not in c:
    c = c.replace(
        "registry.register(AIPentestAdvisorPro())",
        "registry.register(AIPentestAdvisorPro())\n    registry.register(AutonomousPentestEngine())"
    )

with open(f, 'w', encoding='utf-8') as fp:
    fp.write(c)

print("✅ 自主渗透引擎已注册到工具表")

import py_compile
py_compile.compile(f, doraise=True)
print("✅ 语法检查通过")
