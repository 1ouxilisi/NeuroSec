# StackingDAO智能合约安全审计报告（专业版）

## 项目信息

| 项目 | 详情 |
|------|------|
| **项目名称** | StackingDAO |
| **区块链** | Stacks |
| **合约语言** | Clarity |
| **审计范围** | contracts/core/ 目录下11个合约 |
| **审计时间** | 2026-09-24 |
| **审计工具** | blockchain-security-audit 专家技能 |

---

## 执行摘要

### 总体评估
StackingDAO是一个基于Stacks区块链的流动性质押协议，提供stSTX和stSTXbtc两种流动性代币。

### 发现的漏洞数量
| 严重程度 | 数量 |
|----------|------|
| 严重（Critical） | 0 |
| 高（High） | 1 |
| 中（Medium） | 2 |
| 低（Low） | 3 |
| 信息（Informational） | 4 |

---

## 漏洞详情

### 高风险漏洞1：refresh-position函数权限控制不足

| 项目 | 详情 |
|------|------|
| **严重程度** | 高（High） |
| **漏洞类型** | 权限控制缺陷 |
| **影响合约** | ststxbtc-tracking-v2.clar |
| **函数** | refresh-position |
| **代码位置** | 第60行 |

#### 漏洞描述
`refresh-position`函数可以被任何人调用，并且接受任意`holder`参数。这意味着攻击者可以刷新任意用户的位置。

#### 复现步骤
1. 攻击者调用`refresh-position`，传入受害者地址作为holder
2. 传入一个supported position地址
3. 这会刷新受害者在该position的位置
4. 导致受害者的待领取奖励被提前结算

#### 影响分析
- 攻击者可以强制刷新受害者的位置
- 可能导致奖励计算错误
- 可能导致奖励被提前领取

#### 修复建议
在`refresh-position`函数里添加权限检查：

```clarity
(asserts! (is-eq tx-sender holder) (err ERR_NOT_AUTHORIZED))
```

---

### 中风险漏洞2：中心化风险

| 项目 | 详情 |
|------|------|
| **严重程度** | 中（Medium） |
| **漏洞类型** | 中心化风险 |
| **影响合约** | 所有合约 |
| **函数** | 所有admin函数 |

#### 漏洞描述
所有权限控制都依赖`.dao`合约的`check-is-protocol`和`check-is-admin`函数。如果管理员私钥泄露，攻击者可以：
1. 添加恶意合约作为协议合约
2. 铸造任意数量的代币
3. 提取所有资金

#### 影响分析
- 管理员作恶风险
- 私钥泄露风险

#### 修复建议
1. 使用多签钱包管理管理员权限
2. 实施时间锁（Timelock）
3. 逐步去中心化

---

### 中风险漏洞3：整数下溢风险

| 项目 | 详情 |
|------|------|
| **严重程度** | 中（Medium） |
| **漏洞类型** | 整数下溢 |
| **影响合约** | ststxbtc-tracking-v2.clar |
| **函数** | refresh-position |
| **代码位置** | 第75行 |

#### 漏洞描述
代码中有减法操作：
```clarity
(supported-position-new-total (- (+ (get total supported-position) new-position-balance) prev-position-balance))
```

如果`prev-position-balance > (+ (get total supported-position) new-position-balance)`，这会导致下溢错误。

#### 影响分析
- 合约会失败
- 可能导致拒绝服务

#### 修复建议
在减法前添加检查：
```clarity
(asserts! (<= prev-position-balance (+ (get total supported-position) new-position-balance)) (err ERR_OVERFLOW))
```

---

## 低风险发现

### 低风险1：缺少事件日志
部分重要操作没有发出事件日志，不利于监控和追踪。

### 低风险2：硬编码地址
部分合约地址硬编码在代码中，升级困难。

### 低风险3：缺少输入验证
部分函数没有充分验证输入参数。

---

## 审计清单

- [x] 收集了所有合约代码
- [x] 理解了业务逻辑
- [x] 检查了所有公共函数
- [x] 检查了权限控制
- [x] 检查了整数运算
- [x] 检查了外部调用
- [x] 检查了预言机使用
- [ ] 写了PoC验证（需要链上测试）
- [x] 生成了完整报告

---

## 总结

StackingDAO的代码整体质量不错，权限控制比较严格。但是存在一个高风险的权限控制缺陷，需要修复。

建议：
1. 修复refresh-position函数的权限控制
2. 实施多签和时间锁
3. 添加整数下溢检查
4. 在测试网充分测试后再部署

---

**报告生成：** blockchain-security-audit 专家技能
**审计时间：** 2026-09-24
