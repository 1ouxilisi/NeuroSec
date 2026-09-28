# NeuroSec - AI驱动的全功能安全测试平台

## 项目简介

NeuroSec（神经安全）是一个AI驱动的全功能安全测试平台，集成190+安全工具，15个真实核心引擎，覆盖Web安全、内网渗透、移动安全、区块链安全、API安全等领域。支持一键全扫、批量扫描、专业报告生成、项目管理全流程。

**定位**：自动化安全测试工具集（外网+内网+AI自动化），仅限授权环境下的安全检测与验证，不包含漏洞利用/攻击/getshell能力。

**当前版本**：v48.0 | **工具总数**：190+ | **真实核心引擎**：15个

---

## 核心特性

### 15个真实核心引擎（全部调用成熟开源工具）

| 引擎 | 功能 | 底层工具 |
|------|------|---------|
| nmap_engine | 端口扫描+服务识别+OS检测 | Nmap |
| nuclei_engine | 模板化漏洞扫描（数千CVE模板） | Nuclei |
| sqlmap_engine | SQL注入检测与利用 | SQLMap |
| dalfox_engine | XSS漏洞扫描与参数分析 | Dalfox |
| nikto_engine | Web服务器漏洞扫描 | Nikto |
| ffuf_engine | 目录/文件/参数暴力枚举 | FFuF |
| subfinder_engine | 子域名枚举 | Subfinder |
| ssl_audit_engine | SSL/TLS证书+协议+密码套件审计 | Python原生ssl |
| cms_scanner | CMS/框架/服务器/编程语言指纹识别 | 16种指纹库 |
| waf_detector_pro | WAF识别+拦截测试+强度评估 | 18种WAF指纹 |
| hydra_engine | 多协议弱口令暴力破解 | Hydra（14种协议） |
| internal_vuln_scanner | 内网漏洞扫描（MS17-010/BlueKeep等14种） | Nmap脚本引擎 |
| mobile_security_engine_v4 | APK反编译+静态分析+API安全 | jadx+apktool |
| blockchain_security_engine_v4 | Solidity智能合约漏洞审计 | Slither（45种检测器） |
| auto_pentest_pro | 一键全扫（串联全部引擎+自动报告） | 调度以上全部 |

### 4个实战赋能引擎

| 引擎 | 功能 |
|------|------|
| lab_manager | 7个漏洞靶场一键Docker部署+3级学习路径 |
| knowledge_base_engine | 8个漏洞原理详解+3个工具原理解析+攻击链图谱 |
| sop_engine | 7种服务报价+5阶段接单SOP+合同模板+授权书+报价单 |
| smart_orchestrator | 7种目标自动识别+4种扫描策略+P0-P4优先级排序 |

### 3个商业交付引擎

| 引擎 | 功能 |
|------|------|
| project_manager | 客户CRM+项目管理+扫描历史+漏洞全生命周期跟踪+仪表盘 |
| batch_scanner | 多目标批量扫描+文件导入+结果聚合+汇总报告 |
| scan_comparator | 两次扫描对比+新增/修复漏洞识别+复测HTML报告 |

---

## 快速开始

### 环境要求
- Python 3.9+
- Windows 10/11
- 可选：Docker、Nmap、Nuclei、SQLMap等

### 运行
```bash
cd NeuroSec
pip install -r requirements.txt
python main.py
```

### 命令行使用
```python
from pentestai.core.tool_init import get_registry
registry = get_registry()

# 一键全扫
scanner = registry.get("auto_pentest_pro")
result = scanner.run(action="full_scan", target="http://example.com", scan_mode="standard")

# 项目管理
pm = registry.get("project_manager")
pm.run(action="add_client", name="客户名称", contact="联系人")
pm.run(action="add_project", client_id="xxx", name="项目名称", target="http://example.com")

# 生成专业报告
report = registry.get("pro_report_generator")
report.run(action="generate", client_name="客户", project_name="项目", target="http://example.com", findings=[])
```

---

## 合规声明

- 本工具仅限在已获得书面授权的环境中使用
- 仅用于安全检测和漏洞验证，不包含漏洞利用、getshell、提权、免杀、DDoS等攻击能力
- 使用本工具进行未授权测试属于违法行为，使用者需自行承担法律责任
- 建议在测试前签署正式的测试授权书

---

## 技术栈

- 语言：Python 3.9+
- GUI：PySide6
- 核心引擎：Nmap / Nuclei / SQLMap / Dalfox / Nikto / FFuF / Subfinder / jadx / apktool / Slither / Hydra
- 报告：HTML（专业7章节模板）
- 打包：PyInstaller

---

## 项目架构

```
NeuroSec/
├── main.py                    # 入口
├── pentestai/
│   ├── core/                  # 核心框架（base_tool/engine_manager/tool_init）
│   ├── modules/
│   │   ├── recon/             # 信息收集
│   │   ├── vuln_scan/         # 漏洞扫描
│   │   ├── internal/          # 内网渗透
│   │   ├── mobile/            # 移动安全
│   │   ├── blockchain/        # 区块链安全
│   │   ├── automation/        # 自动化
│   │   ├── report/            # 报告生成
│   │   ├── utility/           # 辅助工具（项目管理/靶场/知识库/SOP）
│   │   └── ai/                # AI赋能
│   ├── gui/                   # PySide6 GUI
│   └── data/                  # 数据目录
└── build/                     # 打包目录
```

---

## License

MIT License
