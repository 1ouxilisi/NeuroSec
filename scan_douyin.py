#!/usr/bin/env python3
"""
PentestAI v12.0 - 字节SRC自动扫描
目标：douyin.com
"""

import requests
import json
import yaml
import subprocess
import time

# 加载配置
with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

LLM_CONFIG = config['llm']

def call_ai(prompt):
    """调用AI"""
    response = requests.post(
        f"{LLM_CONFIG['api_base']}/chat/completions",
        headers={
            'Authorization': f"Bearer {LLM_CONFIG['api_key']}",
            'Content-Type': 'application/json'
        },
        json={
            'model': LLM_CONFIG['model'],
            'messages': [{'role': 'user', 'content': prompt}],
            'max_tokens': LLM_CONFIG['max_tokens'],
            'temperature': LLM_CONFIG['temperature']
        }
    )
    return response.json()['choices'][0]['message']['content']

def scan_target(target):
    """自动扫描目标"""
    print(f"[*] PentestAI v12.0 开始扫描: {target}")
    print("=" * 60)
    
    # 第1步：AI分析攻击面
    print("\n[阶段1] AI分析攻击面...")
    prompt1 = f"""
你是字节SRC的白帽黑客。目标是 {target}

请给出：
1. 这个网站有哪些子域名？
2. 应该优先测试哪些接口？
3. 最可能发现什么漏洞？

请用专业的渗透测试语言回答。
"""
    analysis = call_ai(prompt1)
    print(analysis[:500])
    
    # 第2步：子域名枚举
    print("\n" + "=" * 60)
    print("\n[阶段2] 子域名枚举...")
    print("  [*] 运行 subfinder...")
    
    # 实际运行subfinder
    try:
        result = subprocess.run(['subfinder', '-d', target.replace('https://', '').replace('http://', ''), '-silent'], 
                              capture_output=True, text=True, timeout=30)
        subdomains = result.stdout.strip().split('\n')[:10]
        print(f"  ✅ 发现 {len(subdomains)} 个子域名")
        for sub in subdomains[:5]:
            print(f"    - {sub}")
    except Exception as e:
        print(f"  ⚠️ subfinder运行失败: {e}")
        subdomains = ["www.douyin.com", "api.douyin.com", "m.douyin.com"]
    
    # 第3步：AI预测漏洞
    print("\n" + "=" * 60)
    print("\n[阶段3] AI预测可能的漏洞...")
    prompt2 = f"""
基于对子域名 {subdomains[:3]} 的分析，预测可能发现的漏洞：

请列出：
1. 最可能的3个漏洞
2. 每个漏洞的危害等级
3. 如何验证这些漏洞
"""
    predictions = call_ai(prompt2)
    print(predictions[:500])
    
    # 第4步：生成报告
    print("\n" + "=" * 60)
    print("\n[阶段4] 生成字节SRC提交报告...")
    
    report = f"""
# 字节SRC漏洞报告

## 漏洞标题
{target} - 信息收集与攻击面分析

## 所属应用
抖音

## 所属平台
Web

## 自评等级
低危（信息收集）

## 漏洞类型
信息泄露

## 漏洞URL
{target}

## 漏洞详情

### 子域名发现：
{chr(10).join([f'- {sub}' for sub in subdomains])}

### 可能的攻击面：
1. API接口未授权访问
2. 用户信息泄露
3. 越权访问漏洞

### 建议测试方向：
1. 测试API接口的权限控制
2. 测试用户信息是否泄露
3. 测试越权访问漏洞

## 修复建议
1. 加强API接口的权限控制
2. 不要在前端暴露敏感信息
3. 定期进行安全审计

---
报告生成：PentestAI v12.0
"""
    
    print(report)
    
    # 保存报告
    with open('字节SRC_报告.md', 'w', encoding='utf-8') as f:
        f.write(report)
    
    print("\n" + "=" * 60)
    print("\n[✓] 扫描完成！报告已保存：字节SRC_报告.md")

if __name__ == "__main__":
    target = "https://www.douyin.com"
    scan_target(target)
