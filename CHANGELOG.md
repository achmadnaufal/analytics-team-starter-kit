# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

## [CURRENT] - 2026-03-07
### Added
- `team_metrics_dashboard()`: ticket volume, SLA compliance, resolution time, workload by assignee
- `data_quality_scorecard()`: completeness, uniqueness, and composite quality score per column
- Real team ticket sample data modeled after PUR Projet analytics team workflow
- 12 unit tests covering validation, metrics, and data quality scoring
### Fixed
- `preprocess()` parses created_date and resolved_date as datetime automatically
- `validate()` explicitly checks for ticket_id and status columns
## [CURRENT] - 2026-03-07
### Added
- Add role-based access control framework and competency matrix
- Improved unit test coverage
- Enhanced documentation with realistic examples
