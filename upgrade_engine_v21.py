"""升级自主渗透引擎v2.1：集成结果解析器+完善AI决策+自动提取发现+错误恢复"""
f = r"E:\BaiduNetdiskDownload\yuanbao\PentestAI\pentestai\modules\ai_security\autonomous_pentest_engine.py"
with open(f, 'r', encoding='utf-8') as fp:
    c = fp.read()

# 1. 导入ResultParser
if "result_parser" not in c:
    c = c.replace(
        "from pentestai.core.base_tool import BaseTool, ToolResult, ToolRegistry",
        "from pentestai.core.base_tool import BaseTool, ToolResult, ToolRegistry\nfrom pentestai.modules.ai_security.result_parser import ResultParser, Finding"
    )

# 2. PentestState增加failed_tools和parsed_results
if "self.failed_tools" not in c:
    c = c.replace(
        "self.tool_results = {}",
        "self.tool_results = {}\n        self.failed_tools = []  # 失败的工具记录\n        self.parsed_findings = []  # 解析后的结构化发现"
    )

# 3. PentestState增加add_failed_tool方法
if "def add_failed_tool" not in c:
    c = c.replace(
        "def add_finding(self, finding):\n        self.findings.append(finding)",
        "def add_finding(self, finding):\n        self.findings.append(finding)\n\n    def add_failed_tool(self, tool_name, error):\n        self.failed_tools.append({\"tool\": tool_name, \"error\": error[:200]})"
    )

# 4. PentestState.get_summary增加发现和失败工具信息
old_summary = '''    def get_summary(self):
        summary = f"目标: {self.target} ({self.target_type})\\n"
        summary += f"已完成阶段: {len(self.phases_completed)}\\n"
        summary += f"发现数量: {len(self.findings)}\\n"
        if self.findings:
            summary += "发现列表:\\n"
            for i, f in enumerate(self.findings[:10]):
                summary += f"  {i+1}. {f.get('name', '未知')} - 风险: {f.get('risk', '未知')}\\n"
        return summary'''
new_summary = '''    def get_summary(self):
        summary = f"目标: {self.target} ({self.target_type})\\n"
        summary += f"已完成阶段: {len(self.phases_completed)}\\n"
        summary += f"发现数量: {len(self.parsed_findings)}\\n"
        if self.parsed_findings:
            summary += "发现列表(按风险排序):\\n"
            sorted_findings = sorted(self.parsed_findings, key=lambda x: {"高危":0,"中危":1,"低危":2,"信息":3}.get(x.risk, 4))
            for i, f in enumerate(sorted_findings[:8]):
                summary += f"  {i+1}. [{f.risk}] {f.name} - {f.description[:50]}\\n"
        if self.failed_tools:
            summary += f"失败工具: {[ft['tool'] for ft in self.failed_tools[-5:]]}\\n"
        return summary'''
c = c.replace(old_summary, new_summary)

# 5. _execute_phase中增加结果解析和发现提取
old_execute_end = '''        phase.status = "completed" if not self.stop_requested else "stopped"
        phase.end_time = datetime.now()
        if self.state:
            self.state.phases_completed.append(phase)
            self.state.current_phase = None'''
new_execute_end = '''        # 结构化解析结果并自动提取发现
        self._log("")
        self._log(f"🔍 正在结构化解析工具结果...")
        parsed_count = 0
        for result in phase.results:
            if result.get("status") == "success":
                try:
                    findings = ResultParser.parse(
                        result.get("tool_name", ""),
                        result.get("output", ""),
                        result.get("params", {})
                    )
                    for finding in findings:
                        if self.state:
                            self.state.parsed_findings.append(finding)
                            parsed_count += 1
                except Exception as e:
                    self._log(f"    解析{result.get('tool_name')}结果失败: {str(e)[:50]}", "warn")
            elif result.get("status") == "failed":
                if self.state:
                    self.state.add_failed_tool(result.get("tool_name", ""), result.get("error", ""))
        self._log(f"  ✅ 解析完成，提取{parsed_count}个结构化发现")

        phase.status = "completed" if not self.stop_requested else "stopped"
        phase.end_time = datetime.now()
        if self.state:
            self.state.phases_completed.append(phase)
            self.state.current_phase = None'''
c = c.replace(old_execute_end, new_execute_end)

