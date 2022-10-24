from pydantic import BaseModel


class CurrencyListingObj(BaseModel):
    id: int
    code: str
    name: str

    class Config:
        orm_mode = True


class CurrenciesListing(BaseModel):
    currencies: list[CurrencyListingObj]
