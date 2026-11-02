# 企业管理员 AI 管理客户端最终候选（未发行）

0.1.6 最终客户端文件已从 SaaS 规范源构建并验证导入公共 PR #6 工作树。截至本次交接更新，公共 PR #6 尚未合并，0.1.6 尚未正式发行或激活国内分发；SaaS 部署及各宿主真实管理员验收需另记完成回执。

## 规范源与产物

- 规范源：`ZhuoJian-AI/ai-platform` 的 `plugins/`；最终精确源提交 `06576e157707f282022e7f5df9f19640e55d9c6f`，对应已合并的 SaaS PR #808。此前 `07daa51` 仅为早期候选，不是本次最终包来源。
- 公共分支：`codex/enterprise-admin-ai-20261102`，PR #6；最初从 `origin/main` 的 `b68d0aa05f539df25100eaed11e277229b9a7ea0` 建立。最终导入前公共候选提交为 `0fcffc22370ecd17c5c89eba239b7238931eb7c1`，见来源回执。
- 本轮版本为0.1.6：包含 Codex 插件、WorkBuddy 连接器与 Codex marketplace 三个 ZIP，共19个显式分发文件。0.1.4既有公开发行及0.1.5独立分发记录保留，不覆盖旧版本或不可变附件。
- 后台18份嵌入模板由现役生成链同步；连接 guide 与按企业导出包使用同版助手。公共仓库仅导入客户端白名单及回执，不承载 SaaS 私有后端、账号或生产配置。

## 行为与权限边界

Codex 配对助手请求 `business:read,files:read,files:write,admin:read,admin:manage:read,admin:manage:write` 作为客户端申请上限。第一方页面默认只读，实际授予范围由本人选择及服务端身份决定；助手不调用批准接口，不携带管理员 Cookie 或密码。旧连接和刷新令牌不能扩大为新管理授权。

员工继续使用已有业务工具。企业管理员仅在当前服务端实际公开相应工具时，使用 `discover_admin_capabilities`、`query_admin` 与 `execute_admin`；可用操作、输入及权限以实际服务端目录和 scopes 为准。服务器注册与代码上传保留人工处理。写入沿用第一方确认、原请求幂等和未知结果不重放；密码等私密输入仅在本人第一方页面办理。文件操作另外受 `files:read` / `files:write` 和连接所选工作空间限制，新建空间不会自动加入已有连接。

Codex 主文件经 `plugins/build_packages.py sync-shared` 同步 WorkBuddy 共享副本；此处“共享副本”指包内文件同步，不指公司共享 CI 机器。Claude Code 使用其原生 PTY 流程，Claude Desktop 与 WorkBuddy 使用各自原生连接器，不套用其他宿主命令。插件说明或格式兼容检查不代表这些宿主的真实管理员流程已经通过。

## 已完成的验证

本轮正式 CI 均在本机独立 WSL2 `COA-CI` 执行，记录为 `authorized-local-ci`，`company_executed_tests=false`、`github_executed_tests=false`。原始测试记录保留实际 `tested_sha`，只对具有 Git blob 范围一致性证明的内容复用结果，没有将较早提交测试改写为最终合并 SHA 的重新执行。

| 验证 | 实际执行与范围 |
| --- | --- |
| 插件、共享副本、配对与包装测试 | 在 `ca04140d17a55097fc35e91c102f74029ca69103` 执行 `unittest discover -s plugins/tests -v`，104项通过；同轮 `check-source` valid（0.1.6）及当前文档检查通过。`plugins/` 与相关检查脚本的完整 Git 清单摘要在该提交和最终 `06576e15` 一致，原日志与范围证明保留。 |
| 后台插件导出测试 | 在同一 `ca04140d` 执行 `test_enterprise_plugin_export.py`，3项通过；这是离线/模拟路由导出测试。最终证据保留实际测试提交及来源范围证明；同次最终导入还独立比较包内18份来源文件与 `06576e15` Git blob。 |
| 最终包与分发镜像 | 在精确最终源 `06576e157707f282022e7f5df9f19640e55d9c6f` 实际执行 build、verify、国内 publication 构建和分发镜像构建，全部退出0；输出 `packages-016-06576e15`，19文件、三ZIP通过校验。 |
| 本地分发运行检查 | 同次最终镜像在 COA-CI 的临时容器 HTTP 入口检查89个公共文件，并执行 HTTP Git 克隆，全部通过，测试容器已清理。这是本地候选分发验证，正式国内 HTTPS、线上 Git 更新源及安装验收仍待发行后执行。 |
| 最终公共导入 | 读取同次成功 CI 记录并核验日志 SHA256、原始构建回执、19文件及三ZIP成员/字节。18份来源文件与最终 Git blob 比较，仅接受构建器规定的 MCP 地址替换和 README 固定构建尾段；marketplace 的 ID、路径和安装策略保持原样。 |

早期 Windows 的103通过/1符号链接权限跳过，以及调整版本后的28项包装检查，保留为开发阶段历史；最终候选的插件测试依据为上述 COA-CI 的104项通过结果。

## 回执与后续发布

- [release/build-receipt.json](../../release/build-receipt.json) 是最终构建器原始回执，SHA256 为 `54540ee6c07f87aad0839a546cdeb53b9519856cc9f7780f4157974cd8299373`；[release/SHA256SUMS](../../release/SHA256SUMS) 列出同次三个 ZIP 哈希。
- [release/source-receipt.json](../../release/source-receipt.json) 记录最终规范源 SHA、19文件/18来源文件、三ZIP、CI记录与各检查日志摘要，以及导入前公共候选提交。导入工具没有执行构建、CI、提交、推送或发布。
- 构建回执的 `not-deployed`、`not-installed`、`hostAcceptance: not-tested` 描述构建器没有执行这些动作；正式发行和真实验收状态仍须以随后独立回执更新。

待主执行者在本机 COA-CI 对最终公共候选运行 `python scripts/verify_distribution.py --archives <同次构建目录>`，保留回执后提交并合并 PR #6，再按原入口发布0.1.6与国内分发。发行后核验 HTTPS、Git 更新源、附件哈希和历史版本保留；本次本地构建及导入不代表这些步骤已完成。

SaaS 对应版本部署后，仍需本人重新授权，分别完成 Codex、WorkBuddy、Claude 的原生连接、管理查询、第一方确认写入、私密输入及文件空间限制验收，并验证撤销后失效。Claude Code 与 Claude Desktop 若分别使用，应各记结果，不能互相代替。MCP SDK 整链测试、模拟浏览器或单一宿主通过，也不能替代其他宿主的原生管理员或模型推理验收。
