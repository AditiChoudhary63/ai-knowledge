from pydantic import BaseModel, Field


class Config(BaseModel):
    base_dir: str | None = Field(
        default=None, description="Base directory for all operations"
    )


config = Config()