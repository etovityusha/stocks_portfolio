from fastapi import APIRouter, Depends, Body
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from repo.currency import CurrencyRepo, CurrencyObj
from .reponses import (
    CurrenciesListingResponse,
    CurrencyDetailsResponse,
    CreateCurrencyRequest,
    CreateCurrencyResponse,
)

router = APIRouter(prefix="/currencies", dependencies=[], tags=["currencies"])


@router.get("", response_model=CurrenciesListingResponse)
async def currencies_list(session: Session = Depends(get_db)):
    qs: list[CurrencyObj] = CurrencyRepo(session).find()
    return CurrenciesListingResponse(currencies=[CurrencyDetailsResponse.parse_obj(x) for x in qs])


@router.get("/{_id}", response_model=CurrencyDetailsResponse)
async def currency_detail(
    _id: int,
    session: Session = Depends(get_db),
):
    obj: CurrencyObj = CurrencyRepo(session).get_by_id(_id=_id)
    return CurrencyDetailsResponse.parse_obj(obj)


@router.post("", status_code=status.HTTP_201_CREATED, response_model=CreateCurrencyResponse)
async def create_currency(
    body: CreateCurrencyRequest = Body(...),
    session: Session = Depends(get_db),
):
    obj: CurrencyObj = CurrencyRepo(session).create_new(
        code=body.code,
        name=body.name,
    )
    return CreateCurrencyResponse.parse_obj(obj)
