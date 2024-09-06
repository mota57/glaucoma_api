from fastapi import Depends, FastAPI
from fastapi.routing import APIRoute
# routers
from src.router import patient_controller
# database
from .database import engine, Base
# cors
from fastapi.middleware.cors import CORSMiddleware

# start database
Base.metadata.create_all(bind=engine)

def custom_generate_unique_id(route: APIRoute) -> str:
    if len(route.tags) > 0:
        return f"{route.tags[0]}-{route.name}"
    return route.name

# start fast api
app = FastAPI(
    title="glaucoma",
    generate_unique_id_function=custom_generate_unique_id)

# set cors

app.add_middleware(
CORSMiddleware,
allow_origins=["*"], # Allows all origins
allow_credentials=True,
allow_methods=["*"], # Allows all methods
allow_headers=["*"], # Allows all headers
)


# attach routers
app.include_router(patient_controller.router)
# app.include_router(database_controller.router)
# app.include_router(items.router)



# use_route_names_as_operation_ids(app)

# base
@app.get("/")
async def root():
    return {"message": "Hello Applications!"}
