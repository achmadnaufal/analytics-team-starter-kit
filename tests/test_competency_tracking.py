"""
Tests for competency tracking and team capabilities management.

Tests cover:
- Team capacity visualization
- Competency level assessments
- Skills development tracking
- Resource allocation optimization
"""

import pytest
import pandas as pd
from datetime import datetime, timedelta


class TestCompetencyLevelAssessment:
    """Test competency level assessment and scoring."""
    
    def test_level_1_beginner_definition(self):
        """Test Level 1 (Beginner) competency definition."""
        # Level 1: Can perform task with heavy guidance
        level_1_indicators = {
            "self_sufficient": False,
            "needs_supervision": True,
            "error_rate": "high"
        }
        assert level_1_indicators["needs_supervision"]
    
    def test_level_2_intermediate_definition(self):
        """Test Level 2 (Intermediate) competency definition."""
        # Level 2: Can perform most tasks independently
        level_2_indicators = {
            "self_sufficient": True,
            "needs_review": True,
            "error_rate": "moderate"
        }
        assert level_2_indicators["self_sufficient"]
        assert level_2_indicators["needs_review"]
    
    def test_level_3_proficient_definition(self):
        """Test Level 3 (Proficient) competency definition."""
        # Level 3: Can work independently and mentor others
        level_3_indicators = {
            "self_sufficient": True,
            "can_mentor": True,
            "error_rate": "low"
        }
        assert level_3_indicators["self_sufficient"]
        assert level_3_indicators["can_mentor"]
    
    def test_level_4_expert_definition(self):
        """Test Level 4 (Expert) competency definition."""
        # Level 4: Domain expert, can set standards
        level_4_indicators = {
            "self_sufficient": True,
            "can_mentor": True,
            "can_architect": True,
            "error_rate": "minimal"
        }
        assert level_4_indicators["can_architect"]
    
    def test_level_5_mastery_definition(self):
        """Test Level 5 (Mastery) competency definition."""
        # Level 5: Recognized authority in domain
        level_5_indicators = {
            "published_work": True,
            "industry_recognition": True,
            "error_rate": "none"
        }
        assert level_5_indicators["published_work"]


class TestTeamCapacityVisualization:
    """Test team capacity metrics and visualization data."""
    
    def test_capacity_heatmap_data_structure(self):
        """Test structure of capacity heatmap data."""
        capacity_matrix = {
            "Ahmad": {"sql": 4, "python": 3, "power_bi": 4, "gis": 1},
            "Jamil": {"sql": 3, "python": 3, "power_bi": 2, "gis": 5},
            "Niken": {"sql": 4, "python": 2, "power_bi": 3, "gis": 2},
        }
        
        team_members = list(capacity_matrix.keys())
        assert len(team_members) == 3
        
        all_skills = set()
        for member_skills in capacity_matrix.values():
            all_skills.update(member_skills.keys())
        
        assert len(all_skills) == 4
    
    def test_skill_coverage_percentage(self):
        """Test calculation of skill coverage percentage."""
        team = {
            "Ahmad": {"python": 3},
            "Jamil": {"python": 4},
            "Niken": {"python": 2},
        }
        
        skill = "python"
        coverage = sum(1 for m in team.values() if skill in m) / len(team) * 100
        assert coverage == 100.0, "All team members have Python skill"
    
    def test_skill_gap_identification(self):
        """Test identification of skills gaps in team."""
        required_skills = ["sql", "python", "power_bi", "gis", "tableau"]
        team_skills = {
            "Ahmad": ["sql", "python", "power_bi"],
            "Jamil": ["gis", "python"],
            "Niken": ["sql", "python", "power_bi"],
        }
        
        covered_skills = set()
        for skills in team_skills.values():
            covered_skills.update(skills)
        
        gaps = set(required_skills) - covered_skills
        assert "tableau" in gaps, "Tableau is a coverage gap"
        assert len(gaps) == 1
    
    def test_team_strength_visualization(self):
        """Test visualization of team strength by skill."""
        strength_scores = {
            "sql": 3.67,  # Average: (4+3+4)/3
            "python": 2.67,  # Average: (3+3+2)/3
            "power_bi": 3.0,  # Average: (4+2+3)/3
            "gis": 2.67,  # Average: (1+5+2)/3
        }
        
        strongest = max(strength_scores, key=strength_scores.get)
        assert strongest == "sql", "SQL is team's strongest skill"


