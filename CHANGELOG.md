# Changelog

All notable changes to this project will be documented in this file.

## [v2.0.0] - 2026-09-29
### Added
- Two-layer detection: regex fast filter + LLM semantic layer (Qwen3-32B)
- Benchmark suite: 49 samples (29 attacks + 20 benign)
- 7 attack categories: direct, roleplay, leak, exfil, encoding, delimiter, multi_turn
- Quick start example (examples/05_quickstart.py)
- Chinese language rules (6 new patterns)
- Data exfiltration detection (API keys, credentials, internal IP)

### Metrics
- Accuracy: 95.9%
- Precision: 100%
- Recall: 93.1%
- F1: 96.4%
- False Positive Rate: 0%

### Changed
- Cleaned repository: removed 50+ historical report files
- Updated README with benchmark data and architecture
- Version reset from v48.2 to v2.0.0

## [v48.2] - 2026-09-28
### Added
- Prompt Injection Detector with multi-layer detection architecture
- LLM Vulnerability Scanner (OWASP LLM Top 10)
- Adversarial Prompt Generator (evolutionary algorithm)
- Data Leakage Detector with auto-sanitization
- Unit tests (pytest)
- Examples directory
- GitHub Actions CI
- Chinese language injection rules (8 patterns)
- CLI entry point (neurosec.py)
- Complete dependency list

### Changed
- Cleaned up 12,815 lines of legacy code
- Rewrote README with AI security focus
- Updated .gitignore

## [v48.0] - 2026-09-27
### Added
- Initial release
- 15 core security engines
- 190+ integrated tools
- PySide6 GUI
