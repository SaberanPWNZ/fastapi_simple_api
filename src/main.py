import uvicorn
from fastapi import FastAPI
from items.router import items_router, authentication
from tasks.tasks import startup_event

app = FastAPI(lifespan=startup_event)
app.include_router(items_router)
app.include_router(authentication)


@app.get('/')
def main():
    return {"Hello": "World"}


# @app.get("/protected-route")
# def protected_route(user: User = Depends(current_user)):
#     return f"Hello, {user.username}"


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
