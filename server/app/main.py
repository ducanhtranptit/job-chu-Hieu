from fastapi import FastAPI
import uvicorn
from dotenv import load_dotenv
import os
from app.openai_client import Assist, ask_using_embedding
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

load_dotenv()
ASSIST_ID = os.environ.get("ASSIST_ID")
assist = Assist(ASSIST_ID)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)


@app.get("/init_thread/")
async def init_thread():
    thread_id = assist.create_thread().id
    return {"thread_id": thread_id}


@app.get("/ask/")
async def ask(question: str, thread_id: str):
    answer = ask_using_embedding(question, thread_id)
    return {"answer": answer}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
