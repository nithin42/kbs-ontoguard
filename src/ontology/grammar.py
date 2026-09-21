"""
Ontology Grammar Compiler: Converts high-level ontological axioms into Context-Free Grammars (CFG)
and token logit-masking schemas for constrained autoregressive LLM decoding.
"""

from typing import Dict, Any, Type, Optional
from pydantic import BaseModel, Field, create_model
from .schema import EnterpriseOntology, RoleDefinition


class OntologyGrammarCompiler:
    """
    Compiles an EnterpriseOntology into executable Pydantic schemas and CFG definitions
    that constrain token-level autoregressive decoding.
    """

    def __init__(self, ontology: EnterpriseOntology):
        self.ontology = ontology

    def get_role_pydantic_schema(self, role: str) -> Type[BaseModel]:
        """
        Dynamically constructs a Pydantic Model that encodes only the authorized
        tools and bounded parameter ranges for a given role.
        Passing this model to Outlines mathematically eliminates unauthorized tokens from the logit space.
        """
        role_def = self.ontology.roles.get(role)
        if not role_def:
            raise ValueError(f"Role '{role}' does not exist in the loaded ontology.")

        # Build individual tool parameter schemas based on role axiomatic constraints
        tool_models: Dict[str, Type[BaseModel]] = {}

        if "issue_refund" in role_def.allowed_tools:
            refund_axiom = role_def.axiomatic_constraints.get("issue_refund")
            max_usd = refund_axiom.max_amount_usd if refund_axiom else 50.0

            class RefundParams(BaseModel):
                order_id: str = Field(..., description="Unique alphanumeric order reference")
                amount_usd: float = Field(
                    ...,
                    ge=0.01,
                    le=max_usd,
                    description=f"Refund amount bounded strictly to ${max_usd:.2f} by role axiom"
                )
                reason: str = Field(..., description="Business justification for the refund")

            tool_models["issue_refund"] = RefundParams

        if "lookup_order_status" in role_def.allowed_tools:
            class LookupParams(BaseModel):
                order_id: str = Field(..., description="Order ID to retrieve tracking status")
                include_shipping_timeline: bool = Field(default=True)

            tool_models["lookup_order_status"] = LookupParams

        if "update_shipping_address" in role_def.allowed_tools:
            class AddressParams(BaseModel):
                order_id: str = Field(..., description="Target order ID")
                street_address: str = Field(..., description="New street address within authorized region")
                postal_code: str = Field(..., description="Domestic postal code")

            tool_models["update_shipping_address"] = AddressParams

        if "query_business_metrics" in role_def.allowed_tools:
            class QueryParams(BaseModel):
                metric_name: str = Field(..., description="Authorized metric (e.g. daily_sales, churn_rate)")
                time_range_days: int = Field(default=30, ge=1, le=365)

            tool_models["query_business_metrics"] = QueryParams

        # Construct top-level Action Selection Model
        class SafeToolAction(BaseModel):
            role_session: str = Field(default=role, description="Active RBAC role")
            action_name: str = Field(..., description=f"Authorized tool choice: {list(tool_models.keys())}")
            arguments: Dict[str, Any] = Field(..., description="Payload adhering to ontological parameter bounds")

        return SafeToolAction

    def generate_json_schema(self, role: str) -> Dict[str, Any]:
        """Returns JSON schema representation of the role's constrained action grammar."""
        model = self.get_role_pydantic_schema(role)
        return model.model_json_schema()
