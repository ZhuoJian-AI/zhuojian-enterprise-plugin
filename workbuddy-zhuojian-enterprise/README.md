# 灼见企业 · WorkBuddy 连接包

源码目录是连接模板，其中 `.invalid` 地址不能使用；维护者通过构建脚本明确传入 MCP 地址，生成独立连接包。包版本以 `connector-meta.json` 为准，已发行版本以核验过的第一方发行记录和字节摘要为准；实际能力以目标服务工具、当前身份及本次授权范围为准，不从源码版本推定已经上线或安装。

连接器保留 `connector-meta.json` / `mcp.json` / `icon.svg` / `skills/` 格式，最低声明版本为 4.24.0。`streamableHttp` 由 WorkBuddy 连接，省略 `auth_mode` 以使用 MCP 服务自身的标准 OAuth 发现、DCR 和 PKCE；不含企业 ID 或凭据，也不包含常驻本地 MCP 服务或安装器。

本人在第一方页面核对企业与身份并选择范围。员工的业务能力、平台生图及文件分别发现和校验；企业管理员通过明确授予的 `admin:manage:read/write` 使用 `discover_admin_capabilities`、`query_admin` 和 `execute_admin`，现有显式目录覆盖 164 项本企业管理操作，注册服务器和代码上传除外。没有实际管理工具或目标服务尚未部署时，不宣称管理能力已可用。

四步连接默认只读，管理写权限须由本人明确选择，旧授权不自动扩权。密码和长期密钥只在本人页面输入；业务写入及文件上传仍需原有确认，宿主工具允许不能代替。文件访问另受所选工作空间限制，新增空间不会自动进入旧连接。

灼见图片能力通过 `get_media_capabilities` 独立查询。本人一次授予 `files:write` 后，可按明确生图意图调用实际可用的 `generate_image` 创建新图片，复用网页相同 SaaS 服务及正式工作空间交付，无额外逐图业务审批；不改用宿主订阅生图。用 `get_media_job` 查询同一 `jobId`，未知不换 `requestId` 重发，完成以正式 file/version/hash 回执为准。没有视频工具时不承诺生视频。详见[业务、图片与文件说明](skills/zhuojian-enterprise/SKILL.md)。

首次使用或工具缺失时，转到[连接引导](skills/setup/SKILL.md)，区分网络和授权状态，使用 WorkBuddy 自己的连接流程。宿主具备 Python/终端时，可运行随包只读诊断脚本并加 `--skip-host`；不要把本机 Codex 的登录状态当作 WorkBuddy 已连接。没有代码环境时使用原生连接界面，明确未能自动诊断的范围，不要求员工安装开发工具。

Codex 的来源核验和更新脚本仅适用于 Codex，不能推定 WorkBuddy 自动更新或自动 onboarding 已通过。真实客户端导入、本人 OAuth、管理员操作、图片及文件流程分别验收；安装和公共市场审核也独立于本地打包，不宣称所有宿主均已验证。

官方流程：[WorkBuddy 连接器](https://open.workbuddy.cn/docs/connector)。本包不因构建成功取得公共市场审核。Skill 和图标从 Codex 规范源生成，请勿独立编辑共享副本。

构建地址：`https://ai-platform.staging.zhuojianai.com/api/v1/enterprise-mcp`

构建脚本不执行安装或部署；当前发布与宿主验收状态以交接记录为准。
