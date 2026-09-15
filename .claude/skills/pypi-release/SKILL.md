---
name: pypi-release
description: Prepare, validate, and compliance-check a new SparkSerial release before uploading to PyPI — decides the version bump, updates CHANGELOG.md and the in-app "what's new" data, builds and checks the distribution, and walks through the actual upload. Use when the user asks to cut a release, bump the version, publish/upload to PyPI, or prepare a new SparkSerial version.
user-invocable: true
---

# SparkSerial PyPI Release

This project publishes to PyPI as `sparkserial` (`pyproject.toml`, setuptools backend, no CI —
every release is done by hand from a dev machine). Do not run `twine upload` or push a git tag
without the user explicitly confirming — publishing to PyPI is irreversible for that version
number (PyPI never allows re-uploading a filename/version once used, even after deleting it).

Work through these phases in order. Stop and ask the user if any check fails rather than
silently working around it.

## 1. Decide the version number (SemVer: `MAJOR.MINOR.PATCH`)

Read the `## [Unreleased]` section of `CHANGELOG.md` and the actual diff since the last
release tag/commit to classify the changes, then bump the current `version` in
`pyproject.toml` accordingly:

- **PATCH** (`0.2.1` → `0.2.2`): bug fixes only, no new user-facing behavior.
- **MINOR** (`0.2.1` → `0.3.0`): new features/behavior that are backward compatible (this is
  the common case for this project — most releases so far have been MINOR bumps).
- **MAJOR** (`0.x` → `1.0.0`, or later `X.0.0`): breaking changes — e.g. the saved-commands
  JSON schema changes incompatibly, a CLI/entry-point changes, minimum Python version bumps
  in a way that drops support.

Never reuse or go backwards from the version already published on PyPI. Check what's live
first:

```bash
curl -s https://pypi.org/pypi/sparkserial/json | python3 -c "import json,sys; print(json.load(sys.stdin)['info']['version'])"
```

If the current `pyproject.toml` version is already **ahead** of what's on PyPI (i.e. it was
bumped previously but never actually published — check `dist/` for a matching, already-built
wheel as a sign of this), ask the user whether that version should be published as-is or
bumped further before adding new changes to it.

**Don't skip this check even when `pyproject.toml`'s version "looks right."** During the
0.3.0 release, `pyproject.toml` still said `0.2.1` locally, and it turned out `0.2.1` was
*already live* on PyPI — the version in the working tree had been bumped in a previous session
but the actual publish had happened separately. Always hit the PyPI API and compare, don't
trust local state alone. Ask the user to confirm the bump (this is a judgment call — patch vs.
minor — worth a quick confirmation rather than guessing) before touching any files.

## 2. Update version + changelog + in-app "what's new" together

These three must move in lockstep — don't update one without the others:

