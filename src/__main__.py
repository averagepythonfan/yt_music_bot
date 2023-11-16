from fastapi import FastAPI
import uvicorn


app = FastAPI()


@app.get("/healthcheck")
async def healthcheck():
    return {"text": "Back app is working now!"}


if __name__ == "__main__":
    uvicorn.run(
        '__main__:app',
        host="0.0.0.0",
        port=9090,
        log_level="info",
        reload=True
    )
