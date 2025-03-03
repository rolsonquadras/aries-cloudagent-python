"""Aries#0037 v1.0 presentation exchange information with non-secrets storage."""

from marshmallow import fields
from marshmallow.validate import OneOf

from ....models.base_record import BaseRecord, BaseRecordSchema
from ....valid import UUIDFour


class V10PresentationExchange(BaseRecord):
    """Represents an Aries#0037 v1.0 presentation exchange."""

    class Meta:
        """V10PresentationExchange metadata."""

        schema_class = "V10PresentationExchangeSchema"

    RECORD_TYPE = "presentation_exchange_v10"
    RECORD_ID_NAME = "presentation_exchange_id"
    WEBHOOK_TOPIC = "present_proof"

    INITIATOR_SELF = "self"
    INITIATOR_EXTERNAL = "external"

    ROLE_PROVER = 'prover'
    ROLE_VERIFIER = 'verifier'

    STATE_PROPOSAL_SENT = "proposal_sent"
    STATE_PROPOSAL_RECEIVED = "proposal_received"
    STATE_REQUEST_SENT = "request_sent"
    STATE_REQUEST_RECEIVED = "request_received"
    STATE_PRESENTATION_SENT = "presentation_sent"
    STATE_PRESENTATION_RECEIVED = "presentation_received"
    STATE_VERIFIED = "verified"

    def __init__(
        self,
        *,
        presentation_exchange_id: str = None,
        connection_id: str = None,
        thread_id: str = None,
        initiator: str = None,
        role: str = None,
        state: str = None,
        presentation_proposal_dict: dict = None,  # serialized pres proposal message
        presentation_request: dict = None,  # indy proof req
        presentation: dict = None,  # indy proof
        verified: str = None,
        auto_present: bool = False,
        error_msg: str = None,
        **kwargs
    ):
        """Initialize a new PresentationExchange."""
        super().__init__(presentation_exchange_id, state, **kwargs)
        self.connection_id = connection_id
        self.thread_id = thread_id
        self.initiator = initiator
        self.role = role
        self.state = state
        self.presentation_proposal_dict = presentation_proposal_dict
        self.presentation_request = presentation_request  # indy proof req
        self.presentation = presentation  # indy proof
        self.verified = verified
        self.auto_present = auto_present
        self.error_msg = error_msg

    @property
    def presentation_exchange_id(self) -> str:
        """Accessor for the ID associated with this exchange."""
        return self._id

    @property
    def record_value(self) -> dict:
        """Accessor for JSON record value generated for this presentation exchange."""
        result = self.tags
        for prop in (
            "presentation_proposal_dict",
            "presentation_request",
            "presentation",
            "auto_present",
            "error_msg",
        ):
            val = getattr(self, prop)
            if val:
                result[prop] = val
        return result

    @property
    def record_tags(self) -> dict:
        """Accessor for the record tags generated for this presentation exchange."""
        result = {}
        for prop in (
                "connection_id",
                "thread_id",
                "initiator",
                "role",
                "state",
                "verified"):
            val = getattr(self, prop)
            if val:
                result[prop] = val
        return result


class V10PresentationExchangeSchema(BaseRecordSchema):
    """Schema for de/serialization of v1.0 presentation exchange records."""

    class Meta:
        """V10PresentationExchangeSchema metadata."""

        model_class = V10PresentationExchange

    presentation_exchange_id = fields.Str(
        required=False,
        description="Presentation exchange identifier",
        example=UUIDFour.EXAMPLE,  # typically a UUID4 but not necessarily
    )
    connection_id = fields.Str(
        required=False,
        description="Connection identifier",
        example=UUIDFour.EXAMPLE,  # typically a UUID4 but not necessarily
    )
    thread_id = fields.Str(
        required=False,
        description="Thread identifier",
        example=UUIDFour.EXAMPLE,  # typically a UUID4 but not necessarily
    )
    initiator = fields.Str(
        required=False,
        description="Present-proof exchange initiator: self or external",
        example=V10PresentationExchange.INITIATOR_SELF,
        validate=OneOf(["self", "external"]),
    )
    role = fields.Str(
        required=False,
        description="Present-proof exchange role: prover or verifier",
        example=V10PresentationExchange.ROLE_PROVER,
        validate=OneOf(["prover", "verifier"]),
    )
    state = fields.Str(
        required=False,
        description="Present-proof exchange state",
        example=V10PresentationExchange.STATE_VERIFIED,
    )
    presentation_proposal_dict = fields.Dict(
        required=False,
        description="Serialized presentation proposal message",
    )
    presentation_request = fields.Dict(
        required=False,
        description="(Indy) presentation request (also known as proof request)",
    )
    presentation = fields.Dict(
        required=False,
        description="(Indy) presentation (also known as proof)"
    )
    verified = fields.Str(  # tag: must be a string
        required=False,
        description="Whether presentation is verified: true or false",
        example="true",
        validate=OneOf(["true", "false"]),
    )
    auto_present = fields.Bool(
        required=False,
        description="Prover choice to auto-present proof as verifier requests",
        example=False,
    )
    error_msg = fields.Str(
        required=False,
        description="Error message",
        example="Invalid structure"
    )
