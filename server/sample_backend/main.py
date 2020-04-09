from typing import List

import uvicorn
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field


class Item(BaseModel):
    name: str = Field(..., title="The name of the item", min_length=3, max_length=32)
    description: str = Field(None, title="The description of the item", max_length=300)
    price: float
    tax: float = None

items = []

app = FastAPI()

@app.post("/items", status_code=status.HTTP_204_NO_CONTENT)
def create_item(item: Item) -> None:
    items.append(item)
    return

@app.get("/items", response_model=List[Item], responses={404: {"description": "No Items"}})
def get_items():
    if not items:
        raise HTTPException(status_code=404, detail="Items not found")
    return items

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=5000, log_level="info")
