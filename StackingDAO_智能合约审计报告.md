# StackingDAO智能合约安全审计报告

## 项目信息

| 项目 | 详情 |
|------|------|
| **项目名称** | StackingDAO |
| **区块链** | Stacks |
| **类型** | DeFi、Liquid Staking |
| **审计范围** | contracts/core/ 目录下的核心合约 |
| **最高奖金** | $100,000 |

---

## 审计的合约

### 1. dao.clar - DAO权限管理合约
### 2. ststx-token.clar - stSTX代币合约
### 3. ststxbtc-token-v2.clar - stSTXbtc代币合约 v2
### 4. ststxbtc-tracking-v2.clar - 奖励追踪合约 v2
### 5. ststxbtc-tracking-data-v2.clar - 追踪数据合约 v2

---

## 发现的潜在漏洞

### ⚠️ 漏洞1：refresh-position函数可被任意调用

**位置：** ststxbtc-tracking-v2.clar

**问题：**
`refresh-position` 函数可以被任何人调用，但是需要传入 `holder` 参数。

攻击者可以：
1. 传入任意 holder
2. 传入任意 supported position
3. 刷新 holder 在该 position 的位置

**影响：**
- 攻击者可以刷新别人的位置
- 这可能导致奖励计算错误
- 可能导致双重领取奖励

**复现步骤：**
1. 攻击者调用 `refresh-position`，传入受害者地址作为 holder
2. 传入一个 supported position
3. 这会刷新受害者在该 position 的位置
4. 这可能导致受害者的奖励被提前结算

**修复建议：**
在 `refresh-position` 函数里检查 `tx-sender` 是否等于 `holder`：

```clarity
(asserts! (is-eq tx-sender holder) (err ERR_NOT_AUTHORIZED))
```

---

### ⚠️ 漏洞2：权限控制依赖外部合约

**位置：** 所有合约

**问题：**
所有权限控制都依赖 `.dao` 合约的 `check-is-protocol` 和 `check-is-admin` 函数。

如果 `.dao` 合约被攻破，或者管理员私钥泄露，攻击者可以：
1. 添加恶意合约作为协议合约
2. 铸造任意数量的代币
3. 提取所有资金

**影响：**
- 中心化风险
- 管理员作恶风险

**修复建议：**
1. 使用多签钱包管理管理员权限
2. 实施时间锁（Timelock）
3. 逐步去中心化

---

### ⚠️ 漏洞3：整数溢出/下溢

**位置：** ststxbtc-tracking-v2.clar

**问题：**
Clarity语言本身没有整数溢出问题，但是我看到代码里有减法操作：

```clarity
(supported-position-new-total (- (+ (get total supported-position) new-position-balance) prev-position-balance))
```

如果 `prev-position-balance > (+ (get total supported-position) new-position-balance)`，这会导致下溢错误。

**影响：**
- 合约会失败
- 可能导致拒绝服务

**修复建议：**
在减法前检查 `prev-position-balance <= (+ (get total supported-position) new-position-balance)`。

---

## 已检查的安全措施

### ✅ 好的实践：

1. ✅ 所有公共函数都有权限控制
2. ✅ 使用了 `asserts!` 进行输入验证
3. ✅ 使用了 `try!` 进行错误处理
4. ✅ 代币合约符合SIP-010标准
5. ✅ 数据和逻辑分离（tracking-data-v2 和 tracking-v2）

---

## 总结

### 风险等级：**中等**

### 主要发现：
1. **refresh-position函数可被任意调用** - 需要修复
2. **中心化风险** - 管理员权限过大
3. **整数下溢可能** - 需要修复

### 建议：
1. 修复 refresh-position 函数的权限控制
2. 实施多签和时间锁
3. 添加整数下溢检查

---

**报告生成：PentestAI v12.0**
**审计时间：2026-09-24**
