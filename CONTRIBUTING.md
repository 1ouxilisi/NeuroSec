# Contributing to NeuroSec

感谢你对NeuroSec项目的关注！我们欢迎任何形式的贡献。

## 如何贡献

### 报告Bug
- 使用GitHub Issue模板
- 提供详细的复现步骤
- 包含环境信息（OS/Python版本）

### 提交PR
1. Fork本仓库
2. 创建特性分支: `git checkout -b feature/your-feature`
3. 提交修改: `git commit -m 'Add some feature'`
4. 推送分支: `git push origin feature/your-feature`
5. 创建Pull Request

### 代码规范
- 遵循PEP 8
- 添加docstring
- 为新功能添加单元测试
- 保持函数小于50行

## 开发环境设置

```bash
git clone https://github.com/1ouxilisi/NeuroSec.git
cd NeuroSec
pip install -r requirements.txt
python neurosec.py version
```

## 测试

```bash
python -m pytest tests/ -v
```
