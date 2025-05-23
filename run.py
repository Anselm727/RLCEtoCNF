#!/usr/bin/env python3
"""
RLCE到CNF转换工具快速运行脚本
"""

import sys
import os

# 添加src目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from main import main

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n程序被用户中断")
        sys.exit(1)
    except Exception as e:
        print(f"运行时出错: {e}")
        sys.exit(1) 