1. **`pyproject.toml`**: bump `version = "X.Y.Z"`.
2. **`CHANGELOG.md`**: rename `## [Unreleased]` to `## [X.Y.Z] - YYYY-MM-DD` (today's date),
   then add a fresh empty `## [Unreleased]` above it for future work.
3. **`sparkserial/data/whats_new.json`**: add a new `"X.Y.Z": [...]` entry containing only the
   **user-facing** highlights from that changelog section (skip internal-only fixes/refactors
   nobody would notice — e.g. "fixed a typo in a comment" doesn't belong here, but "fixed
   Up/Down arrow history navigation" does). Keep each bullet short — this renders in a small
   popup dialog (`sparkserial/gui/whats_new_dialog.py`), not a full changelog. This is what
   `sparkserial/core/version_info.py` reads to decide what to show a user who upgrades past
   this version.
4. **`README.md`**: update the `Current version: **X.Y.Z**` line to match.

Keep the wording of the CHANGELOG entry and the whats_new.json bullet for the same change
consistent — the changelog can be more technical/complete, the popup version should be
plain-language and short (one line per bullet, no jargon like "refactored" or file names).

## 3. Validate before building

```bash
uv sync --group dev              # ensure build + twine are installed and lockfile is current
uv run python -c "import ast; ast.parse(open('sparkserial/main.py').read())"  # quick syntax sanity check
```

**Always use `--group dev`, never bare `uv sync`.** `build` and `twine` are declared in
`[dependency-groups] dev` in `pyproject.toml` specifically so `uv sync` doesn't remove them —
but a bare `uv sync` (no `--group`) still only installs the base project deps and will
*uninstall* `build`/`twine` from the venv if they're currently present, even though they're
declared, because dependency groups are opt-in per invocation. This happened once already
during development: a stray `uv sync` silently stripped both tools from the venv mid-session.
If a later step reports `twine`/`build` not found, re-run `uv sync --group dev` before
assuming something is broken.

Confirm:
- `pyproject.toml` version, `CHANGELOG.md` heading, `whats_new.json` key, and `README.md` all
  show the **same** new version number.
- `sparkserial/data/whats_new.json` is valid JSON (`python3 -m json.tool sparkserial/data/whats_new.json`).
- No debug artifacts are staged: check `git status` for stray test scripts, `logs/*.txt`,
  or `saved_commands.json` (that file living at the repo root is a leftover local data file,
  not part of the package — it must never be committed or bundled; the app's real data lives
  under `~/.sparkserial/`).
- Every non-`.py` runtime asset directory (`assets/`, `data/`, and any new ones added later)
  is declared **both** in `[tool.setuptools] packages` (as `"sparkserial.assets"`,
  `"sparkserial.data"`, etc. — plain subdirectories with no `__init__.py` still need to be
  listed explicitly) **and** has its own `[tool.setuptools.package-data]` entry, e.g.:
  ```toml
  [tool.setuptools]
  packages = ["sparkserial", "sparkserial.core", "sparkserial.gui", "sparkserial.assets", "sparkserial.data"]

  [tool.setuptools.package-data]
  "sparkserial.assets" = ["*.png"]
  "sparkserial.data" = ["*.json"]
  ```
  A single glob under the top-level `sparkserial` key (e.g. `sparkserial = ["data/*.json"]`)
  *does* still bundle the file into the wheel, but setuptools prints a loud
  `SetuptoolsDeprecationWarning` about implicit namespace/package-data handling on every
  build — treat that warning as something to fix now, not ignore, since a future setuptools
  version may make it a hard error. Confirm the fix by running the build and checking the
  warning is gone, then `unzip -l dist/*.whl` to confirm the file still made it in.

## 4. Build and compliance-check the distribution

```bash
rm -rf dist/ build/ *.egg-info sparkserial.egg-info   # clean slate — stale dist/ files (there
                                                        # may already be an old build in dist/)
                                                        # can otherwise get uploaded by mistake
uv run python -m build
uv run twine check dist/*
```

`twine check` catches the most common PyPI rejection causes (bad long-description rendering,
missing metadata) — treat any warning as blocking, not just errors. Additionally verify by
hand:

- **License consistency**: `pyproject.toml` declares `license = "MIT"` and a matching
  `classifiers` entry style; `LICENSE` file at repo root must exist and actually say MIT.
- **Version consistency**: unzip/inspect the built wheel's metadata matches the intended
  version (`unzip -p dist/sparkserial-X.Y.Z-py3-none-any.whl sparkserial-X.Y.Z.dist-info/METADATA | head -20`).
- **No secrets**: `unzip -l dist/sparkserial-X.Y.Z-py3-none-any.whl` — confirm it contains only
  expected package files (`sparkserial/**`, no `.env`, no `~/.sparkserial` user data, no
  `.git`).
- **Package importability**: install the built wheel into a throwaway venv and confirm it
  launches without import errors:
  ```bash
  uv venv /tmp/sparkserial-release-check --python 3.11
  uv pip install --python /tmp/sparkserial-release-check/bin/python dist/sparkserial-*.whl
  /tmp/sparkserial-release-check/bin/python -c "import sparkserial.main; from importlib.metadata import version; print(version('sparkserial'))"
  ```

## 5. Commit, tag, and publish (confirm with the user before each irreversible step)

```bash
git add pyproject.toml CHANGELOG.md sparkserial/data/whats_new.json README.md uv.lock
git commit -m "Release vX.Y.Z"
git tag vX.Y.Z
```

Ask the user separately whether to push the commit/tag now vs. after a successful upload, and
whether they'll run the upload themselves or want you to.

**Never run `twine upload` yourself with a token pasted into the chat, and don't read
`~/.pypirc`'s contents.** PyPI tokens are long-lived, high-privilege secrets — having the
agent handle or echo one is unnecessary risk when the user's own terminal already has (or can
get) valid auth. Hand back the exact command and let the user run and authenticate it
themselves:

```bash
uv run twine upload dist/*         # prompts for PyPI credentials/API token
```

Prefer uploading to TestPyPI first (`twine upload --repository testpypi dist/*`) if the user
is unsure or this is a risky/large change, and confirm the test install works
(`pip install --index-url https://test.pypi.org/simple/ sparkserial`) before the real upload.

### Troubleshooting a failed upload

If the user reports the upload failed, get the exact console output (twine's `--verbose` output
is safe to share back — it doesn't print the raw token) and diagnose from there rather than
guessing. One real occurrence and its cause:

- **`403 Forbidden: Invalid or non-existent authentication information`** after manually
  entering a token at the `Enter your API token:` prompt: this happened even though the token
  itself looked correct. Likely causes, roughly in order of likelihood:
  1. **A stale `~/.pypirc`** is also in play — twine logs `Using configuration from
     ~/.pypirc` even when you're prompted for a token, and a leftover `username`/`password`
     pair in that file (from an old, non-token auth setup, or an expired token) can conflict
     with what you just typed. Ask the user to check the file's *structure* (never its
     contents verbatim, since it may hold a live secret) — for token auth it must be exactly:
     ```ini
     [pypi]
     username = __token__
     password = pypi-...
     ```
     If `username` isn't literally `__token__`, that's the bug.
  2. **Expired/revoked token** — have the user generate a fresh one at
     https://pypi.org/manage/account/token/, scoped to the `sparkserial` project (or the whole
     account if simpler).
  3. **Paste artifacts** — a trailing newline or a token copied without its `pypi-` prefix
     produces the same 403. Re-copying carefully often fixes it outright.
  - To isolate whether `.pypirc` is the culprit, have the user bypass it entirely:
    `twine upload -u __token__ -p <token> dist/*` (run and typed by the user, never by you).
  - `WARNING This environment is not supported for trusted publishing` in the output is
    expected/harmless on a local dev machine (trusted publishing is a GitHub-Actions-only
    OIDC mechanism) — it's not the cause of a 403, just noise that appears before twine falls
    back to asking for a token.

After a successful publish, verify the popup actually fires for upgraders: an existing user
with an older `last_seen_version` in `~/.sparkserial/config.json` should see the new
`whats_new.json` entry on their next launch (see `version_info.get_unseen_release_notes()`).
