# Changelog

All notable changes to this project are recorded here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added

- Drawn architecture and flow figures in `docs/diagrams/`, light and dark, shown in the README.

## [0.1.0] - 2026-10-26

### Added

- ADR 0007 (how the orders service announces paid orders), its three audience versions, a reaction log (a worked example), a three-minute talk, ADR 0005 (the late record, superseded) and ADR 0006 (the interim index).
- `adr-toolkit check | log | report`: the decision-record, audience, reaction, talk and decision-log rules (ADR001 to ADR103, AUD001 to AUD008, REA001 to REA004, TLK001, DOC001, DOC002, LOG001).
- Layered package (`domain`, `application`, `infrastructure`, `interfaces`) with the dependency rule enforced by import-linter, unit tests, one integration test per "Done when" line, ruff, mypy strict, hash-pinned lock files and a CI workflow.
