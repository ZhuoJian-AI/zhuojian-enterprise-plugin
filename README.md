# 灼见企业插件

在 Codex 中连接你已获授权的企业业务：查询业务数据、发现可用应用、处理资料，并把结果交付到企业工作空间。

**这是可直接安装的插件分发仓库。当前版本：0.1.1。**

[下载安装包](https://github.com/ZhuoJian-AI/zhuojian-enterprise-plugin/releases/latest) · [版本说明](./release/RELEASE_NOTES.md)

## 在 Codex 中安装

需要支持插件的 Codex 版本，以及已有权限的灼见企业账号。先在终端执行：

```sh
codex plugin marketplace add ZhuoJian-AI/zhuojian-enterprise-plugin
codex plugin add zhuojian-enterprise@zhuojian-enterprise-pilot
```

安装后，在 Codex 的插件/应用管理中连接“灼见企业”，按页面引导用**自己的账号**登录并授权。然后打开新对话，选择“灼见企业”，问：

> 请检查我当前登录的是哪家企业、哪个账号，以及有哪些可用的业务能力。

`zhuojian-enterprise-pilot` 是现有插件市场的技术名称，因此界面可能显示“灼见企业试点”。已经安装并启用 0.1.1 的用户无需重复安装；本仓库提供的 0.1.1 包与已交付版本一致。

如果终端提示没有 `codex` 或 `plugin` 命令，请先安装/更新支持插件的 Codex，或把本仓库链接交给你的 Codex，请它依照本页安装。不同版本的图形界面入口可能不同。

### 手动下载安装

1. 从 [Releases](https://github.com/ZhuoJian-AI/zhuojian-enterprise-plugin/releases/latest) 下载 **`zhuojian-enterprise-marketplace-0.1.1-pilot.zip`**。
2. 完整解压，保留 `.agents` 隐藏目录。
3. 将下面的路径换成解压后包含 `.agents/plugins/marketplace.json` 的目录，再执行安装命令：

```sh
codex plugin marketplace add "/path/to/extracted-marketplace"
codex plugin add zhuojian-enterprise@zhuojian-enterprise-pilot
```

不要把 ZIP 文件或其中单独的 `zhuojian-enterprise` 子目录作为 marketplace 根目录。

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
| `zhuojian-enterprise-marketplace-0.1.1-pilot.zip` | 推荐：Codex 完整市场包，可按上述步骤安装 |
| `zhuojian-enterprise-0.1.1-pilot.zip` | 单独插件目录，供支持该格式的导入流程使用 |
| `workbuddy-zhuojian-enterprise-0.1.1-pilot.zip` | WorkBuddy 连接器试点包，真实客户端导入和 OAuth 尚待验收 |

WorkBuddy 的说明见 [连接器 README](./workbuddy-zhuojian-enterprise/README.md)。本次未提交任何公共插件商店，也未完成 Claude Code 客户端适配验收。

## 验证与维护

2026-10-16 发布时，Codex 包的五个文件与现有已安装 0.1.1 完全一致，11 个交付文件和三个 ZIP 均通过 SHA256 核对。2026-10-12 的 Codex 试点已完成真实 OAuth 和三项读取工具验收；本次分发没有重新执行业务操作，写入、上传、企业管理员及 WorkBuddy 完整流程仍以各自验收结果为准。

校验文件见 [`release/SHA256SUMS`](./release/SHA256SUMS) 和 [`release/build-receipt.json`](./release/build-receipt.json)。回执中的 `not-deployed` / `not-installed` / `not-tested` 表示构建脚本本身不执行这些动作，不能据此判断当前线上服务状态。

维护者可运行 `python scripts/verify_distribution.py` 验证分发文件；加 `--archives <下载目录>` 可同时检查 ZIP 哈希与内容。更新时发布新版本，避免覆盖历史安装包。
