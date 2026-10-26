# 灼见企业插件

在 Codex 中连接你已获授权的企业业务：查询业务数据、发现可用应用、处理资料，并把结果交付到企业工作空间。

**当前候选为 0.1.3，已通过公司隔离 CI 和分发制品校验，尚待上线验收及公开发行。** 国内第一方入口已承载并实际验证 `0.1.2`；不能据此认定 `0.1.3` 已上线或跨版本自动升级已通过。见[候选交接](docs/handoff/2026-10-26_onboarding-candidate.md)。

[维护者版本附件](https://github.com/ZhuoJian-AI/zhuojian-enterprise-plugin/releases) · [版本说明](./release/RELEASE_NOTES.md)

## 员工安装与首次连接

员工使用国内灼见官方分发和更新入口，不需要访问 GitHub、配置 VPN 或维护代理。`0.1.3` 完成真实入口验收后，本页会提供对应的安装和旧来源迁移步骤。已有版本和授权应保留。

需要支持插件的 Codex 及已有权限的灼见企业账号。安装后运行插件的设置引导，或选择“灼见企业”并说：

> 检查灼见企业连接并引导我登录。

引导先检查当前工具和连接。网络正常且需要授权时，使用宿主原生流程，由你在灼见第一方页面用自己的账号核对企业、身份和授权范围。网络认证、证书或服务异常会给出对应状态和下一步，不把“已安装”当作“已连接”，也不把换热点作为正式使用条件。

授权后以真实身份和获权目录验证可用范围。工具尚未加载时，按宿主支持的方式刷新连接，必要时在新聊天继续。浏览器已登录灼见，不等于插件已获授权。

`zhuojian-enterprise-pilot` 是现有市场的技术名称，界面可能显示“灼见企业试点”。不同宿主版本的入口可能不同；没有终端或代码环境时使用宿主已有的插件连接界面，不要求员工自行安装开发依赖。

### 更新与旧版本迁移

已核对的 Codex `0.164.0-alpha.11.1` 会在宿主启动时后台检查已登记的 Git 更新源，有新 revision 时刷新已安装插件缓存。这不是固定周期轮询，也不保证当前聊天立即加载新工具或 Skill；必要时新开聊天。更新源暂时不可达时保留已有版本，并明确提示状态。

`0.1.3` 修复来源迁移中的状态误判：原生宿主已经返回真实已安装插件时，接入脚本优先核对该安装项的来源，不再要求它同时出现在“尚可安装”的列表中。`installed` 非空而 `available=[]` 是合法状态；一次接入能否直接完成仍以本次真实验收为准。

旧 `0.1.1` 的本地或境外来源需要一次迁移到国内官方 Git 来源，再完成升级；本地 ZIP 路径不会自动联网下载新版本。接入通过宿主原生市场管理，不覆盖其他来源，不安装自升级常驻进程，也不修改整机代理或证书。

本次保持 MCP 服务名称和连接地址，不要求为了升级主动退出登录或删除原有授权；升级后仍须核验当前企业身份和有效权限。过期或撤销的授权按实际状态处理，插件更新不增加业务权限。

## 维护者安装与手动分发

GitHub 仅供维护者托管和制品核验，不作为员工安装或更新的前提：

```sh
codex plugin marketplace add ZhuoJian-AI/zhuojian-enterprise-plugin
codex plugin add zhuojian-enterprise@zhuojian-enterprise-pilot
```

维护者也可从版本附件取得 ZIP，通过获准的国内通道交付：

1. 从 [Releases](https://github.com/ZhuoJian-AI/zhuojian-enterprise-plugin/releases) 下载目标版本的 `zhuojian-enterprise-marketplace-0.1.3-pilot.zip` 并核对 SHA256；候选未发行时不要把旧附件当成新版本。
2. 完整解压，保留 `.agents` 隐藏目录。
3. 将下面的路径换成解压后包含 `.agents/plugins/marketplace.json` 的目录：

```sh
codex plugin marketplace add "/path/to/extracted-marketplace"
codex plugin add zhuojian-enterprise@zhuojian-enterprise-pilot
```

不要将 ZIP 文件或其中单独的 `zhuojian-enterprise` 子目录作为 marketplace 根目录。本地路径适用于手动导入，持续更新使用经部署和验收的国内官方来源。

包内原 README 的 `.invalid` 地址是规范源模板说明；本仓库和附件中的 `mcp.json` 已配置实际公开服务地址。格式说明见 [OpenAI 插件文档](https://developers.openai.com/plugins/build/plugins)。

## 账号与权限

- 插件面向灼见平台已开通接入的企业，不只对应某个固定企业；具体能力由当前身份和服务端权限决定。
- 安装包不包含个人账号或令牌。下载插件不会获得其他企业的数据权限；缺少账号或权限时联系所在企业管理员。
- 写入、上传等操作仍由本人在第一方页面确认，宿主工具许可不能代替业务确认。
- 插件提供企业工具和业务说明；模型与本机代码执行能力由客户端提供。

## 包的区别

| 文件 | 用途 |
| --- | --- |
| `zhuojian-enterprise-marketplace-0.1.3-pilot.zip` | Codex 完整市场包，供手动分发和导入 |
| `zhuojian-enterprise-0.1.3-pilot.zip` | 单独插件目录，供支持该格式的导入流程使用 |
| `workbuddy-zhuojian-enterprise-0.1.3-pilot.zip` | WorkBuddy 连接器试点包，真实客户端导入及 OAuth 待验收 |

WorkBuddy 说明见[连接器 README](./workbuddy-zhuojian-enterprise/README.md)。本次未提交公共插件商店，也未完成 Claude Code 客户端适配验收。

## 验证与维护

本候选继承首次接入 Skill、只读连接诊断、本人登录引导和国内来源接入，并修复真实安装状态校验。17 个文件从规范源最终 `0.1.3` 构建逐字导入，三个 ZIP 的哈希及内容校验通过；公司隔离 CI 已通过 96 项测试、共享源同步检查、构建和分发验证。

此前 `0.1.2` 已通过本机及 Linux 容器静态分发检查、国内真实 HTTPS 的 29 个公共文件校验、严格 TLS Git clone、原生安装和启动检查。隔离 fixture 还覆盖版本升级及离线保留；这些历史证据不替代 `0.1.3` 的真实上线、一次来源迁移和跨版本启动自动升级验收。

Codex 只读业务联通已有独立验收；真实业务写入、上传、企业管理员宿主、WorkBuddy 和手机真机仍须分别验证。具体范围见[候选交接](docs/handoff/2026-10-26_onboarding-candidate.md)。

校验文件见 [`release/SHA256SUMS`](./release/SHA256SUMS) 和 [`release/build-receipt.json`](./release/build-receipt.json)。回执中的 `not-deployed`、`not-installed`、`not-tested` 说明构建器不执行这些动作，不能代表当前线上状态。

维护者运行 `python scripts/verify_distribution.py` 检查分发文件，加 `--archives <下载目录>` 同时核对 ZIP 哈希与内容。新版本单独发行，保留历史版本字节。
