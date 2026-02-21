# Changelog

All notable changes to this project are documented in this file.

The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and versioning follows [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- _No changes yet._

### Changed
- _No changes yet._

## [1.0.0] - 2026-02-21

### Added
- Expanded docs in `docs/` (`getting-started`, `architecture`, `contributing`, `faq`).
- Improved root and SDK READMEs with clearer positioning, runtime compatibility notes, comparison guidance, and usage boundaries.
- Added explicit data-source and indexing attribution for Uber H3 and OpenStreetMap contributors in project docs.

### Changed
- JavaScript geocoder now returns `null` for out-of-range coordinates instead of allowing invalid H3 conversion.
- JavaScript tests now cover out-of-range coordinate handling.

---

## How to maintain this file

For every PR/feature/fix:

1. Add a short bullet under `## [Unreleased]`.
2. Place entries in one of these buckets:
   - `Added`
   - `Changed`
   - `Fixed`
   - `Removed`
   - `Security` (if relevant)
3. Keep bullets user-facing (what changed, not implementation internals).

When releasing:

1. Create a new section:
   - `## [x.y.z] - YYYY-MM-DD`
2. Move all `Unreleased` bullets into that version.
3. Reset `## [Unreleased]` with empty buckets (or remove empty buckets).
4. Ensure versions match package/module versions in:
   - `libs/javascript/package.json`
   - `libs/python/pyproject.toml`
   - `libs/go` release/tag strategy


