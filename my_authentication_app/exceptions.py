from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = [{"field": err["loc"][-1], "message": err["msg"]} for err in exc.errors()]
    return JSONResponse(
        status_code=422,
        content={
            "errors": errors,
        },
    )

class AuthenticationError(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=401, detail={
            "status": "Bad request",
            "message": "Authentication failed",
            "statusCode": 401,
            "detail": detail
        })
