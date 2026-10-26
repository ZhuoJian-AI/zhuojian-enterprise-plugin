# 0.1.4 图片能力发行记录

当前状态：**发行候选，本地构建、原始源码字节核对及分发完整性通过；后端激活、真实模型生图、公开 Release 与国内正式指针尚待主任务确认。** 此记录不以包版本号替代运行时验收。

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

本仓运行 `python scripts/verify_distribution.py --archives <validated-build>`，已通过 17 文件白名单、全部哈希、marketplace、三 ZIP 成员及内容检查。规范源本地现有96项离线包测试通过；正式主分支 CI 与运行时验收结果另行记录，不由本地回执推定。

## 国内候选与历史保留

国内候选 Git 为 `aa610462252d2f7a573964fe1adf26ae5aa96070`，58 个公共文件，发行清单 SHA256 为 `7c0bef63c6437052bf5dcde0e321a8e60ff7d57f13bcd55dc2dcf36369537aa9`。按上一发行目录构建，旧38个不可变对象和版本下载保持原字节；不覆盖已公开的 `0.1.2/0.1.3`。

员工仍使用国内同域来源，不依赖 GitHub。静态入口登记范围不扩大，不通过业务发布身份更新它。不可变文件、引用、`latest.json` 的顺序及实际 HTTPS 验证由主任务确认后记录。

历史公开 `v0.1.3` 标签为 `f1df7aa8dc4a2d21cfc0c52953cd5646d4b72c35`，`v0.1.1` 为 `209edabdf07f4efa6424215a7374fd58ae005504`；已有 Release 与附件不覆盖。此前首次接入与自动更新验收见[历史记录](2026-10-26_onboarding-candidate.md)。

## 发布门槛与未验收范围

公开 main/Release 与国内正式指针必须等主分支 CI、SaaS 后端激活和相应验收确认，不抢先引导员工使用未激活接口。真实生图、原生预览和正式文件回执以本轮真实回执记录为准。

WorkBuddy 实机、管理员宿主、手机真机、原业务写入和外部上传不因本版图片桥接自动变为已验收。不存在视频生成工具时不宣称支持视频；本版不增加本机执行或长期记忆。
