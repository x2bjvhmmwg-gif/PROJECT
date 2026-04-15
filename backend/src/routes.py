from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.workflow import create_board_workflow
from langchain_core.messages import HumanMessage, AIMessage
from db import findAll, findOne

router = APIRouter()

# 1. 워크플로우 그래프 생성
graph = create_board_workflow()

# 2. Pydantic 모델 정의
class ChatRequest(BaseModel):
    message: str
    thread_id: str = "default_user"

class ChatResponse(BaseModel):
    response: str
    sender: str

# --- 채팅 엔드포인트 ---
@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        config = {"configurable": {"thread_id": request.thread_id}}
        inputs = {"messages": [HumanMessage(content=request.message)]}
        result = graph.invoke(inputs, config=config)
        final_answer = "죄송해요, 답변을 준비하는 중에 문제가 생겼어요. 다시 말씀해 주시겠어요?"
        for msg in reversed(result["messages"]):
            if isinstance(msg, AIMessage) and msg.content.strip():
                if "call:" not in msg.content: 
                    final_answer = msg.content
                    break
        
        return ChatResponse(
            response=final_answer,
            sender="AI_Assistant"
        )
    except Exception as e:
        print(f"Chat Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# --- 게시글 목록 조회 엔드포인트 ---
@router.get("/posts")
async def get_board_list(page: int = 1, size: int = 10): 
    try:
        # 1. OFFSET 계산 (몇 번째 데이터부터 가져올지)
        offset = (page - 1) * size
        # 2. 전체 데이터 개수 구하기 (페이지네이션 계산용)
        total_sql = "SELECT COUNT(*) as cnt FROM board WHERE is_deleted = 0"
        total_res = findOne(total_sql)
        total_count = total_res['cnt'] if total_res else 0
        # 3. LIMIT과 OFFSET을 적용한 쿼리
        sql = """
            SELECT id, author, title, content, update_date, category 
            FROM board 
            WHERE is_deleted = 0 
            ORDER BY id DESC 
            LIMIT %s OFFSET %s
        """
        # findAll 함수가 params를 받을 수 있도록 구성되어 있어야 합니다 (db.py 참고)
        posts = findAll(sql, (size, offset))
        for post in posts:
            if post.get('update_date'):
                post['update_date'] = post['update_date'].isoformat().replace('T', ' ')
        # 4. 프론트엔드가 필요한 정보들을 묶어서 반환
        return {
            "items": posts,
            "total_count": total_count,
            "page": page,
            "size": size
        }
    except Exception as e:
        print(f"Error fetching posts: {e}")
        raise HTTPException(status_code=500, detail="목록을 불러오는 중 서버 오류가 발생했습니다.")

# --- 게시글 상세 조회 엔드포인트 ---

@router.get("/posts/{post_id}")
async def get_post_detail(post_id: int):
    try:
        sql = """
            SELECT 
                id, author, title, content, link, category,
                DATE_FORMAT(update_date, '%Y-%m-%d %H:%i') as update_date 
            FROM board 
            WHERE id = %s AND is_deleted = 0
        """
        post = findOne(sql, (post_id,))
        
        if not post:
            print(f"Post not found for ID: {post_id}")
            raise HTTPException(status_code=404, detail="게시글을 찾을 수 없습니다.")
            
        return post
    except Exception as e:
        print(f"상세 조회 중 오류 발생: {e}")
        # 에러 메시지를 더 구체적으로 반환합니다.
        raise HTTPException(status_code=500, detail=str(e))