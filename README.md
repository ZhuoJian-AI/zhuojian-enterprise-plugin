# 灼见企业插件

在 Codex 中连接你已获授权的企业业务：查询业务数据、发现可用应用、处理资料，并把结果交付到企业工作空间。

**这是可直接安装的插件分发仓库。当前候选版本：0.1.2。** 发布状态以 [Releases](https://github.com/ZhuoJian-AI/zhuojian-enterprise-plugin/releases) 为准。

[下载安装包](https://github.com/ZhuoJian-AI/zhuojian-enterprise-plugin/releases/latest) · [版本说明](./release/RELEASE_NOTES.md)

## 在 Codex 中安装

需要支持插件的 Codex 版本，以及已有权限的灼见企业账号。推荐使用本仓库的 Git marketplace 来源，以便由宿主原生机制刷新市场和更新插件。可以让 Codex 完成下面的安装步骤：

```sh
codex plugin marketplace add ZhuoJian-AI/zhuojian-enterprise-plugin
codex plugin add zhuojian-enterprise@zhuojian-enterprise-pilot
```

安装后运行插件的设置引导，或选择“灼见企业”并说：

> 检查灼见企业连接并引导我登录。

引导先检查当前工具和连接：网络正常且需要授权时，使用宿主原生流程，由你在灼见第一方页面用**自己的账号**核对企业、身份和授权范围。网络认证、证书或服务异常会给出对应状态与下一步，不把“已安装”当作“已连接”，也不把换热点作为正式使用条件。

授权后由真实身份和能力查询验证可用范围；工具尚未加载时，按宿主实际支持的方式刷新连接，必要时在新聊天继续。浏览器里已经登录灼见，不等于插件已经完成授权。

`zhuojian-enterprise-pilot` 是现有插件市场的技术名称，因此界面可能显示“灼见企业试点”。

如果终端提示没有 `codex` 或 `plugin` 命令，请先安装/更新支持插件的 Codex，或把本仓库链接交给你的 Codex，请它依照本页安装。不同版本的图形界面入口可能不同。

### 更新与旧版本迁移

通过官方 Git marketplace 安装后，市场刷新和已安装缓存更新交给 Codex 原生机制；实际是否完成更新，以本机显示的已安装版本为准。更新插件文件不代表当前聊天已加载新工具或新 Skill，必要时新开聊天。插件不安装自升级常驻进程，不修改整机代理或证书。

旧 `0.1.1` 如果来自本地解压目录，需要先做一次来源切换，改为本仓库的 Git marketplace，并完成本次升级。可以把本仓库链接交给 Codex，让它核对当前来源后使用宿主支持的市场管理流程处理。不要把本地 ZIP 安装与原生 Git 来源的联网更新混为一谈。

本次保留 MCP 服务名称和连接地址，不要求为了升级主动退出登录或删除原有授权；升级后仍须核验当前企业身份和有效权限，过期或撤销的授权按实际状态处理。插件更新不增加业务权限。

### 手动下载安装

1. 从 [Releases](https://github.com/ZhuoJian-AI/zhuojian-enterprise-plugin/releases/latest) 下载对应版本的 **`zhuojian-enterprise-marketplace-0.1.2-pilot.zip`**；尚未发布时不要把旧版本下载结果当成新版本。
2. 完整解压，保留 `.agents` 隐藏目录。
3. 将下面的路径换成解压后包含 `.agents/plugins/marketplace.json` 的目录，再执行安装命令：

```sh
codex plugin marketplace add "/path/to/extracted-marketplace"
codex plugin add zhuojian-enterprise@zhuojian-enterprise-pilot
```

不要把 ZIP 文件或其中单独的 `zhuojian-enterprise` 子目录作为 marketplace 根目录。

本地 ZIP 适用于手动分发和离线导入。添加解压后的本地路径，不会让该路径自动从 GitHub 下载新版本；需要持续原生更新时使用上面的 Git 来源。

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

`0.1.2` 增加随包首次接入 Skill 和只读连接检查脚本，Codex 清单声明标准安装引导入口，WorkBuddy 共享业务 Skill 和诊断资源。验收须覆盖配置、网络/OAuth 发现、授权状态分类、宿主工具恢复、构建与包内资源完整性；构建成功不代表真实员工登录或业务调用通过。

历史 `0.1.1` 的 OAuth 和读取工具验收只证明当时版本，不能代替 `0.1.2` 验证。具体测试与未测项以本次交接为准；真实业务写入、上传、企业管理员及 WorkBuddy 完整流程仍须独立验收。

校验文件见 [`release/SHA256SUMS`](./release/SHA256SUMS) 和 [`release/build-receipt.json`](./release/build-receipt.json)。回执中的 `not-deployed` / `not-installed` / `not-tested` 表示构建脚本本身不执行这些动作，不能据此判断当前线上服务状态。

维护者可运行 `python scripts/verify_distribution.py` 验证分发文件；加 `--archives <下载目录>` 可同时检查 ZIP 哈希与内容。更新时发布新版本，避免覆盖历史安装包。
