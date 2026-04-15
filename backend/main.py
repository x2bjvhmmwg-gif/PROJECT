# main.py
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes import router as chat_router
from src.save_image import save_graph_image 

app = FastAPI(title="AI Board Agent API")

# React 프론트엔드와 통신하기 위한 CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173","http://localhost:80",
                   "http://aiedu.tplinkdns.com","http://aiedu.tplinkdns.com:6060"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# 라우터 등록
app.include_router(chat_router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)