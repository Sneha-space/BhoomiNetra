"""Request/response shapes for the record routes.

These describe JSON going in and out over HTTP. The database shape lives in
src/models/ and is allowed to differ.
"""

from pydantic import BaseModel


class FieldCorrection(BaseModel):
    """One value a reviewer typed on the correction screen."""

    field_id: int
    corrected_value: str


class VerifyRequest(BaseModel):
    """Body of POST /records/{record_id}/verify.

    An object wrapping the list rather than a bare list, so extra keys can be
    added later without breaking callers.
    """

    corrections: list[FieldCorrection]
