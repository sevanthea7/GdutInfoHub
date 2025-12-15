# 广工枢纽

| 这个项目属于哪个课程 | [课程链接](https://edu.cnblogs.com/campus/gdgy/Class34Grade23ComputerScience) |
| -------------------- | ------------------------------------------------------------ |
| 作业要求             | [作业链接](https://edu.cnblogs.com/campus/gdgy/Class34Grade23ComputerScience/homework/13483) |
| 作业的目标           | 通过7天的敏捷冲刺，完成Alpha阶段的项目实现                   |
| Github链接           | [仓库地址](https://github.com/sevanthea7/GdutInfoHub)        |

## 一、 冲刺博客汇总

[Day1 Scrum冲刺博客](https://www.cnblogs.com/sevanthea7/p/19266012)

[Day2 Scrum冲刺博客](https://www.cnblogs.com/sevanthea7/p/19270425)

[Day3 Scrum冲刺博客](https://www.cnblogs.com/sevanthea7/p/19274842)

[Day4 Scrum冲刺博客](https://www.cnblogs.com/sevanthea7/p/19279732)

[Day5 Scrum冲刺博客](www.cnblogs.com/sevanthea7/p/19284297)

[Day6 Scrum冲刺博客](https://www.cnblogs.com/sevanthea7/p/19287617)

[Day7 Scrum冲刺博客](https://www.cnblogs.com/sevanthea7/p/19299424)



## 二、主要功能展示

广工枢纽（GDUT Hub）是广东工业大学校园智能信息聚合平台，支持师生获取通知公告、水电服务、后勤报修、教务信息等校内内容，实现校园信息的聚合与智能化服务。

### 1. 登录页面

#### 功能流程

1. 用户在对应输入框填写学号 / 工号、密码
2. 点击 “Sign In” 按钮提交身份验证请求
3. 验证通过后跳转至系统首页

![](https://sevanthea7.oss-cn-beijing.aliyuncs.com/QGworks/202512022155865.png)



##### 1.1  输入密码登录

1. 用户填写用户名、密码至对应输入框
2. 点击 “Sign Up” 按钮提交注册请求
3. ![](https://sevanthea7.oss-cn-beijing.aliyuncs.com/QGworks/202512022155867.png)



##### 1.2  忘记密码

1. 登录界面点击 “Forget password?” 触发弹窗
2. 查看弹窗内的密码找回说明
3. 点击关闭按钮（×）返回注册界面

![](https://sevanthea7.oss-cn-beijing.aliyuncs.com/QGworks/202512022155866.png)



### 2.  登录成功进入首页

1. 可通过侧边栏 / 快捷入口访问对应校园服务功能
2. 在查询输入框提交内容（如假期安排）以获取对应信息

![](https://sevanthea7.oss-cn-beijing.aliyuncs.com/QGworks/202512022155864.png)



#### 2.1 自然语言问答

用户输入问题，系统结合知识库与大模型生成回答

==注：因为安全考虑api key无法上传github，使用问答模式需要找团队成员要api key==

![](https://sevanthea7.oss-cn-beijing.aliyuncs.com/QGworks/202512022155874.png)



#### 2.2 信息栏目

1. 跳转到相关关键词条目，如校园通知、水电服务、教务公告、后勤通知等
2. 按类型分类：校园通知、水电服务、教务公告、后勤通知等。
3. 详情查看：点击通知标题查看完整内容。
4. 关键词搜索：可按关键词、时间区间筛选通知。
5. 通知更新：结合爬虫实时更新水电服务公告。
6. 考试安排：提供各类考试、比赛时间、地点及报名信息。
7. 公告与提醒：教务通知、选课提醒等集中显示。

##### 2.2.1 通知公告

![](https://sevanthea7.oss-cn-beijing.aliyuncs.com/QGworks/202512022155872.png)
![](https://sevanthea7.oss-cn-beijing.aliyuncs.com/QGworks/202512022155870.png)

![](https://sevanthea7.oss-cn-beijing.aliyuncs.com/QGworks/202512022155871.png)

![](https://sevanthea7.oss-cn-beijing.aliyuncs.com/QGworks/202512022247039.png)

##### 2.2.2 水电服务

![](https://sevanthea7.oss-cn-beijing.aliyuncs.com/QGworks/202512022142786.png)

##### 2.2.3 后勤服务

![](https://sevanthea7.oss-cn-beijing.aliyuncs.com/QGworks/202512022155869.png)

##### 2.2.4 教务信息

![](https://sevanthea7.oss-cn-beijing.aliyuncs.com/QGworks/202512022155863.png)

### 3. 关于我们

关于我们团队详细介绍

![](https://sevanthea7.oss-cn-beijing.aliyuncs.com/QGworks/202512022155861.png)

### 4. 个人设置

对账号进行密码修改

![](https://sevanthea7.oss-cn-beijing.aliyuncs.com/QGworks/202512022155873.png)

### 5.  退出登录

完成操作后退出登录

![](https://sevanthea7.oss-cn-beijing.aliyuncs.com/QGworks/202512022155868.png)



## 三、团队小结

![](https://sevanthea7.oss-cn-beijing.aliyuncs.com/QGworks/202512022207732.png)

本次为期 **7 天的敏捷冲刺开发**以快速迭代、小步快跑的方式推进项目，从前端、后端到测试团队均保持高频沟通与协作，在限定时间内完成了主要功能模块的构建与联调。整体来看，本次冲刺目标达成度高、问题暴露及时、解决效率良好，为后续稳定迭代奠定了基础。

#### 1. 整体进展概述

在本次冲刺周期中，团队通过每日会议同步进度，采用“短周期交付-快速反馈”的模式实现了稳步推进。核心成果包括：

- **前端**
  - 完成问答模式与栏目模式的界面开发与前后端对接
  - 完成数据过滤、分页显示、栏目页构建等核心逻辑
  - 依据测试反馈进行了多轮优化，提高页面交互与稳定性
- 后端
  - 完成多站点爬虫程序的适配与增强
  - 优化数据清洗与时间解析等底层处理逻辑
  - 完成问答接口与栏目接口的整理、调试和联调
  - 对接口格式、知识库结构进行了统一与规范化
- **测试**
  - 覆盖主要功能的测试代码开发与手工测试
  - 发现并推动解决多处前端和后端的细节问题
  - 输出测试文档，为后续迭代提供质量基线

### 2. 团队协作情况

团队在冲刺期间保持了顺畅、高效的协作：

- 前后端沟通紧密：接口规范通过多轮确认逐步收敛，减少对接阻塞。
- 问题响应及时：测试阶段发现的错误均能当天反馈、当天修复或给出解决方案。
- UI 与逻辑开发同步推进：UI 与前端保持高频互动，有效减少返工量。
- 代码规范统一化改进明显：经过测试的格式检查后，整体代码可读性显著提升。

### 3. 冲刺中遇到的主要问题

- 跨域问题影响前后端联调效率，需要反复调整配置，同时实现流式输出需要学习新的知识。
- 部分爬虫站点结构不统一导致适配逻辑复杂度增加，以及时间字段格式不统一，所以数据清洗阶段需要多层处理。
- 前后端接口调整，带来了少量返工与兼容性修改。

虽然存在阻碍，但均在冲刺周期内成功解决，没有影响整体交付节奏。

### 4. 团队表现亮点

- 任务自驱能力强：各成员都能独立完成模块并主动跟进测试反馈。
- 节奏把控良好：关键任务均在预期时间内完成，少有延误。
- 沟通透明：问题都能在当日会议中说明，并迅速形成解决策略。
- 质量意识增强：代码格式、接口规范、数据校验等方面明显进步。

### 5. 冲刺成果总结

本次 7 天敏捷冲刺成功交付了：

- 问答模式与栏目浏览模式、登录设置等核心功能
- 多源网站爬虫与数据清洗体系
- 前后端联调成功的核心接口
- 全功能覆盖的基础测试用例与测试文档

系统现已具备基础可用性，为后续功能扩展奠定了稳定基础。

### 6. 下一步计划

基于本次冲刺成果，下一阶段将重点推进：

- 增强问答模式的多轮能力与异常处理
- 扩充爬虫范围并完善自动更新机制
- 优化前端交互体验（搜索、筛选、分页等）
- 深化测试覆盖，包括压力测试与异常流测试
- 进行小规模用户试用，收集体验反馈

