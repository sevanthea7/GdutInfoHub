<template>
  <div class="container">
    <div class="header" v-if="!isQuestionMode">
      <div class="title">{{ welcome }} {{ username }} ^_^</div>
      <div class="input-with-suffix">
        <el-input
          v-model="textarea"
          type="textarea"
          :rows="6"
          placeholder="请输入内容...（eg.2025寒假放假安排）"
          :show-word-limit="true"
          @keydown.enter.prevent="handleEnter"
        />
        <img
          v-if="textarea.trim() === ''"
          :src="noSend"
          class="custom-suffix-icon"
        />
        <img
          v-else
          :src="send"
          class="custom-suffix-icon"
          @click="handleIconClick"
        />
      </div>
    </div>

    <div class="feature-section" v-if="!isQuestionMode">
      <h2>GDUT Hub 广工枢纽</h2>
      <p>
        一个面向校园生活的智能信息聚合平台，旨在帮助师生快速获取校内的各类通知公告、水电服务、后勤报修、教务信息等内容。我们希望让繁杂分散的校园信息实现自动化聚合与智能化服务，使师生无需频繁浏览多个网站即可快速获取所需内容。
      </p>
      <div class="features-grid">
        <div
          class="feature-item"
          v-for="(item, index) in features"
          :key="index"
          @click="$router.push(item.goTo)"
        >
          <div class="icon-container">
            <img :src="item.icon" :alt="item.title" />
          </div>
          <div class="feature-title">{{ item.title }}</div>
          <div class="feature-desc">{{ item.description }}</div>
        </div>
      </div>
    </div>
  </div>
  <questionAnswerMode
    :content="textarea"
    v-if="isQuestionMode"
    @back="handleBack"
  />
</template>

<script setup>
import { ref, onMounted, onActivated, onDeactivated, nextTick } from "vue";
import noSend from "../assets/images/noSend.png";
import send from "../assets/images/send.png";
import noticeIcon from "../assets/images/通知公告.png";
import waterElectricityIcon from "../assets/images/水电服务.png";
import maintenanceIcon from "../assets/images/后勤报修.png";
import academicIcon from "../assets/images/教务信息.png";
import questionAnswerMode from "./questionAnswerMode.vue";
defineOptions({
  name: "IndexQuestionAnswer",
});
const featureIcons = {
  notice: noticeIcon,
  waterElectricity: waterElectricityIcon,
  maintenance: maintenanceIcon,
  academic: academicIcon,
};

const username = ref("");
const textarea = ref("");
const welcome = ref("");
const isQuestionMode = ref(false);

const handleIconClick = () => {
  isQuestionMode.value = true;
};

const handleBack = () => {
  isQuestionMode.value = false;
  // 清空输入框内容
  textarea.value = "";
};

onMounted(() => {
  console.log("IndexQuestionAnswer mounted");
  username.value = sessionStorage.getItem("userId") || "未知用户";
  updateGreeting();
});

onActivated(() => {
  console.log("IndexQuestionAnswer activated");
});

onDeactivated(() => {
  console.log("IndexQuestionAnswer deactivated");
});

const updateGreeting = () => {
  const currentTime = new Date();
  const hour = currentTime.getHours();
  if (hour < 12) {
    welcome.value = "早上好！";
  } else if (hour < 18) {
    welcome.value = "下午好！";
  } else {
    welcome.value = "晚上好！";
  }
};

// 定义功能模块数据
const features = ref([
  {
    title: "通知公告",
    description: "查询考试、放假安排通知等",
    icon: featureIcons.notice,
    goTo: "/noticeAnnouncement",
  },
  {
    title: "水电服务",
    description: "查询水电方面通知",
    icon: featureIcons.waterElectricity,
    goTo: "/waterElectricService",
  },
  {
    title: "后勤报修",
    description: "查询报修通知",
    icon: featureIcons.maintenance,
    goTo: "/logisticsRepair",
  },
  {
    title: "教务信息",
    description: "查询考试安排、教学活动等",
    icon: featureIcons.academic,
    goTo: "/academicInfo",
  },
]);

// enter键处理
const handleEnter = (event) => {
  // 如果同时按下了 Shift + Enter，则允许换行
  if (event.shiftKey) {
    return;
  }

  // 检查内容是否为空
  if (!textarea.value.trim()) {
    ElMessage.warning("请输入内容");
    return;
  }

  // 发送内容
  handleIconClick();
};
</script>

<style scoped>
/* 保持原有样式不变 */
.container {
  padding: 40px 80px 0 80px;
  color: #404040;
  width: 68vw;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.header {
  .title {
    font-size: 28px;
    font-weight: bold;
    font-family: FZYaSongS-B-GB;
    margin-bottom: 10px;
  }

  .input-with-suffix {
    position: relative;
    width: 62vw;
  }

  .input-with-suffix .custom-suffix-icon {
    position: absolute;
    right: 15px;
    bottom: 15px;
    width: 28px;
    cursor: pointer;
    z-index: 10;
  }
}

.feature-section {
  width: 93%;
}

.feature-section h2 {
  font-size: 24px;
  font-weight: bold;
  color: #0056b3;
  margin-top: 8%;
}

.feature-section p {
  font-size: 14px;
  color: #666;
  margin: 20px 0;
  border-left: #0056b3 5px solid;
  padding: 15px;
  background-color: #f0f5fb;
}

.features-grid {
  display: flex;
  justify-content: space-around;
}

.feature-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 10px;
  width: calc(25% - 20px);
  transition: transform 0.2s ease;
}

.feature-item:hover {
  transform: translateY(-5px);
}

.feature-item .icon-container {
  width: 90px;
  height: 90px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.feature-item img {
  max-width: 100%;
  max-height: 100%;
}

.feature-title {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 5px;
}

.feature-desc {
  font-size: 14px;
  color: #666;
  text-align: center;
}

:deep(.el-textarea__inner) {
  border-radius: 10px;
}
</style>
