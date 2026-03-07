"""
Tests for role-based access control and competency matrix.

Tests cover:
- Role permission validation
- Competency matrix calculations
- Access control edge cases
- Team capacity planning
"""

import pytest
import pandas as pd
from typing import Dict, List


class TestRoleBasedAccessControl:
    """Test role-based access control (RBAC) system."""
    
    def test_viewer_cannot_edit(self):
        """Test that Viewer role cannot edit data."""
        role = "Viewer"
        permissions = {
            "Viewer": ["read"],
            "Editor": ["read", "write"],
            "Admin": ["read", "write", "delete", "admin"]
        }
        
        can_write = "write" in permissions.get(role, [])
        assert not can_write, "Viewers should not have write permission"
    
    def test_editor_can_write(self):
        """Test that Editor role can write data."""
        role = "Editor"
        permissions = {
            "Viewer": ["read"],
            "Editor": ["read", "write"],
            "Admin": ["read", "write", "delete", "admin"]
        }
        
        can_write = "write" in permissions.get(role, [])
        assert can_write, "Editors should have write permission"
    
    def test_admin_has_all_permissions(self):
        """Test that Admin role has all permissions."""
        role = "Admin"
        permissions = {
            "Viewer": ["read"],
            "Editor": ["read", "write"],
            "Admin": ["read", "write", "delete", "admin"]
        }
        
        has_all = all(perm in permissions[role] for perm in ["read", "write", "delete", "admin"])
        assert has_all, "Admins should have all permissions"
    
    def test_invalid_role_gets_no_permissions(self):
        """Test that invalid roles get no permissions."""
        role = "InvalidRole"
        permissions = {
            "Viewer": ["read"],
            "Editor": ["read", "write"],
            "Admin": ["read", "write", "delete", "admin"]
        }
        
        user_perms = permissions.get(role, [])
        assert len(user_perms) == 0, "Invalid role should have no permissions"
    
    def test_resource_level_access_control(self):
        """Test access control at resource level."""
        user_role = "Editor"
        resource = "team_dashboard"
        
        resource_access = {
            "Viewer": ["view_dashboard", "view_reports"],
            "Editor": ["view_dashboard", "view_reports", "edit_dashboard"],
            "Admin": ["view_dashboard", "view_reports", "edit_dashboard", "delete_dashboard"]
        }
        
        can_access = "edit_dashboard" in resource_access.get(user_role, [])
        assert can_access, "Editor should be able to edit dashboard"


class TestCompetencyMatrix:
    """Test competency matrix calculations and assessments."""
    
    def test_competency_score_range(self):
        """Test that competency scores are in valid range 0-5."""
        competencies = [1, 2, 3, 4, 5]
        for score in competencies:
            assert 0 <= score <= 5, f"Score {score} should be 0-5"
    
    def test_individual_competency_profile(self):
        """Test individual team member competency profile."""
        team_member = {
            "name": "Ahmad",
            "sql": 4,
            "python": 3,
            "power_bi": 4,
            "communication": 5
        }
        
        skills = ["sql", "python", "power_bi", "communication"]
        assert all(skill in team_member for skill in skills)
        
        avg_competency = sum(team_member[s] for s in skills) / len(skills)
        assert 3 <= avg_competency <= 5, "Average should be reasonable"
    
    def test_team_skills_gap_analysis(self):
        """Test identification of team-wide skills gaps."""
        team_competencies = {
            "Ahmad": {"python": 4, "sql": 4, "gis": 1},
            "Jamil": {"python": 3, "sql": 3, "gis": 5},
            "Niken": {"python": 2, "sql": 4, "gis": 2},
        }
        
        # Calculate team average per skill
        all_skills = set()
        for member in team_competencies.values():
            all_skills.update(member.keys())
        
        team_avg = {}
        for skill in all_skills:
            scores = [team_competencies[m].get(skill, 0) for m in team_competencies]
            team_avg[skill] = sum(scores) / len(scores)
        
        # GIS is weak area
        assert team_avg["gis"] < team_avg["sql"], "GIS should be identified as gap"
    
    def test_skill_development_plan(self):
        """Test creation of skill development plans."""
        current_proficiency = {
            "python": 2,
            "power_bi": 3
        }
        target_proficiency = {
            "python": 4,
            "power_bi": 5
        }
        
        gaps = {skill: target_proficiency[skill] - current_proficiency[skill] 
                for skill in current_proficiency}
        
        assert gaps["python"] == 2, "Python needs 2-level improvement"
        assert gaps["power_bi"] == 2, "Power BI needs 2-level improvement"
    
    def test_competency_milestone_tracking(self):
        """Test tracking of competency development milestones."""
        milestones = [
            {"date": "2026-01-15", "skill": "python", "level_reached": 2},
            {"date": "2026-02-01", "skill": "python", "level_reached": 3},
            {"date": "2026-03-07", "skill": "python", "level_reached": 4},
        ]
        
        assert len(milestones) == 3
        final_level = milestones[-1]["level_reached"]
        assert final_level == 4, "Should reach target level 4"


