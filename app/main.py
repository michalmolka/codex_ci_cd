from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI(
    title="FastAPI CI/CD Demo",
    version="0.1.0",
    description="Small FastAPI service used to demonstrate Docker-based CI/CD.",
)


class Greeting(BaseModel):
    message: str


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/hello/{name}", response_model=Greeting)
def hello(name: str) -> Greeting:
    return Greeting(message=f"Hello, {name}!")
