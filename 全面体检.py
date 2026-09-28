"""
PentestAI 全面体检脚本
检查项目：代码语法、模块导入、工具注册、GUI启动、配置、数据库、引擎、授权、文件完整性
"""
import sys, os, json, time, importlib, traceback
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

class HealthChecker:
    def __init__(self):
        self.results = []
        self.passed = 0
        self.failed = 0
        self.warnings = 0
        self.project_root = os.path.dirname(os.path.abspath(__file__))

    def check(self, name, func):
        """执行一项检查"""
        print(f"\n{'='*60}")
        print(f"  检查: {name}")
        print(f"{'='*60}")
        try:
            result = func()
            if result.get("status") == "pass":
                self.passed += 1
                print(f"  ✅ 通过: {result.get('message', '')}")
            elif result.get("status") == "warn":
                self.warnings += 1
                print(f"  ⚠️  警告: {result.get('message', '')}")
            else:
                self.failed += 1
                print(f"  ❌ 失败: {result.get('message', '')}")
            if result.get("details"):
                for d in result["details"]:
                    print(f"     - {d}")
            self.results.append({"name": name, **result})
            return result
        except Exception as e:
            self.failed += 1
            print(f"  ❌ 异常: {str(e)[:200]}")
            traceback.print_exc()
            self.results.append({"name": name, "status": "fail", "message": str(e)[:200]})

    def check_code_syntax(self):
        """检查所有Python文件语法"""
        import py_compile
        errors = []
        count = 0
        for root, dirs, files in os.walk(os.path.join(self.project_root, "pentestai")):
            for f in files:
                if f.endswith(".py"):
                    count += 1
                    path = os.path.join(root, f)
                    try:
                        py_compile.compile(path, doraise=True)
                    except py_compile.PyCompileError as e:
                        errors.append(f"{f}: {str(e)[:100]}")
        if errors:
            return {"status": "fail", "message": f"{len(errors)}/{count}个文件有语法错误", "details": errors[:10]}
        return {"status": "pass", "message": f"全部{count}个Python文件语法正确"}

    def check_module_imports(self):
        """检查核心模块能否导入"""
        modules = [
            "pentestai.core.base_tool",
            "pentestai.core.tool_init",
            "pentestai.utils.config",
            "pentestai.utils.logger",
            "pentestai.llm.client",
            "pentestai.gui.main_window",
            "pentestai.gui.home_page",
            "pentestai.gui.about_dialog",
            "pentestai.gui.tools_page",
            "pentestai.modules.ai_security.ai_security_analyzer",
            "pentestai.modules.ai_security.ai_pentest_advisor_pro",
        ]
        errors = []
        for mod in modules:
            try:
                importlib.import_module(mod)
            except Exception as e:
                errors.append(f"{mod}: {str(e)[:100]}")
        if errors:
            return {"status": "fail", "message": f"{len(errors)}/{len(modules)}个模块导入失败", "details": errors}
        return {"status": "pass", "message": f"全部{len(modules)}个核心模块导入成功"}

    def check_tool_registration(self):
        """检查工具注册"""
        from pentestai.core.tool_init import init_all_tools
        registry = init_all_tools()
        tools = registry.list_tools()
        count = len(tools) if isinstance(tools, list) else len(list(tools.keys()) if hasattr(tools, 'keys') else tools)
        if count >= 190:
            return {"status": "pass", "message": f"成功注册{count}个工具"}
        elif count >= 100:
            return {"status": "warn", "message": f"注册{count}个工具，少于预期196个"}
        return {"status": "fail", "message": f"仅注册{count}个工具，严重不足"}

    def check_config_file(self):
        """检查配置文件"""
        config_path = os.path.join(self.project_root, "config.yaml")
        if not os.path.exists(config_path):
            return {"status": "fail", "message": "config.yaml不存在"}
        try:
            from pentestai.utils.config import config
            config.load("config.yaml")
            width = config.get("gui.window_width", 0)
            return {"status": "pass", "message": f"配置文件正常，窗口宽度={width}"}
        except Exception as e:
            return {"status": "fail", "message": f"配置加载失败: {str(e)[:100]}"}

    def check_database(self):
        """检查数据库"""
        dbs = []
        data_dir = os.path.join(self.project_root, "pentestai", "data")
        if os.path.exists(data_dir):
            for f in os.listdir(data_dir):
                if f.endswith(".db"):
                    dbs.append(f)
        if dbs:
            return {"status": "pass", "message": f"找到{len(dbs)}个数据库文件", "details": dbs}
        return {"status": "warn", "message": "未找到数据库文件（首次运行时会自动创建）"}

    def check_engines(self):
        """检查外部引擎"""
        engines = {
            "nmap": r"C:\Users\ASUS\tools\nmap.exe",
            "nuclei": r"C:\Users\ASUS\tools\nuclei.exe",
        }
        found = []
        missing = []
        for name, path in engines.items():
            if os.path.exists(path):
                found.append(name)
            else:
                missing.append(name)
        # 检查Python
        python_ok = sys.executable and os.path.exists(sys.executable)
        if python_ok:
            found.append("python")
        else:
            missing.append("python")
        # 检查Docker
        import shutil
        if shutil.which("docker"):
            found.append("docker")
        else:
            missing.append("docker")
        if missing:
            return {"status": "warn", "message": f"找到{len(found)}个引擎，{len(missing)}个未找到", "details": [f"✅ {e}" for e in found] + [f"❌ {e}" for e in missing]}
        return {"status": "pass", "message": f"全部{len(found)}个引擎可用", "details": found}

    def check_license(self):
        """检查授权系统"""
        license_path = os.path.join(self.project_root, "pentestai", "data", "license.dat")
        if os.path.exists(license_path):
            size = os.path.getsize(license_path)
            return {"status": "pass", "message": f"授权文件存在，大小={size}字节"}
        return {"status": "warn", "message": "授权文件不存在（首次运行时会创建试用授权）"}

    def check_file_integrity(self):
        """检查关键文件完整性"""
        key_files = [
            "main.py",
            "config.yaml",
            "pentestai/core/tool_init.py",
            "pentestai/gui/main_window.py",
            "pentestai/gui/home_page.py",
            "pentestai/gui/about_dialog.py",
            "pentestai/llm/client.py",
            "pentestai/modules/ai_security/ai_security_analyzer.py",
            "pentestai/modules/ai_security/ai_pentest_advisor_pro.py",
            "使用手册_PentestAI.md",
            "升级报告_v50.0_AI能力重大升级.md",
        ]
        missing = []
        for f in key_files:
            path = os.path.join(self.project_root, f)
            if not os.path.exists(path):
                missing.append(f)
        if missing:
            return {"status": "fail", "message": f"{len(missing)}个关键文件缺失", "details": missing}
        return {"status": "pass", "message": f"全部{len(key_files)}个关键文件存在"}

    def check_sales_materials(self):
        """检查销售素材包"""
        sales_dir = os.path.join(self.project_root, "销售素材包")
        if not os.path.exists(sales_dir):
            return {"status": "fail", "message": "销售素材包目录不存在"}
        files = os.listdir(sales_dir)
        if len(files) >= 10:
            return {"status": "pass", "message": f"销售素材包包含{len(files)}个文件", "details": files}
        return {"status": "warn", "message": f"销售素材包仅{len(files)}个文件，建议补充"}

    def check_optimized_build(self):
        """检查优化版打包"""
        dist_dir = os.path.join(self.project_root, "dist_optimized", "PentestAI")
        exe_path = os.path.join(dist_dir, "PentestAI.exe")
        if os.path.exists(exe_path):
            all_files = []
            for root, dirs, files in os.walk(dist_dir):
                all_files.extend(files)
            total_size = sum(os.path.getsize(os.path.join(root, f)) for root, dirs, files in os.walk(dist_dir) for f in files)
            return {"status": "pass", "message": f"优化版打包完成，{len(all_files)}个文件，{total_size//1024//1024}MB"}
        # 检查是否在打包中
        log_path = os.path.join(self.project_root, "build_optimized_log2.txt")
        if os.path.exists(log_path):
            with open(log_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = f.readlines()
            last_lines = [l.strip() for l in lines[-3:] if l.strip()]
            return {"status": "warn", "message": "优化版打包进行中", "details": last_lines}
        return {"status": "warn", "message": "优化版打包未启动"}

    def run_all(self):
        """运行全部检查"""
        print("\n" + "🔍" * 30)
        print("  PentestAI 全面体检")
        print(f"  时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("🔍" * 30)

        self.check("代码语法", self.check_code_syntax)
        self.check("模块导入", self.check_module_imports)
        self.check("工具注册", self.check_tool_registration)
        self.check("配置文件", self.check_config_file)
        self.check("数据库", self.check_database)
        self.check("外部引擎", self.check_engines)
        self.check("授权系统", self.check_license)
        self.check("文件完整性", self.check_file_integrity)
        self.check("销售素材", self.check_sales_materials)
        self.check("优化打包", self.check_optimized_build)

        # 总结
        print("\n" + "=" * 60)
        print("  体检总结")
        print("=" * 60)
        total = self.passed + self.failed + self.warnings
        print(f"  总检查项: {total}")
        print(f"  ✅ 通过: {self.passed}")
        print(f"  ⚠️  警告: {self.warnings}")
        print(f"  ❌ 失败: {self.failed}")
        if self.failed == 0:
            print(f"\n  🎉 体检结果: 全部通过！项目状态良好。")
        elif self.failed <= 2:
            print(f"\n  ⚠️  体检结果: 基本健康，有{self.failed}个问题需要修复")
        else:
            print(f"\n  ❌ 体检结果: 有{self.failed}个严重问题，需要立即修复")

        # 保存报告
        report = {
            "check_time": datetime.now().isoformat(),
            "total": total,
            "passed": self.passed,
            "warnings": self.warnings,
            "failed": self.failed,
            "details": self.results
        }
        report_path = os.path.join(self.project_root, "体检报告.json")
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2, default=str)
        print(f"\n  详细报告已保存: {report_path}")

        return self.failed == 0


if __name__ == "__main__":
    checker = HealthChecker()
    success = checker.run_all()
    sys.exit(0 if success else 1)
