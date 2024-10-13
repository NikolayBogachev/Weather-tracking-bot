
import uvicorn
from fastapi import FastAPI
from fastapi.routing import APIRouter


from handlers import router, logger


app = FastAPI(title="Chat-Bot")


main_api_router = APIRouter()

main_api_router.include_router(router)

app.include_router(main_api_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
