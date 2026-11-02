# 任务

`0.1.4` 生图发行与验收见[交接记录](docs/handoff/2026-10-26_image-generation-0.1.4.md)。

## ENTERPRISE-ADMIN-AI-20261102（@Codex-admin-ai）

已认领最终客户端候选交接收尾。0.1.6 的19文件、三ZIP及来源回执已从本机 COA-CI 最终规范源 `06576e157707f282022e7f5df9f19640e55d9c6f` 验证导入；构建、包校验、分发镜像89个公共文件的本地 HTTP 检查及 Git 克隆均通过。Codex→WorkBuddy 共享副本和包装/导出测试的实际提交与复用范围见[交接](docs/handoff/2026-11-02_enterprise-admin-ai-client.md)。

- [ ] 本机 COA-CI 对最终公共候选执行 `scripts/verify_distribution.py --archives <同次构建目录>` 并保留回执。
- [ ] 提交最终候选并合并公共 PR #6，登记最终提交及校验回执。
- [ ] 按既有入口发行0.1.6及国内分发；核验正式 HTTPS、Git 更新源和不可变附件，保留0.1.4/0.1.5。
- [ ] SaaS 对应版本部署后，以本人新管理授权分别验收 Codex、WorkBuddy、Claude 的真实管理员流程；各宿主结果独立记录。


## AI-PAIRING-FOUR-STEPS-20261102（@Codex-pairing）

0.1.5候选19文件/三ZIP校验通过，规范源102检查（102通过、1跳过）。SaaS正式CI/上线、国内发行、本人授权和真实MCP业务读取仍待完成；WorkBuddy与Claude Desktop独立未验，不合并为正式发行。见[候选交接](docs/handoff/2026-11-02_four-step-pairing-candidate.md)。
