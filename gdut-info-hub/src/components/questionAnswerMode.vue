<template>
  <!-- 顶部导航 -->
  <div class="header">
    <div class="title">新对话</div>

    <div class="back" @click="handleBack">
      <img src="../assets/images/back.png" alt="返回图标" />
      <el-button type="text" class="back-btn"> 返回 </el-button>
    </div>
  </div>
  <div class="qa-container">
    <!-- 对话内容区域 -->
    <div class="chat-content">
      <div
        v-for="(item, index) in chatHistory"
        :key="index"
        :class="[
          'message-item',
          item.role === 'user' ? 'user-message' : 'system-message',
        ]"
      >
        <div class="message-time">{{ item.time }}</div>
        <div class="message-bubble">
          {{ item.content }}
        </div>
      </div>
    </div>

    <!-- 输入框区域 -->
    <div class="input-area">
      <div class="input-with-suffix">
        <el-input
          v-model="userInput"
          type="textarea"
          :rows="6"
          placeholder="请输入内容...（eg.2025寒假放假安排）"
          :show-word-limit="true"
          @keyup.enter="sendQuestion"
        />
        <img
          v-if="userInput.trim() === ''"
          :src="noSend"
          class="custom-suffix-icon"
        />
        <img
          v-else
          :src="send"
          class="custom-suffix-icon"
          @click="sendQuestion"
        />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from "vue";
import noSend from "../assets/images/noSend.png";
import send from "../assets/images/send.png";
import { onActivated, onDeactivated } from "vue";

// 组件激活时的逻辑
onActivated(() => {
  console.log("QuestionAnswerMode activated");
  // 可以在这里恢复滚动位置或其他状态
});

// 组件停用时的逻辑
onDeactivated(() => {
  console.log("QuestionAnswerMode deactivated");
  // 可以在这里保存状态
});
// 接收父组件传递的初始问题内容
const props = defineProps({
  content: {
    type: String,
    default: "",
  },
});

// 定义 emit 事件，用于通知父组件关闭问答模式
const emit = defineEmits(["back"]);

// 聊天历史记录
const chatHistory = ref([]);

// 用户输入框内容
const userInput = ref("");

// 模拟数据：预设答案（可根据实际后端接口替换）
const mockAnswers = {
  "2025寒假放假安排": `
各位同学：
2025年寒假自2025年1月10日（星期五）起至2月28日（星期五）止，共49天。
下学期于2025年3月1日（星期六）报到注册，3月3日（星期一）正式上课。
请同学们合理安排假期时间，注意安全，按时返校。
`,
  新生报到: `
各位2024级新生及家长：
新生报到时间为9月1日 - 2日（8:00-18:00），报到地点为学校体育馆。
需携带身份证、录取通知书、档案材料及近期1寸免冠照片3张。
逾期未报到将按规定处理。咨询电话：XXX-XXXXXXX。
`,
  水电服务: `
校园水电服务提醒：
1. 每月1-5日为抄表期，请勿在此期间进行大功率电器操作。
2. 如遇停水停电，请关注"广工后勤"公众号或拨打后勤服务中心电话：020-XXXXXXX。
3. 学生宿舍电费可通过"校园一卡通"APP在线充值。
`,
  教务信息: `
教务处重要通知：
本学期期末考试将于2025年1月6日开始，具体安排请登录教务系统查询。
补考安排另行通知，请及时关注学院公告。
`,
  1: `我收到了你的输入。`,
};

// 返回主页
const handleBack = () => {
  emit("back");
};

onMounted(() => {
  // 初始化：将父组件传入的内容作为第一条用户消息
  if (props.content.trim()) {
    const now = new Date();
    const timeStr = formatTime(now);
    chatHistory.value.push({
      role: "user",
      content: props.content,
      time: timeStr,
    });
    // 自动回复
    setTimeout(() => {
      const answer = getMockAnswer(props.content);
      chatHistory.value.push({
        role: "system",
        content: answer,
        time: formatTime(new Date()),
      });
      // 滚动到底部
      nextTick(() => {
        scrollToBottom();
      });
    }, 800);
  }
});

