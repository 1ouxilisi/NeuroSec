"""集成自主渗透页面到主窗口"""
f = r"E:\BaiduNetdiskDownload\yuanbao\PentestAI\pentestai\gui\main_window.py"
with open(f, 'r', encoding='utf-8') as fp:
    c = fp.read()

# 1. 添加导入
if "autonomous_pentest_page" not in c:
    c = c.replace(
        "from pentestai.gui.about_dialog import AboutDialog",
        "from pentestai.gui.about_dialog import AboutDialog\n        from pentestai.gui.autonomous_pentest_page import AutonomousPentestPage"
    )

# 2. 创建页面实例（在self.empower_page之后）
if "self.autonomous_page" not in c:
    c = c.replace(
        "self.empower_page = EmpowerPage(self.registry)",
        "self.empower_page = EmpowerPage(self.registry)\n        self.autonomous_page = AutonomousPentestPage(self.registry)"
    )

# 3. 添加标签页（在实战赋能之后）
if '"🤖 自主渗透"' not in c:
    c = c.replace(
        'self.tabs.addTab(self.empower_page, "实战赋能")',
        'self.tabs.addTab(self.empower_page, "实战赋能")\n        self.tabs.addTab(self.autonomous_page, "🤖 自主渗透")'
    )

with open(f, 'w', encoding='utf-8') as fp:
    fp.write(c)

print("✅ 自主渗透页面已集成到主窗口")

import py_compile
py_compile.compile(f, doraise=True)
print("✅ 语法检查通过")
