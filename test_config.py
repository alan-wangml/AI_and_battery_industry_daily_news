#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# 加载 .env
load_dotenv()

print("=" * 60)
print("配置诊断")
print("=" * 60)

# 检查环境变量
print("\n1. 环境变量检查:")
for key in ["DEEPSEEK_API_KEY", "DEEPSEEK_MODEL", "GMAIL_ADDRESS"]:
    val = os.environ.get(key, "")
    if val:
        if "KEY" in key or "PASSWORD" in key:
            print("  {}: {}... (已设置)".format(key, val[:20]))
        else:
            print("  {}: {}".format(key, val))
    else:
        print("  {}: [未设置]".format(key))

# 导入模块检查
print("\n2. 模块配置检查:")
try:
    from src.ai_summarizer import DEEPSEEK_BASE_URL, DEEPSEEK_API_KEY, DEEPSEEK_MODEL
    print("  DEEPSEEK_BASE_URL: {}".format(DEEPSEEK_BASE_URL))
    print("  DEEPSEEK_MODEL: {}".format(DEEPSEEK_MODEL))
    print("  DEEPSEEK_API_KEY 是否存在: {}".format(bool(DEEPSEEK_API_KEY)))
except Exception as e:
    print("  ERROR: {}".format(e))
    import traceback
    traceback.print_exc()

print("\n3. 搜索所有 Python 文件中是否有豆包引用:")
import subprocess
try:
    result = subprocess.run(
        ["grep", "-r", "ark.cn-beijing|volces|豆包", "src/", "--include=*.py"],
        capture_output=True,
        text=True
    )
    if result.stdout:
        print("  找到豆包引用:")
        print(result.stdout)
    else:
        print("  未找到豆包引用")
except Exception as e:
    print("  无法执行 grep: {}".format(e))

print("\n" + "=" * 60)