# 6. 完善_build_next_phase_prompt，增加完整工具清单和发现摘要
old_prompt = '''    def _build_next_phase_prompt(self):
        state_summary = self.state.get_summary() if self.state else ""
        return f"""你是专业渗透测试AI智能体。正在对目标进行渗透测试。

当前状态:
{state_summary}

已完成阶段: {len(self.state.phases_completed) if self.state else 0}
最大阶段: {self.state.max_phases if self.state else 10}

根据当前状态决定下一步:
1. 继续下一阶段
2. 深入挖掘某个漏洞(deep_dive)
3. 验证漏洞(vuln_verify)
4. 生成报告(report)
5. 停止(stop)

可用工具: web_scanner, cve_checker, weak_password, vuln_verifier, sqlmap_engine, nuclei_engine, report_generator, internal_vuln_checker, domain_enumerator

返回JSON:
{{"decision":"决策说明","action":"next_phase|deep_dive|vuln_verify|report|stop","phase":{{"name":"阶段名","description":"描述","phase_type":"vuln_scan|deep_dive|vuln_verify|report","tools":[{{"tool_name":"","params":{{}},"description":""}}],"expected_output":""}}}}

停止时action设为stop，phase设为null。只返回JSON。"""'''

new_prompt = '''    def _build_next_phase_prompt(self):
        state_summary = self.state.get_summary() if self.state else ""
        # 发现统计
        high_risk = sum(1 for f in self.state.parsed_findings if f.risk == "高危") if self.state else 0
        medium_risk = sum(1 for f in self.state.parsed_findings if f.risk == "中危") if self.state else 0
        low_risk = sum(1 for f in self.state.parsed_findings if f.risk == "低危") if self.state else 0

        return f"""你是专业渗透测试AI智能体。正在对目标进行渗透测试，需要决定下一步做什么。

【当前状态】
{state_summary}

【发现统计】高危:{high_risk} 中危:{medium_risk} 低危:{low_risk}
已完成阶段: {len(self.state.phases_completed) if self.state else 0}
最大阶段: {self.state.max_phases if self.state else 10}

【决策原则】
1. 信息收集不充分时，先补充信息收集（端口/子域名/目录/技术栈）
2. 发现高危漏洞后，优先验证和深入挖掘
3. 工具执行失败时，换工具或换参数重试
4. 已经没有更多可挖的（高危都验证完、信息收集充分）时，生成报告并停止
5. 不要重复已经做过的阶段
6. 每个阶段工具不超过5个，聚焦最有价值的工具

【可用工具清单（按类别）】
信息收集: port_scanner(端口扫描,params:target,ports), subdomain_enum(子域名,params:domain), dir_bruter(目录爆破,params:url,wordlist), tech_detector(技术栈,params:url), waf_detector(WAF,params:url), whois_dns, web_spider(爬虫)
漏洞扫描: web_scanner(Web漏洞8种,params:url,scan_type), cve_checker(CVE,params:target), weak_password(弱口令,params:target), ssl_auditor(SSL,params:target), internal_vuln_checker(内网漏洞,params:target), nuclei_engine(Nuclei,params:target)
漏洞验证: vuln_verifier(PoC验证,params:target), sqlmap_engine(SQLMap,params:url), poc_framework
内网渗透: internal_scanner(存活扫描,params:target), domain_enumerator(域枚举,params:target), lateral_movement_helper
报告: report_generator(生成报告,params:target)

【返回格式】严格JSON:
{{"decision":"决策理由(50字内，说明为什么选这个下一步)","action":"next_phase|deep_dive|vuln_verify|report|stop","phase":{{"name":"阶段名","description":"阶段描述","phase_type":"recon|vuln_scan|deep_dive|vuln_verify|report","tools":[{{"tool_name":"工具名必须从上面清单选","params":{{"参数名":"参数值"}},"description":"工具用途"}}],"expected_output":"预期输出"}}}}

如果决定停止，action设为"stop"，phase设为null。
只返回JSON，不要其他文字，不要markdown代码块。"""'''
c = c.replace(old_prompt, new_prompt)

