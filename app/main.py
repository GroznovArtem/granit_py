from fastapi import FastAPI
from app.api.main import main_router
from app.api.routers.user import user_router
import uvicorn

app = FastAPI()

app.include_router(main_router)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
