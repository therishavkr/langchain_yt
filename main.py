from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from langchain.chat_models import ChatOpenAI
from langchain.chains import RetrievalQA
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.document_loaders import Document
from youtube_transcript_api import YouTubeTranscriptApi
from dotenv import load_dotenv
import os, re

load_dotenv()
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class VideoQARequest(BaseModel):
    url: str
    question: str

def get_video_id(url):
    match = re.search(r"v=([a-zA-Z0-9_-]+)", url)
    return match.group(1) if match else None

def fetch_transcript(video_url):
    video_id = get_video_id(video_url)
    if not video_id:
        raise ValueError("Invalid YouTube URL.")
    transcript = YouTubeTranscriptApi.get_transcript(video_id)
    return " ".join([t["text"] for t in transcript])

def create_vectorstore(text):
    doc = Document(page_content=text, metadata={"source": "youtube"})
    embeddings = OpenAIEmbeddings()
    return FAISS.from_documents([doc], embeddings)

@app.post("/ask")
async def ask_video_question(request: VideoQARequest):
    transcript = fetch_transcript(request.url)
    vectorstore = create_vectorstore(transcript)
    qa = RetrievalQA.from_chain_type(
        llm=ChatOpenAI(temperature=0, openai_api_key=os.getenv("OPENAI_API_KEY")),
        chain_type="stuff",
        retriever=vectorstore.as_retriever()
    )
    answer = qa.run(request.question)
    return {"answer": answer}
