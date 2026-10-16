# 0.1.1 分发交接

- 主责：插件客户端分发；执行者：Codex。
- 复用现有 0.1.1 交付制品，插件文件与本机已安装版本逐字一致。
- 增加公开仓库安装说明、市场入口及本地哈希校验脚本。当前 GitHub OAuth 未授权上传 Actions workflow，未新增云端工作流；发布包已本地校验。
- 本地验收：`python scripts/verify_distribution.py --archives <原交付目录>` 通过，覆盖 11 个文件、3 个 ZIP 的清单、SHA256、归档内容；`git diff --check` 通过。
- 内容审查：无账号、令牌、私钥或企业业务数据；MCP 配置使用公开 HTTPS 服务地址。
- 真实客户端边界：复用 2026-10-12 Codex OAuth 与读取工具验收；本次不调用业务、不重新授权，也不宣称 WorkBuddy/写入/上传完整验收。
- 已发布：[公开仓库](https://github.com/ZhuoJian-AI/zhuojian-enterprise-plugin)，[Release v0.1.1](https://github.com/ZhuoJian-AI/zhuojian-enterprise-plugin/releases/tag/v0.1.1)，tag 指向 `209edabdf07f4efa6424215a7374fd58ae005504`。
- 发布验收：仓库 HTML 与 raw marketplace 均匿名 HTTP 200；三个 ZIP 以不含凭据的请求重新下载后，`verify_distribution.py --archives <下载目录>` 全部通过。Release 非草稿，五个附件状态均为 `uploaded`。
- 安装说明已对照本机原生 Codex 的 `plugin marketplace add --help` 与 `plugin add --help` 核实。本次未另行安装或重新 OAuth。
- 网络备注：GitHub 未认证 API 请求返回 403，但公开仓库页面、raw 索引与 Release 文件均正常；身份认证 API 已核实 Release 元信息。
- 未涉及 SaaS 后端、权限变更、服务器部署或个人 Skill 同步。
