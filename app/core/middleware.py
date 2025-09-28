from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response


class CompanyContextMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Заглушка: позже извлечём company_id из JWT/SSO и проставим в контекст
        response: Response = await call_next(request)
        return response


