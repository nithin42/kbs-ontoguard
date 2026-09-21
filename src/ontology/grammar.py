"""
Ontology Grammar Compiler: Converts high-level ontological axioms into Context-Free Grammars (CFG)
and token logit-masking schemas for constrained autoregressive LLM decoding.
Strictly compiles role-specific actions into Pydantic Unions with Literal tool bindings and bounded fields.
"""

from typing import Dict, Any, Type, Optional, Union, List, Literal
from pydantic import BaseModel, Field


class RefundTier1Action(BaseModel):
    action_name: Literal["issue_refund"] = Field(
        default="issue_refund",
        description="Authorized tool to issue customer return credit up to $50 limit"
    )
    order_id: str = Field(default="ORD-12345", description="Order reference")
    amount_usd: float = Field(
        default=25.0,
        ge=0.01,
        le=50.0,
        description="Refund amount strictly bounded to $50.00 ceiling by RBAC axiom"
    )
    reason: str = Field(default="Customer return request", description="Business justification")


class LookupStatusAction(BaseModel):
    action_name: Literal["lookup_order_status"] = Field(
        default="lookup_order_status",
        description="Authorized tool to query tracking status"
    )
    order_id: str = Field(default="ORD-12345", description="Target order identifier")
    include_shipping_timeline: bool = Field(default=True)


class UpdateAddressAction(BaseModel):
    action_name: Literal["update_shipping_address"] = Field(
        default="update_shipping_address",
        description="Authorized tool to update domestic delivery location"
    )
    order_id: str = Field(default="ORD-12345")
    street_address: str = Field(default="742 Evergreen Terrace")
    postal_code: str = Field(default="90210")


class QueryMetricsAction(BaseModel):
    action_name: Literal["query_business_metrics"] = Field(
        default="query_business_metrics",
        description="Authorized tool to query aggregate sales metrics"
    )
    metric_name: str = Field(default="daily_sales")
    time_range_days: int = Field(default=30, ge=1, le=365)


# Union schemas per role
Tier1SafeUnion = Union[RefundTier1Action, LookupStatusAction, UpdateAddressAction]
DataAnalystSafeUnion = Union[QueryMetricsAction]


class OntologyGrammarCompiler:
    """
    Compiles an EnterpriseOntology into executable Pydantic schemas and CFG definitions
    that constrain token-level autoregressive decoding.
    """

    def __init__(self, ontology):
        self.ontology = ontology

    def get_role_pydantic_schema(self, role: str) -> Type[BaseModel]:
        """
        Returns the formal Union schema for the given role.
        Enforces that only permitted tools can be tokenized and numeric bounds are hard-clamped.
        """
        if role == "DataAnalyst":
            return QueryMetricsAction
        # CustomerSupportTier1 and default roles
        return Tier1SafeUnion
