# Plan: Publish TravelPlan 0.1.1

**Date**: 2026-11-27
**Task**: Bump the app version to 0.1.1 and publish a GitHub release whose notes cover the analytics pin change since 0.1.0.
**Priority**: Medium
**Estimated Effort**: 1 hour / 3 steps

## 1. Context & Requirements
- **Goal**: `travel_planner.__version__` and `pyproject.toml` are `0.1.1`. `GET /api/health` returns `app_version` `0.1.1`. GitHub release `0.1.1` is published on `main` with notes for ZD-33 / pull request #10.
- **Constraints**: Tag the version-bump commit. Do not retag `0.1.0`. Leave untracked local catalogs, `.cursor/`, and `.worktrees/` out of the commit.
- **Assumptions**: `origin/main` is `c34b9a1` (merge of pull request #10). The only product change since tag `0.1.0` (`2c3531f`) is the base-9.1 analytics pin.
- **Out of Scope**: Fixing the pre-existing `LLM_MODEL` assertion in `test_env_contract_keeps_secrets_out_of_committed_json`. Changing the Zeus client pin. Syncing catalogs from a live Zeus.

## 2. Analysis & Research
- Key files explored: `pyproject.toml`, `src/travel_planner/__init__.py`, `src/travel_planner/app.py`, `tests/test_app.py`, `tests/test_vendored_catalog.py`, `data/chat_requests/chat_request_analytics_base-9.1.json`, GitHub release `0.1.0`
- Potential risks/edge cases:
  - Branch protection rejects a direct push to `main` → Mitigation: open a pull request and publish the release only after that commit is on `main`
  - Release notes describe a catalog the bytes do not match → Mitigation: compare the 0.1.0 pin to the base-9.1 file before writing the notes
  - Health fallback stays `0.1.0` if `__version__` is missing → Mitigation: update the fallback and assert `app_version == "0.1.1"`
- Alternatives considered: Tag `c34b9a1` without a version commit (the running app would still report `0.1.0`). A changelog file in the repo (0.1.0 put the notes on the GitHub release only).

## 3. Step-by-Step Implementation Plan
1. **Bump the version strings**
   - Files to change: `pyproject.toml`, `src/travel_planner/__init__.py`, `src/travel_planner/app.py`, `tests/test_app.py`
   - Changes: version and health fallback `0.1.1`; health test expects that string
   - Commands to run: `.venv/bin/pytest tests/test_app.py::test_health_zeus_client_version tests/test_vendored_catalog.py -q`
   - Tests needed: [x] health `app_version` is `0.1.1`; vendored pin tests still pass (3 passed)

2. **Record the release**
   - Files to change: `.grok/plans/BUMP_VERSION_0_1_1.md`, `.grok/guides/RELEASE_0_1_1.md`
   - Changes: plan and guide for the 0.1.1 publish
   - Tests needed: [ ]

3. **Publish**
   - Files to change: none (git tag + GitHub release)
   - Changes: commit the bump, push `main`, `gh release create 0.1.1` with the pin notes
   - Commands to run: `git push origin main`, `gh release create 0.1.1`
   - Tests needed: [ ] `gh release view 0.1.1` shows the notes and the new tag

## 4. Verification & Rollback
- **Tests**: `tests/test_app.py::test_health_zeus_client_version`, `tests/test_vendored_catalog.py`
- **Review Checklist**:
  - [ ] Code style/linting passes
  - [x] No breaking changes
  - [x] Feature guide created or updated in `.grok/guides/RELEASE_0_1_1.md`
- **Rollback Plan**: Delete the GitHub release and tag `0.1.1`, then revert the version commit. `0.1.0` stays on `2c3531f`.

## 5. Open Questions / Decisions Needed
- None. Publish goes to the existing GitHub repo release, matching `0.1.0`.
