from repo.currency import CurrencyObj
from services.unit_of_work import AbstractUnitOfWork


class CurrencyService:
    def __init__(
        self,
        uof: AbstractUnitOfWork,
    ):
        self.uof = uof

    def listing(self) -> list[CurrencyObj]:
        with self.uof:
            result = self.uof.currency_repo.find_all()
        return result

    def get_by_id(self, _id: int) -> CurrencyObj | None:
        with self.uof:
            result = self.uof.currency_repo.get_by_id(_id)
        return result

    def create(self, code: str, name: str) -> CurrencyObj:
        with self.uof:
            result = self.uof.currency_repo.create_new(code=code, name=name)
            self.uof.commit()
        return result

    def update(self, _id: int, code: str | None = None, name: str | None = None) -> int:
        with self.uof:
            updated_count = self.uof.currency_repo.update(_id=_id, code=code, name=name)
            self.uof.commit()
        return updated_count
