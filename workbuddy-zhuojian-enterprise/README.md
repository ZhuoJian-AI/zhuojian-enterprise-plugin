# 灼见企业 · WorkBuddy 试点包

源码目录是连接模板，其中 `.invalid` 地址不能使用；维护者通过构建脚本明确传入 MCP 地址，生成独立试点包。杭州服务已启用 Alphabet 试点；当前机器没有 WorkBuddy，真实宿主导入与 OAuth 仍待验。

连接器采用 `connector-meta.json` / `mcp.json` / `icon.svg` / `skills/` 格式，最低声明版本为 4.24.0。`streamableHttp` 由 WorkBuddy 连接，省略 `auth_mode` 以使用 MCP 服务自身的标准 OAuth 发现、DCR 和 PKCE；不含企业 ID 或凭据。

本人在第一方页面核对企业与授权，业务写入及上传另行确认；宿主工具允许不能代替。包包含元数据、图标、业务说明和只读连接诊断脚本，不包含常驻本地 MCP 服务或安装器。安装须有用户授权；包没有提交公共市场。

`0.1.3` 的共享业务 Skill 在首次使用或工具缺失时转到[连接引导](skills/setup/SKILL.md)，先分清网络与授权状态，再使用 WorkBuddy 自己的连接流程。宿主具备 Python/终端时可使用随包诊断脚本并加 `--skip-host`，不要在 WorkBuddy 中把本机 Codex 的登录状态当成当前连接状态。没有代码环境时使用原生连接界面，明确未能自动诊断的范围，不要求员工安装开发工具。WorkBuddy 未声明未经验证的自动 onboarding 机制，真实客户端导入、首次授权和工具恢复仍待验收。

本版同步 Codex 更新检查脚本的已安装来源核验修复；该脚本仅用于 Codex，不代表 WorkBuddy 自动更新已经验收。已公开的 `0.1.2` 制品保留。

官方流程：[WorkBuddy 连接器](https://open.workbuddy.cn/docs/connector)。市场提交和客户端验收独立于本地打包；当前包未获市场审核。Skill 和图标从 Codex 包的规范源生成，请勿独立编辑。

构建地址：`https://ai-platform.staging.zhuojianai.com/api/v1/enterprise-mcp`

构建脚本不执行安装或部署；当前发布与宿主验收状态以交接记录为准。
