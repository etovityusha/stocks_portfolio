from fastapi import APIRouter, Depends, Body, HTTPException
from starlette import status

from services.currency import CurrencyService
from services.unit_of_work import AbstractUnitOfWork
from .reponses import (
    CurrenciesListingResponse,
    CurrencyDetailsResponse,
    CreateCurrencyRequest,
    UpdateCurrencyRequest,
)

router = APIRouter(prefix="/currencies", dependencies=[], tags=["currencies"])


@router.get("", response_model=CurrenciesListingResponse)
async def currencies_list(UOF: AbstractUnitOfWork = Depends()):
    qs = CurrencyService(UOF).listing()
    return CurrenciesListingResponse(currencies=[CurrencyDetailsResponse.parse_obj(x) for x in qs])


@router.get("/{_id}", response_model=CurrencyDetailsResponse)
async def currency_detail(
    _id: int,
    UOF: AbstractUnitOfWork = Depends(),
):
    currency = CurrencyService(UOF).get_by_id(_id)
    if currency is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Currency not found")
    return CurrencyDetailsResponse.parse_obj(currency)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_currency(
    body: CreateCurrencyRequest = Body(...),
    UOF: AbstractUnitOfWork = Depends(),
):
    CurrencyService(UOF).create(code=body.code, name=body.name)


@router.patch("/{_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_currency(
    _id: int,
    body: UpdateCurrencyRequest = Body(...),
    UOF: AbstractUnitOfWork = Depends(),
):
    updated: int = CurrencyService(UOF).update(_id=_id, code=body.code, name=body.name)
    if updated == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Currency not found")
