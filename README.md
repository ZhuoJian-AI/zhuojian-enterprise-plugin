# 灼见企业插件

在 Codex 中连接你已获授权的企业业务：查询业务数据、发现可用应用、处理资料，并把结果交付到企业工作空间。

**当前候选版本为 0.1.2，已完成本机验收，尚未公开发布。国内员工分发入口尚未部署。** 详见[本次候选交接](docs/handoff/2026-10-26_onboarding-candidate.md)；维护者公开版本以 [Releases](https://github.com/ZhuoJian-AI/zhuojian-enterprise-plugin/releases) 为准。

[维护者版本附件](https://github.com/ZhuoJian-AI/zhuojian-enterprise-plugin/releases/latest) · [版本说明](./release/RELEASE_NOTES.md)

## 员工安装与首次连接

员工端的正式方案是**国内灼见官方分发和更新入口**，不要求员工访问 GitHub、配置 VPN 或维护代理。当前 `0.1.2` 候选尚待接入和验收这个入口；未上线前，不能将本仓库的 GitHub 地址当成员工可用入口。

需要支持插件的 Codex 版本，以及已有权限的灼见企业账号。国内入口发布并验收后，本页将给出可直接交给 Codex 执行的员工安装步骤。旧版本和现有授权应保留，不能为了等待入口就绪先卸载。

安装后运行插件的设置引导，或选择“灼见企业”并说：

> 检查灼见企业连接并引导我登录。

引导先检查当前工具和连接：网络正常且需要授权时，使用宿主原生流程，由你在灼见第一方页面用**自己的账号**核对企业、身份和授权范围。网络认证、证书或服务异常会给出对应状态与下一步，不把“已安装”当作“已连接”，也不把换热点作为正式使用条件。

授权后由真实身份和能力查询验证可用范围；工具尚未加载时，按宿主实际支持的方式刷新连接，必要时在新聊天继续。浏览器里已经登录灼见，不等于插件已经完成授权。

`zhuojian-enterprise-pilot` 是现有插件市场的技术名称，因此界面可能显示“灼见企业试点”。

不同版本的图形界面入口可能不同。没有终端或代码环境时，使用宿主已有的插件连接界面；不能要求员工为连接业务自行安装开发依赖。

### 更新与旧版本迁移

在已核对的 Codex `0.164.0-alpha.11.1` 中，宿主启动时会在后台检查已登记的 Git 更新源，有新 revision 时刷新已安装插件缓存；没有固定周期轮询的承诺。本机隔离验收已覆盖首次安装、原生升级、启动自动升级和离线保留安装，但国内正式 HTTPS 入口尚未部署，员工端自动更新仍未启用。

实际是否完成更新，以本机显示的已安装版本为准。更新插件文件不代表当前聊天已加载新工具或新 Skill，必要时新开聊天。更新源暂时不可达时应保留已有版本，并明确提示更新状态。插件不安装自升级常驻进程，不修改整机代理或证书。

旧 `0.1.1` 无论来自本地解压目录还是 GitHub，都需要在国内入口就绪后核对并切换到国内官方来源，再完成本次升级。使用宿主支持的市场管理流程处理，不覆盖其他来源或删除现有授权。不要把本地 ZIP 路径当成自动联网更新源。

本次保留 MCP 服务名称和连接地址，不要求为了升级主动退出登录或删除原有授权；升级后仍须核验当前企业身份和有效权限，过期或撤销的授权按实际状态处理。插件更新不增加业务权限。

## 维护者安装与手动分发

以下 GitHub 通道只面向维护者和制品核验，不作为员工安装或更新的前提：

```sh
codex plugin marketplace add ZhuoJian-AI/zhuojian-enterprise-plugin
codex plugin add zhuojian-enterprise@zhuojian-enterprise-pilot
```

维护者也可从版本附件取得 ZIP，校验后通过获准的国内通道交付：

1. 从 [Releases](https://github.com/ZhuoJian-AI/zhuojian-enterprise-plugin/releases/latest) 下载对应版本的 **`zhuojian-enterprise-marketplace-0.1.2-pilot.zip`**；尚未发布时不要把旧版本下载结果当成新版本。
2. 完整解压，保留 `.agents` 隐藏目录。
3. 将下面的路径换成解压后包含 `.agents/plugins/marketplace.json` 的目录，再执行安装命令：

```sh
codex plugin marketplace add "/path/to/extracted-marketplace"
codex plugin add zhuojian-enterprise@zhuojian-enterprise-pilot
```

不要把 ZIP 文件或其中单独的 `zhuojian-enterprise` 子目录作为 marketplace 根目录。

本地 ZIP 适用于手动分发和离线导入。添加解压后的本地路径，不会让该路径自动联网下载新版本；员工持续更新使用经部署和验收的国内官方来源。

包内原 README 的 `.invalid` 源码模板说明供维护者参考；本仓库及下载包的 `mcp.json` 已配置实际服务地址，可按本页直接安装。

官方格式与市场说明：[OpenAI 插件文档](https://developers.openai.com/plugins/build/plugins)。

## 账号与权限

- 插件面向灼见平台已开通接入的企业，不只对应某个固定企业；目前已完成 Alphabet 的 Codex 试点。
- 企业、用户身份及可操作范围由登录授权和服务端权限决定，安装包不包含任何人的账号或令牌。
- 下载插件不会自动获得 Alphabet 或其他企业的数据权限。没有灼见账号/权限时，请联系所在企业管理员开通。
- 涉及写入、上传等操作，按第一方页面的确认流程完成；Codex 的工具许可不能代替业务确认。
- 本插件提供企业工具和业务说明；模型与本机代码执行能力由所使用的客户端提供。

## 包的区别

| 文件 | 用途 |
| --- | --- |
| `zhuojian-enterprise-marketplace-0.1.2-pilot.zip` | Codex 完整市场包，供手动分发和导入 |
| `zhuojian-enterprise-0.1.2-pilot.zip` | 单独插件目录，供支持该格式的导入流程使用 |
| `workbuddy-zhuojian-enterprise-0.1.2-pilot.zip` | WorkBuddy 连接器试点包，真实客户端导入和 OAuth 尚待验收 |

WorkBuddy 的说明见 [连接器 README](./workbuddy-zhuojian-enterprise/README.md)。本次未提交任何公共插件商店，也未完成 Claude Code 客户端适配验收。

## 验证与维护

`0.1.2` 增加随包首次接入 Skill、只读连接检查和国内更新接入脚本，Codex 清单声明标准安装引导入口，WorkBuddy 共享业务 Skill 和诊断资源。分发文件从规范源最终构建逐字导入，17 个文件及三个 ZIP 的哈希和归档内容校验通过。

最终真实插件包已通过本机 Nginx `1.28.0` 的六项静态分发检查及真实 Git clone；原生更新机制通过隔离 fixture 的四项验收。这些结果验证本机构建和更新机制，不代表国内 HTTPS 已上线、员工自动更新已启用，或所有企业业务已经验收。详见[候选交接](docs/handoff/2026-10-26_onboarding-candidate.md)。

本机已原生安装最终 `0.1.2` 包并逐文件核对一致，Codex 只读业务联通通过；安装来源仍为本地最终构建，国内自动更新来源未启用。写入、上传及其他宿主的验收范围分别保留。

历史 `0.1.1` 的 OAuth 和读取工具验收只证明当时版本，不能代替 `0.1.2` 验证。具体测试与未测项以本次交接为准；真实业务写入、上传、企业管理员及 WorkBuddy 完整流程仍须独立验收。

校验文件见 [`release/SHA256SUMS`](./release/SHA256SUMS) 和 [`release/build-receipt.json`](./release/build-receipt.json)。回执中的 `not-deployed` / `not-installed` / `not-tested` 表示构建脚本本身不执行这些动作，不能据此判断当前线上服务状态。

维护者可运行 `python scripts/verify_distribution.py` 验证分发文件；加 `--archives <下载目录>` 可同时检查 ZIP 哈希与内容。更新时发布新版本，避免覆盖历史安装包。