// 发送问题
const sendQuestion = () => {
  if (!userInput.value.trim()) return;

  const now = new Date();
  const timeStr = formatTime(now);

  // 添加用户消息
  chatHistory.value.push({
    role: "user",
    content: userInput.value,
    time: timeStr,
  });

  // 清空输入框
  const question = userInput.value;
  userInput.value = "";

  // 模拟异步回复
  setTimeout(() => {
    const answer = getMockAnswer(question);
    chatHistory.value.push({
      role: "system",
      content: answer,
      time: formatTime(new Date()),
    });
    // 滚动到底部
    nextTick(() => {
      scrollToBottom();
    });
  }, 800);
};

// 根据关键词匹配模拟答案
const getMockAnswer = (question) => {
  for (const key in mockAnswers) {
    if (question.includes(key)) {
      return mockAnswers[key];
    }
  }
  return "不好意思，我还没接入接口，没有检索到相关关键词。请重试。";
};

// 格式化时间显示
const formatTime = (date) => {
  const year = date.getFullYear();
  const month = String(date.getMonth() + 1).padStart(2, "0");
  const day = String(date.getDate()).padStart(2, "0");
  const hours = String(date.getHours()).padStart(2, "0");
  const minutes = String(date.getMinutes()).padStart(2, "0");
  const seconds = String(date.getSeconds()).padStart(2, "0");
  return `${year}/${month}/${day} ${hours}:${minutes}:${seconds}`;
};

// 滚动到底部
const scrollToBottom = () => {
  const container = document.querySelector(".chat-content");
  if (container) {
    container.scrollTop = container.scrollHeight;
  }
};
</script>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
  width: 90%;
  height: 5vh;
  padding: 0 5%;
  margin-top: -15px;
}

.title {
  font-size: 20px;
  font-weight: 400;
  font-family: FZYaSongS-B-GB;
  color: #404040;
}

.back-btn {
  color: #0056b3;
  font-size: 16px;
}

.back {
  display: flex;
  flex-direction: column;
  align-items: center;
  cursor: pointer;

  img {
    width: 19px;
    height: 20px;
    margin-left: 5px;
  }
}
.qa-container {
  height: 90vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
}

.chat-content {
  width: 80%;
  height: 65vh;
  padding: 10px 0;
  /* 内容区域滚动条不显示 */
  overflow-y: auto;
  scrollbar-width: none;
  -ms-overflow-style: none;
}

.message-item {
  margin: 15px 0;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}

.user-message {
  align-items: flex-end;
}

.message-time {
  font-size: 12px;
  color: #999;
  margin-bottom: 5px;
}

.user-message .message-time {
  text-align: right;
}

.system-message .message-time {
  text-align: left;
}

.message-bubble {
  max-width: 70%;
  padding: 12px 15px;
  border-radius: 15px;
  line-height: 1.5;
  word-break: break-word;
  white-space: pre-wrap;
}

.user-message .message-bubble {
  background-color: #f0f5fb;

  border-top-right-radius: 0;
}

.system-message .message-bubble {
  background-color: #f5f5f5;
  border: 1px solid #ddd;
  border-top-left-radius: 0;
}

.input-area {
  width: 70%;
  position: fixed;
  bottom: 20px;
}

.input-with-suffix {
  position: relative;
}

.input-with-suffix .custom-suffix-icon {
  position: absolute;
  right: 15px;
  bottom: 15px;
  width: 28px;
  cursor: pointer;
  z-index: 10;
}

/* 隐藏滚动条（可选） */
.chat-content::-webkit-scrollbar {
  width: 6px;
}

.chat-content::-webkit-scrollbar-thumb {
  background-color: #ccc;
  border-radius: 10px;
}

.chat-content::-webkit-scrollbar-thumb:hover {
  background-color: #aaa;
}

:deep(.el-textarea__inner) {
  border-radius: 10px;
  font-size: 14px;
  line-height: 1.5;
  resize: none;
}

:deep(.el-textarea .el-input__count) {
  background: transparent;
}
</style>
