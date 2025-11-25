<template>
  <div class="layout-container">
    <!-- 左侧菜单 -->
    <aside :class="['sidebar', { collapse: isCollapse, hidden: isMenuHidden }]">
      <!-- Logo 区域 -->
      <div class="logo">
        <img src="@/assets/images/logo.png" alt="GDUT Hub" />
        <span v-if="!isCollapse && !isMenuHidden">GDUT Hub</span>
      </div>

      <!-- 主菜单 -->
      <el-menu
        :default-active="$route.path"
        :collapse="isCollapse || isMenuHidden"
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
          <el-icon><ChatLineRound /></el-icon>
          <span>问答模式</span>
        </el-menu-item>

        <!-- 表单模式（带子菜单） -->
        <el-sub-menu index="/formMode">
          <template #title>
            <el-icon><Menu /></el-icon>
            <span>表单模式</span>
          </template>
          <el-menu-item index="/noticeAnnouncement">
            <el-icon><Document /></el-icon>
            <span>通知公告</span>
          </el-menu-item>
          <el-menu-item index="/waterElectricService">
            <el-icon><Opportunity /></el-icon>
            <span>水电服务</span>
          </el-menu-item>
          <el-menu-item index="/logisticsRepair">
            <el-icon><Tools /></el-icon>
            <span>后勤报修</span>
          </el-menu-item>
          <el-menu-item index="/academicInfo">
            <el-icon><Reading /></el-icon>
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
            <el-icon><InfoFilled /></el-icon>
            <span>关于我们</span>
            <!-- 弹窗 -->
            <transition name="fade">
              <div class="popup-mask" v-if="isPopupShow" @click="closePopup">
                <div class="popup-content" @click.stop>
                  <button class="close-btn" @click="closePopup">×</button>
                  <div class="team-info">
                    <h3>我们的团队</h3>
                    <p>团队名称：超能女人</p>
                    <p>团队规模：7 人</p>
                    <p>团队选题：广工枢纽：AI 驱动的智能校园信息助手</p>
                    <p>
                      团队特色：集数据智能、前端美学、系统性能与产品思维于一体的综合型开发团队。
                    </p>
                    <p>
                      团队目标：通过本项目，我们希望以真实需求为出发点，
                      以AI与前端开发为核心驱动，实现一个可落地、可迭代的校园智能信息平台。让“信息触手可及”，成为校园生活的日常助手。
                    </p>
                  </div>
                </div>
              </div>
            </transition>
          </div>
          <div class="footer-menu-item" @click="goToProfile">
            <el-icon><Setting /></el-icon>
            <span>个人设置</span>
          </div>
          <div class="footer-menu-item" @click="logout">
            <el-icon><SwitchButton /></el-icon>
            <span>退出登录</span>
          </div>
        </div>

        <!-- 用户信息 -->
        <div class="user-info">
          <el-avatar :size="30" :src="userAvatar" />
          <span v-if="!isCollapse && !isMenuHidden">{{ userName }}</span>
        </div>
      </div>
    </aside>

    <!-- 右侧主内容区 -->
    <main :class="['content', { expanded: isMenuHidden }]">
      <!-- 菜单切换按钮 - 只在菜单隐藏时显示 -->
      <div class="menu-toggle" v-if="isMenuHidden" @click="toggleMenu">
        <el-icon><Expand /></el-icon>
      </div>

      <!-- 路由视图，添加缓存功能 -->
      <router-view v-slot="{ Component, route }">
        <keep-alive :include="cachedComponents">
          <component
            :is="Component"
            :key="route.fullPath"
            v-if="route.meta.keepAlive"
          />
        </keep-alive>
        <component
          :is="Component"
          :key="route.fullPath"
          v-if="!route.meta.keepAlive"
        />
      </router-view>
    </main>
  </div>

  <!-- 个人设置弹窗 -->
  <el-dialog title="个人设置" v-model="isProfileVisible" width="30%">
    <!-- 修改姓名密码 -->
    <div>
      <el-form label-position="top" :model="{ name: userName }">
        <el-form-item label="账号">
          <el-input v-model="newUserName" disabled />
        </el-form-item>
        <el-form-item label="新密码">
          <el-input
            v-model="newPassword"
            type="password"
            placeholder="请输入新密码"
          />
        </el-form-item>
        <el-form-item label="确认密码">
          <el-input
            v-model="confirmPassword"
            type="password"
            placeholder="请再次输入新密码"
          />
        </el-form-item>
      </el-form>
    </div>
    <template #footer>
      <span class="dialog-footer">
        <el-button @click="isProfileVisible = false">取 消</el-button>
        <el-button type="primary" @click="comfirmProfile">确 定</el-button>
      </span>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue";
