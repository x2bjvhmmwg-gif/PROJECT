from db import save, findAll, findOne
import json

def create_board_post(title: str, content: str, author: str, category: str = "기타", link: str = None) -> str:
    """
    새로운 게시물을 생성합니다. 작성자(author) 정보가 반드시 필요합니다.
    """
    sql = "INSERT INTO board (title, content, author, category, link) VALUES (%s, %s, %s, %s, %s)"
    success = save(sql, (title, content, author, category, link))
    return f"✅ [{category}] 게시물이 생성되었습니다." if success else "❌ 생성 실패"

def get_board_list(page: int = 1, size: int = 10) -> str:
    """작성자를 포함한 목록을 가져옵니다."""
    offset = (page - 1) * size

    # 전체 개수 확인용 쿼리 (프론트에서 총 페이지 수 계산을 위해 필요)
    total_sql = "SELECT COUNT(*) as cnt FROM board WHERE is_deleted = 0"
    total_count = findOne(total_sql)['cnt']

    # 데이터 페이징 쿼리
    sql = f"SELECT id, title, author, reg_date, category FROM board WHERE is_deleted = 0 ORDER BY id DESC LIMIT %s OFFSET %s"
    rows = findAll(sql, (size, offset))

    return json.dumps({
        "items": rows,
        "total_count": total_count,
        "page": page,
        "size": size
    }, ensure_ascii=False, default=str)

def update_board_post(post_id: int, title: str = None, content: str = None, author: str = None) -> str:
    """작성자 이름도 수정 가능하도록 대응합니다."""
    if not any([title, content, author]): return "수정할 내용이 없습니다."
    
    updates, params = [], []
    if title: updates.append("title = %s"); params.append(title)
    if content: updates.append("content = %s"); params.append(content)
    if author: updates.append("author = %s"); params.append(author)
    
    params.append(post_id)
    sql = f"UPDATE board SET {', '.join(updates)} WHERE id = %s AND is_deleted = 0"
    return f"✅ {post_id}번 수정 완료" if save(sql, tuple(params)) else "❌ 수정 실패"

def delete_board_post(post_id: int) -> str:
    """
    게시물을 논리적으로 삭제합니다 (is_deleted 필드를 1로 변경).
    사용자가 '삭제해줘' 혹은 '지워줘'라고 할 때 사용합니다.
    """
    sql = "UPDATE board SET is_deleted = 1 WHERE id = %s"
    success = save(sql, (post_id,))
    return f"✅ {post_id}번 게시물이 삭제 처리되었습니다." if success else "❌ 삭제에 실패했습니다."

def read_board_post(post_id: int) -> str:
    """상세 조회 시 작성자 정보를 포함합니다."""
    sql = f"SELECT * FROM board WHERE id = {post_id} AND is_deleted = 0"
    row = findOne(sql)
    if not row: return f"ID {post_id}번 글을 찾을 수 없습니다."
    return json.dumps(row, ensure_ascii=False, indent=2, default=str)