# 7. 完善_build_first_phase_prompt
old_first_prompt = '''    def _build_first_phase_prompt(self):
        return f"""你是专业渗透测试AI智能体。开始对目标进行渗透测试。

目标: {self.target}
目标类型: {self.target_type}

请生成第一个渗透阶段（信息收集）。

可用工具: port_scanner(端口扫描), subdomain_enum(子域名枚举), dir_bruter(目录爆破), tech_detector(技术栈识别), waf_detector(WAF检测), whois_dns, web_spider, internal_scanner

返回JSON:
{{"name":"阶段名","description":"描述","phase_type":"recon","tools":[{{"tool_name":"工具名","params":{{}},"description":"描述"}}],"expected_output":"预期输出","decision":"决策说明"}}

只返回JSON。"""'''
new_first_prompt = '''    def _build_first_phase_prompt(self):
        return f"""你是专业渗透测试AI智能体。开始对目标进行渗透测试，生成第一个信息收集阶段。

目标: {self.target}
目标类型: {self.target_type}

【信息收集工具清单】
port_scanner(端口扫描,params:target,ports) - 必选
subdomain_enum(子域名枚举,params:domain) - URL/域名目标必选
dir_bruter(目录爆破,params:url,wordlist) - Web目标推荐
tech_detector(技术栈识别,params:url) - Web目标推荐
waf_detector(WAF检测,params:url) - Web目标推荐
internal_scanner(内网存活扫描,params:target) - IP/IP段目标必选
whois_dns(whois查询,params:domain) - 可选
web_spider(爬虫,params:url) - 可选

【要求】
1. 根据目标类型选择最合适的工具组合（3-5个）
2. 每个工具必须指定正确的参数
3. 工具名必须从上面清单中选择
4. phase_type必须是"recon"

【返回格式】严格JSON:
{{"name":"阶段名","description":"阶段描述","phase_type":"recon","tools":[{{"tool_name":"工具名","params":{{"参数名":"参数值"}},"description":"工具用途"}}],"expected_output":"预期输出","decision":"决策说明"}}

只返回JSON，不要其他文字，不要markdown代码块。"""'''
c = c.replace(old_first_prompt, new_first_prompt)

# 8. 版本号升级到2.1.0
c = c.replace('version = "2.0.0"', 'version = "2.1.0"')
c = c.replace('AI自主渗透引擎 v2.0', 'AI自主渗透引擎 v2.1')

# 9. run_autonomous结果中增加发现统计
old_result = '''            result = {
                "target": self.target, "target_type": self.target_type,
                "mode": self.mode, "ai_enabled": self.ai_enabled,
                "agent_mode": True,'''
new_result = '''            # 发现统计
            all_findings = self.state.parsed_findings if self.state else []
            high = sum(1 for f in all_findings if f.risk == "高危")
            medium = sum(1 for f in all_findings if f.risk == "中危")
            low = sum(1 for f in all_findings if f.risk == "低危")
            info = sum(1 for f in all_findings if f.risk == "信息")

            result = {
                "target": self.target, "target_type": self.target_type,
                "mode": self.mode, "ai_enabled": self.ai_enabled,
                "agent_mode": True,
                "findings_total": len(all_findings),
                "findings_high": high, "findings_medium": medium,
                "findings_low": low, "findings_info": info,
                "findings": [f.to_dict() for f in all_findings[:20]],'''
c = c.replace(old_result, new_result)

# 10. 完成日志增加发现统计
old_finish = '''            self._log(f"  执行工具: {total_tools}个 (成功{successful}/失败{failed})")
            self._log(f"  停止原因: {result['stop_reason']}")'''
new_finish = '''            self._log(f"  执行工具: {total_tools}个 (成功{successful}/失败{failed})")
            self._log(f"  发现统计: 高危{high}/中危{medium}/低危{low}/信息{info} (共{len(all_findings)}个)")
            self._log(f"  停止原因: {result['stop_reason']}")'''
c = c.replace(old_finish, new_finish)

with open(f, 'w', encoding='utf-8') as fp:
    fp.write(c)

print("✅ 引擎v2.1升级完成")
print("  - 集成ResultParser结果结构化解析")
print("  - 自动提取发现到state")
print("  - 完善AI决策prompt（完整工具清单+发现统计+决策原则）")
print("  - 错误恢复机制（失败工具记录）")
print("  - 发现统计输出（高危/中危/低危/信息）")
print("  - 版本升级到2.1.0")

import py_compile
py_compile.compile(f, doraise=True)
print("✅ 语法检查通过")
