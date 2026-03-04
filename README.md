# Analytics Team Starter Kit

Team operations toolkit for analytics leads: SLA tracking, workload distribution,
and data quality monitoring for NbS/ESG data teams.

## Features
- **Team metrics dashboard**: ticket volume, SLA %, resolution time, workload per analyst
- **Data quality scorecard**: completeness, uniqueness, composite quality score per dataset
- **Configurable SLA**: adjust target resolution days per team agreement
- **Sample data**: PUR Projet-style analytics team ticket log

## Quick Start

```python
from src.main import AnalyticsTeamStarterKit

kit = AnalyticsTeamStarterKit(config={"sla_days": 5, "team_size": 3})
df = kit.load_data("sample_data/team_tickets.csv")

metrics = kit.team_metrics_dashboard(df)
print(f"SLA Compliance:   {metrics['sla_compliance_pct']:.1f}%")
print(f"Avg Resolution:   {metrics['avg_resolution_days']:.1f} days")
print(f"Workload: {metrics['workload_by_assignee']}")

# Data quality check on any dataset
quality = kit.data_quality_scorecard(df)
print(f"Quality Score: {quality['composite_score']}")
```

## Running Tests
```bash
pytest tests/ -v
```
