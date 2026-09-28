p = 'pentestai/modules/ai_security/autonomous_pentest_engine.py'
with open(p, 'r', encoding='utf-8') as f:
    content = f.read()

old = '''        return ToolResult(
            success=result.get("status") == "completed",
            data=result,
            message=f"AI智能体自主渗透完成，{result.get('phases_executed', 0)}个阶段，耗时{result.get('total_duration', 0)}秒"
        )'''

new = '''        return ToolResult(
            success=result.get("status") == "completed",
            tool_name="autonomous_pentest_engine",
            output=f"AI智能体自主渗透完成，{result.get('phases_executed', 0)}个阶段，耗时{result.get('total_duration', 0)}秒",
            data=result
        )'''

if old in content:
    content = content.replace(old, new)
    with open(p, 'w', encoding='utf-8') as f:
        f.write(content)
    print('修复成功: ToolResult message -> output')
else:
    print('未找到目标字符串')
    idx = content.find('return ToolResult(')
    if idx >= 0:
        print(content[idx:idx+300])
