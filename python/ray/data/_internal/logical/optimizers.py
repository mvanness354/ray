from typing import List

from ray.data._internal.logical.interfaces import (
    LogicalPlan,
    Optimizer,
    PhysicalPlan,
    Rule,
)
from ray.data._internal.logical.rules._user_provided_optimizer_rules import (
    USER_PROVIDED_LOGICAL_RULES,
    USER_PROVIDED_PHYSICAL_RULES,
)
from ray.data._internal.logical.rules.operator_fusion import OperatorFusionRule
from ray.data._internal.logical.rules.randomize_blocks import ReorderRandomizeBlocksRule
from ray.data._internal.planner.planner import Planner

DEFAULT_LOGICAL_RULES = [
    ReorderRandomizeBlocksRule,
]

DEFAULT_PHYSICAL_RULES = [
    OperatorFusionRule,
]


class LogicalOptimizer(Optimizer):
    """The optimizer for logical operators."""

    @property
    def rules(self) -> List[Rule]:
        rules = DEFAULT_LOGICAL_RULES + USER_PROVIDED_LOGICAL_RULES
        return [rule_cls() for rule_cls in rules]


class PhysicalOptimizer(Optimizer):
    """The optimizer for physical operators."""

    @property
    def rules(self) -> List["Rule"]:
        rules = DEFAULT_PHYSICAL_RULES + USER_PROVIDED_PHYSICAL_RULES
        return [rule_cls() for rule_cls in rules]


def get_execution_plan(logical_plan: LogicalPlan) -> PhysicalPlan:
    """Get the physical execution plan for the provided logical plan.

    This process has 3 steps:
    (1) logical optimization: optimize logical operators.
    (2) planning: convert logical to physical operators.
    (3) physical optimization: optimize physical operators.
    """
    optimized_logical_plan = LogicalOptimizer().optimize(logical_plan)
    logical_plan._dag = optimized_logical_plan.dag
    physical_plan = Planner().plan(optimized_logical_plan)
    return PhysicalOptimizer().optimize(physical_plan)
