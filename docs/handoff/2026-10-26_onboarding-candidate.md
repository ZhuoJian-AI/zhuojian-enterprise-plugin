# 0.1.2 首次接入候选交接

当前状态：**已修改、已构建并完成分层验收，候选已推送并创建 [Draft PR #1](https://github.com/ZhuoJian-AI/zhuojian-enterprise-plugin/pull/1)；未合并或公开发行，国内员工入口未部署。**

## 责任和范围

- 规范源由 `ai-platform` 维护，本仓只接收最终验证过的客户端制品。
- 插件/Skill 负责首次接入、连接检查、本人登录引导、网络错误提示及国内更新接入；MCP 服务名和地址保持，企业授权和业务确认规则保持。
- 本次没有部署 SaaS、修改企业业务子系统或增加员工权限。WorkBuddy 共享资源更新不代表其真实客户端已验收。

## 导入和完整性

从最终 `0.1.2` 构建逐字导入 17 个白名单文件，含 Codex/WorkBuddy 包和 marketplace 索引；同步 `release/build-receipt.json` 与 `release/SHA256SUMS`。三个 ZIP 保留为待发行附件，没有放入 Git。

本仓独立执行 `python scripts/verify_distribution.py --archives <final-build>`，结果为 `PASS: 17 distribution files; version 0.1.2; archives=verified`；`git diff --check` 通过。MCP 配置仍仅包含服务公开地址和原生传输字段，没有个人配置、账号、令牌或企业业务数据。

| 最终附件 | SHA256 |
| --- | --- |
| `zhuojian-enterprise-0.1.2-pilot.zip` | `3dd633a43eb7fca9a4a31b46c0c053f919c6f83e1496a5c057d410e367337e54` |
| `zhuojian-enterprise-marketplace-0.1.2-pilot.zip` | `f6fd5e3f5532f56cbae1c2226c155ff29ec16fea18275fd8952bdd4c6be93580` |
| `workbuddy-zhuojian-enterprise-0.1.2-pilot.zip` | `fcc537a717ea6a46269a83f50541aa91ef6a9bba3823b7e60a6eebfca559aa41` |

构建回执 SHA256 为 `63b387b4528a23637c20eebcf6c40382d0f4313bb2ed0bfc787a496253cee815`。回执中的 `not-deployed`、`not-installed`、`not-tested` 只说明构建器不执行这些动作，不能取代本次分层验收记录。

## 已完成的分层验收

- 本机通过原生流程安装最终 `0.1.2` 包，已安装文件与最终构建逐字匹配，其他宿主配置保持。Codex 只读业务联通通过；不在公开记录中加入企业账号、凭据或业务响应内容。
- 最终真实包通过本机 Nginx `1.28.0` 六项检查：健康响应、发布指针原字节、Git 发现、缺失及私有路径 404、写入及无关路径拒绝、真实插件包 Git clone。
- Linux CI 容器已实际验证固定 Nginx `1.28`：根文件系统只读、临时可写位置使用 tmpfs，仅精确只读挂载公共发行目录。Docker 健康、HTTP HEAD、29 个公共文件的 HTTP 字节 SHA256、缺失/私有路径 404、POST 403 均通过；真实 Git clone 得到分发提交 `f433f7c3fe0bb1a3dd23222d734e1539437da8a8`，插件版本为 `0.1.2`。这是容器内静态发行验收，不是生产 HTTPS 上线。
- Codex `0.164.0-alpha.11.1` 的原生更新使用隔离 `CODEX_HOME` 和本机 HTTP fixture 验收：首次安装、原生 marketplace 升级、宿主启动自动升级已安装缓存、离线失败保留原安装，共四项通过。
- 原生启动检查是已验收行为，不是固定计时器，也不保证当前聊天热加载。fixture 不包含企业 MCP 或业务访问，不能当成真实员工端到端业务验收。
- 国内静态发行候选含 29 个公共文件。独立分发快照 Git 提交为 `f433f7c3fe0bb1a3dd23222d734e1539437da8a8`；该提交不等于 SaaS 源码或运行版本。
- 静态发行清单按不可变对象/版本附件、refs、latest 的顺序切换，保留旧对象和下载；public 不包含 Git config、hooks、logs 或私有 SaaS 历史。

## 当前未交付项

国内第一方 HTTPS 入口尚未部署，不能向员工宣称可下载或自动更新已启用。下一步须验证真实国内入口在员工无需 GitHub/VPN 的环境下完成安装和更新，并核验第一方 HTTPS、发布指针和实际安装版本。

最终本机安装仍来自本地构建，`automaticUpdateSourceLive=false`；四项原生更新机制演练不改变这个现网状态。

本候选未创建公开 `0.1.2` Release，也未更新公开商店。GitHub 只保留为维护者托管与附件核验通道。旧本地或境外来源需要在国内入口就绪后做一次来源迁移，保留现有授权与已安装版本。

真实业务写入、上传、企业管理员宿主、WorkBuddy 和手机真机仍须独立验收；历史 `0.1.1` 的 OAuth/读取证据不替代新版本或这些场景的测试。
