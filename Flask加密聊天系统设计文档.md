<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" class="logo" width="120"/>

# Flask加密聊天系统设计文档

## 一、项目概述

本系统基于Flask框架，结合RSA非对称加密与AES对称加密技术，实现一套安全的Web聊天系统。系统支持用户注册、登录、好友管理、消息加密传输等功能，保障通信内容的机密性、完整性与身份认证。

---

## 二、系统架构

### 2.1 架构总览

- **前端**：基于react实现用户界面、密钥生成与加密操作。
- **后端**：基于Flask实现API接口、用户管理、消息转发与加解密处理。
- **数据库**：存储用户信息、RSA公钥、消息记录（密文）、会话状态等。
- **缓存/消息队列**：提升消息实时性与系统扩展性（可选）。

---

## 三、核心功能模块

### 3.1 用户管理

- 用户注册：生成RSA密钥对，本地保存私钥，公钥上传服务器。
- 用户登录：身份验证，分配会话令牌。
- 好友管理：添加、删除、查询好友列表。


### 3.2 密钥管理

- RSA密钥对：每个用户唯一，私钥仅存本地，公钥由服务器存储。
- AES会话密钥：每次会话临时生成，用于消息内容加密。
- 密钥交换：通过RSA加密安全传递AES密钥。


### 3.3 消息加密与传输

- 消息加密：客户端用AES加密消息内容。
- 密钥加密：AES密钥用接收方公钥（RSA）加密。
- 消息签名：用发送方私钥对消息摘要签名，接收方用公钥验证。
- 消息传输：通过HTTPS或WebSocket发送加密消息包。


### 3.4 消息解密与验证

- 解密AES密钥：接收方用私钥解密获得AES密钥。
- 解密消息内容：用AES密钥解密消息正文。
- 验证签名：用发送方公钥验证消息完整性与身份。

---

## 四、安全设计

- **机密性**：消息内容全程加密，服务器无法解密。
- **完整性**：消息签名防篡改。
- **认证性**：密钥对与签名确保身份。
- **前向保密**：每次会话生成新AES密钥。
- **防重放**：消息包含时间戳与随机数，防止重放攻击。
- **密钥轮换**：定期更换RSA密钥对。

---

## 五、数据结构设计

### 5.1 用户表

| 字段 | 类型 | 说明 |
| :-- | :-- | :-- |
| user_id | String | 用户唯一ID |
| username | String | 用户名 |
| password | String | 密码（加密存储） |
| public_key | Text | RSA公钥 |
| ... | ... | ... |

### 5.2 消息表

| 字段 | 类型 | 说明 |
| :-- | :-- | :-- |
| msg_id | String | 消息唯一ID |
| from_user | String | 发送者ID |
| to_user | String | 接收者ID |
| timestamp | DateTime | 发送时间 |
| encrypted_key | Text | RSA加密的AES密钥 |
| iv | Text | AES初始向量 |
| ciphertext | Text | AES加密的消息内容 |
| signature | Text | 消息签名 |


---

## 六、接口设计

### 6.1 用户相关

- `/register`：用户注册，提交用户名、公钥等信息。
- `/login`：用户登录，身份验证。
- `/friends`：好友管理接口。


### 6.2 消息相关

- `/send_message`：发送加密消息。
- `/get_messages`：获取聊天记录（密文）。

---

## 七、流程说明

### 7.1 注册与密钥生成

1. 用户注册时本地生成RSA密钥对。
2. 公钥上传服务器，私钥本地保存。

### 7.2 会话密钥协商

1. 发送方生成随机AES密钥。
2. 用接收方公钥加密AES密钥，随消息一同发送。

### 7.3 消息加密与签名

1. 用AES密钥加密消息内容。
2. 用发送方私钥对消息摘要签名。

### 7.4 消息解密与验证

1. 接收方用私钥解密AES密钥。
2. 用AES密钥解密消息内容。
3. 用发送方公钥验证签名。

---

## 八、性能与扩展

- 支持异步消息处理，提升并发能力。
- 支持消息队列和缓存，优化实时性。
- 可扩展为多终端同步、群聊等高级功能。

---

## 九、部署与运维

- 采用HTTPS保障传输安全。
- 定期备份数据库与密钥数据。
- 日志审计与异常告警机制。

---

## 十、总结

本系统通过RSA与AES混合加密、数字签名等机制，保障了聊天通信的安全性和可靠性。架构清晰，易于扩展，适用于对信息安全有较高要求的聊天应用场景。

