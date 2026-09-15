# Changelog

All notable changes to SparkSerial Pro are documented here.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and versioning
follows [Semantic Versioning](https://semver.org/) (`MAJOR.MINOR.PATCH`).

Entries under **Unreleased** are pending — they move into a new dated, versioned section
(and get mirrored into `sparkserial/data/whats_new.json` as user-facing highlights) as part
of the release process. See `.claude/skills/pypi-release/SKILL.md`.

## [Unreleased]

## [0.3.1] - 2026-09-15

### Fixed
- The Saved Commands panel showed a white background instead of the app's dark theme —
  the stylesheet only styled the old flat list widget, not the new categorized tree view
  introduced in 0.3.0.
- The "What's New" popup didn't appear for users upgrading from a version older than 0.3.0
  (the first version to have it), since it had no record of what they'd already seen and
  assumed that meant a brand new install. It now recognizes an existing installation and
  shows everything they've missed.

## [0.3.0] - 2026-09-15

### Fixed
- Command history Up/Down arrow navigation could get hijacked by Qt's native combo-box
  item cycling (reversing "previous"/"next" direction) depending on how the input field
  acquired focus.

### Added
- Command Shortcuts can now be organized into categories/subsections instead of one flat
  list — add or edit a shortcut's Category to group related commands.
- Multiple independent windows: **File → New Window** (`Ctrl+N`) opens another SparkSerial
  window with its own connection, so different serial devices can be worked with at once.
- A small "What's New" popup now appears the first time the app is opened after an upgrade.

## [0.2.1]

### Added
- Base Converter tool (Decimal / Hex / Binary / ASCII) under the Tools menu.

### Changed
- Clarified Windows install instructions (PATH issues, `pipx` recommendation) in the README.

## [0.2.0]

### Added
- Custom-drawn checkboxes for a consistent look across platforms.
- Command history navigation via Up/Down arrow keys.
- Bulk find/replace across all saved command shortcuts.
- Import/export of the saved command library as JSON.

## [0.1.1]

### Changed
- Author metadata updated.

## [0.1.0]

### Added
- Initial release: serial connection management, saved command shortcuts, real-time
  terminal with Hex view/timestamps/logging, and dark-mode UI.
