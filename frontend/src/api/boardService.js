import axiosInstance from './axiosInstance';

export const boardService = {
  // 게시글 목록 조회 (페이지네이션 포함)
  getPosts: (page = 1, size = 5) => 
    axiosInstance.get(`/posts?page=${page}&size=${size}`),

  // 단일 게시글 상세 조회
  getPostDetail: (id) => 
    axiosInstance.get(`/posts/${id}`),

  // 챗봇 메시지 전송
  sendChatMessage: (message, threadId = "chaehoon_user") => 
    axiosInstance.post('/chat', { message, thread_id: threadId }),
};