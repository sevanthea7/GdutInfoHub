<template>
  <div class="layout-container">
    <!-- 左侧菜单 -->
    <aside :class="['sidebar', isCollapse ? 'collapse' : '']">
      <!-- Logo 区域 -->
      <div class="logo">
        <img src="@/assets/images/logo.png" alt="GDUT Hub" />
        <span v-if="!isCollapse">GDUT Hub</span>
      </div>

      <!-- 主菜单 -->
      <el-menu
        :default-active="$route.path"
        :collapse="isCollapse"
        :default-openeds="['/formMode', '/index']"
        background-color="#f5f5f5"
        text-color="#333"
        active-text-color="#409EFF"
        unique-opened
        router
        class="custom-menu"
      >
        <!-- 问答模式 -->
        <el-menu-item index="/index">
          <el-icon><chat-line-round /></el-icon>
          <span>问答模式</span>
        </el-menu-item>

        <!-- 表单模式（带子菜单） -->
        <el-sub-menu index="/formMode">
          <template #title>
            <el-icon><menu /></el-icon>
            <span>表单模式</span>
          </template>
          <el-menu-item index="/noticeAnnouncement">
            <el-icon><document /></el-icon>
            <span>通知公告</span>
          </el-menu-item>
          <el-menu-item index="/waterElectricService">
            <el-icon><water-drop /></el-icon>
            <span>水电服务</span>
          </el-menu-item>
          <el-menu-item index="/logisticsRepair">
            <el-icon><tools /></el-icon>
            <span>后勤报修</span>
          </el-menu-item>
          <el-menu-item index="/academicInfo">
            <el-icon><reading /></el-icon>
            <span>教务信息</span>
          </el-menu-item>
        </el-sub-menu>
      </el-menu>

      <!-- 底部用户信息 & 设置 -->
      <div class="footer-section">
        <div
          class="footer-menu"
          background-color="#f5f5f5"
          text-color="#333"
          active-text-color="#409EFF"
          :router="false"
        >
          <div class="footer-menu-item" @click="goToAbout">
            <el-icon><info-filled /></el-icon>
            <span>关于我们</span>
          </div>
          <div class="footer-menu-item" @click="goToProfile">
            <el-icon><setting /></el-icon>
            <span>个人设置</span>
          </div>
          <div class="footer-menu-item" @click="logout">
            <el-icon><switch-button /></el-icon>
            <span>退出登录</span>
          </div>
        </div>

        <!-- 用户信息 -->
        <div class="user-info">
          <el-avatar :size="30" :src="userAvatar" />
          <span v-if="!isCollapse">{{ userName }}</span>
        </div>
      </div>
    </aside>

    <!-- 右侧主内容区 -->
    <main class="content">
      <router-view />
    </main>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { ElMessage, ElMessageBox } from "element-plus";

// 用户信息，从本地获取
const userName = ref(sessionStorage.getItem("userId") || "未知用户");
const userAvatar = ref(
  "https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png"
); // 默认头像

// 菜单折叠状态
const isCollapse = ref(false);

// 路由
const router = useRouter();

// 关于我们
const goToAbout = () => {};

// 个人设置
const goToProfile = () => {};

// 退出登录
const logout = () => {
  ElMessageBox.confirm("确定要退出登录吗？", "提示", {
    confirmButtonText: "确定",
    cancelButtonText: "取消",
    type: "warning",
  }).then(() => {
    sessionStorage.removeItem("userId");
    router.push("/login");
    ElMessage.success("已退出登录");
  });
};
</script>

<style scoped>
.layout-container {
  display: flex;
  height: 100vh;
  overflow: hidden;
}

.sidebar {
  width: 240px;
  background-color: #f5f5f5;
  transition: width 0.3s ease;
  overflow-y: auto;
  border-right: 1px solid #ddd;
  display: flex;
  flex-direction: column;
}

.sidebar.collapse {
  width: 64px;
}

.logo {
  display: flex;
  align-items: center;
  padding: 20px;
  font-size: 25px;
  font-weight: bold;
  color: #333;
  border-bottom: 1px solid #ddd;
}

.logo img {
  width: 45px;
  height: 42px;
  margin-right: 10px;
}

/* 主菜单样式 */
.custom-menu {
  border-right: none;
  flex: 1; /* 让主菜单占据剩余空间 */
}

/* 自定义选中状态：添加蓝色边框 */
.custom-menu .el-menu-item.is-active {
  border-left: 4px solid #0056b3;
  background-color: rgba(0, 86, 179, 0.12) !important;
  transition: all 0.3s ease;
}

/* 折叠时的选中状态 */
.sidebar.collapse .custom-menu .el-menu-item.is-active {
  margin: 4px 2px; /* 折叠时边距更小 */
}

/* 子菜单项的选中状态 */
.custom-menu .el-sub-menu .el-menu-item.is-active {
  border-left: 4px solid #0056b3;
  background-color: rgba(0, 86, 179, 0.12) !important;
}

/* 底部用户信息与菜单区域 */
.footer-section {
  color: #404040;
  cursor: pointer;
  padding: 15px 20px;
  border-top: 1px solid #ddd;
  background-color: #f5f5f5;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 0;
}

.user-info span {
  font-size: 14px;
  color: #333;
}

.footer-menu {
  border-top: 1px solid #eee;
}
.footer-menu-item {
  font-size: 16px;
  padding: 5px 0;
  color: #404040;
}

.footer-menu-item:hover {
  color: #0056b3;
}
/* 折叠时隐藏文字 */
.sidebar.collapse .el-menu-item span,
.sidebar.collapse .el-sub-menu__title span {
  display: none;
}

.sidebar.collapse .el-menu-item i,
.sidebar.collapse .el-sub-menu__title i {
  margin-right: 0;
}
</style>
