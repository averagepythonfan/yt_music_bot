import uvicorn
from fastapi import FastAPI
from src.routers import (user_router,
                         pl_router)


app = FastAPI()


app.include_router(router=user_router)
app.include_router(router=pl_router)


@app.get("/healthcheck")
async def healthcheck():
    return {"text": "Back app is working now!"}


uvicorn.run(
    app=app,
    host="0.0.0.0",
    port=9090,
    log_level="info"
)