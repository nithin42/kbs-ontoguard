"""
Formal Pydantic-based Enterprise Least-Privilege Role-Based Access Control (RBAC) Ontology.
Implements axiomatic validation of LLM tool actions against formal security bounds.
"""

from typing import Dict, List, Any, Optional, Tuple
from pydantic import BaseModel, Field, field_validator
import json
from pathlib import Path


class ToolCallAxiom(BaseModel):
    max_amount_usd: Optional[float] = None
    requires_manager_override: Optional[bool] = None
    mask_pii_fields: Optional[List[str]] = None
    allow_international: Optional[bool] = None
    allow_drop_table: Optional[bool] = None
    allow_alter_table: Optional[bool] = None
    max_rows_returned: Optional[int] = None
    prohibited_tables: Optional[List[str]] = None


class RoleDefinition(BaseModel):
    description: str
    allowed_tools: List[str]
    axiomatic_constraints: Dict[str, ToolCallAxiom] = Field(default_factory=dict)


class GlobalAxiom(BaseModel):
    id: str
    rule: str
    description: str


class EnterpriseOntology(BaseModel):
    roles: Dict[str, RoleDefinition]
    global_security_axioms: List[GlobalAxiom] = Field(default_factory=list)

    def is_tool_allowed(self, role: str, tool_name: str) -> bool:
        """Check if a specific tool is authorized under the role definition."""
        role_def = self.roles.get(role)
        if not role_def:
            return False
        return tool_name in role_def.allowed_tools

    def validate_tool_execution(
        self, role: str, tool_name: str, arguments: Dict[str, Any]
    ) -> Tuple[bool, str]:
        """
        Formally validates whether a proposed tool call with specific arguments
        satisfies the ontological axioms of the current user session role.
        """
        role_def = self.roles.get(role)
        if not role_def:
            return False, f"Axiom Violation: Unknown role '{role}'"

        if tool_name not in role_def.allowed_tools:
            return (
                False,
                f"Privilege Escalation: Tool '{tool_name}' is not authorized for role '{role}'."
            )

        constraints = role_def.axiomatic_constraints.get(tool_name)
        if not constraints:
            return True, "Authorized (no parameter constraints)"

        # Check numeric ceiling axioms (e.g., refund caps)
        if constraints.max_amount_usd is not None:
            amount = arguments.get("amount") or arguments.get("amount_usd") or arguments.get("refund_amount")
            if amount is not None:
                try:
                    amount_float = float(amount)
                    if amount_float > constraints.max_amount_usd:
                        return (
                            False,
                            f"Parametric Axiom Violation: Requested amount ${amount_float:.2f} exceeds "
                            f"allowed ceiling of ${constraints.max_amount_usd:.2f} for role '{role}'."
                        )
                except (ValueError, TypeError):
                    return False, "Data Integrity Violation: Non-numeric amount parameter."

        # Check prohibited table query axioms (SQL / BI injection defense)
        if constraints.prohibited_tables:
            query = str(arguments.get("query", "")).lower()
            for prohibited in constraints.prohibited_tables:
                if prohibited.lower() in query:
                    return (
                        False,
                        f"Data Isolation Axiom Violation: Query targets prohibited entity '{prohibited}'."
                    )

        # Check SQL DDL prohibited operations
        if constraints.allow_drop_table is False:
            query = str(arguments.get("query", "")).lower()
            if "drop table" in query or "drop database" in query or "truncate" in query:
                return (
                    False,
                    "Security Invariant Violation: DDL DROP/TRUNCATE prohibited for analytical roles."
                )

        return True, "Action satisfied all ontological axioms"


def load_ontology_from_json(json_path: str) -> EnterpriseOntology:
    """Loads and instantiates the formal ontology from an external JSON specification."""
    path = Path(json_path)
    if not path.exists():
        raise FileNotFoundError(f"Ontology file not found at {json_path}")

    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return EnterpriseOntology(
        roles={k: RoleDefinition(**v) for k, v in data.get("roles", {}).items()},
        global_security_axioms=[GlobalAxiom(**a) for a in data.get("global_security_axioms", [])]
    )
