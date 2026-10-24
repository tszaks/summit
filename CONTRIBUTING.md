# Contributing to Summit

Thanks for helping. Summit is a small kit of method files, prompts, scripts, and templates. The bar for changes: does it keep the method honest, and does it keep the money and the keys safe?

By taking part you agree to follow the [Code of Conduct](CODE_OF_CONDUCT.md).

## Before you start

- For bugs or unclear instructions, open an issue with the template.
- For new features or methods, open an issue first and describe the problem you want to solve.
- Small fixes (typos, clear bugs) can go straight to a pull request.
- Security problems go through [SECURITY.md](SECURITY.md), not a public issue.

## Setup

You need Python 3. There is nothing to install.

```sh
git clone https://github.com/tszaks/summit.git
cd summit
```

## Check your change

There is no test suite. CI compiles every script and runs each one with `--help`. Run the same checks locally:

```sh
for f in scripts/*.py; do python3 -m py_compile "$f" && python3 "$f" --help > /dev/null || echo "FAIL $f"; done
```

Remove the `scripts/__pycache__` folder afterward if it appears. It is git-ignored.

If you change `grade_with_codex.py`, `isolation_check.py`, or the macOS sandbox template, say in the pull request which Codex version and OS you tested on. Those depend on Codex flags that change between versions.

## Code style

- **Match the surrounding code.** Same naming, same comment density, same idiom as the file you are editing.
- Scripts use only the Python standard library. No new dependencies without discussion.
- Docs use short, plain sentences. American English. No em dashes, no emoji in headings.

## Safety rules

- **Claude judges run on an Anthropic API key only.** Never add a path that drives a Claude subscription (`claude -p`, Claude Code, the Claude app). See [judges.md](judges.md).
- The dollar cap lives in runner code (`scripts/budget.py`), not in a prompt.
- Never print, log, or commit a key or login file. Check a variable with `[ -n "$VAR" ]`, never by echoing it.
- Do not weaken a rule in `AGENTS.md` or a skill to make a change pass. If a rule is wrong, say why in the pull request.

## Pull request checklist

- [ ] Every script still compiles and runs with `--help`.
- [ ] The change is small and focused. Unrelated cleanups go in their own pull request.
- [ ] The code and docs match the surrounding style and add no dependency.
- [ ] Skills, prompts, `AGENTS.md`, and `judges.md` still agree with each other.
- [ ] A line added under `[Unreleased]` in [CHANGELOG.md](CHANGELOG.md) for anything a user would notice.

## Using AI agents to contribute

Fine, as long as you read and understand what you submit and the checklist above is true. [AGENTS.md](AGENTS.md) tells agents how this repository works.

## License

By contributing you agree that your contribution is licensed under the [MIT License](LICENSE).
