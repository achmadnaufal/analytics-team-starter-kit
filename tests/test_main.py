"""Unit tests for AnalyticsTeamStarterKit."""
import pytest
import pandas as pd
import sys
sys.path.insert(0, "/Users/johndoe/projects/analytics-team-starter-kit")
from src.main import AnalyticsTeamStarterKit


@pytest.fixture
def ticket_df():
    return pd.DataFrame({
        "ticket_id": [f"T{i:03d}" for i in range(1, 11)],
        "assignee": ["Ahmad", "Ahmad", "Jamil", "Jamil", "Niken", "Niken", "Ahmad", "Jamil", "Niken", "Ahmad"],
        "priority": ["High", "High", "Medium", "Low", "High", "Medium", "Low", "High", "Medium", "Low"],
        "status": ["Resolved", "Resolved", "Open", "Resolved", "In Progress", "Resolved", "Closed", "Open", "Resolved", "Closed"],
        "created_date": pd.date_range("2026-02-01", periods=10, freq="2D"),
        "resolved_date": ["2026-02-03", "2026-02-06", None, "2026-02-09", None, "2026-02-14", "2026-02-16", None, "2026-02-22", "2026-02-24"],
        "project": ["NbS Carbon", "PUR Monitor", "Jira Rollout", "KoboToolbox", "Thailand VCI", "NbS Carbon", "PUR Monitor", "Jira Rollout", "Thailand VCI", "KoboToolbox"],
    })


@pytest.fixture
def kit():
    return AnalyticsTeamStarterKit(config={"sla_days": 5, "team_size": 3})


class TestValidation:
    def test_empty_raises(self, kit):
        with pytest.raises(ValueError, match="empty"):
            kit.validate(pd.DataFrame())

    def test_missing_columns_raises(self, kit):
        df = pd.DataFrame({"assignee": ["Ahmad"], "priority": ["High"]})
        with pytest.raises(ValueError, match="Missing required columns"):
            kit.validate(df)

    def test_valid_passes(self, kit, ticket_df):
        assert kit.validate(ticket_df) is True


class TestTeamMetricsDashboard:
    def test_returns_expected_keys(self, kit, ticket_df):
        result = kit.team_metrics_dashboard(ticket_df)
        assert "total_tickets" in result
        assert "open_tickets" in result
        assert "resolved_tickets" in result
        assert "sla_compliance_pct" in result

    def test_total_ticket_count(self, kit, ticket_df):
        result = kit.team_metrics_dashboard(ticket_df)
        assert result["total_tickets"] == 10

    def test_resolution_rate_positive(self, kit, ticket_df):
        result = kit.team_metrics_dashboard(ticket_df)
        assert result["resolution_rate_pct"] > 0

    def test_workload_by_assignee_present(self, kit, ticket_df):
        result = kit.team_metrics_dashboard(ticket_df)
        assert "Ahmad" in result["workload_by_assignee"]
        assert "Jamil" in result["workload_by_assignee"]

    def test_backlog_by_priority_present(self, kit, ticket_df):
        result = kit.team_metrics_dashboard(ticket_df)
        assert isinstance(result["backlog_by_priority"], dict)

    def test_avg_resolution_days_positive(self, kit, ticket_df):
        result = kit.team_metrics_dashboard(ticket_df)
        assert result["avg_resolution_days"] > 0


class TestDataQualityScorecard:
    def test_returns_expected_keys(self, kit, ticket_df):
        result = kit.data_quality_scorecard(ticket_df)
        assert "completeness_pct" in result
        assert "composite_score" in result
        assert "column_scores" in result

    def test_completeness_between_0_and_100(self, kit, ticket_df):
        result = kit.data_quality_scorecard(ticket_df)
        assert 0 <= result["completeness_pct"] <= 100

    def test_complete_df_scores_100_completeness(self, kit):
        df = pd.DataFrame({"a": [1, 2, 3], "b": ["x", "y", "z"]})
        result = kit.data_quality_scorecard(df)
        assert result["completeness_pct"] == 100.0
