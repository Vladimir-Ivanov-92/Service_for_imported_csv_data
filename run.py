import uvicorn
from fastapi import APIRouter, FastAPI

from api.file.file_handlers import file_router
from api.users.user_handlers import user_router

app = FastAPI(title="service_for_imported_csv_data")

# create the instance for the routes
main_api_router = APIRouter()

# set routers to the app instance
main_api_router.include_router(user_router, prefix="/user", tags=["user"])
main_api_router.include_router(file_router, prefix="/file", tags=["file"])

app.include_router(main_api_router)

if __name__ == '__main__':
    # run app on the host and port
    uvicorn.run(app, host="0.0.0.0", port=8000)
