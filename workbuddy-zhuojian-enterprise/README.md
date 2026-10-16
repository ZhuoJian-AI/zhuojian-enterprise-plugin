# 灼见企业 · WorkBuddy 试点包

源码目录是连接模板，其中 `.invalid` 地址不能使用；维护者通过构建脚本明确传入 MCP 地址，生成独立试点包。杭州服务已启用 Alphabet 试点；当前机器没有 WorkBuddy，真实宿主导入与 OAuth 仍待验。

连接器采用 `connector-meta.json` / `mcp.json` / `icon.svg` / `skills/` 格式，最低声明版本为 4.24.0。`streamableHttp` 由 WorkBuddy 连接，省略 `auth_mode` 以使用 MCP 服务自身的标准 OAuth 发现、DCR 和 PKCE；不含企业 ID 或凭据。

本人在第一方页面核对企业与授权，业务写入及上传另行确认；宿主工具允许不能代替。包仅含元数据、图标和业务说明，不包含本地服务、安装脚本或 CLI。安装须有用户授权；包没有提交公共市场。

官方流程：[WorkBuddy 连接器](https://open.workbuddy.cn/docs/connector)。市场提交和客户端验收独立于本地打包；当前包未获市场审核。Skill 和图标从 Codex 包的规范源生成，请勿独立编辑。

构建地址：`https://ai-platform.staging.zhuojianai.com/api/v1/enterprise-mcp`

构建脚本不执行安装或部署；当前发布与宿主验收状态以交接记录为准。
