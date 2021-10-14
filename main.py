from fastapi import FastAPI
import pony.orm as pony

app = FastAPI()

@app.get("/home")
async def home():
    return {"message" : "Project home Grupo Peluche"}
