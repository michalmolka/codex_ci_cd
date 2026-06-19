from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI(
    title="FastAPI CI/CD App",
    version="0.1.0",
    description="Small FastAPI service used to a Docker-based CI/CD process.",
)


class Greeting(BaseModel):
    message: str


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/hello/{name}", response_model=Greeting)
def hello(name: str) -> Greeting:
    name2 = "Name2"
    return Greeting(message=f"Hello, {name}!")
