# 屎山重构.skill

<p align="center">
  <img src="docs/assets/social-preview-zh.png" alt="屎山重构.skill showcase" width="100%" />
</p>

<p align="center">
  <a href="https://github.com/YH7916/Reconstruct.skill/stargazers"><img src="https://img.shields.io/github/stars/YH7916/Reconstruct.skill?style=flat-square" alt="GitHub stars" /></a>
  <a href="https://github.com/YH7916/Reconstruct.skill/blob/main/LICENSE"><img src="https://img.shields.io/github/license/YH7916/Reconstruct.skill?style=flat-square" alt="License" /></a>
  <a href="https://github.com/YH7916/Reconstruct.skill/commits/main"><img src="https://img.shields.io/github/last-commit/YH7916/Reconstruct.skill?style=flat-square" alt="Last commit" /></a>
</p>

<p align="center">
  Route-first AI skills for refactoring dangerous legacy code without blowing up tightly coupled systems.
</p>

<p align="center">
  <a href="#english">English</a> | <a href="#中文">中文</a>
</p>

## English

### What It Is

`屎山重构.skill` is a two-layer skill suite for risky legacy refactors:

| Skill | Role |
|------|------|
| `refactoring-legacy-code` | The execution skill. It maps blast radius, locks behavior, picks a safe boundary, and refactors in bounded waves. |
| `gsd-legacy-refactor` | The orchestration skill. It inspects the target, writes `.planning/refactors/<slug>/` artifacts, asks for route approval, then executes with git checkpoints. |

