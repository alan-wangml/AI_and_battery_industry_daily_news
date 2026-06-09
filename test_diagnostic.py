#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
深度诊断脚本 - 检测为什么会调用豆包 API
"""

import os
import sys
import json
import requests
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

print("=" * 80)
print("深度诊断脚本 - 豆包 API 问题排查")
print("=" * 80)

# 1. 环境检查
print("\n1️⃣  环境变量检查:")
env_vars = {
    "DEEPSEEK_API_KEY": os.environ.get("DEEPSEEK_API_KEY", ""),
    "DEEPSEEK_MODEL": os.environ.get("DEEPSEEK_MODEL", ""),
    "DEEPSEEK_BASE_URL": os.environ.get("DEEPSEEK_BASE_URL", ""),
}
for key, val in env_vars.items():
    if val:
        display = val[:20] + "..." if len(val) > 20 else val
        print(f"  ✓ {key}: {display}")
    else:
        print(f"  ✗ {key}: [未设置]")

# 2. 系统和 Python 信息
print("\n2️⃣  Python 环境信息:")
print(f"  Python 版本: {sys.version}")
print(f"  Python 路径: {sys.executable}")
print(f"  requests 版本: {requests.__version__}")
print(f"  requests 位置: {requests.__file__}")

# 3. 检查 requests 是否被 monkey patch
print("\n3️⃣  requests 库完整性检查:")
print(f"  requests.post 类型: {type(requests.post)}")
print(f"  requests.Session 类型: {type(requests.Session)}")

# 获取 requests.post 的源代码位置
try:
    import inspect
    source_file = inspect.getsourcefile(requests.post)
    print(f"  requests.post 源文件: {source_file}")
except Exception as e:
    print(f"  无法获取源文件: {e}")

# 4. 检查是否有代理或中间件
print("\n4️⃣  网络代理检查:")
proxies = {
    "http_proxy": os.environ.get("http_proxy", ""),
    "https_proxy": os.environ.get("https_proxy", ""),
    "HTTP_PROXY": os.environ.get("HTTP_PROXY", ""),
    "HTTPS_PROXY": os.environ.get("HTTPS_PROXY", ""),
}
has_proxy = any(v for v in proxies.values())
if has_proxy:
    print("  ⚠️  检测到代理配置:")
    for key, val in proxies.items():
        if val:
            print(f"    {key}: {val}")
else:
    print("  ✓ 未检测到代理")

# 5. 检查环境中是否有豆包相关的配置
print("\n5️⃣  豆包相关配置检查:")
bytedance_vars = {k: v for k, v in os.environ.items() 
                  if any(x in k.lower() for x in ["ark", "bytedance", "volces", "doubao"])}
if bytedance_vars:
    print("  ⚠️  发现豆包相关的环境变量:")
    for key, val in bytedance_vars.items():
        display = val[:20] + "..." if len(val) > 20 else val
        print(f"    {key}: {display}")
else:
    print("  ✓ 未发现豆包相关的环境变量")

# 6. 导入 ai_summarizer 并检查配置
print("\n6️⃣  模块配置检查:")
try:
    from src.ai_summarizer import DEEPSEEK_BASE_URL, DEEPSEEK_API_KEY, DEEPSEEK_MODEL
    print(f"  ✓ ai_summarizer 导入成功")
    print(f"    DEEPSEEK_BASE_URL: {DEEPSEEK_BASE_URL}")
    print(f"    DEEPSEEK_MODEL: {DEEPSEEK_MODEL}")
    print(f"    DEEPSEEK_API_KEY 存在: {bool(DEEPSEEK_API_KEY)}")
except Exception as e:
    print(f"  ✗ 导入失败: {e}")

# 7. 模拟请求
print("\n7️⃣  模拟 requests.post 请求:")
try:
    print("  正在发送测试请求...")
    
    session = requests.Session()
    test_url = "https://api.deepseek.com/chat/completions"
    
    print(f"  目标 URL: {test_url}")
    
    # 记录请求对象的信息
    req = requests.Request(
        'POST',
        test_url,
        headers={"test": "value"}
    )
    prepared = session.prepare_request(req)
    print(f"  准备的请求 URL: {prepared.url}")
    print(f"  准备的请求方法: {prepared.method}")
    
except Exception as e:
    print(f"  ✗ 错误: {e}")

print("\n" + "=" * 80)
print("诊断完成")
print("=" * 80)
