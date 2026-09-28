"""
Tests for Data Leakage Detector
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pentestai.modules.ai_security.data_leakage_detector import (
    DataLeakageDetector,
    LeakageType,
)


def test_phone_leak():
    detector = DataLeakageDetector()
    findings = detector.scan("联系我 13812345678 详谈")
    assert any(f.leakage_type == LeakageType.PII_PHONE for f in findings)
    print("[PASS] test_phone_leak")


def test_email_leak():
    detector = DataLeakageDetector()
    findings = detector.scan("我的邮箱是 test@example.com")
    assert any(f.leakage_type == LeakageType.PII_EMAIL for f in findings)
    print("[PASS] test_email_leak")


def test_api_key_leak():
    detector = DataLeakageDetector()
    findings = detector.scan("API Key: sk-abc123xyz789def456ghi012jkl")
    assert any(f.leakage_type == LeakageType.CREDENTIAL_API_KEY for f in findings)
    print("[PASS] test_api_key_leak")


def test_sanitize():
    detector = DataLeakageDetector()
    text = "我的手机号是13812345678，邮箱test@example.com"
    safe, findings = detector.sanitize(text)
    assert "13812345678" not in safe
    assert "test@example.com" not in safe
    print("[PASS] test_sanitize")


if __name__ == "__main__":
    test_phone_leak()
    test_email_leak()
    test_api_key_leak()
    test_sanitize()
    print("\n✅ All leakage tests passed!")
