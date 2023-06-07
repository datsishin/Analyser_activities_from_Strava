import os
from time import time

from telegram import get_training_data

import uvicorn
from fastapi import FastAPI, Request
from fastapi.encoders import jsonable_encoder
from starlette import status
from starlette.responses import JSONResponse

app = FastAPI()


@app.get("/", status_code=status.HTTP_200_OK)
def get_webhook(request: Request):
    request_args_dict = dict(request.query_params)
    print(request_args_dict)
    challenge = request_args_dict['hub.challenge']

    return JSONResponse(content=jsonable_encoder({'hub.challenge': challenge}))


@app.post("/", status_code=status.HTTP_200_OK)
async def get_data(request: Request):
    global user_id
    data = await request.json()
    print(data)

    if data['aspect_type'] == 'create':
        # user_id = os.getenv('FIRST_USER_ID')
        # athlete = data['owner_id']
        # if athlete == os.getenv('FIRST_ATHLETE_ID'):
        #     user_id = os.getenv('FIRST_USER_ID')
        # elif athlete == os.getenv('SECOND_ATHLETE_ID'):
        #     user_id = os.getenv('SECOND_USER_ID')
        #
        # print(type(user_id))
        # print(user_id)
        start = time()
        await get_training_data(666785382)
        print(time()-start)
        print('def is run')
        return status.HTTP_200_OK

    return status.HTTP_200_OK