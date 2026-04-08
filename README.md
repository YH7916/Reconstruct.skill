# 屎山重构.skill

<p align="center">
  <img src="docs/assets/social-preview-zh.png" alt="屎山重构.skill showcase" width="100%" />
</p>

<p align="center">
  <a href="https://github.com/YH7916/Reconstruct.skill/stargazers"><img src="https://img.shields.io/github/stars/YH7916/Reconstruct.skill?style=for-the-badge&label=GitHub%20Stars" alt="GitHub Stars" /></a>
  <a href="https://github.com/YH7916/Reconstruct.skill/blob/main/LICENSE"><img src="https://img.shields.io/github/license/YH7916/Reconstruct.skill?style=for-the-badge&label=MIT%20License" alt="MIT License" /></a>
  <a href="https://github.com/YH7916/Reconstruct.skill/commits/main"><img src="https://img.shields.io/github/last-commit/YH7916/Reconstruct.skill?style=for-the-badge&label=Last%20Update" alt="Last Update" /></a>
</p>

<p align="center">
  面向危险遗留代码的路线优先重构 AI skill 套件。
</p>

<p align="center">
  <a href="README.en.md">English README</a>
</p>

## 它解决什么问题

`屎山重构.skill` 是一套双层 skill：

| Skill | 作用 |
|------|------|
| `refactoring-legacy-code` | 执行层。负责评估爆炸半径、冻结行为、划定安全边界，并按波次重构。 |
| `gsd-legacy-refactor` | 编排层。负责扫描目标、生成 `.planning/refactors/<slug>/` 工件、给用户确认路线，然后按 git checkpoint 执行。 |

这套 skill 专门处理最容易把 AI 重构搞崩的场景：

- 依赖图过密
- 隐式副作用太多
- 共享可变状态
- 改一处崩三处的核心模块

默认工作方式不是“先改再说”，而是：

1. 先把当前结构摸清
2. 先锁定行为
3. 先评估 blast radius
4. 先把路线给用户确认
5. 确认后再执行
6. 每个验证通过的波次都用 git checkpoint 固化

## 适用平台

| 平台 | 使用方式 |
|------|----------|
| Codex | 放到 `$CODEX_HOME/skills` 或 `~/.codex/skills`，用 skill 名或自然语言调用 |
| Claude Code | 放到 `~/.claude/skills`，让 agent 读取并按 `SKILL.md` 执行 |
| Agent Skills 兼容客户端 | 放到项目内 `.agents/skills/` 或客户端约定目录 |
| 其他 agent / runner | 直接加载对应 `SKILL.md`，并保留同目录下的 `references/`、`templates/`、`workflows/` |

只要宿主支持 `SKILL.md` 风格技能，或者至少支持“把一整个技能目录作为工作说明加载进来”，这套 skill 就能工作。它不是只给 Codex 写的，只是仓库里默认同时照顾了 Codex 的调用习惯。

## 快速开始

### 安装

#### 方式一：用安装脚本

```text
python scripts/install_skills.py --platform codex --force
```

```text
python scripts/install_skills.py --platform claude --force
```

```text
python scripts/install_skills.py --platform agents --force
```

如果你要装到自定义位置：

```text
python scripts/install_skills.py --platform custom --dest /path/to/skills --force
```

常用参数：

- `--dest <path>` 指定安装路径
- `--mode link` 用软链接代替复制
- `--dry-run` 只预览不写入

#### 方式二：手动复制

把这两个目录复制到你的 skill 目录里：

```text
skills/refactoring-legacy-code
skills/gsd-legacy-refactor
```

常见目标位置：

```text
Codex:        $CODEX_HOME/skills 或 ~/.codex/skills
Claude Code:  ~/.claude/skills
Repo local:   ./.agents/skills
```

### 怎么调用

#### 命令式宿主

```text
$gsd-legacy-refactor src/auth --goal "split auth orchestration from token storage"
```

```text
$refactoring-legacy-code src/reporting/legacy_parser.py
```

#### 自然语言宿主

```text
Use gsd-legacy-refactor on src/auth.
Plan first, write the .planning artifacts, show me the route, and wait for approval before editing code.
```

```text
Use refactoring-legacy-code on src/reporting/legacy_parser.py.
If the blast radius is high, switch to untangle-first and stop after presenting the safe route.
```

#### 不支持技能自动发现的 agent

把对应目录下的 `SKILL.md` 直接提供给 agent，同时保留相邻资源目录：

```text
skills/refactoring-legacy-code/SKILL.md
skills/gsd-legacy-refactor/SKILL.md
```

如果你的 agent 支持按需读取相对路径资源，保留原目录结构即可；如果不支持，至少要把 `references/`、`templates/`、`workflows/` 一并提供。

## 它怎么工作

整个 suite 只允许两种模式：

| 模式 | 适用场景 |
|------|----------|
| `untangle-first` | 风险高、行为不清晰、耦合重、测试弱 |
| `refactor-wave` | 边界小、调用方已知、验证手段可靠 |

默认偏好永远是：

- 一次只动一个热点
- 外部行为尽量稳定
- 先加兼容层再动内部结构
- 先要可验证进展，不要英雄式大改

## 一次典型运行会发生什么

1. 扫描目标区域、入口、依赖和副作用
2. 写出 `.planning/refactors/<slug>/`
3. 评估风险并选择 `untangle-first` 或 `refactor-wave`
4. 把路线展示给用户确认
5. 只执行明确批准的波次
6. 每个完成波次都做验证和 git checkpoint

## 产物

`$gsd-legacy-refactor` 会写出：

```text
.planning/refactors/<slug>/
  01-CONTEXT.md
  02-RISK-MAP.md
  03-SAFETY-NET.md
  04-WAVE-PLAN.md
  05-VERIFY.md
  06-HANDOFF.md
  07-EXECUTION-LOG.md
```

执行 skill 在正式动结构前，必须先产出：

```text
Risk Level: high
Mode: untangle-first
Current State Map: callers, dependencies, side effects
Safety Net: existing tests + missing characterization coverage
Safe Boundary: adapter seam around token store
Verification Gate: targeted tests + smoke checks + rollback point
```

## 相关文档

- [Demo 用例](docs/demo-cases.md)
- [GitHub 发布素材](docs/github-launch.md)
- [英文 README](README.en.md)
- [许可证](LICENSE)

## 它不是什么

- 不是一键重写单体系统的按钮
- 不是泛泛的代码整理提示词
- 不是给小型独立 bugfix 用的
- 不是“AI 可以跳过测试和验证”的借口

## 仓库内容

```text
skills/
  refactoring-legacy-code/
  gsd-legacy-refactor/
scripts/
  install_skills.py
docs/
  assets/social-preview-zh.png
  demo-cases.md
  github-launch.md
```

## 路线图

- 增加 TypeScript 和 Python 的真实 demo
- 增加 forward-test prompts 和期望产物
- 增加更方便的 release packaging
- 增加和 naive refactor prompt 的对比 benchmark

## 贡献

欢迎 issue 和 PR，尤其是：

- 真实屎山案例
- 更稳的 wave planning 规则
- 更好的触发描述
- 更顺手的安装和打包流程
- 公共 demo 仓库

## License

MIT. See [LICENSE](LICENSE).
