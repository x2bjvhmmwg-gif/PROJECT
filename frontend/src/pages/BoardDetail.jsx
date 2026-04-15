import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router';
import { boardService } from '@api/boardService'; // API 서비스 임포트
import '@styles/Board.css';

function BoardDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [post, setPost] = useState(null);

  useEffect(() => {
    const fetchPost = async () => {
      try {
        const res = await boardService.getPostDetail(id);
        setPost(res.data);
      } catch (err) {
        // 이미 axiosInstance에서 에러 로그를 남기므로, 여기선 사용자 피드백만 처리합니다.
        alert("게시글을 찾을 수 없습니다.");
        navigate('/');
      }
    };
    fetchPost();
  }, [id, navigate]);

  if (!post) return <div className="loading">로딩 중...</div>;

  return (
    <div className="board-card">
      <div className="post-detail-view">
        <button className="back-btn" onClick={() => navigate('/')}>← 목록으로</button>
        <div className="detail-header">
          <h2>{post.title}</h2>
          <div className="detail-meta">
            <span>작성자: <b>{post.author}</b></span>
            <span>날짜: {post.update_date}</span>
          </div>
        </div>
        <hr />
        {post.category && <span className={`badge ${post.category}`}>#{post.category}</span>}
        <div className="detail-content" style={{ whiteSpace: 'pre-wrap', marginBottom: '20px' }}>
          {post.content}
        </div>
        {post.link && (
          <div className="article-link-section" style={{ marginTop: '30px', padding: '15px', borderTop: '1px dashed #eee' }}>
            <p style={{ fontSize: '14px', color: '#666' }}>🔗 뉴스 원문 확인하기</p>
            <a 
              href={post.link} 
              target="_blank" 
              rel="noopener noreferrer" 
              className="article-btn"
              style={{
                display: 'inline-block',
                padding: '10px 20px',
                backgroundColor: '#e0f2f1',
                color: '#00796b',
                borderRadius: '5px',
                textDecoration: 'none',
                fontWeight: 'bold',
                marginTop: '10px'
              }}
            >
              기사 보러가기
            </a>
          </div>
        )}
      </div>
    </div>
  );
}

export default BoardDetail;