import { useRouter } from "vue-router";
import { ElMessage, ElMessageBox } from "element-plus";
import {
  ChatLineRound,
  Menu,
  Document,
  Tools,
  Reading,
  InfoFilled,
  Setting,
  SwitchButton,
  Expand,
  Opportunity,
} from "@element-plus/icons-vue";

// 用户信息，从本地获取
const userName = ref(sessionStorage.getItem("userId") || "未知用户");
const userAvatar = ref(
  "https://cube.elemecdn.com/3/7c/3ea6beec64369c2642b92c6726f1epng.png"
);

// 菜单状态
const isCollapse = ref(false);
const isMenuHidden = ref(false);

// 需要缓存的组件列表
const cachedComponents = ref([
  "IndexQuestionAnswer",
  "NoticeAnnouncement",
  "WaterElectricService",
  "LogisticsRepair",
  "AcademicInfo",
]);

// 响应式断点 - 只在屏幕缩小时隐藏
const breakpoints = {
  sm: 768, // 小屏幕：隐藏菜单
  md: 1024, // 中等屏幕：折叠菜单
  lg: 1440, // 大屏幕：正常显示
};

const isProfileVisible = ref(false);
const newPassword = ref("");
const confirmPassword = ref("");
const newUserName = ref(userName.value);

const router = useRouter();

// 检查屏幕尺寸并更新菜单状态
const checkScreenSize = () => {
  const width = window.innerWidth;

  if (width < breakpoints.sm) {
    // 小屏幕：完全隐藏菜单
    isMenuHidden.value = true;
    isCollapse.value = false;
  } else if (width < breakpoints.md) {
    // 中等屏幕：折叠菜单（只显示图标）
    isMenuHidden.value = false;
    isCollapse.value = true;
  } else {
    // 大屏幕：正常显示完整菜单
    isMenuHidden.value = false;
    isCollapse.value = false;
  }
};

// 切换菜单显示/隐藏
const toggleMenu = () => {
  isMenuHidden.value = !isMenuHidden.value;
};

// 关于我们
const isPopupShow = ref(false); // 定义弹窗状态（默认隐藏）
const goToAbout = () => {
  // 修改原有的 goToAbout 函数
  isPopupShow.value = true; // 核心：点击后显示弹窗
};
const closePopup = () => {
  // 关闭弹窗函数
  isPopupShow.value = false;
};

// 个人设置
const goToProfile = () => {
  isProfileVisible.value = true;
};

// 确认修改个人信息
const comfirmProfile = () => {
  if (newPassword.value.trim() === "") {
    ElMessage.error("密码不能为空");
    return;
  }
  if (newPassword.value !== confirmPassword.value) {
    ElMessage.error("两次输入密码不一致");
    return;
  }

  saveUserToStorage(newUserName.value, newPassword.value);
  isProfileVisible.value = false;
  ElMessage.success("修改成功，请重新登录！");
  router.push("/login");
};

// 从本地存储获取用户数据
const getUsersFromStorage = () => {
  const users = localStorage.getItem("users");
  return users ? JSON.parse(users) : {};
};

const saveUserToStorage = (newUserName, newPassword) => {
  const users = getUsersFromStorage();
  const oldUserData = users[userName.value];

  if (!oldUserData) {
    ElMessage.error("用户数据异常，请重新登录");
    return;
  }

  sessionStorage.setItem("userId", newUserName);
  userName.value = newUserName;

  const finalPassword = newPassword !== "" ? newPassword : oldUserData.password;

  const newUserData = { password: finalPassword };

  if (newUserName === userName.value) {
    users[newUserName] = newUserData;
  } else {
    users[newUserName] = newUserData;
    delete users[userName.value];
  }

  localStorage.setItem("users", JSON.stringify(users));
  // 清楚本地缓存的用户信息
  sessionStorage.removeItem("userId");
};

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

// 生命周期
onMounted(() => {
  checkScreenSize();
  window.addEventListener("resize", checkScreenSize);
});

onUnmounted(() => {
  window.removeEventListener("resize", checkScreenSize);
});
</script>

<style scoped>
.layout-container {
  display: flex;
  min-height: 100vh;
  overflow: hidden;
}

/* 侧边栏样式 */
.sidebar {
  width: 18%;
  min-width: 200px;
  background-color: #f3f4f6 !important;
  transition: all 0.3s ease;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  position: fixed;
  height: 100vh;
  z-index: 1000;
}

/* 折叠状态 - 只显示图标 */
.sidebar.collapse {
  width: 64px;
  min-width: 64px;
}

/* 隐藏状态 */
.sidebar.hidden {
  transform: translateX(-100%);
  width: 0;
  min-width: 0;
  opacity: 0;
}

