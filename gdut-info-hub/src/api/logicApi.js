import axios from "axios";
import logisticsRepairMock from "@/mock/mockLogisticsRepairData";

// 模拟API请求函数
export const logicApi = {
  // 获取后勤报修通知
  getLogisticsRepair: () => {
    // 实际项目中这里会是真实的API请求
    // return axios.get('/api/logistics-repair');
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve(logisticsRepairMock);
      }, 500); // 模拟网络延迟
    });
  },
};
