from pydantic import BaseModel


class CurrencyDetailsResponse(BaseModel):
    id: int
    code: str
    name: str

    class Config:
        orm_mode = True


class CurrenciesListingResponse(BaseModel):
    currencies: list[CurrencyDetailsResponse]


class CreateCurrencyRequest(BaseModel):
    code: str
    name: str


class CreateCurrencyResponse(BaseModel):
    id: int
