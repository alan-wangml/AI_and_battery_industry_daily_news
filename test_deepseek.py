#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试 DeepSeek API 连接
"""

import os
import json
import requests
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY", "")
DEEPSEEK_MODEL = os.environ.get("DEEPSEEK_MODEL", "deepseek-chat")
DEEPSEEK_BASE_URL = "https://api.deepseek.com/chat/completions"

print("=" * 70)
print("DeepSeek API 连接测试")
print("=" * 70)

print("\n1. 配置检查:")
print(f"   API URL: {DEEPSEEK_BASE_URL}")
print(f"   Model: {DEEPSEEK_MODEL}")
print(f"   API Key 存在: {bool(DEEPSEEK_API_KEY)}")
if DEEPSEEK_API_KEY:
    print(f"   API Key 前缀: {DEEPSEEK_API_KEY[:20]}...")

if not DEEPSEEK_API_KEY:
    print("\n❌ 错误：DEEPSEEK_API_KEY 未设置")
    exit(1)

print("\n2. 发送测试请求...")
try:
    response = requests.post(
        DEEPSEEK_BASE_URL,
        headers={
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json",
        },
        json={
            "model": DEEPSEEK_MODEL,
            "messages": [{"role": "user", "content": "Hello, please respond with: OK"}],
            "max_tokens": 50,
            "temperature": 0.2,
        },
        timeout=30,
    )
    
    print(f"   状态码: {response.status_code}")
    print(f"   请求 URL: {response.url}")
    print(f"   响应内容: {response.text[:200]}")
    
    if response.status_code == 200:
        print("\n✅ 成功：DeepSeek API 连接正常")
        print(f"   响应: {response.json()['choices'][0]['message']['content']}")
    else:
        print(f"\n❌ 错误 ({response.status_code}): {response.text}")
        
except requests.exceptions.RequestException as e:
    print(f"\n❌ 请求异常: {e}")
    print(f"   请检查网络连接和 API Key 是否正确")

print("\n" + "=" * 70)
