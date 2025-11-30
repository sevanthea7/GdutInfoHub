//import axios from "axios";
// const streamInstance = axios.create({
//   baseURL: import.meta.env.VITE_APP_URL,
//   timeout: 60000,
//   // 不要设置 responseType: 'stream'，Axios 不支持
// });

export const getStreamAnswer = async (data) => {
  // 使用原生 fetch 处理流式
  const response = await fetch("/api/stream", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  return response;
};
