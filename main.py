import os
import csv
from datetime import datetime, timedelta
from logger import Logger

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.cors import CORSMiddleware
import uvicorn
from pydantic import BaseModel

logger = Logger(log_level="DEBUG")
app = FastAPI()
app.mount(path="/static", app=StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# CORS回避
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# read csv
async def read_db(file):
    with open(file) as f:
        reader = csv.reader(f)
        data = [row for row in reader]
        logger.debug(data)
        return data

# write csv
async def write_db(file, new_row):
    with open(file, 'a', newline="") as f:
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
    await write_db('data/db.csv', data_row)
    return {"Message": "POST OK"}

@app.get("/snow")
async def get_snow_data(data_before_hour: int = 0):
    logger.debug("GET: get_snow_data ( /snow )")
    data = await read_db('data/db.csv')
    if data_before_hour != 0:
        now = datetime.now()
        del_rows = []
        for index, row in enumerate(data):
            row_time = datetime.strptime(row[2], '%Y-%m-%d %H:%M:%S')
            if now - row_time > timedelta(hours=data_before_hour):
                del_rows.append(index)
        if del_rows != []:
            del_rows.reverse()
            for i in del_rows:
                del data[i]
    return data

class POST_CHAT_MODEL(BaseModel):
    user_name: str
    message: str

@app.post("/chat/new_message")
async def new_message(data: POST_CHAT_MODEL):
    logger.debug("POST: new_message ( /chat/new_message )")
    data_row = [data.user_name, data.message]
    await write_db('data/chat.csv',data_row)
    return {"Message": "POST OK"}

@app.get("/chat")
async def get_chat_data():
    logger.debug("GET: get_chat_data ( /chat )")
    data = await read_db('data/chat.csv')
    return data


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)