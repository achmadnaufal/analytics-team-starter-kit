"""
Analytics team starter kit for nature-based solutions (NbS) and ESG data programs.

Provides reusable frameworks for data analytics team management: SLA tracking,
ticket backlog analysis, data quality scoring, and team capacity planning.
Designed for analytics leads managing small-to-medium data teams.

Author: github.com/achmadnaufal
"""
import pandas as pd
import numpy as np
from pathlib import Path
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta


class AnalyticsTeamStarterKit:
    """
    Analytics team operations and metrics starter kit.

    Helps analytics leads track team workload, SLA compliance,
    ticket resolution rates, and data quality across projects.

    Args:
        config: Optional dict with keys:
            - sla_days: Default SLA target in business days (default 5)
            - team_size: Number of analysts (for capacity calc, default 3)

    Example:
        >>> kit = AnalyticsTeamStarterKit(config={"sla_days": 5, "team_size": 3})
        >>> df = kit.load_data("data/tickets.csv")
        >>> report = kit.team_metrics_dashboard(df)
        >>> print(report["sla_compliance_pct"])
    """

    def __init__(self, config: Optional[Dict] = None):
        self.config = config or {}
        self.sla_days = self.config.get("sla_days", 5)
        self.team_size = self.config.get("team_size", 3)

    def load_data(self, filepath: str) -> pd.DataFrame:
        """
        Load team ticket/request data from CSV or Excel.

        Args:
            filepath: Path to file. Expected columns: ticket_id, assignee,
                      created_date, resolved_date, priority, status, project.

        Returns:
            DataFrame with ticket data.

        Raises:
            FileNotFoundError: If file does not exist.
        """
        p = Path(filepath)
        if not p.exists():
            raise FileNotFoundError(f"Data file not found: {filepath}")
        if p.suffix in (".xlsx", ".xls"):
            return pd.read_excel(filepath)
        return pd.read_csv(filepath)

    def validate(self, df: pd.DataFrame) -> bool:
        """
        Validate ticket data structure.

        Args:
            df: Ticket DataFrame.

        Returns:
            True if valid.

        Raises:
            ValueError: If empty or missing required columns.
        """
        if df.empty:
            raise ValueError("Input DataFrame is empty")
        df_cols = [c.lower().strip().replace(" ", "_") for c in df.columns]
        required = ["ticket_id", "status"]
        missing = [c for c in required if c not in df_cols]
        if missing:
            raise ValueError(f"Missing required columns: {missing}")
        return True

    def preprocess(self, df: pd.DataFrame) -> pd.DataFrame:
        """Normalize column names and parse date columns."""
        df = df.copy()
        df.dropna(how="all", inplace=True)
        df.columns = [c.lower().strip().replace(" ", "_") for c in df.columns]
        for col in ["created_date", "resolved_date"]:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors="coerce")
        return df

    def team_metrics_dashboard(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Generate team operational metrics dashboard.

        Calculates ticket volume, SLA compliance, resolution time,
        workload distribution, and backlog by priority.

        Args:
            df: Ticket DataFrame with ticket_id, status, and optionally
                created_date, resolved_date, assignee, priority.

        Returns:
            Dict with:
                - total_tickets: Total ticket count
                - open_tickets: Currently open count
                - resolved_tickets: Resolved count
                - sla_compliance_pct: % resolved within SLA days
                - avg_resolution_days: Mean time to resolve (days)
                - backlog_by_priority: Count by priority level
                - workload_by_assignee: Tickets per team member
                - resolution_rate_pct: Resolved / total %
        """
        df = self.preprocess(df)

        total = len(df)
        status_col = "status" if "status" in df.columns else df.columns[0]
        open_tickets = int(df[df[status_col].str.lower().isin(["open", "in progress", "pending"])].shape[0])
        resolved = int(df[df[status_col].str.lower().isin(["resolved", "closed", "done"])].shape[0])

        # SLA compliance
        sla_compliance = None
        avg_resolution = None
        if "created_date" in df.columns and "resolved_date" in df.columns:
            resolved_df = df[df["resolved_date"].notna()].copy()
            if not resolved_df.empty:
                resolved_df["resolution_days"] = (
                    (resolved_df["resolved_date"] - resolved_df["created_date"])
                    .dt.total_seconds() / 86400
                ).round(1)
                within_sla = resolved_df[resolved_df["resolution_days"] <= self.sla_days]
                sla_compliance = round(len(within_sla) / len(resolved_df) * 100, 2)
                avg_resolution = round(float(resolved_df["resolution_days"].mean()), 2)

        # Backlog by priority
        backlog = {}
        if "priority" in df.columns:
            open_df = df[df[status_col].str.lower().isin(["open", "in progress", "pending"])]
            backlog = open_df.groupby("priority").size().to_dict()

        # Workload by assignee
        workload = {}
        if "assignee" in df.columns:
            workload = df.groupby("assignee").size().sort_values(ascending=False).to_dict()

        return {
            "total_tickets": total,
            "open_tickets": open_tickets,
            "resolved_tickets": resolved,
            "resolution_rate_pct": round(resolved / total * 100, 2) if total > 0 else 0,
            "sla_compliance_pct": sla_compliance,
            "avg_resolution_days": avg_resolution,
            "backlog_by_priority": backlog,
            "workload_by_assignee": workload,
        }

    def data_quality_scorecard(self, df: pd.DataFrame) -> Dict[str, Any]:
        """
        Generate a data quality scorecard for a dataset.

        Calculates completeness, uniqueness, and validity scores
        across all columns, returning a composite quality score.

        Args:
            df: Any DataFrame to assess for data quality.

        Returns:
            Dict with:
                - completeness_pct: % non-null values
                - uniqueness_pct: % unique values (of non-null)
                - column_scores: Per-column quality breakdown
                - composite_score: Overall quality score (0-100)
        """
        df2 = self.preprocess(df)
        total_cells = df2.shape[0] * df2.shape[1]
        null_cells = df2.isnull().sum().sum()
        completeness = round((1 - null_cells / total_cells) * 100, 2) if total_cells > 0 else 0

        col_scores = {}
        for col in df2.columns:
            non_null = df2[col].dropna()
            completeness_col = round(len(non_null) / len(df2) * 100, 2) if len(df2) > 0 else 0
            uniqueness_col = round(non_null.nunique() / len(non_null) * 100, 2) if len(non_null) > 0 else 0
            col_scores[col] = {
                "completeness_pct": completeness_col,
                "uniqueness_pct": uniqueness_col,
                "null_count": int(df2[col].isnull().sum()),
            }

        composite = round((completeness + np.mean([v["uniqueness_pct"] for v in col_scores.values()])) / 2, 2)

        return {
            "completeness_pct": completeness,
            "composite_score": composite,
            "column_scores": col_scores,
        }

    def analyze(self, df: pd.DataFrame) -> Dict[str, Any]:
        """Run descriptive analysis and return summary metrics."""
        df = self.preprocess(df)
        result = {
            "total_records": len(df),
            "columns": list(df.columns),
            "missing_pct": (df.isnull().sum() / len(df) * 100).round(1).to_dict(),
        }
        numeric_df = df.select_dtypes(include="number")
        if not numeric_df.empty:
            result["summary_stats"] = numeric_df.describe().round(3).to_dict()
            result["totals"] = numeric_df.sum().round(2).to_dict()
            result["means"] = numeric_df.mean().round(3).to_dict()
        return result

    def run(self, filepath: str) -> Dict[str, Any]:
        """Full pipeline: load → validate → analyze."""
        df = self.load_data(filepath)
        self.validate(df)
        return self.analyze(df)

    def to_dataframe(self, result: Dict) -> pd.DataFrame:
        """Convert result dict to flat DataFrame for export."""
        rows = []
        for k, v in result.items():
            if isinstance(v, dict):
                for kk, vv in v.items():
                    rows.append({"metric": f"{k}.{kk}", "value": vv})
            else:
                rows.append({"metric": k, "value": v})
        return pd.DataFrame(rows)
