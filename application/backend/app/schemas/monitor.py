from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class MonitorCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    url: str = Field(min_length=1, max_length=500)
    interval_seconds: int = Field(default=60, ge=10)
    is_active: bool = True


class MonitorUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    url: str | None = Field(default=None, min_length=1, max_length=500)
    interval_seconds: int | None = Field(default=None, ge=10)
    is_active: bool | None = None


class MonitorResponse(BaseModel):
    id: int
    name: str
    url: str
    interval_seconds: int
    is_active: bool

    current_status: str
    last_http_status: int | None
    last_response_time_ms: int | None
    last_checked_at: datetime | None

    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
