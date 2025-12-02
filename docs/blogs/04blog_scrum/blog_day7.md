# Day7 Scrum冲刺博客

## 1. 团队会议

==todo补充会议照片==

### 1）大前天已完成的工作

- 前端
  - 完成了问答模式与栏目模式的前后端对接
- 后端
  - 完成了适配更多网站的爬虫程序
  - 重新整理接口与知识库，与前端完成对接
- 测试
  - 完成多个基础功能的测试代码

### 2）今天计划完成的工作

- 前端
  - 根据测试结果优化代码
- 后端
  - 根据测试结果优化代码
- 测试
  - 完成全部测试，撰写测试文档

### 3）工作中遇到的困难

- 前端
  - 跨域导致前端无法正常请求接口
- 后端
  - 暂无
- 测试
  - 暂无

## 2. 项目燃尽图

今日为第七天，已完成所有工作。

![](https://sevanthea7.oss-cn-beijing.aliyuncs.com/QGworks/202512021712003.png)

## 3.代码/文档签入记录

- 今日签入记录

  ![](https://sevanthea7.oss-cn-beijing.aliyuncs.com/QGworks/202512022139861.png)

- 签入记录链接：https://github.com/sevanthea7/GdutInfoHub/commits/main/

- 相关联issue见commit记录中`#`后链接内容

- 接口文档与返回格式文档见 `docs/api_doc.md` 与 `docs/return_doc.md`

## 4. 运行截图

- 前端

  - 修正了水电服务栏目api设置错误

    ```javascript
import axios from "axios";
    // 模拟API请求函数
    export const waterElectricApi = {
      // 获取教务信息通知
      getWaterElectricService: async () => {
        try {
          // 实际项目中这里会是真实的API请求
          const response = await axios.get("/api/service_notices");
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
    ```
    
    ![](https://sevanthea7.oss-cn-beijing.aliyuncs.com/QGworks/202512022142786.png)
    
  
- 后端

  - 今日无主要内容修改

- 测试

  完成了测试文档，见 `docs\test_docs\测试文档.md`。

  

## 5. 每人每日总结

- 前端
  - 吴佳童：今日负责的部分内容均已完成，包括前期对接功能的收尾工作，没有新增任务需要处理。继续保持与后端、测试的对齐，为下一阶段迭代做准备。
  - 张洁：今天根据测试同学给出的反馈，对前端页面的数据处理逻辑和交互细节进行了优化，主要集中在请求与响应结构的细化、状态管理与渲染逻辑的修正。已解决部分影响用户体验的小问题，使整体界面处理更加稳定。
  - 李恺凝：已完成今日所有负责的内容，包括与前端页面相关的 UI 细节支持，没有额外问题阻塞工作。
- 后端
  - 王韵清：今日的相关任务均已全部完成，主要工作集中在代码整理与测试反馈的同步处理，无阻塞情况。
  - 曾钰仪：已完成今日全部任务，包括对时间处理逻辑和后端接口的校对与优化，没有遇到新的问题。
  - 徐伊彤：今日完成了所有后端所需的修订内容，包含对接口逻辑与知识库结构的维护调整，确保与测试结果一致。
- 测试
  - 戴军霞：今日完成了全部测试工作，包含所有功能点的系统性验证，并按计划撰写了测试文档初稿。整体进展顺利，没有遇到技术层面的阻碍。

