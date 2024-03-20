import os
import csv
from datetime import datetime
from logger import Logger

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from pydantic import BaseModel

logger = Logger(log_level="DEBUG")
app = FastAPI()
app.mount(path="/static", app=StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


# read csv
async def read_db():
    with open('data/db.csv') as f:
        reader = csv.reader(f)
        data = [row for row in reader]
        logger.debug(data)
        return data

# write csv
async def write_db(new_row):
    with open('data/db.csv', 'a', newline="") as f:
        writer = csv.writer(f, lineterminator="\n", quoting=csv.QUOTE_ALL)
        writer.writerow(new_row)


# [API] json Model
class POST_DATA_MODEL(BaseModel):
    latitude: str
    longitude: str
    user_id: int


@app.get("/", response_class=HTMLResponse)
async def root(request: Request,):
    logger.debug("GET: root ( / )")
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/snow/new_post")
async def new_post(data: POST_DATA_MODEL):
    logger.debug("POST: new_post ( /snow/new_post )")
    time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    data_row = [data.latitude, data.longitude, time, data.user_id]
    await write_db(data_row)
    return {"Message": "POST OK"}

@app.get("/snow")
async def get_snow_data():
    logger.debug("GET: get_snow_data ( /snow )")
    data = await read_db()
    return data


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)