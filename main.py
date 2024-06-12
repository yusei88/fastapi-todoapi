import multiprocessing
import uvicorn
from fastapi import FastAPI
import json
from pydantic import BaseModel
from datetime import datetime
from logging import getLogger

logger = getLogger("uvicorn.app")

app = FastAPI()

DATA_FILE = 'data.json'
INITIAL_DATA = {
    "created": "",
    "updated": "",
    "data": []
}


class Todo(BaseModel):
    id: int
    title: str
    description: str = ""
    due_date: datetime
    is_done: bool = False


@app.get('/todos')
def get_todos() -> list[Todo]:
    with open(DATA_FILE) as f:
        raw_data = json.load(f)
    logger.info(f"raw_data: {raw_data}")
    if not raw_data['data']:
        return []

    return [Todo(**item)for item in raw_data['data']]


@app.get('/todos/{id}')
def get_todo(id: int) -> Todo | dict:
    with open(DATA_FILE) as f:
        raw_data = json.load(f)
    logger.info(f"raw_data: {raw_data}")
    if not raw_data['data']:
        return {}

    find_data = find_one(id=id, data=raw_data['data'])
    if not find_data:
        return {}
    return Todo(**find_data)


def find_one(id: int, data: dict) -> dict | None:
    return next((f for f in data if f['id'] == id), None)


def init():
    """Init data.json

    Args:
        input: None

    Returns:
        None
    """
    try:
        with open(DATA_FILE, mode='x') as f:
            json.dump(INITIAL_DATA, f, indent=4)

    except FileExistsError:
        pass


if __name__ == '__main__':
    multiprocessing.freeze_support()
    init()
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=False, workers=1)
