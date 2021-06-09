from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from demo.views import router


app = FastAPI()
app.include_router(router)


@app.middleware('http')
async def check_auth_token(request: Request, call_next):
    # import pudb; pu.db
    token = request.headers.get('Authorization')
    if token != 'Bearer valid-token':
        return JSONResponse(status_code=401, content={'detail': 'Invalid token'})
    return await call_next(request)