This README structure takes cues from high-star skill/tool repos such as [anthropics/skills](https://github.com/anthropics/skills) and [daymade/claude-code-skills](https://github.com/daymade/claude-code-skills): lead with value, show install fast, make the workflow concrete, then provide deeper docs.

### Why It Exists

Most AI refactor helpers break down exactly where legacy systems hurt most:

- dense dependency graphs
- hidden side effects
- shared mutable state
- modules that break three things when you touch one

This project is opinionated about that failure mode.

It does not assume the answer is "rewrite everything."  
It assumes the safer sequence is:

1. map the current shape
2. lock behavior
3. estimate blast radius
4. show the route to the user
5. execute only after approval
6. checkpoint each verified wave with git

### Why It Feels Different

- `Route first, edit second`: no structural edits before an explicit approved route.
- `Automatic downgrade for high risk`: tangled code falls back to `untangle-first`.
- `Git is part of execution`: baseline checkpoint, branch strategy, per-wave commits.
- `Planning artifacts are first-class`: every risky refactor gets a documented handoff package.
- `Bilingual trigger coverage`: descriptions include both English and Chinese trigger phrases.

### Quick Start

#### Install

Copy both skill folders into your skill directory:

```text
$CODEX_HOME/skills
```

Or, if `CODEX_HOME` is unset:

```text
~/.codex/skills
```

You can also use the bundled installer:

```text
python scripts/install_skills.py --force
```

Useful flags:

- `--dest <path>` installs to a custom path
- `--mode link` creates symlinks instead of copies
- `--dry-run` previews the destination

#### Run A Full Risky Refactor Flow

```text
$gsd-legacy-refactor src/auth --goal "split auth orchestration from token storage"
```

What happens:

1. inspect the target
2. write `.planning/refactors/<slug>/`
3. classify risk and choose mode
4. show the route for approval
5. execute approved waves
6. checkpoint progress with git

#### Run A Single Guardrailed Wave

```text
$refactoring-legacy-code src/reporting/legacy_parser.py
```

Use this when you already know the boundary and want execution guardrails.

### How It Thinks

The suite uses two execution modes:

| Mode | Use when |
|------|----------|
| `untangle-first` | Risk is high, behavior is fuzzy, coupling is dense, or tests are weak |
| `refactor-wave` | Boundary is small, callers are known, and verification is credible |

It always prefers:

- one hotspot per wave
- stable external behavior
- compatibility seams over blanket rewrites
- verified progress over heroic big-bang changes

### Artifact Output

`$gsd-legacy-refactor` writes:

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

The execution skill always emits these decisions before structural edits:

```text
Risk Level: high
Mode: untangle-first
Current State Map: callers, dependencies, side effects
Safety Net: existing tests + missing characterization coverage
Safe Boundary: adapter seam around token store
Verification Gate: targeted tests + smoke checks + rollback point
```

### Repo Layout

```text
skills/
  refactoring-legacy-code/
    SKILL.md
    agents/openai.yaml
    references/
  gsd-legacy-refactor/
    SKILL.md
    agents/openai.yaml
    workflows/legacy-refactor.md
    references/artifact-contract.md
    templates/
scripts/
  install_skills.py
docs/
  assets/social-preview-zh.png
  demo-cases.md
  github-launch.md
```

### Docs

- [Demo cases](docs/demo-cases.md)
- [GitHub launch kit](docs/github-launch.md)
- [License](LICENSE)

### What This Is Not

- not a one-click monolith rewrite button
- not a generic cleanup prompt
- not for tiny isolated bug fixes
- not a promise that AI can skip tests, verification, or git hygiene

### Roadmap

- add real demo runs on TypeScript and Python repos
- add forward-test prompts and expected artifacts
- add release packaging for easier sharing
- add benchmark comparisons against naive refactor prompts

### Contributing

Issues and PRs are welcome, especially for:

- real legacy-code case studies
- safer wave-planning heuristics
- better trigger descriptions
- install and packaging improvements
- public demo repos

## 中文

### 这是什么

`屎山重构.skill` 是一套双层 skill：

| Skill | 作用 |
|------|------|
| `refactoring-legacy-code` | 执行层。负责评估爆炸半径、冻结行为、划定安全边界，并按波次重构。 |
| `gsd-legacy-refactor` | 编排层。负责扫描目标、生成 `.planning/refactors/<slug>/` 工件、给用户确认路线，然后按 git checkpoint 执行。 |

这个 README 的组织方式参考了高 star skill / tooling 项目常见的首页模式，比如 [anthropics/skills](https://github.com/anthropics/skills) 和 [daymade/claude-code-skills](https://github.com/daymade/claude-code-skills)：先讲价值，再给安装和上手，再落到更细的说明。

### 为什么做它

大部分 AI 重构工具最容易翻车的地方，恰恰就是遗留系统最痛的地方：

- 依赖图过密
- 隐式副作用太多
- 共享可变状态
- 改一处崩三处的核心模块

这个项目就是针对这个失败模式设计的。

它不假设答案是“全部重写”，而是假设更安全的顺序应该是：

1. 先把当前结构摸清
2. 先锁定行为
3. 先评估 blast radius
4. 先把路线给用户确认
5. 确认后再执行
6. 每个验证通过的波次都用 git checkpoint 固化

### 它和普通重构提示词有什么不同

- `先路线，后改代码`：没有明确批准前，不允许做结构性修改。
- `高风险自动降级`：耦合太重时自动切到 `untangle-first`。
- `把 git 当执行系统的一部分`：baseline、分支、每波 commit 都是规则，不是善后。
- `规划工件是第一公民`：每次高风险重构都要留下可交接的 `.planning` 包。
- `中英双语触发词`：英文和中文场景都更容易被 skill 发现。

### 快速开始

#### 安装

把两个 skill 文件夹复制到你的 skill 目录：

```text
$CODEX_HOME/skills
```

如果没有设置 `CODEX_HOME`，就放到：

```text
~/.codex/skills
```

也可以直接用安装脚本：

```text
python scripts/install_skills.py --force
```

常用参数：

- `--dest <path>` 指定安装路径
- `--mode link` 用软链接代替复制
- `--dry-run` 只预览不写入

#### 跑完整高风险重构流程

```text
$gsd-legacy-refactor src/auth --goal "split auth orchestration from token storage"
```

执行流程：

1. 扫描目标
2. 生成 `.planning/refactors/<slug>/`
3. 评估风险并选择模式
4. 把路线展示给用户确认
5. 执行已批准的波次
6. 用 git 做 checkpoint

#### 直接执行单个受保护波次

```text
$refactoring-legacy-code src/reporting/legacy_parser.py
```

适合你已经知道边界，只想要执行护栏的时候。

### 它的思考方式

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

### 产物输出

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

### 仓库结构

```text
skills/
  refactoring-legacy-code/
    SKILL.md
    agents/openai.yaml
    references/
  gsd-legacy-refactor/
    SKILL.md
    agents/openai.yaml
    workflows/legacy-refactor.md
    references/artifact-contract.md
    templates/
scripts/
  install_skills.py
docs/
  assets/social-preview-zh.png
  demo-cases.md
  github-launch.md
```

### 相关文档

- [Demo 用例](docs/demo-cases.md)
- [GitHub 发布素材](docs/github-launch.md)
- [许可证](LICENSE)

### 它不是什么

- 不是一键重写单体系统的按钮
- 不是泛泛的代码整理提示词
- 不是给小型独立 bugfix 用的
- 不是“AI 可以跳过测试和验证”的借口

### 路线图

- 增加 TypeScript 和 Python 的真实 demo
- 增加 forward-test prompts 和期望产物
- 增加更方便的 release packaging
- 增加和 naive refactor prompt 的对比 benchmark

### 贡献

欢迎 issue 和 PR，尤其是：

- 真实屎山案例
- 更稳的 wave planning 规则
- 更好的触发描述
- 更顺手的安装和打包流程
- 公共 demo 仓库

## License

MIT. See [LICENSE](LICENSE).
