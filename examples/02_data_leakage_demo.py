"""
Example 2: Data Leakage Detection
===================================
扫描AI输出中的敏感信息并自动脱敏
"""
from pentestai.modules.ai_security import DataLeakageDetector

detector = DataLeakageDetector()

# 模拟AI输出（包含敏感信息）
ai_response = """
根据您的查询，相关信息如下：
联系电话：13812345678
邮箱：admin@company.com
内网地址：http://192.168.1.100:8080
API Key：sk-live-abcdef1234567890xyz
"""

print("原始输出:")
print(ai_response)
print("-" * 40)

# 扫描
findings = detector.scan(ai_response)
print(f"\n发现 {len(findings)} 个泄露:")
for f in findings:
    print(f"  [{f.severity}] {f.description}: {f.matched_content[:30]}...")

# 自动脱敏
safe_output, _ = detector.sanitize(ai_response)
print(f"\n脱敏后输出:")
print(safe_output)
