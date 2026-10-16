# 灼见企业插件分发仓库

先读 `README.md`、`TASKS.md` 和最新 `docs/handoff/`。

此仓库发布可安装的客户端插件与 marketplace，不承载 SaaS 后端、不部署服务器。
当前插件规范源由灼见 SaaS 项目维护；更新应取经过验证的构建产物，不直接修改已发布版本。
每次发版核对清单、文件哈希、ZIP 内容及版本，并保留真实客户端验收范围。
本地验证：`python scripts/verify_distribution.py`（Python 3，标准库，无需安装依赖）。
禁止加入个人配置、账号、令牌、企业业务数据或私有后端源码。
插件下载不授予业务权限；企业身份与权限由服务端本人授权决定。
一个 agent 一个工作目录；改动前在 `TASKS.md` 认领任务，完成后删除任务块并记录交接。
里程碑合并后更新 `zhuojian-llm-wiki` 的 `cards/zhuojian-enterprise-plugin.md`。

