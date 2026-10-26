# 0.1.4 图片能力发行记录

当前状态：**国内 `0.1.4` 与公开五附件已正式发行；HTTPS、匿名下载、原生升级、OAuth 保留及当前聊天真实灼见生图通过。** 此记录不以包版本号替代运行时验收。

## 责任与范围

SaaS 提供模型网关、生图执行、持久任务、实时身份和工作空间文件交付。插件说明负责发现、调用、任务恢复与原生预览。本仓只接收客户端白名单制品，不包含后端私有源码、凭据、原始业务资料或运行日志。现有业务子系统无需修改；生产激活由主任务沿既有受保护入口串行完成。

本版以 `get_media_capabilities`、`generate_image`、`get_media_job` 接通图片服务。默认只读授权不会自动获得生成权限；本人一次授予 `files:write` 后，按明确生图意图创建新文件。原有业务写入与外部文件上传的第一方确认保持。任务结果未知不更换请求编号重新生成，不把排队或受理视为图片已交付。

## 构建与完整性

规范源为已合并提交 `8bbc6ec834c3f80abe859d1887a4430bc5fe4be6`。30 个插件源文件均与该提交的原始 Git blob 核对；以命令级 `core.autocrlf=false` / `core.eol=lf` 导出，不改用户全局设置。插件文件本来就符合原始字节，新导出未改变候选文件；不将其他后端文件的换行发现泛化成插件制品损坏。

17 个客户端白名单文件逐字导入，包含 Codex/WorkBuddy 包和 marketplace 索引。`release/build-receipt.json` 及 `release/SHA256SUMS` 同步正式候选字节；三个 ZIP 只作为 Release 附件，不加入 Git。构建回执 SHA256 为 `1de9d3d4d980b99341707b1867f3a4a58c2c4bbfaad9f38e31fbff4e58d094ee`。

| 附件 | SHA256 |
|---|---|
| `zhuojian-enterprise-marketplace-0.1.4-pilot.zip` | `19b15cc1beffe9277c3760b467c31a8df771da0b3a7e83fe37680a364e0f52c7` |
| `zhuojian-enterprise-0.1.4-pilot.zip` | `6c452ec97f88a70626fb09714a3831714db9d364d8963a46410da4599e5b93b3` |
| `workbuddy-zhuojian-enterprise-0.1.4-pilot.zip` | `9f579c9a0c66f0b7d101de1fbc9513ceebcbe81f4c030a4e63108d556ab0c18b` |
| `build-receipt.json` | `1de9d3d4d980b99341707b1867f3a4a58c2c4bbfaad9f38e31fbff4e58d094ee` |
| `SHA256SUMS` | `250fa847e4c40745c22d856979be22540230092f0bee87a590e83d128749bbe4` |

本仓运行 `python scripts/verify_distribution.py --archives <validated-build>`，已通过 17 文件白名单、全部哈希、marketplace、三 ZIP 成员及内容检查。规范源本地现有96项离线包测试通过；源码主分支 `8bbc6ec` 的 CI `40279157933` attempt 2 成功，原 attempt 1 旧移动视口检查失败记录保留。

## 国内发行与历史保留

国内正式 Git 为 `aa610462252d2f7a573964fe1adf26ae5aa96070`，58 个公共文件，发行清单 SHA256 为 `7c0bef63c6437052bf5dcde0e321a8e60ff7d57f13bcd55dc2dcf36369537aa9`。按上一发行目录构建，旧38个不可变对象和版本下载保持原字节；不覆盖已公开的 `0.1.2/0.1.3`。

员工使用国内同域来源，不依赖 GitHub。静态入口由已登记的固定 publisher 激活，范围不扩大；58 个文件状态/MIME/SHA、latest/HEAD、私有或缺失文件404及 POST403 均通过。严格 TLS Git 克隆核对固定提交和9个原始文件，38项历史不可变对象保留。

历史公开 `v0.1.3` 标签为 `f1df7aa8dc4a2d21cfc0c52953cd5646d4b72c35`，`v0.1.1` 为 `209edabdf07f4efa6424215a7374fd58ae005504`；已有 Release 与附件不覆盖。此前首次接入与自动更新验收见[历史记录](2026-10-26_onboarding-candidate.md)。

## 公开发行验收

[PR #3](https://github.com/ZhuoJian-AI/zhuojian-enterprise-plugin/pull/3) 正常合入 `1027830a4f2a303f197752c1ed22c3447347457a`，`v0.1.4` 标签精确指向该提交。[正式 Release](https://github.com/ZhuoJian-AI/zhuojian-enterprise-plugin/releases/tag/v0.1.4) ID 为 `424030168`，发布时间 `2026-10-26T09:03:52Z`，已设为最新稳定版本；没有覆盖或重建冻结资产。

公开匿名 HTTPS 验收通过：五附件的名称、大小、SHA256 与 GitHub asset digest 均等于本页冻结表；三个下载 ZIP 成员白名单、唯一性和全部内容逐字核对通过。历史 `v0.1.3/v0.1.1` 标签，以及原有 Release ID、发布时间、正文和附件身份/大小/digest/类型/创建时间与发布前快照相同。本仓无配置的 GitHub 检查，不将这些本地验收伪装成 Actions CI。

## 真实运行时与客户端验收

后端图片服务来源仍为 `8bbc6ec`，镜像 `sha256:a6d31756f0b3f4e781df07ff558585b1853647489a352c4388875eb57ad75de1`。首次真实任务在模型调度前因 worker 未同步 MCP 企业配置被拒绝，失败证据保留；未把未知结果换编号重放。主任务经 PR682 增加固定 root-only 配置类型，合入 `7d2a03cf928917087babfb26b521203817c5f15e`，精确 main Maintenance CI `40294018293` 成功，经受保护入口仅刷新 worker；72 个其它容器及五个语义 floor 保持，镜像未变，维护恢复 normal。

修复后在当前聊天通过正式 MCP 完成一次获权图片任务，直接展示原生预览并交付正式文件回执。只读一致性证据确认一条成功任务、一条图片计量审计，企业目录模型 `gpt-image-2`；正式文件元数据为 PNG、`1536×1024`、`2,275,590` 字节，内容哈希 `a0fbfa3b0d16343b8309051a5420f6c52508a4c402c025505d5c057c64c60c4d`。此为正式任务/文件/版本/审计元数据与当前网关绑定证据，不冒充历史网络目的地主机日志或实测请求次数。没有下载原图，不宣称客户端原图字节复算；`storageVersionPinned=false`，不宣称固定 OSS 对象版本。

原生宿主通过正常更新流程升到 `0.1.4`，OAuth 保留、无关配置及 Git 换行设置保持。宿主安装采用正常投影一致验收，不宣称缓存与 Git 原始字节相同。包内候选状态文案保留冻结时事实；当前状态以此交接和正式 Release 为准。

## 未验收范围

WorkBuddy 实机、管理员宿主、手机真机、原业务写入和外部上传不因本版图片桥接自动变为已验收。不存在视频生成工具时不宣称支持视频；本版不增加本机执行或长期记忆。
