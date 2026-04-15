import axios from 'axios';

const axiosInstance = axios.create({
  // baseURL: 'http://localhost:8000/api', // 베이스 URL 설정
  baseURL: 'http://aiedu.tplinkdns.com:6061/api',
  headers: {
    'Content-Type': 'application/json',
  },
});

// 필요 시 인터셉터를 추가하여 요청/응답 시 공통 로직(로그인 토큰 등)을 처리할 수 있습니다.
axiosInstance.interceptors.response.use(
  (response) => response,
  (error) => {
    console.error('API 에러 발생:', error.response?.data || error.message);
    return Promise.reject(error);
  }
);

export default axiosInstance;