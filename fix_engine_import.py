"""修复自主渗透引擎的导入和工具注册表"""
f = r"E:\BaiduNetdiskDownload\yuanbao\PentestAI\pentestai\modules\ai_security\autonomous_pentest_engine.py"
with open(f, 'r', encoding='utf-8') as fp:
    c = fp.read()

# 1. 修改导入
c = c.replace(
    "from pentestai.core.base_tool import BaseTool, ToolResult, tool_registry",
    "from pentestai.core.base_tool import BaseTool, ToolResult, ToolRegistry"
)

# 2. 在__init__中增加_registry变量
c = c.replace(
    "self._load_ai_config()",
    "self._registry = None\n        self._load_ai_config()"
)

# 3. 增加_get_registry方法（在_load_ai_config之前）
get_registry_method = '''    def _get_registry(self):
        """获取工具注册表（延迟初始化）"""
        if self._registry is None:
            from pentestai.core.tool_init import init_all_tools
            self._registry = init_all_tools()
        return self._registry

'''
c = c.replace(
    "    def _load_ai_config(self):",
    get_registry_method + "    def _load_ai_config(self):"
)

# 4. 修改_execute_tool中的工具获取
c = c.replace("tool = tool_registry.get(tool_name)", "tool = self._get_registry().get(tool_name)")
c = c.replace("all_tools = tool_registry.list_tools()", "all_tools = self._get_registry().list_tools()")

with open(f, 'w', encoding='utf-8') as fp:
    fp.write(c)

print("✅ 导入和注册表修复完成")

import py_compile
py_compile.compile(f, doraise=True)
print("✅ 语法检查通过")
