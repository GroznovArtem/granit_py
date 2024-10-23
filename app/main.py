from fastapi import FastAPI
from app.api.main import main_router
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

app.include_router(main_router)

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://192.168.0.103:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
