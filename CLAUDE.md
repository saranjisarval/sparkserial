# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project overview

SparkSerial Pro is a lightweight, cross-platform (macOS/Windows/Linux) desktop Serial GUI tool built with **PyQt6** and **PySerial**, aimed at hardware engineers/developers debugging UART/serial devices. It's distributed on PyPI as `sparkserial`.

## Commands

```bash
./setup.sh          # installs uv if missing, then `uv sync` to create the venv
./run.sh             # launches the app via `uv run python sparkserial/main.py`
uv run sparkserial   # equivalent, using the installed console-script entry point
python -m sparkserial  # alternate entry point (sparkserial/__main__.py)
```

There is no test suite, linter, or CI configuration in this repo currently — don't assume `pytest`/`ruff`/etc. exist.

Packaging uses `setuptools` via `pyproject.toml` (not a `src/` layout — `sparkserial/` is the package at repo root). Build with `uv run python -m build` or `python -m build`; publish with `twine`. Any actual PyPI release should go through the `pypi-release` skill (`.claude/skills/pypi-release/SKILL.md`), which covers version bumping, changelog/"what's new" updates, and pre-upload compliance checks.

## Architecture

**Entry point chain**: `sparkserial/main.py:main()` creates the single `QApplication`, applies macOS-specific dock/icon setup, then instantiates `MainWindow` (`sparkserial/gui/main_window.py`) and calls `app.exec()`. Both `main.py` (repo root, thin re-export) and `sparkserial/__main__.py` just delegate to this.

**GUI layer** (`sparkserial/gui/`):
- `main_window.py` is the bulk of the application — the main window, all dialogs (`CommandDialog` for add/edit shortcuts, `BulkReplaceDialog`), the terminal view, connection settings, and every UI event handler. It's intentionally a large, mostly flat file rather than split into many small widget classes.
- Multiple independent `MainWindow` instances can coexist in one process (File → New Window / `Ctrl+N`, see `open_new_window`) — each owns its own `SerialManager`/connection, so different windows can talk to different serial devices simultaneously. New windows are kept alive via the module-level `_open_windows` list (PyQt has no other strong reference once a window has no Python-side owner), and are removed from it in `closeEvent`.
- The command-history combo box (`self.command_input`) intercepts Up/Down arrow keys via `eventFilter`, installed on **both** the `QComboBox` and its internal `lineEdit()` — key events can land on either depending on how focus was acquired, and only watching the line edit lets Qt's native item-cycling behavior hijack the arrows (see the comment at the install site for the full explanation).
- `converter_dialog.py` — standalone base-converter tool (Decimal/Hex/Binary/ASCII), opened from the Tools menu.
- `styles.py` — single `get_stylesheet()` function returning the entire dark-mode Qt stylesheet; every window/dialog applies it via `apply_styles()`/`setStyleSheet(get_stylesheet())`. There's no theming system — it's one hardcoded stylesheet string.

**Core layer** (`sparkserial/core/`), UI-independent:
- `serial_manager.py`: `SerialWorker` (a `QObject` moved to a `QThread`) owns the actual `pyserial.Serial` connection and polls it in a loop, emitting `data_received`/`error_occurred`/`connection_status` signals. `SerialManager` is the per-window facade that creates/tears down that worker+thread pair. This worker-thread pattern is what keeps serial I/O from blocking the UI — don't do serial reads/writes directly on the GUI thread.
- `command_manager.py`: persists the saved "Command Shortcuts" library to `~/.sparkserial/saved_commands.json` (not inside the repo/package — this survives package upgrades/reinstalls). Each command dict has `name`, `command`, `is_hex`, and `category` (added for grouping shortcuts into subsections in the UI tree; defaults to `"General"` and is auto-migrated in for older saved files missing it). Supports a custom storage location via `~/.sparkserial/config.json`'s `commands_file` key, with automatic one-time migration from an old package-relative location.

**Shared config file**: `~/.sparkserial/config.json` is a general small-settings store, not owned by a single class — `CommandManager` reads/writes its `commands_file` key, and version-upgrade tracking (`last_seen_version`, for the "what's new" popup) lives there too. Any code touching this file must read-modify-write the whole JSON object rather than overwriting it, so unrelated keys aren't clobbered.

**State/data that lives outside the package**: saved commands, custom config, and log files (`Log to File` checkbox, timestamped under `./logs/` relative to cwd) all live in the user's home directory or cwd, not next to the source — keep this in mind when reasoning about "where does X get saved."
