# 0.1.3 首次接入与来源修复候选交接

当前状态：**已导入公司 CI 验证的最终 0.1.3 制品；[PR #1](https://github.com/ZhuoJian-AI/zhuojian-enterprise-plugin/pull/1) 待审查，尚未合并或公开发行。国内入口已验证旧版 0.1.2；0.1.3 上线与跨版本验收待完成。**

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
- 国内 `0.1.3` 候选包含 43 个公共文件，Git 快照为 `0f6ca6d778a21f4d5148c72fa8c6fccd2a0b6840`；发行清单 SHA256 为 `74f2d00ec3827f41e382c3e01c3286b15ee46a94ff411b93c1796558c91092bd`。这些是待部署候选标识，不是上线证明。
- 候选以旧发行目录为历史基础，保留所有已发布 `0.1.2` Git 对象和下载字节，旧提交为新提交祖先；原目录保持。切换顺序为不可变文件、refs、latest，公共目录不包含 Git config/hooks/logs 或 SaaS 私有历史。
- 历史 `0.1.2`：本机原生安装字节核对和 Codex 只读业务联通通过；本机 Nginx `1.28.0` 六项检查及 Linux 容器只读运行、健康、HTTP HEAD、29 文件 SHA、私有/缺失 404、POST 403、真实 Git clone 通过。
- 国内真实 HTTPS `0.1.2`：29 个文件的状态/MIME/SHA、发布指针、私有/缺失 404、POST 403、严格 TLS Git clone、隔离原生安装和启动检查通过。真实启动 Trace 观察到该国内源的 `ls-remote` 与 `clone` 退出 0；此时为同版本检查，不冒充跨版本升级。
- Codex `0.164.0-alpha.11.1` 的隔离本机 fixture 已通过首次安装、手动原生升级、启动自动升级及离线保留。fixture 没有企业 MCP/模型调用，不能代替业务验收。

## 待完成

1. 部署并检查真实国内 HTTPS 的 `0.1.3` 指针、全部公共文件、访问拒绝规则及 Git 字节。
2. 在保留的无凭据 `0.1.2` 安装中，仅启动 app-server，验证实际 `0.1.2 → 0.1.3` 自动升级；不手动升级或改写版本。
3. 在另一个隔离安装中从本地 `0.1.2` 来源执行一次 `0.1.3` 接入，验证 `installed` 非空、`available=[]` 时首次结果直接为 `ready`，且实际版本与 Git 来源一致。
4. 验收通过后更新本交接、合并 PR、创建独立 Release 并核验三个下载附件；不覆盖历史 `0.1.1` 或已有国内 `0.1.2` 字节。

GitHub 仅面向维护者，不作为员工使用前提。真实业务写入、上传、企业管理员宿主、WorkBuddy 和手机真机仍须分别验收。