.logo {
  display: flex;
  align-items: center;
  padding: 20px;
  font-size: 25px;
  font-weight: bold;
  color: #333;
  border-bottom: 1px solid #ddd;
  white-space: nowrap;
  overflow: hidden;
  height: 80px;
  box-sizing: border-box;
}

.logo img {
  width: 45px;
  height: 42px;
  margin-right: 10px;
  flex-shrink: 0;
}

/* 主菜单样式 */
.custom-menu {
  border-right: none;
  flex: 1;
  transition: all 0.3s ease;
}

/* 确保图标在折叠状态下正常显示 */
.custom-menu :deep(.el-menu-item),
.custom-menu :deep(.el-sub-menu__title) {
  display: flex;
  align-items: center;
}

.custom-menu :deep(.el-icon) {
  flex-shrink: 0;
  margin-right: 12px;
}

/* 折叠状态下调整图标间距 */
.sidebar.collapse .custom-menu :deep(.el-icon) {
  margin-right: 0;
}

/* 自定义选中状态 */
.custom-menu :deep(.el-menu-item.is-active) {
  border-left: 4px solid #0056b3;
  background-color: rgba(0, 86, 179, 0.12) !important;
  transition: all 0.3s ease;
}

.custom-menu :deep(.el-sub-menu .el-menu-item.is-active) {
  border-left: 4px solid #0056b3;
  background-color: rgba(0, 86, 179, 0.12) !important;
}

/* 底部区域 */
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
  white-space: nowrap;
  overflow: hidden;
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
  padding: 8px 0;
  color: #404040;
  display: flex;
  align-items: center;
  gap: 8px;
  white-space: nowrap;
  transition: color 0.3s ease;
}

.footer-menu-item:hover {
  color: #0056b3;
}

/* 折叠时隐藏文字但保持图标 */
.sidebar.collapse .el-menu-item span,
.sidebar.collapse .el-sub-menu__title span,
.sidebar.collapse .logo span,
.sidebar.collapse .user-info span,
.sidebar.collapse .footer-menu-item span {
  display: none;
}

/* 确保折叠状态下图标居中 */
.sidebar.collapse .custom-menu :deep(.el-menu-item),
.sidebar.collapse .custom-menu :deep(.el-sub-menu__title) {
  justify-content: center;
  padding-left: 0 !important;
}

/* 主内容区域 */
.content {
  flex: 1;
  margin-left: 18%;
  background-color: #ffffff;
  transition: all 0.3s ease;
  position: relative;
  min-height: 100vh;
}

/* 折叠状态下的内容区域 */
.sidebar.collapse ~ .content {
  margin-left: 64px;
}

/* 菜单隐藏时的内容区域 */
.content.expanded {
  margin-left: 0;
  width: 100%;
}

/* 菜单切换按钮 */
.menu-toggle {
  position: fixed;
  top: 20px;
  left: 20px;
  z-index: 999;
  background: #fff;
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 8px;
  cursor: pointer;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 36px;
  height: 36px;
}

.menu-toggle:hover {
  background: #f5f5f5;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

/* 响应式设计 */
@media (max-width: 767px) {
  .sidebar:not(.hidden) {
    width: 100%;
    z-index: 2000;
  }

  .content {
    margin-left: 0;
  }
}

@media (min-width: 768px) and (max-width: 1023px) {
  .sidebar {
    width: 64px;
  }

  .content {
    margin-left: 64px;
  }
}

@media (min-width: 1024px) {
  .sidebar {
    width: 18%;
  }

  .content {
    margin-left: 18%;
  }
}

/*弹窗样式*/
.trigger-btn {
  padding: 10px 20px;
  font-size: 16px;
  background: #42b983;
  color: #fff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  transition: background 0.3s;
}
.trigger-btn:hover {
  background: #359469;
}
.popup-mask {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}
.popup-content {
  width: 90%;
  max-width: 500px;
  background: #fff;
  border-radius: 8px;
  padding: 24px;
  position: relative;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}
.close-btn {
  position: absolute;
  top: 16px;
  right: 16px;
  font-size: 20px;
  border: none;
  background: transparent;
  cursor: pointer;
  color: #999;
}
.close-btn:hover {
  color: #333;
}
.team-info h3 {
  margin: 0 0 16px 0;
  color: #2c3e50;
  text-align: center;
}
.team-info p {
  margin: 8px 0;
  color: #666;
  line-height: 1.6;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}
.popup-content {
  transition: transform 0.3s ease;
}
.fade-enter-from .popup-content,
.fade-leave-to .popup-content {
  transform: scale(0.9);
}
</style>
