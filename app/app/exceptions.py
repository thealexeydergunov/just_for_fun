class BaseAppError(Exception): ...


class DBNotFoundError(BaseAppError):
    def __init__(self, name: str, _id: int) -> None:
        self.name = name
        self._id = _id


class OrganisationNotFoundError(DBNotFoundError): ...
