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
      <!-- 流式响应显示区域 -->
      <div v-if="isStreaming" class="message-item system-message">
        <div class="message-time">{{ currentTime }}</div>
        <div class="message-bubble">
          {{ streamingContent }}
          <span class="cursor">|</span>
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
          :disabled="isStreaming"
        />
        <img
          v-if="userInput.trim() === '' || isStreaming"
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

// 流式响应相关状态
const isStreaming = ref(false);
const streamingContent = ref("");
const currentTime = ref("");

// 返回主页
const handleBack = () => {
  if (isStreaming.value) {
    // 可以在这里添加取消请求的逻辑
    console.log("取消流式请求");
  }
  emit("back");
};

onMounted(() => {
  if (props.content.trim()) {
    const now = new Date();
    const timeStr = formatTime(now);
    chatHistory.value.push({
      role: "user",
      content: props.content,
      time: timeStr,
    });
    sendStreamRequest(props.content);
  }
});

// 发送问题
const sendQuestion = () => {
  if (!userInput.value.trim() || isStreaming.value) return;

  const now = new Date();
  const timeStr = formatTime(now);

  chatHistory.value.push({
    role: "user",
    content: userInput.value,
    time: timeStr,
  });

  const question = userInput.value;
  userInput.value = "";

  sendStreamRequest(question);
};

// 发送流式请求
const sendStreamRequest = async (question) => {
  isStreaming.value = true;
  streamingContent.value = "";
  currentTime.value = formatTime(new Date());

  try {
    const response = await fetch("/api/stream", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ question: question.trim() }),
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    console.log("响应体:", response);
    // 处理流式响应
    await processRealStream(response);
  } catch (error) {
    console.error("流式请求错误:", error);
    streamingContent.value = "抱歉，请求过程中出现错误，请稍后重试。";
  } finally {
    completeStreamResponse();
  }
};

// 处理真正的流式数据
const processRealStream = async (response) => {
  const reader = response.body.getReader();
  const decoder = new TextDecoder("utf-8");
  let hasContent = false;

  try {
    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      const chunk = decoder.decode(value, { stream: true });

      // 检查状态标记
      if (chunk.includes("[STATUS]NO_CONTENT")) {
        streamingContent.value = "抱歉，无法理解您的问题。";
      } else if (chunk.includes("[STATUS]NO_MATCHING_CONTENT")) {
        streamingContent.value = "抱歉，未找到相关内容。";
      } else {
        hasContent = true;
        streamingContent.value += chunk;
      }

      nextTick(scrollToBottom);
    }

    // 如果整个流式过程都没有实际内容
    if (!hasContent && !streamingContent.value) {
      streamingContent.value = "抱歉，未找到相关内容。";
    }
  } finally {
    reader.releaseLock();
  }
};

// 完成流式响应
const completeStreamResponse = () => {
  if (streamingContent.value) {
    chatHistory.value.push({
      role: "system",
      content: streamingContent.value,
      time: currentTime.value,
    });
  }

  isStreaming.value = false;
  streamingContent.value = "";
  currentTime.value = "";

  nextTick(() => {
    scrollToBottom();
  });
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
}

.back img {
  width: 19px;
  height: 20px;
  margin-left: 5px;
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

/* 流式响应光标效果 */
.cursor {
  animation: blink 1s infinite;
  color: #666;
}

@keyframes blink {
  0%,
  50% {
    opacity: 1;
  }
  51%,
  100% {
    opacity: 0;
  }
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

/* 禁用状态样式 */
:deep(.el-textarea.is-disabled .el-textarea__inner) {
  background-color: #f5f7fa;
  border-color: #e4e7ed;
  color: #c0c4cc;
  cursor: not-allowed;
}
</style>
