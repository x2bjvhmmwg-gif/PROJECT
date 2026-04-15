import React, { useState, useEffect } from 'react';
import { boardService } from '@api/boardService'; // API 서비스 임포트
import '@styles/Chat.css';

function Chat({ onUploadSuccess }) {
  const [isChatOpen, setIsChatOpen] = useState(false);
  
  // 1. 초기값을 localStorage에서 불러오기
  const [messages, setMessages] = useState(() => {
    const saved = localStorage.getItem('chat_messages');
    return saved ? JSON.parse(saved) : [{ sender: 'ai', text: '기록을 도와드릴까요? 🌿' }];
  });

  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);

  // 2. 메시지가 변경될 때마다 localStorage에 자동 저장
  useEffect(() => {
    localStorage.setItem('chat_messages', JSON.stringify(messages));
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMsg = { sender: 'user', text: input };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setIsLoading(true);

    try {
      // 서비스 레이어를 통해 메시지 전송
      const res = await boardService.sendChatMessage(input);

      const aiResponse = res.data.response;
      setMessages(prev => [...prev, { sender: 'ai', text: aiResponse }]);

      // DB 갱신 로직
      const syncKeywords = ['성공', '완료', '등록', '삭제', '수정', '업데이트', '생성'];
      if (syncKeywords.some(key => aiResponse.includes(key))) {
        if (onUploadSuccess) {
          setTimeout(() => onUploadSuccess(), 500);
        }
      }
    } catch (err) {
      // 공통 에러 처리는 axiosInstance에서 수행하므로 UI 피드백만 추가
      setMessages(prev => [...prev, { sender: 'ai', text: '통신 중 오류가 발생했어요. 😢' }]);
    } finally {
      setIsLoading(false);
    }
  };

  const clearChat = () => {
    if (window.confirm("대화 내역을 모두 지울까요?")) {
      const initialMsg = [{ sender: 'ai', text: '기록을 도와드릴까요? 🌿' }];
      setMessages(initialMsg);
      localStorage.removeItem('chat_messages');
    }
  };

  return (
    <>
      <button className="chat-toggle" onClick={() => setIsChatOpen(!isChatOpen)}>
        {isChatOpen ? '✕' : '💬'}
      </button>

      {isChatOpen && (
        <div className="chat-window">
          <div className="chat-header">
            <span>🌿</span> <b>AI Assistant</b>
            <button onClick={clearChat} 
            style={{marginLeft: 'auto', background: 'none', border: 'none', cursor: 'pointer', fontSize: '12px', color: '#889'}}
            >[지우기]</button>
          </div>
          
          <div className="chat-body">
            {messages.map((msg, index) => (
              <div key={index} className={`message ${msg.sender}`}>
                {msg.text}
              </div>
            ))}
            {isLoading && (
              <div className="message ai typing">
                <div className="dot"></div>
                <div className="dot"></div>
                <div className="dot"></div>
              </div>
            )}
          </div>

          <div className="chat-input-area">
            <input 
              value={input} 
              onChange={(e) => setInput(e.target.value)}
              onKeyPress={(e) => e.key === 'Enter' && handleSend()}
              placeholder="AI에게 게시글 관리를 시켜보세요..."
            />
            <button className="send-btn" onClick={handleSend}>전송</button>
          </div>
        </div>
      )}
    </>
  );
}

export default Chat;