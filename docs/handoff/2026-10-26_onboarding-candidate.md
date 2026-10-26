# 0.1.3 首次接入与来源修复交付

当前状态：**国内第一方入口已上线 0.1.3，真实 HTTPS、一次来源接入及实际跨版本启动自动升级均已验证；公开 v0.1.3 已发行并完成五个附件的匿名下载校验。** 客户端交付见 [PR #1](https://github.com/ZhuoJian-AI/zhuojian-enterprise-plugin/pull/1)，版本及附件见 [v0.1.3 Release](https://github.com/ZhuoJian-AI/zhuojian-enterprise-plugin/releases/tag/v0.1.3)。

## 责任和范围

- SaaS 项目维护规范源及第一方静态发行入口，本仓仅接收经验证的客户端制品。
- 插件/Skill 负责首次接入、只读连接诊断、本人登录及国内来源接入。本次 `0.1.3` 修复已安装插件没有出现在 `available` 列表时的来源误判；有效来源不符仍拒绝。
- MCP 服务名和地址、企业权限及本人业务确认规则保持；没有修改业务子系统或新增员工权限。WorkBuddy 共享资源更新不代表其实机流程通过。

## 导入与完整性

最终 `0.1.3` 构建的 17 个白名单文件逐字导入，包含 Codex/WorkBuddy 包和 marketplace 索引；同步 `release/build-receipt.json` 与 `release/SHA256SUMS`。三个 ZIP 只作为待发行附件，没有加入 Git。没有复制原始 CI 日志、个人配置、凭据、业务数据或私有后端源码。

本仓执行 `python scripts/verify_distribution.py --archives <final-build>`，结果为 `PASS: 17 distribution files; version 0.1.3; archives=verified`；`git diff --check` 通过。

| 最终附件 | SHA256 |
| --- | --- |
| `zhuojian-enterprise-0.1.3-pilot.zip` | `5ba177e58ed9fd00bb476c0bf8df168e51b41885206b6486463aeca21cf12a27` |
| `zhuojian-enterprise-marketplace-0.1.3-pilot.zip` | `9198ed6754a050aa3c14ab9a9ec2aaadadec5d13714919faa5c576812587bec6` |
| `workbuddy-zhuojian-enterprise-0.1.3-pilot.zip` | `4167a65990c10e2d0d9eb50e5b3e3909896f93aaa81bdc8e99e143fa0ca953be` |

构建回执 SHA256：`7021bcbd68b650154d69a1e447a6c94f85b8ee400effdd20061329e8018cb91b`。回执的 `not-deployed`、`not-installed`、`not-tested` 只表示构建器不执行这些动作，不能替代运行时验收。

## 已完成的验收

- `0.1.3` 公司隔离 CI：96 项测试、共享源同步检查、构建、分发回执及三个归档验证通过。
- 国内 `0.1.3` 包含 43 个公共文件，Git 快照为 `0f6ca6d778a21f4d5148c72fa8c6fccd2a0b6840`；发行清单 SHA256 为 `74f2d00ec3827f41e382c3e01c3286b15ee46a94ff411b93c1796558c91092bd`。固定发行入口的 active、healthy、公共文件匹配及路由匹配均通过核验。
- 本版以旧发行目录为历史基础，保留所有已发布 `0.1.2` Git 对象和下载字节，旧提交为新提交祖先；原目录保持。切换顺序为不可变文件、refs、latest，公共目录不包含 Git config/hooks/logs 或 SaaS 私有历史。
- 历史 `0.1.2`：本机原生安装字节核对和 Codex 只读业务联通通过；本机 Nginx `1.28.0` 六项检查及 Linux 容器只读运行、健康、HTTP HEAD、29 文件 SHA、私有/缺失 404、POST 403、真实 Git clone 通过。
- 国内真实 HTTPS `0.1.2`：29 个文件的状态/MIME/SHA、发布指针、私有/缺失 404、POST 403、严格 TLS Git clone、隔离原生安装和启动检查通过。真实启动 Trace 观察到该国内源的 `ls-remote` 与 `clone` 退出 0；此时为同版本检查，不冒充跨版本升级。
- Codex `0.164.0-alpha.11.1` 的隔离本机 fixture 已通过首次安装、手动原生升级、启动自动升级及离线保留。fixture 没有企业 MCP/模型调用，不能代替业务验收。

## 0.1.3 真实验收

- 国内直接 HTTPS 保留 TLS 校验且拒绝跟随重定向，43 个公共文件逐项状态、MIME、SHA256 全匹配。最新指针为 `0.1.3` 与上述提交；HEAD 200、私有/缺失路径 404、POST 403 均通过。
- 保留的无凭据 `0.1.2` 安装仅启动 app-server，自动安装最终 `0.1.3` 的 8 个文件，原始 SHA256 全匹配。没有手动升级、改写版本或更换来源；真实 Git Trace 的国内 `ls-remote`、`clone` 均退出 0，app-server 正常退出 0。
- 宿主实际 Git checkout 的 HEAD 为上述 `0.1.3` 提交，9 个分发文件（Codex 8 文件及市场索引）与最终构建逐字匹配，无私有源码。唯一额外项为宿主生成的安装标记，其来源、main 引用、revision 及无 sparse 配置均已核验。
- 另一份隔离安装从冻结本地 `0.1.2` 包原生安装，再执行一次最终 `0.1.3` 的 `configure(apply=True)`。首次直接返回 `ready`，实际版本为 `0.1.3`，8 文件 SHA、登记及有效 Git/main 来源匹配。真实中间状态 `installed` 非空、`available=[]` 已被正确接受，没有用第二次只读检查掩盖首次结果。
- 两项隔离验收未复制用户凭据，禁用企业 MCP，无模型或业务调用。早期测试夹具失败记录保留，未覆盖为成功。
- 现有真实宿主核验安装版本为 `0.1.3`、国内 Git/main 来源且接入脚本返回 `ready`；OAuth 前后保持，其他用户配置哈希保持，身份查询和获权目录完成并返回 26 项能力。
- 真实 Windows 宿主原有 `core.autocrlf=true` 将 LF 转为 CRLF：Git 原 blob 与 CI 制品逐字一致，安装文件与原生 checkout 逐字一致，差异仅为已声明的换行转换。原始字节比较失败记录及补充证明均保留，未声称该宿主安装文件与 ZIP 原始字节完全相同；没有为验收改动全局 Git 配置或重装。

## 发布与剩余边界

维护者公开发行使用独立 `v0.1.3`，对应 PR #1 合并提交 `f1df7aa8dc4a2d21cfc0c52953cd5646d4b72c35`。发布于 `2026-10-26 02:32:12 UTC`，已核验为最新稳定 Release。

五个附件（三个 ZIP、构建回执、校验表）已逐项匿名下载，HTTP 200，实际 SHA256、大小和 API 文件摘要全部匹配；下载得到的三个 ZIP 再通过归档白名单和逐文件内容校验。标签指向上述已验证合并提交，没有将文档收尾提交重新指派给该标签。

历史 `v0.1.1` 标签仍为 `209edabdf07f4efa6424215a7374fd58ae005504`，其 Release 及五个附件的不可变字段前后保持；已有国内 `0.1.2/0.1.3` 字节未覆盖。

GitHub 仅面向维护者，不作为员工使用前提。真实业务写入、上传、企业管理员宿主、WorkBuddy 和手机真机仍须分别验收。
