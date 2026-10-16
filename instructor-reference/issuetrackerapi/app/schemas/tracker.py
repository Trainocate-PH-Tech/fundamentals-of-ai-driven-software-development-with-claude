from enum import StrEnum
from pydantic import BaseModel, ConfigDict, Field, field_validator


class Status(StrEnum):
    open = "open"
    in_progress = "in_progress"
    resolved = "resolved"
    closed = "closed"


class Priority(StrEnum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class TrackerInput(BaseModel):
    model_config = ConfigDict(extra="forbid")

    @field_validator("name", "title", mode="before", check_fields=False)
    @classmethod
    def nonblank(cls, value):
        if not isinstance(value, str) or not value.strip():
            raise ValueError("Must not be blank")
        return value.strip()

    @field_validator("category_id", "status", "priority", mode="before", check_fields=False)
    @classmethod
    def required_when_supplied(cls, value):
        if value is None:
            raise ValueError("Must not be null")
        return value


class CategoryCreate(TrackerInput):
    name: str = Field(max_length=100)
    description: str | None = Field(default=None, max_length=500)


class CategoryUpdate(TrackerInput):
    name: str | None = Field(default=None, max_length=100)
    description: str | None = Field(default=None, max_length=500)


class IssueCreate(TrackerInput):
    title: str = Field(max_length=200)
    description: str | None = Field(default=None, max_length=5000)
    status: Status = Status.open
    priority: Priority = Priority.medium
    category_id: str
    assigned_user_id: str | None = None


class IssueUpdate(TrackerInput):
    title: str | None = Field(default=None, max_length=200)
    description: str | None = Field(default=None, max_length=5000)
    status: Status | None = None
    priority: Priority | None = None
    category_id: str | None = None
    assigned_user_id: str | None = None
