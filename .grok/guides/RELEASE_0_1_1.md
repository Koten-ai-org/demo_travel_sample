# Guide: TravelPlan 0.1.1

**Date**: 2026-11-27
**Feature**: App version 0.1.1 and the GitHub release that records the base-9.1 analytics pin
**Status**: Active
**Related Plan**: `.grok/plans/BUMP_VERSION_0_1_1.md`

## 1. Overview
- **Purpose**: Identify this checkout as TravelPlan `0.1.1` and publish the changes since release `0.1.0`.
- **Scope**: Version strings, the `/api/health` app version, and the GitHub release notes. The product change in this release is the vendored analytics pin from [pull request #10](https://github.com/Koten-ai-org/demo_travel_sample/pull/10) (ZD-33).
- **Entry points**:
  - `GET /api/health` field `app_version`
  - `travel_planner.__version__`
  - GitHub release `0.1.1`

## 2. Architecture & Flow
- **High-level flow**:
  1. `src/travel_planner/__init__.py` sets `__version__`.
  2. `pyproject.toml` `[project].version` is the same string for the package metadata.
  3. `GET /api/health` reads `travel_planner.__version__`. The fallback in `app.py` is `0.1.1` when the attribute is missing.
  4. The GitHub tag `0.1.1` points at the commit that contains those strings. The release body describes ZD-33.
- **Key components**:
  - `src/travel_planner/__init__.py` — runtime version
  - `src/travel_planner/app.py` — `api_health` `app_version`
  - `pyproject.toml` — package version
  - `data/chat_requests/chat_request_analytics_base-9.1.json` — vendored pin shipped in this release
  - `tests/test_app.py` — asserts `app_version` is `0.1.1`
  - `tests/test_vendored_catalog.py` — asserts the pin lineage and byte-identical load copies
- **Data flow**: Health has no external call for `app_version`. It is the import-time string.
- **Dependencies**: GitHub repo `Koten-ai-org/demo_travel_sample`. No new env vars.

## 3. Setup
- **Prerequisites**: A checkout at tag `0.1.1` or later on `main`.
- **Environment variables**: None added in this release.
- **Install / bootstrap steps**:
  1. `pip install -e ".[dev]"` from this repo, with `../zeus_client_python` present.
  2. `python -m travel_planner`
- **Configuration**: Unchanged. `client_floor` stays `client-floor-6.1`.
- **Verification**: `GET /api/health` returns `"app_version": "0.1.1"`.

## 4. How to Use
- **Primary workflow**:
  1. Open the app or call `GET /api/health`.
  2. Read `app_version`. It is `0.1.1` on this release.
- **Examples**:
  - `python -c "import travel_planner; print(travel_planner.__version__)"`
  - `gh release view 0.1.1`
- **Edge cases**: A process started before the version commit keeps the old string until restart.
- **Limitations**: `build_version` in `config.json` is separate from `app_version` and was not bumped.

## 5. Debugging & Known Issues
- **Common symptoms → causes → fixes**:
  | Symptom | Likely Cause | Fix |
  |---------|--------------|-----|
  | Health still says `0.1.0` | Process or image built before the bump | Restart from a tree that contains `__version__ = "0.1.1"` |
  | Vendored pin tests fail on `base-6.1` | Checkout is tag `0.1.0` or older | Use tag `0.1.1` or `main` after the version commit |
- **Debug checklist**:
  - [ ] `travel_planner.__version__` is `0.1.1`
  - [ ] `data/chat_requests/chat_request_analytics_base-9.1.json` exists and `_lineage.base_id` is `base-9.1`
  - [ ] `gh release view 0.1.1` resolves
- **Known issues**:
  - **`test_env_contract_keeps_secrets_out_of_committed_json` LLM_MODEL mismatch** — Present before this release. `.env.example` says `grok-4.5-latest`. The 0.1.1 pin commit did not change that test.
- **Logging & observability**: `/api/health` JSON. No new log line.

## 6. Related Artifacts
- **Files changed / owned by this feature**:
  - `pyproject.toml` — package version `0.1.1`
  - `src/travel_planner/__init__.py` — `__version__`
  - `src/travel_planner/app.py` — health fallback
  - `tests/test_app.py` — health assertion
  - `data/chat_requests/chat_request_analytics_base-9.1.json` — pin included from ZD-33 (already on `main` before the version commit)
- **Tickets**:
  - ZD-33 — vendor the analytics pin as base-9.1
- **Commits**:
  - `4a673a9` — ZD-33 vendor the analytics pin as base-9.1
  - `c34b9a1` — Merge pull request #10
- **Pull requests**:
  - [#10](https://github.com/Koten-ai-org/demo_travel_sample/pull/10) — ZD-33: vendor the analytics pin as base-9.1

## 7. Changelog
| Date | Author | Change |
|------|--------|--------|
| 2026-11-27 | Grok | Initial guide for the 0.1.1 version bump and release |
