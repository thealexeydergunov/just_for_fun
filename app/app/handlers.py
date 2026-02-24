from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import ORJSONResponse

from app.exceptions import CustomValidationError, DBNotFoundError


def setup_handlers(app: FastAPI) -> FastAPI:
    @app.exception_handler(DBNotFoundError)
    async def service_exception_handler(request: Request, exc: DBNotFoundError) -> ORJSONResponse:  # noqa: ARG001
        return ORJSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"message": f"Object {exc.name} with id={exc._id} does not exists"},
        )

    @app.exception_handler(RequestValidationError)
    async def request_validation_handler(request: Request, exc: RequestValidationError) -> ORJSONResponse:  # noqa: ARG001
        errors = [
            {"field": ".".join(map(str, error["loc"][1:])), "message": error["msg"], "type": error["type"]}
            for error in exc.errors()
        ]

        return ORJSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"status": "error", "message": "Validation Error", "details": errors},
        )

    @app.exception_handler(CustomValidationError)
    async def custom_validation_handler(request: Request, exc: CustomValidationError) -> ORJSONResponse:  # noqa: ARG001
        return ORJSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"message": exc.msg},
        )

    return app
