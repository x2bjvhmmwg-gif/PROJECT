import React from 'react';
import { useNavigate } from 'react-router';

const NotFound = () => {
  const navigate = useNavigate();
  return (
    <div className="board-card" style={{ textAlign: 'center', padding: '100px 20px' }}>
      <h1 style={{ fontSize: '5rem', color: 'var(--accent-mint)' }}>404</h1>
      <p style={{ fontSize: '1.2rem', marginBottom: '30px' }}>찾으시는 페이지가 존재하지 않습니다. 🌿</p>
      <button className="page-btn" onClick={() => navigate('/')}>메인으로 돌아가기</button>
    </div>
  );
};

export default NotFound;