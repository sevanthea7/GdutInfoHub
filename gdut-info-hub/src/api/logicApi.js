import axios from "axios";
// import logisticsRepairMock from "@/mock/mockLogisticsRepairData";

// // 模拟API请求函数
// export const logicApi = {
//   // 获取后勤报修通知
//   getLogisticsRepair: () => {
//     // 实际项目中这里会是真实的API请求
//     // return axios.get('/api/logistics-repair');
//     return new Promise((resolve) => {
//       setTimeout(() => {
//         resolve(logisticsRepairMock);
//       }, 500); // 模拟网络延迟
//     });
//   },
// };
// 模拟API请求函数
export const logicApi = {
  // 获取教务信息通知
  getLogisticsRepair: async () => {
    try {
      // 实际项目中这里会是真实的API请求
      const response = await axios.get("/api/maintainance_notices");
      // 统一处理响应格式，适配页面层的预期（{ code, data, msg }）
      const result = response.data;

      // 标准化返回格式
      return {
        code: result.code ?? result.data?.code ?? 500,
        data: result.data ?? result, // 兼容数据在根节点或data节点的情况
        msg: result.msg ?? result.data?.msg ?? "请求异常",
      };
    } catch (error) {
      // 统一处理请求错误（网络错误、超时等）
      return {
        code: 500,
        data: null,
        msg: error.message || "网络请求失败",
      };
    }
  },
};
