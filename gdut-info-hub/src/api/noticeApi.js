import axios from "axios";
// import { mockNoticeData } from "@/mock/mockNoticeData";

export const getNoticeList = async () => {
  try {
    const response = await axios.get(`/api/notices`);
    return response.data;
  } catch (error) {
    console.error("获取通知列表失败:", error);
    // 可以在这里统一处理错误，如抛出异常让页面处理
    throw error;
  }
};

// export const getNoticeList = async () => {
//   try {
//     // 开发环境使用模拟数据
//     return mockNoticeData;
//   } catch (error) {
//     console.error("获取通知列表失败:", error);
//     throw error;
//   }
// };
