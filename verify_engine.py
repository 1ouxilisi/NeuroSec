"""验证工具总数和自主渗透引擎注册"""
import sys
sys.path.insert(0, r"E:\BaiduNetdiskDownload\yuanbao\PentestAI")
from pentestai.core.tool_init import init_all_tools

r = init_all_tools()
tools = r.list_tools()
print(f"工具总数: {len(tools)}")

ae = r.get('autonomous_pentest_engine')
print(f"自主渗透引擎已注册: {ae is not None}")
if ae:
    print(f"  显示名: {ae.display_name}")
    print(f"  分类: {ae.category}")
    print(f"  描述: {ae.description[:50]}...")
