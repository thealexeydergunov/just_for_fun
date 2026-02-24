class BaseAppError(Exception): ...


class DBNotFoundError(BaseAppError):
    def __init__(self, name: str, _id: int) -> None:
        self.name = name
        self._id = _id


class OrganisationNotFoundError(DBNotFoundError): ...


class CustomValidationError(BaseAppError):
    def __init__(self, msg: str) -> None:
        self.msg = msg
