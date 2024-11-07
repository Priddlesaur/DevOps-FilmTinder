from dotenv import load_dotenv
from fastapi import FastAPI

# Load environment variables
load_dotenv()

# Create FastAPI instance
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}
