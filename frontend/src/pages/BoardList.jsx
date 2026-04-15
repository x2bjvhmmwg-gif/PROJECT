import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router';
import { boardService } from '@api/boardService'; // API 서비스 임포트
import '@styles/Board.css';

const BoardList = ({ posts, setPosts }) => { 
  const [searchTerm, setSearchTerm] = useState('');
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(0);
  const navigate = useNavigate();
  const pageSize = 5;

  // 데이터를 불러오는 로직 (서비스 레이어 활용)
  const loadPosts = useCallback(async (currentPage) => {
    try {
      // 분리한 boardService를 호출합니다.
      const res = await boardService.getPosts(currentPage, pageSize);
      
      if (res.data.items) {
        setPosts(res.data.items);
        setTotalPages(Math.ceil(res.data.total_count / pageSize));
      } else {
        setPosts(res.data);
      }
    } catch (err) {
      // 상세 에러 로깅은 axiosInstance에서 처리하므로 컴포넌트에서는 사용자 알림 정도만 남깁니다.
      console.error("게시글 목록을 불러오지 못했습니다.");
    }
  }, [setPosts, pageSize]);

  useEffect(() => {
    loadPosts(page);
  }, [page, loadPosts]);

  // 검색 필터링 로직 (기존과 동일)
  const filteredPosts = posts.filter(post => 
    post.title?.toLowerCase().includes(searchTerm.toLowerCase()) ||
    post.author?.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="board-card">
      <header className="board-header">
        <div>
          <h1>Agent <span>Board</span></h1>
          <p style={{ color: '#999', marginTop: '8px' }}>AI 챗을 이용해 게시판 만들기</p>
        </div>
        <div className="search-container">
          <input 
            type="text"
            className="search-input"
            placeholder="제목 또는 작성자 검색..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
          />
        </div>
      </header>

      <div className="list-container">
        <div className="list-header">
          <div>No.</div><div>Title</div><div>Author</div><div>Date</div>
        </div>
        <div className="list-body">
          {filteredPosts.length > 0 ? (
            filteredPosts.map((post) => (
              <div 
                key={post.id} 
                className="post-item" 
                onClick={() => navigate(`/post/${post.id}`)}
              >
                <div className="post-id">{post.id}</div>
                <div className="post-title">
                  {post.category && <span className={`badge ${post.category}`}>[{post.category}]</span>} 
                  {post.title}
                </div>
                <div className="post-author">{post.author}</div>
                <div className="post-date">{post.update_date}</div>
              </div>
            ))
          ) : (
            <div className="no-data">게시글이 없습니다.</div>
          )}
        </div>
      </div>

      <div className="pagination-controls" style={{ display: 'flex', justifyContent: 'center', gap: '15px', marginTop: '20px' }}>
        <button 
          onClick={() => setPage(p => Math.max(1, p - 1))} 
          disabled={page === 1}
          className="page-btn"
        >
          이전
        </button>
        <span className="page-info">{page} / {totalPages || 1}</span>
        <button 
          onClick={() => setPage(p => Math.min(totalPages, p + 1))} 
          disabled={page === totalPages || totalPages === 0}
          className="page-btn"
        >
          다음
        </button>
      </div>
    </div>
  );
}

export default BoardList;