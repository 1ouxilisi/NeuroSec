"""集成关于对话框到主窗口"""
f = r"E:\BaiduNetdiskDownload\yuanbao\PentestAI\pentestai\gui\main_window.py"
with open(f, 'r', encoding='utf-8') as fp:
    content = fp.read()

# 1. 增加AboutDialog导入
if 'AboutDialog' not in content:
    content = content.replace(
        'from pentestai.gui.home_page import HomePage',
        'from pentestai.gui.home_page import HomePage\nfrom pentestai.gui.about_dialog import AboutDialog'
    )

# 2. 在_setup_shortcuts方法中增加F1快捷键
if 'about_shortcut' not in content:
    content = content.replace(
        '        # Ctrl+Q 退出\n        quit_shortcut = QShortcut(QKeySequence("Ctrl+Q"), self)\n        quit_shortcut.activated.connect(self.close)',
        '        # F1 打开关于对话框\n        about_shortcut = QShortcut(QKeySequence("F1"), self)\n        about_shortcut.activated.connect(self._show_about)\n\n        # Ctrl+Q 退出\n        quit_shortcut = QShortcut(QKeySequence("Ctrl+Q"), self)\n        quit_shortcut.activated.connect(self.close)'
    )

# 3. 增加_show_about方法
if 'def _show_about(self):' not in content:
    method = '''    def _show_about(self):
        """显示关于对话框"""
        dialog = AboutDialog(self.registry, self)
        dialog.exec()

'''
    content = content.replace(
        '    def _on_config_updated(self):',
        method + '    def _on_config_updated(self):'
    )

with open(f, 'w', encoding='utf-8') as fp:
    fp.write(content)

print("✅ 关于对话框已集成到主窗口")

import py_compile
py_compile.compile(f, doraise=True)
print("✅ 语法检查通过")
