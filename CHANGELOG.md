# Changelog

All notable changes to Summit are listed here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/). Summit has no tagged releases yet, so entries are dated, not versioned.

## [Unreleased]

### Added
- House documentation: `CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`, this changelog, issue and pull request templates, and a CI workflow that compiles every script and runs each with `--help`.

### Changed
- `README.md` and `AGENTS.md` restructured. All existing content and rules are kept.

## 2026-10-10

### Changed
- Claude judges run on an Anthropic API key only, never a Claude subscription. Stated in the README, `AGENTS.md`, and `judges.md`, and enforced in `scripts/two_judges.py` and `scripts/grade_with_codex.py` (#1).

## 2026-10-07

### Added
- First commit. Three skills (`build-eval`, `hillclimb`, `red-team`), six prompts for API and ChatGPT-subscription billing, `judges.md`, seven scripts, templates, and `SOURCES.md`. MIT license.
