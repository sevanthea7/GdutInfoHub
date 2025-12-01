import axios from "axios";
import academicInfoMock from "@/mock/mockAcademicData";

// 模拟API请求函数
export const noticeApi = {
  // 获取教务信息通知
  getAcademicInfo: () => {
    // 实际项目中这里会是真实的API请求
    // return axios.get('/api/academic-info');
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve(academicInfoMock);
      }, 500); // 模拟网络延迟
    });
  },
};
