"""修复main_window.py的导入"""
f = r"E:\BaiduNetdiskDownload\yuanbao\PentestAI\pentestai\gui\main_window.py"
with open(f, 'r', encoding='utf-8') as fp:
    lines = fp.readlines()

# 找到导入部分并替换
new_lines = []
skip_until_import_end = False
for i, line in enumerate(lines):
    if 'from PySide6.QtWidgets import' in line:
        # 替换整个QtWidgets导入块
        new_lines.append('from PySide6.QtWidgets import (\n')
        new_lines.append('    QApplication, QMainWindow, QTabWidget, QWidget, QVBoxLayout,\n')
        new_lines.append('    QStatusBar, QLabel, QMessageBox\n')
        new_lines.append(')\n')
        # 跳过原来的导入块直到遇到from PySide6.QtCore
        skip_until_import_end = True
        continue
    if skip_until_import_end:
        if 'from PySide6.QtCore' in line:
            new_lines.append('from PySide6.QtCore import Qt\n')
            continue
        if 'from PySide6.QtGui' in line:
            new_lines.append('from PySide6.QtGui import QIcon, QKeySequence, QShortcut\n')
            skip_until_import_end = False
            continue
        # 跳过其他行
        continue
    new_lines.append(line)

with open(f, 'w', encoding='utf-8') as fp:
    fp.writelines(new_lines)

print("✅ 导入已修复")

# 验证
import py_compile
py_compile.compile(f, doraise=True)
print("✅ 语法检查通过")

from pentestai.gui.main_window import MainWindow
print("✅ main_window导入成功")
