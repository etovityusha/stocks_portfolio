from fastapi import APIRouter, Depends

from database import get_db
from repo.currency import CurrencyRepo, CurrencyObj
from .reponses import CurrenciesListing, CurrencyListingObj

router = APIRouter(prefix="/currencies", dependencies=[], tags=["currencies"])


@router.get("", response_model=CurrenciesListing)
async def get_currencies_list(session=Depends(get_db)):
    qs: list[CurrencyObj] = CurrencyRepo(session).find()
    return CurrenciesListing(currencies=[CurrencyListingObj.parse_obj(x) for x in qs])
