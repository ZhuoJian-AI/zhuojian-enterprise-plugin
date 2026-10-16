# 灼见企业 · Codex 试点包

源码目录是连接模板，其中 `.invalid` 地址不能使用；维护者通过构建脚本明确传入 MCP 地址，生成可安装的独立试点包。实际发布与宿主验收状态以项目交接回执为准。

包采用根目录 `plugin.json` / `mcp.json` / `skills/` 格式；远程 server 只含 `type` 和 `url`，原生宿主通过标准元数据发现 OAuth 并完成 DCR/PKCE。不含企业 ID 或凭据；真实企业、身份与授权范围在第一方流程中绑定。插件本身不授予业务权限。业务操作和上传须由本人在第一方页面确认，宿主工具允许不能代替。

本插件可通过构建工具同时生成的 Codex marketplace 交付：完整解压 marketplace ZIP 后，将含 `.agents/plugins/marketplace.json` 的根目录作为 marketplace 来源。不要把此单独插件目录或 ZIP 文件当作 marketplace 根目录。索引声明可选安装及安装时认证策略；实际 OAuth 可能在宿主连接时发起，以宿主为准。构建和验证不会登记来源或安装插件。

构建不代表服务可用或所有客户端流程已验收。安装须有用户授权；安装后完成 OAuth，并在新会话调用 `get_identity` 检查身份。2026-10-12 的 `0.1.1` Alphabet 试点已完成真实 Codex OAuth 和三项读取工具验收；真实业务写入、上传和企业管理员宿主联测仍待验。

官方格式：[OpenAI 插件打包](https://developers.openai.com/plugins/build/plugins)。包内 Skill 是业务说明的唯一编辑源；WorkBuddy 副本由仓库构建工具同步。

构建地址：`https://ai-platform.staging.zhuojianai.com/api/v1/enterprise-mcp`

构建脚本不执行安装或部署；当前发布与宿主验收状态以交接记录为准。
