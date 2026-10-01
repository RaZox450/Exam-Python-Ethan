from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

Status = Literal["open", "closed", "maintenance"]


class StationCreate(BaseModel):
    """Données d'une station en entrée (sans id)."""

    model_config = ConfigDict(str_strip_whitespace=True)

    code: str = Field(min_length=1)
    name: str = Field(min_length=1)
    capacity: int = Field(ge=1)
    status: Status = "open"


class StationUpdate(BaseModel):
    """Seuls name et status sont modifiables ; tout autre champ est refusé (422)."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="forbid")

    name: str | None = Field(default=None, min_length=1)
    status: Status | None = None

    @field_validator("name", "status", mode="before")
    @classmethod
    def no_explicit_null(cls, v):
        if v is None:
            raise ValueError("ne peut pas être null")
        return v


class StationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    code: str
    name: str
    capacity: int
    status: Status
