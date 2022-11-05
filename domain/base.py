from pydantic import BaseModel


class BaseEntity(BaseModel):
    id: int | None

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
