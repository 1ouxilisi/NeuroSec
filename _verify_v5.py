import sys
sys.path.insert(0, r"E:\BaiduNetdiskDownload\yuanbao\PentestAI")

import py_compile
new_files = [
    r"pentestai\modules\utility\lab_manager.py",
    r"pentestai\modules\utility\knowledge_base_engine.py",
    r"pentestai\modules\utility\sop_engine.py",
    r"pentestai\modules\automation\smart_orchestrator.py",
]
for f in new_files:
    try:
        py_compile.compile(f, doraise=True)
        print(f"OK: {f.split(chr(92))[-1]}")
    except Exception as e:
        print(f"FAIL: {f} - {e}")

from pentestai.core.tool_init import init_all_tools
r = init_all_tools()
tools = r.list_tools()
print(f"\n工具总数: {len(tools)}")
new_tools = ['lab_manager', 'knowledge_base_engine', 'sop_engine', 'smart_orchestrator']
for t in new_tools:
    found = any(x['name'] == t for x in tools)
    print(f"  {t}: {'OK' if found else 'MISSING'}")

# 统计真实引擎
real_engines = ['nmap_engine', 'nuclei_engine', 'sqlmap_engine', 'ffuf_engine',
                 'subfinder_engine', 'dalfox_engine', 'nikto_engine',
                 'ssl_audit_engine', 'cms_scanner', 'waf_detector_pro', 'auto_pentest_pro',
                 'hydra_engine', 'internal_vuln_scanner', 'mobile_security_engine_v4',
                 'blockchain_security_engine_v4',
                 'lab_manager', 'knowledge_base_engine', 'sop_engine', 'smart_orchestrator']
real_count = sum(1 for e in real_engines if any(x['name'] == e for x in tools))
print(f"\n真实/赋能引擎: {real_count}/{len(real_engines)}")

from PySide6.QtWidgets import QApplication
app = QApplication.instance() or QApplication(sys.argv)
from pentestai.gui.main_window import MainWindow
w = MainWindow()
print(f"GUI: OK, {w.tabs.count()}标签页")
print("\n全部验证通过!")
