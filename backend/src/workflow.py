from langgraph.checkpoint.memory import InMemorySaver
from langgraph_swarm import create_swarm
# 이전에 만든 에이전트들을 가져옵니다.
from src.board_agents import db_agent, writer_agent, news_agent

def create_board_workflow():
    """
    게시판 관리 에이전트들을 Swarm 구조로 묶어 워크플로우를 생성합니다.
    """
    
    # 1. 메모리 설정: 대화의 맥락(thread_id)을 유지하여 에이전트가 이전 명령을 기억하게 합니다.
    checkpointer = InMemorySaver()
    
    # 2. 스웜 생성: 모든 에이전트를 리스트에 넣고, 시작 에이전트를 설정합니다.
    # 사용자의 모든 통제를 담당하는 DBAgent를 기본 활성 에이전트로 설정할 수 있습니다.
    workflow = create_swarm(
        [db_agent, writer_agent, news_agent],
        default_active_agent="DBAgent"
    )
    
    # 3. 컴파일: 체크포인터를 포함하여 실행 가능한 그래프 형태로 만듭니다.
    app = workflow.compile(checkpointer=checkpointer)
    
    return app

# 외부에서 이 파일을 직접 실행하여 구조를 확인할 수 있도록 구성합니다.
if __name__ == "__main__":
    from src.save_image import save_graph_image
    
    graph = create_board_workflow()
    # 그래프 구조를 이미지로 저장하여 흐름이 맞는지 확인합니다.
    save_graph_image(graph)
    print("✅ 워크플로우 그래프 이미지가 저장되었습니다.")