# main.py
from fastapi import FastAPI

# Create an instance of the FastAPI application
app = FastAPI()

# Define a path operation (or "route")
@app.get("/")
async def read_root():
    """
    This is the first endpoint of our FastAPI application.
    It returns a simple "Hello, World!" message.
    """

    return {"message": "Hello, World!"}
