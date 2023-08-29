import os
import logging
import ssl
from fastapi import FastAPI,Request
from fastapi.middleware.cors import CORSMiddleware
from motor.motor_asyncio import AsyncIOMotorClient
import certifi
from typing import Optional

from dotenv import load_dotenv

from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from app.src.query import Qnabot

log = logging.getLogger(__name__)

middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*",""],
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*']
    )
]

import dns.resolver
dns.resolver.default_resolver=dns.resolver.Resolver(configure=False)
dns.resolver.default_resolver.nameservers=['8.8.8.8']

app = FastAPI(middleware=middleware)

load_dotenv() 
# ssl._create_default_https_context = ssl._create_unverified_context




@app.post("/api/v1.0/qabot")

# async def root(request: Request, SLNo: Optional[str] = None):
# async def root(user_input:str, SLNo: str):
async def root(info: Request):
    # print('request',request.json())
    # user_input =request.question
    req_info = await info.json()

    print('user_input',req_info["user_input"])
    user_input=req_info["user_input"]
    bot=Qnabot()
    result={} 
    document_path=r"app/artifacts/wiki"
    if user_input in ['Hi','hi','hello','hola']: # first time being called
        result["question"] = user_input
        result["answer"]= "Hi there! This is QNABot,Please type in your queries here..."
        created_index = bot.first_chat(document_path)
    # else:
    #     try:

    #         result,all_messages = bot.generate_chat(document_path,user_input)
    #         result["question"] = user_input
    #         result["answer"]= result
    #     except Exception as e:
    #         print('Éxception occurred during document fetch:', str(e)) 
    return result





