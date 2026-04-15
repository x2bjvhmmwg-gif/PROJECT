import React, { useState, useCallback } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router';
import BoardList from '@pages/BoardList';
import BoardDetail from '@pages/BoardDetail';
import Chat from '@components/Chat';
import { boardService } from '@api/boardService';
import '@styles/App.css';

const App = () => {
  const [posts, setPosts] = useState([]);

  const fetchPosts = useCallback(async () => {
    try {
      const res = await boardService.getPosts(1, 10);
      setPosts(res.data.items || res.data); 
    } catch (err) {
      console.error("데이터 로드 실패:", err);
    }
  }, []);

  return (
    <Router>
      {/* AI가 글을 쓰면 fetchPosts를 호출해 리스트를 새로고침함 */}
      <Chat onUploadSuccess={fetchPosts} />
      
      <div className="container">
        <Routes>
          <Route 
            path="/" 
            element={<BoardList posts={posts} setPosts={setPosts} fetchPosts={fetchPosts} />} 
          />
          <Route path="/post/:id" element={<BoardDetail />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;