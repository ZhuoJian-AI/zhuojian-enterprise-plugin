# 企业管理员 AI 管理客户端候选（未发行）

本轮仅修改公共客户端候选；SaaS 后台实现与真实管理能力由 ai-platform 对应候选提供。当前不代表服务器已部署，也不代表任何本人账号或宿主已获管理授权。

## 规范源与产物

- 规范源：`ZhuoJian-AI/ai-platform` 的 `plugins/`；精确源提交 `07daa51eb0570e37e6baad1999909da58a3a38ac`。该提交同时同步了18份后台嵌入模板，配对guide与按企业导出包也使用0.1.6及新助手。
- 公共分支：`codex/enterprise-admin-ai-20261102`，从 `origin/main` 的 `b68d0aa05f539df25100eaed11e277229b9a7ea0` 建立；原候选与已发行版本分别保留。
- 本轮使用0.1.6候选：首次查询公共最新稳定版为0.1.4，但同轮SaaS main已推进并登记0.1.5独立分发镜像，因此为避免与另一发布流程复用版本而升为0.1.6。未修改0.1.4/0.1.5的Release、部署登记或不可变附件。

## 改动

Codex配对助手请求 `business:read,files:read,files:write,admin:read,admin:manage:read,admin:manage:write` 作为客户端申请上限。第一方页面默认只读，实际授予范围由本人选择及服务端身份决定，助手不调用批准接口、不携带管理员Cookie或密码；旧连接和刷新令牌不能扩大为新管理授权。

业务与设置Skill按真实工具目录分流：员工用现有业务工具；企业管理员只有在当前服务端实际暴露管理工具时，使用 `discover_admin_capabilities`、`query_admin` 与 `execute_admin`。服务器注册与代码上传保留人工处理。私密输入仅在本人第一方页面办理；普通文件仍受 `files:read` / `files:write` 与本人所选工作空间限制。

规范源只编辑Codex主文件，使用现役 `plugins/build_packages.py sync-shared` 同步WorkBuddy。Claude Code继续使用其原生PTY流程，Claude Desktop与WorkBuddy沿各自原生连接器，不套用其他宿主命令。

## 验证

规范源 `check-source` valid（0.1.6）；升版本前完整插件测试104项，103通过、1项因当前Windows账户不能创建符号链接而跳过。8项配对测试均通过，其中新增测试验证仅扩展scope请求上限，没有代批或凭据参数。显式LF后共享副本一致。

0.1.6版本调整后的包装测试28项全部通过；后台嵌入导出包3项离线/模拟路由测试通过。随后在精确源提交07daa51的干净plugins源码上执行现役构建器build与verify，生成19个显式分发文件、3个ZIP及SHA256回执，均通过。公共仓库只按构建回执白名单导入客户端文件；`python scripts/verify_distribution.py --archives <本轮构建目录>`通过，19文件、version0.1.6、archives verified。

`release/build-receipt.json`是该次构建器原始回执，`release/SHA256SUMS`列出同次三个ZIP哈希。未手改包内哈希、未把源码模板的.invalid地址当实际构建入口，未把私有后端源码加入公开仓库。

## 未执行

未推送分支、发布Release、修改国内active指针、安装或更新个人插件、创建真实管理员授权、执行真实企业管理或变更服务器。SaaS正式CI与发布、本人新授权、Codex/WorkBuddy/Claude各宿主真实管理员管理流程均另行验收。客户端源码和离线包检查不替代这些结果。
