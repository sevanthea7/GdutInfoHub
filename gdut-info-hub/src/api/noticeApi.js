import axios from "axios";
import { mockNoticeData } from "@/mock/mockNoticeData";

const BASE_URL = "/api";

// export const getNoticeList = async () => {
//   try {
//     const response = await axios.get(`${BASE_URL}/notices`);
//     return response.data;
//   } catch (error) {
//     console.error("获取通知列表失败:", error);
//     // 可以在这里统一处理错误，如抛出异常让页面处理
//     throw error;
//   }
// };

export const getNoticeList = async () => {
  try {
    // 开发环境使用模拟数据
    // 实际部署时注释掉下面一行，启用真实接口请求
    return mockNoticeData;

    // 真实接口请求（部署时启用）
    // const response = await axios.get(`${BASE_URL}/notices`);
    // return response.data;
  } catch (error) {
    console.error("获取通知列表失败:", error);
    throw error;
  }
};
