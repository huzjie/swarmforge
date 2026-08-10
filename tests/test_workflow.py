"""Tests for workflow engine."""
import pytest
from swarmforge.core.workflow import WorkflowDefinition, WorkflowStep, WorkflowEngine, StepStatus

class TestWorkflowStep:
    def test_step_creation(self):
        step = WorkflowStep(name="step1", agent_name="agent1", task_template="Do {task}")
        assert step.name == "step1"
        assert step.status == StepStatus.PENDING

    def test_step_dependencies(self):
        step = WorkflowStep(name="step2", agent_name="agent1", task_template="Process {result}", depends_on=["step1"])
        assert "step1" in step.depends_on

class TestWorkflowDefinition:
    def test_workflow_creation(self):
        wf = WorkflowDefinition(name="test-wf", description="Test workflow")
        assert wf.name == "test-wf"

    def test_add_steps(self):
        wf = WorkflowDefinition(name="test-wf")
        wf.steps = [
            WorkflowStep(name="s1", agent_name="a1", task_template="Step 1"),
            WorkflowStep(name="s2", agent_name="a2", task_template="Step 2", depends_on=["s1"]),
        ]
        assert len(wf.steps) == 2
