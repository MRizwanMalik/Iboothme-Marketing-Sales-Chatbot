
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from openai import AsyncOpenAI

from apps.social_media import models as social_media_models
from apps.case_study import models as case_study_models
from apps.blog_app import model as blog_models
from apps.chatbot import models as chatbot_models

from apps.social_media import app as social_media_app
from apps.chatbot import app as chatbot_app
from apps.case_study import app as case_study_app
from apps.blog_app import app as blog_app
#from apps.chatbot.api import router as chatbot_router

from dotenv import load_dotenv
load_dotenv()
import datetime


app = FastAPI(default_response_class=ORJSONResponse)
client = AsyncOpenAI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"],
)


#app.include_router(chatbot_router, prefix="/api")


@app.post(
    "/generate-social-media-caption", response_model=social_media_models.CaptionResponse
)
async def social_media_generate_caption(request: social_media_models.CaptionRequest):
    print(f"[{datetime.datetime.now().isoformat()}] /generate-social-media-caption called")
    res = await social_media_app.generate_caption(client, request)
    return res


@app.websocket("/chat")
async def chat(websocket: WebSocket):
    res = await chatbot_app.chat(websocket=websocket)
    return res


# TODO: make this endpoint for training chhatbot
@app.post("/train-chatbot")
async def train_chatbot():
    res = await chatbot_app.train_ai_endpoint()
    return res


@app.post("/generate-case-study", response_model=case_study_models.CaseStudyResponse)
async def case_study(request: case_study_models.CaseStudyRequest):
    print(f"[{datetime.datetime.now().isoformat()}] /generate-case-study called")
    res = await case_study_app.generate_case_study(client, request)
    return case_study_models.CaseStudyResponse(case_study=res)


@app.post("/generate-blog-post")
async def blog(request: blog_models.GenerateRequest):
    print(f"[{datetime.datetime.now().isoformat()}] /generate-blog-post called")
    res = await blog_app.generate_blog_post(client, request)
    return res

@app.post("/update-ai", response_model=chatbot_models.UpdateAIResponse)
async def update_prompt_ai(data:chatbot_models.UpdateAIRequest): 
    res = await chatbot_app.update_prompt(data)
    return res
if __name__ =="__main__":
    import uvicorn

    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        ws_ping_interval=30,
        ws_ping_timeout=30,
    )