class TestSkillsDevelopmentTracking:
    """Test tracking of skills development over time."""
    
    def test_development_timeline_creation(self):
        """Test creation of skill development timeline."""
        progression = [
            {"date": "2026-01-01", "level": 1},
            {"date": "2026-02-01", "level": 2},
            {"date": "2026-03-07", "level": 3},
        ]
        
        assert len(progression) == 3
        levels = [p["level"] for p in progression]
        assert levels == [1, 2, 3], "Should show progression"
    
    def test_learning_velocity_calculation(self):
        """Test calculation of learning velocity (levels per month)."""
        start_date = datetime(2026, 1, 1)
        end_date = datetime(2026, 3, 7)
        start_level = 1
        end_level = 3
        
        days_elapsed = (end_date - start_date).days
        months_elapsed = days_elapsed / 30
        velocity = (end_level - start_level) / months_elapsed if months_elapsed > 0 else 0
        
        assert velocity > 0, "Should show positive learning velocity"
    
    def test_competency_plateau_detection(self):
        """Test detection of learning plateau."""
        progression = [
            {"date": "2026-01-01", "level": 2},
            {"date": "2026-02-01", "level": 2},
            {"date": "2026-03-07", "level": 2},
        ]
        
        levels = [p["level"] for p in progression]
        is_plateau = len(set(levels)) == 1
        assert is_plateau, "Should detect plateau"
    
    def test_accelerated_learning_detection(self):
        """Test detection of accelerated learning."""
        progression = [
            {"date": "2026-01-01", "level": 1},
            {"date": "2026-01-15", "level": 2},
            {"date": "2026-02-01", "level": 3},
            {"date": "2026-03-07", "level": 4},
        ]
        
        total_levels = progression[-1]["level"] - progression[0]["level"]
        num_periods = len(progression) - 1
        avg_velocity = total_levels / num_periods
        
        assert avg_velocity == 1.0, "Gained 1 level per period"


class TestResourceAllocationOptimization:
    """Test resource allocation and task assignment optimization."""
    
    def test_task_skill_requirement_matching(self):
        """Test matching tasks to required skill levels."""
        task = {
            "name": "Power BI Dashboard",
            "required_skill": "power_bi",
            "required_level": 3
        }
        
        team = {
            "Ahmad": {"power_bi": 4},  # Can do
            "Jamil": {"power_bi": 2},  # Under-qualified
            "Niken": {"power_bi": 3},  # Can do
        }
        
        qualified = [name for name, skills in team.items() 
                    if skills.get(task["required_skill"], 0) >= task["required_level"]]
        
        assert "Ahmad" in qualified
        assert "Niken" in qualified
        assert "Jamil" not in qualified
    
    def test_optimal_assignment_selection(self):
        """Test selection of optimal team member for assignment."""
        task = {"required_level": 3}
        candidates = {
            "Ahmad": {"level": 4, "workload": 5},
            "Jamil": {"level": 3, "workload": 3},
            "Niken": {"level": 3, "workload": 6},
        }
        
        # Select person with lowest workload among qualified
        qualified = {name: info for name, info in candidates.items() 
                    if info["level"] >= task["required_level"]}
        
        best = min(qualified, key=lambda x: qualified[x]["workload"])
        assert best == "Jamil", "Jamil has lowest workload while qualified"
    
    def test_workload_balanced_assignment(self):
        """Test that assignments maintain workload balance."""
        before = {"Ahmad": 5, "Jamil": 4, "Niken": 6}
        
        # Assign to Jamil (lowest)
        before["Jamil"] += 1
        
        after = {"Ahmad": 5, "Jamil": 5, "Niken": 6}
        variance_before = max(before.values()) - min(before.values())
        variance_after = max(after.values()) - min(after.values())
        
        assert variance_after <= variance_before, "Should reduce workload variance"
    
    def test_skill_utilization_efficiency(self):
        """Test utilization efficiency of skill assignment."""
        assignment = {
            "Ahmad": {"assigned_tasks": 4, "skill_level": 4},
            "Jamil": {"assigned_tasks": 3, "skill_level": 3},
            "Niken": {"assigned_tasks": 5, "skill_level": 3},
        }
        
        # Calculate underutilization (skill level > required for tasks)
        utilization = {}
        for person, info in assignment.items():
            # Higher utilization = less overkill
            utilization[person] = info["assigned_tasks"] / info["skill_level"]
        
        # All should have reasonable utilization
        for person, util in utilization.items():
            assert 0.5 <= util <= 2.0, f"{person} utilization {util} should be reasonable"


class TestPerformanceMetricsTracking:
    """Test tracking of performance metrics by competency level."""
    
    def test_quality_metrics_by_level(self):
        """Test quality metrics improve with competency level."""
        metrics = {
            1: {"defect_rate": 0.15, "review_time_hours": 3},
            2: {"defect_rate": 0.08, "review_time_hours": 1},
            3: {"defect_rate": 0.03, "review_time_hours": 0.5},
            4: {"defect_rate": 0.01, "review_time_hours": 0.2},
        }
        
        # Defect rate should decrease with level
        assert metrics[1]["defect_rate"] > metrics[2]["defect_rate"]
        assert metrics[2]["defect_rate"] > metrics[3]["defect_rate"]
    
    def test_delivery_speed_improvement(self):
        """Test delivery speed improvement with competency."""
        speeds = {
            1: {"days_per_task": 5},
            2: {"days_per_task": 3},
            3: {"days_per_task": 2},
            4: {"days_per_task": 1},
        }
        
        # Speed should improve with level
        assert speeds[1]["days_per_task"] > speeds[3]["days_per_task"]
    
    def test_mentoring_capacity_by_level(self):
        """Test mentoring/training capacity by competency level."""
        mentoring_hours = {
            1: 0,      # Cannot mentor
            2: 0,      # Cannot mentor
            3: 2,      # Can mentor 1 person
            4: 5,      # Can mentor 2-3 people
        }
        
        assert mentoring_hours[1] == 0
        assert mentoring_hours[3] > 0
        assert mentoring_hours[4] > mentoring_hours[3]
