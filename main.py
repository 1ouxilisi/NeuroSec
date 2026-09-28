"""PentestAI - AI驱动的全功能渗透测试平台
GUI入口
"""
import sys
import os

# 将项目根目录加入Python路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from pentestai.gui.main_window import main

if __name__ == "__main__":
    main()