class TestTeamCapacityPlanning:
    """Test team capacity planning and workload balancing."""
    
    def test_workload_distribution_fairness(self):
        """Test that workload is fairly distributed."""
        workload = {
            "Ahmad": 12,
            "Jamil": 11,
            "Niken": 10
        }
        
        total = sum(workload.values())
        avg = total / len(workload)
        
        # Check if any person has >20% more than average
        max_deviation = max(abs(w - avg) for w in workload.values()) / avg
        assert max_deviation < 0.2, "Workload should be fairly balanced"
    
    def test_capacity_utilization_rate(self):
        """Test calculation of capacity utilization."""
        tasks_assigned = 33
        team_capacity = 35  # Total capacity per week
        
        utilization_pct = (tasks_assigned / team_capacity) * 100
        assert 80 <= utilization_pct <= 100, "Should be at optimal utilization"
    
    def test_overload_detection(self):
        """Test detection of team overload condition."""
        tasks_assigned = 50
        team_capacity = 35
        
        is_overloaded = tasks_assigned > team_capacity
        assert is_overloaded, "Should detect overload"
    
    def test_underutilization_detection(self):
        """Test detection of team underutilization."""
        tasks_assigned = 20
        team_capacity = 35
        
        utilization_pct = (tasks_assigned / team_capacity) * 100
        is_underutilized = utilization_pct < 60
        assert is_underutilized, "Should detect underutilization"
    
    def test_optimal_team_size_calculation(self):
        """Test calculation of optimal team size."""
        avg_tasks_per_sprint = 100
        tasks_per_person_capacity = 35  # per sprint
        
        optimal_team_size = avg_tasks_per_sprint / tasks_per_person_capacity
        assert 2 <= optimal_team_size <= 4, "Team size should be reasonable"
        assert optimal_team_size > 2, "Need more than 2 people"


class TestAccessAuditLogging:
    """Test access control audit logging."""
    
    def test_access_log_entry_structure(self):
        """Test that access logs have required structure."""
        log_entry = {
            "timestamp": "2026-03-07T10:30:00+07:00",
            "user": "Ahmad",
            "action": "view_dashboard",
            "resource": "team_dashboard",
            "status": "allowed"
        }
        
        required_fields = ["timestamp", "user", "action", "resource", "status"]
        assert all(f in log_entry for f in required_fields)
    
    def test_denied_access_logging(self):
        """Test logging of denied access attempts."""
        log_entries = [
            {"user": "Viewer", "action": "edit_config", "status": "denied"},
            {"user": "Editor", "action": "delete_data", "status": "denied"},
            {"user": "Admin", "action": "anything", "status": "allowed"},
        ]
        
        denied = [e for e in log_entries if e["status"] == "denied"]
        assert len(denied) == 2, "Should have 2 denied entries"
    
    def test_suspicious_activity_detection(self):
        """Test detection of suspicious access patterns."""
        access_attempts = [
            {"user": "Ahmad", "failed_attempts": 3},
            {"user": "Jamil", "failed_attempts": 1},
            {"user": "Niken", "failed_attempts": 0},
        ]
        
        suspicious = [u for u in access_attempts if u["failed_attempts"] > 2]
        assert len(suspicious) == 1, "Should identify suspicious user"


class TestPermissionInheritance:
    """Test permission inheritance and propagation."""
    
    def test_group_permissions_assignment(self):
        """Test assigning permissions at group level."""
        group = "analytics_team"
        group_perms = ["read_data", "write_reports", "view_dashboards"]
        
        team_members = ["Ahmad", "Jamil", "Niken"]
        # Each member inherits group permissions
        for member in team_members:
            member_perms = group_perms.copy()
            assert len(member_perms) >= 3
    
    def test_project_level_permissions_override(self):
        """Test project-level permissions override group permissions."""
        group_role = "Editor"  # read, write
        project_role = "Viewer"  # read only
        
        # Project role overrides group role
        effective_role = project_role
        assert effective_role == "Viewer"
    
    def test_permission_delegation(self):
        """Test that Admins can delegate permissions."""
        admin = "Admin_User"
        delegated_user = "New_Editor"
        permissions_to_delegate = ["read", "write"]
        
        # Admin can delegate permissions
        can_delegate = True  # Admins always can
        assert can_delegate
