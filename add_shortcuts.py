"""给main_window.py增加快捷键支持"""
import re

f = r"E:\BaiduNetdiskDownload\yuanbao\PentestAI\pentestai\gui\main_window.py"
with open(f, 'r', encoding='utf-8') as fp:
    content = fp.read()

# 1. 增加QShortcut导入
if 'QShortcut' not in content:
    content = content.replace(
        'from PySide6.QtWidgets import (',
        'from PySide6.QtWidgets import (\n    QShortcut,'
    )

# 2. 增加QKeySequence导入
if 'QKeySequence' not in content:
    content = content.replace(
        'from PySide6.QtCore import Qt',
        'from PySide6.QtCore import Qt, QKeySequence'
    )

# 3. 在连接设置页信号前增加快捷键调用
if '_setup_shortcuts()' not in content:
    content = content.replace(
        '        # 连接设置页面的配置更新信号\n        self.settings_page.config_updated.connect(self._on_config_updated)',
        '        # 快捷键支持（Ctrl+1~9切换标签页，Ctrl+Q退出）\n        self._setup_shortcuts()\n\n        # 连接设置页面的配置更新信号\n        self.settings_page.config_updated.connect(self._on_config_updated)'
    )

# 4. 增加_setup_shortcuts方法
if 'def _setup_shortcuts(self):' not in content:
    method = '''    def _setup_shortcuts(self):
        """创建快捷键"""
        tab_count = self.tabs.count()
        for i in range(min(tab_count, 9)):
            shortcut = QShortcut(QKeySequence(f"Ctrl+{i+1}"), self)
            shortcut.activated.connect(lambda checked, idx=i: self.tabs.setCurrentIndex(idx))
        # Ctrl+Q 退出
        quit_shortcut = QShortcut(QKeySequence("Ctrl+Q"), self)
        quit_shortcut.activated.connect(self.close)

'''
    content = content.replace(
        '    def _on_config_updated(self):',
        method + '    def _on_config_updated(self):'
    )

with open(f, 'w', encoding='utf-8') as fp:
    fp.write(content)

print("✅ 快捷键支持已添加")

# 语法检查
import py_compile
py_compile.compile(f, doraise=True)
print("✅ 语法检查通过")
