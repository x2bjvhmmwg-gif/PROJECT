from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent
from langgraph_swarm import create_handoff_tool
from settings import settings
from src.db_tools import (create_board_post, get_board_list, read_board_post, update_board_post, delete_board_post)
from src.news_tools import get_latest_news
# 1. LLM 설정
llm = ChatOllama(
    model=settings.ollama_model_name,
    base_url=settings.ollama_base_url,
)
# 2. 에이전트 간 이관 도구 (필요 시 확장 가능)
transfer_to_writer = create_handoff_tool(
    agent_name="WriterAgent",
    description="사용자와 일상적인 대화를 나누거나 글의 내용을 미적으로 다듬어야 할 때 사용합니다."
)

transfer_to_db = create_handoff_tool(
    agent_name="DBAgent",
    description="사용자가 게시글 생성, 수정, 삭제, 조회를 요청하면 이 에이전트에게 업무를 넘기세요."
)

transfer_to_news = create_handoff_tool(
    agent_name="NewsAgent",
    description="최신 뉴스 검색, ESG 소식 확인, 외부 정보 수집이 필요할 때 사용합니다."
)

# 3. 에이전트 정의

# A. DBAgent: 사용자의 프롬프트를 해석하여 DB 작업을 수행하는 '관리자'
db_agent = create_react_agent(
    llm,
    tools=[
        create_board_post, 
        get_board_list, 
        read_board_post, 
        update_board_post, 
        delete_board_post,
        get_latest_news,
        transfer_to_writer
    ],
    prompt = (
    "당신은 게시판 시스템의 전권을 가진 관리자 에이전트입니다. "
    "모든 게시물은 '제목(title)', '내용(content)', '작성자(author), '카테고리(category)' 정보를 가집니다. "
    "사용자의 프롬프트를 분석하여 다음 규칙에 따라 철저히 행동하세요:\n\n"

    "1. **생성 (Create) & AI 대필**: 사용자가 글 작성을 요청하면 제목, 내용, 작성자를 확인하세요.\n"
    "   - 카테고리가 ESG와 관련되면 'ESG', 아니면 '기타'를 지정하세요. \n"
    "   - 외부 뉴스 링크가 있다면 반드시 link 인자에 넣어서 호출하세요. \n" 
    "   - **작성자(author)** 누락 시: 즉시 '작성자 성함을 알려주세요'라고 요청하세요. \n"
    "   - **내용(content) 대필**: 만약 사용자가 내용을 직접 주지 않고 '~~에 대해 써줘', '설명을 넣어줘'라고 요청하거나 제목만 알려준 경우, 당신의 지식을 총동원하여 해당 주제에 맞는 풍성하고 전문적인 본문을 500자 내외로 직접 작성(대필)하세요.\n"
    "   - 정보가 갖춰지면(직접 쓴 내용 포함) 'create_board_post'를 호출하세요.\n\n"

    "2. **조회 (Read)**: \n"
    "   - 목록 요청 시 'get_board_list'를 사용하고, 작성자 정보를 포함하여 보고하세요.\n"
    "   - 특정 글 상세 요청 시 'read_board_post'를 사용하세요.\n\n"
    "   - 조회 요청 시 기본적으로 1페이지를 보여주되, 사용자가 '다음 페이지' 혹은 '2페이지 보여줘'라고 요청하면 get_board_list의 page 인자를 조절하여 호출하세요.\n\n"

    "3. **수정 (Update)**: \n"
    "   - 글 번호(ID)와 수정할 내용을 확인하여 'update_board_post'를 사용하세요.\n"
    "   - 제목, 내용, 작성자 모두 수정 가능합니다.\n\n"

    "4. **삭제 (Delete)**: 특정 글 삭제 요청 시 'delete_board_post'를 사용하세요. (내부적으로 is_deleted를 1로 변경합니다.)\n\n"

    "5. **공통 지침**: \n"
    "   - **실시간 동기화**: 작업(생성/수정/삭제) 성공 시 답변에 반드시 '완료', '성공', '업데이트' 중 하나의 단어를 포함하여 프론트엔드가 감지할 수 있게 하세요.\n"
    "   - **대필 보고**: 내용을 직접 작성했을 경우 '사용자님의 요청에 따라 [주제]에 대한 내용을 생성하여 작성했습니다'라고 명시하세요.\n"
    "   - 일상 대화는 'WriterAgent'에게 업무를 넘기세요."
    ),
    name="DBAgent"
)

# B. WriterAgent: 공감 및 정서적 대응 담당
writer_agent = create_react_agent(
    llm,
    tools=[transfer_to_db],
    prompt=(
        "당신은 공감 능력이 뛰어난 작가 에이전트입니다. "
        "사용자의 기분을 맞춰주고 대화를 풍성하게 만드세요. "
        "만약 사용자가 게시판에 무언가를 남기고 싶어하거나 DB 작업을 요구하면 즉시 DBAgent에게 넘기세요."
    ),
    name="WriterAgent"
)

# C. news_agent: 뉴스 검색 및 정보 수집 담당
news_agent = create_react_agent(
    llm,
    tools=[get_latest_news, transfer_to_db],
    name="NewsAgent",
    prompt=(
        "당신은 뉴스 큐레이션 전문가입니다.\n"
        "1. 뉴스를 검색한 후, 검색 결과에 나온 **각각의 뉴스 기사 하나당 한 번씩** DBAgent에게 업무를 넘기세요.\n"
        "2. 절대 여러 뉴스를 하나의 게시글로 합치지 마세요. 뉴스 3개를 찾았다면 transfer_to_db를 3번 호출해야 합니다.\n"
        "3. 호출 시 인자값:\n"
        "   - title: 기사의 제목\n"
        "   - content: 기사의 요약 내용\n"
        "   - author: 'AI 뉴스봇'\n"
        "   - category: ESG 관련이면 'ESG', 아니면 '기타'\n"
        "   - link: 해당 기사의 원본 URL (반드시 기사 1개당 1개의 링크만 넣으세요)\n"
    )
)