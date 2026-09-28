"""
Example 3: Adversarial Prompt Generation
==========================================
生成对抗测试用例，测试LLM安全防护
"""
from pentestai.modules.ai_security import AdversarialPromptGenerator
from pentestai.modules.ai_security.prompt_injection_detector import AttackCategory

gen = AdversarialPromptGenerator(seed=42)

print("生成对抗测试用例:")
print("=" * 60)

for cat in [AttackCategory.JAILBREAK, AttackCategory.ROLEPLAY, AttackCategory.SYSTEM_LEAK]:
    cases = gen.generate(category=cat, count=3)
    print(f"\n【{cat.value}】")
    for c in cases:
        print(f"  [{c.difficulty}] {c.prompt[:80]}...")
