import axios from "axios";
import waterElectricServiceMock from "@/mock/mockWaterElectricData";

// 模拟API请求函数
export const waterElectricApi = {
  // 获取水电服务通知
  getWaterElectricService: () => {
    // 实际项目中这里会是真实的API请求
    // return axios.get('/api/water-electric-service');
    return new Promise((resolve) => {
      setTimeout(() => {
        resolve(waterElectricServiceMock);
      }, 500); // 模拟网络延迟
    });
  },
};
