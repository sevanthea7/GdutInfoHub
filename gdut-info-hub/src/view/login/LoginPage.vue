<template>
  <img src="@/assets/images/GroupLogo.png" alt="GDUT Hub" class="logoImg" />
  <div class="login-container animated-background">
    <!-- 登录卡片 -->
    <div class="glass-component login-card" ref="tiltCardRef">
      <div class="glass-content">
        <div class="login-title">
          <h2>{{ isLogin ? "Welcome Back" : "Create Account" }}</h2>
          <p>
            {{
              isLogin
                ? "Please enter your credentials to login"
                : "Please register a new account"
            }}
          </p>
        </div>

        <form
          class="login-form"
          @submit.prevent="isLogin ? handleLogin() : handleRegister()"
        >
          <div class="form-group">
            <input
              type="text"
              id="username"
              v-model="form.username"
              class="form-control"
              :placeholder="isLogin ? 'username' : 'create username'"
              @input="clearError('username')"
            />
            <div class="error-message" v-if="errors.username">
              {{ errors.username }}
            </div>
          </div>

          <div class="form-group">
            <input
              id="password"
              v-model="form.password"
              class="form-control"
              :placeholder="isLogin ? 'password' : 'create password'"
              @input="clearError('password')"
            />
            <div class="error-message" v-if="errors.password">
              {{ errors.password }}
            </div>
          </div>

          <button type="submit" class="btn" :disabled="isSubmitting">
            {{
              isSubmitting
                ? isLogin
                  ? "Signing in..."
                  : "Creating account..."
                : isLogin
                ? "Sign In"
                : "Sign Up"
            }}
          </button>

          <div class="form-footer">
            <a
              href="#"
              @click.prevent="showForgotPasswordModal = true"
              class="foot-text"
              v-if="isLogin"
              >Forgot password?</a
            >
            <a href="#" @click.prevent="toggleMode" class="foot-text">
              {{
                isLogin
                  ? "Don't have an account? Sign Up"
                  : "Already have an account? Sign In"
              }}
            </a>
          </div>
        </form>
      </div>
    </div>

    <!-- 忘记密码弹窗 -->
    <div class="modal-overlay" :class="{ active: showForgotPasswordModal }">
      <div class="modal-content">
        <div class="modal-icon info">
          <svg width="80" height="80" viewBox="0 0 24 24" fill="none">
            <path
              d="M12 16V12M12 8H12.01M22 12C22 17.5228 17.5228 22 12 22C6.47715 22 2 17.5228 2 12C2 6.47715 6.47715 2 12 2C17.5228 2 22 6.47715 22 12Z"
              stroke="currentColor"
              stroke-width="2"
              stroke-linecap="round"
              stroke-linejoin="round"
            />
          </svg>
        </div>
        <div class="modal-header">
          <h3 class="modal-title">忘记密码</h3>
        </div>
        <div class="modal-body">
          <p>请重新注册一个新账户</p>
          <p>注册原账号后密码会被重新覆盖</p>
          <p class="hint">系统暂不支持密码找回功能</p>
        </div>
        <button class="modal-close" @click="showForgotPasswordModal = false">
          &times;
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, onUnmounted, nextTick } from "vue";
import { useRouter } from "vue-router";
import { ElMessage } from "element-plus";

// 路由
const router = useRouter();

const tiltCardRef = ref(null);
const showForgotPasswordModal = ref(false);
const isSubmitting = ref(false);
const isLogin = ref(true);

// 表单数据
const form = reactive({
  username: "",
  password: "",
});

// 错误信息
const errors = reactive({
  username: "",
  password: "",
});

// 切换登录/注册模式
const toggleMode = () => {
  isLogin.value = !isLogin.value;
  // 重置表单和错误信息
  form.username = "";
  form.password = "";
  errors.username = "";
  errors.password = "";
};

// 生成随机token
const generateToken = () => {
  const characters =
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
  let token = "";
  for (let i = 0; i < 32; i++) {
    token += characters.charAt(Math.floor(Math.random() * characters.length));
  }
  return token;
};

// 从本地存储获取用户数据
const getUsersFromStorage = () => {
  const users = localStorage.getItem("users");
  return users ? JSON.parse(users) : {};
};

// 保存用户数据到本地存储
const saveUserToStorage = (username, password) => {
  const users = getUsersFromStorage();
  users[username] = { password };
  localStorage.setItem("users", JSON.stringify(users));
};

// 检查用户名是否已存在
const isUsernameExists = (username) => {
  const users = getUsersFromStorage();
  return users.hasOwnProperty(username);
};

// 验证登录凭据
const validateCredentials = (username, password) => {
  const users = getUsersFromStorage();
  return users[username] && users[username].password === password;
};

// 表单验证
const validateForm = () => {
  let isValid = true;

  // 验证用户名
  if (form.username.trim() === "") {
    errors.username = "用户名不能为空";
    isValid = false;
  } else if (!isLogin && isUsernameExists(form.username)) {
    errors.username = "用户名已存在";
    isValid = false;
  } else {
    errors.username = "";
  }

  // 验证密码
  if (form.password === "") {
    errors.password = "密码不能为空";
    isValid = false;
  } else {
    errors.password = "";
  }

  return isValid;
};

// 清除特定字段的错误
const clearError = (field) => {
  errors[field] = "";
};

// 处理注册
const handleRegister = async () => {
  if (!validateForm()) {
    return;
  }

  isSubmitting.value = true;

  try {
    // 模拟网络延迟
    await new Promise((resolve) => setTimeout(resolve, 1000));

    // 保存用户到本地存储
    saveUserToStorage(form.username, form.password);

    // 显示Element Plus成功消息
    ElMessage({
      message: "注册成功！请登录您的账户。",
      type: "success",
      duration: 3000,
      showClose: true,
    });

    // 自动切换到登录模式
    isLogin.value = true;
    // 清空密码字段，保留用户名
    form.password = "";
  } catch (error) {
    console.error("Registration error:", error);
    errors.username = "注册过程中发生错误";
  } finally {
    isSubmitting.value = false;
  }
};

// 处理登录
const handleLogin = async () => {
  if (!validateForm()) {
    return;
  }

  isSubmitting.value = true;

  try {
    // 模拟网络延迟
    await new Promise((resolve) => setTimeout(resolve, 1000));

    // 验证凭据
    if (validateCredentials(form.username, form.password)) {
      // 登录成功 - 生成token并保存
      const token = generateToken();
      localStorage.setItem("token", token);

      // 保存用户信息到sessionStorage
      sessionStorage.setItem("userId", form.username);

      // 显示登录成功消息
      ElMessage({
        message: "登录成功！正在跳转...",
        type: "success",
      });

      // 延迟跳转，让用户看到成功消息
      setTimeout(() => {
        router.push("/");
      }, 800);
    } else {
      // 显示错误信息
      errors.username = "用户名或密码错误";
      errors.password = "";
    }
  } catch (error) {
    console.error("Login error:", error);
    errors.username = "登录过程中发生错误";
  } finally {
    isSubmitting.value = false;
  }
};

// 鼠标移动事件处理
const handleMouseMove = (e) => {
  if (!tiltCardRef.value) return;

  const rect = tiltCardRef.value.getBoundingClientRect();
  const x = e.clientX - rect.left;
  const y = e.clientY - rect.top;
  const centerX = rect.width / 2;
  const centerY = rect.height / 2;
  const maxTilt = 18;

  const rotateY = ((x - centerX) / centerX) * maxTilt;
  const rotateX = -((y - centerY) / centerY) * maxTilt;

  tiltCardRef.value.style.transform = `perspective(600px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale(1.03)`;
};

// 鼠标离开事件处理
const handleMouseLeave = () => {
  if (!tiltCardRef.value) return;
  tiltCardRef.value.style.transform =
    "perspective(600px) rotateX(0deg) rotateY(0deg) scale(1)";
};

// 关闭弹窗
const closeModal = () => {
  showForgotPasswordModal.value = false;
};

// ESC键关闭弹窗
const handleKeydown = (e) => {
  if (e.key === "Escape" && showForgotPasswordModal.value) {
    closeModal();
  }
};

// 组件挂载时
onMounted(() => {
  // 添加鼠标事件监听
  if (tiltCardRef.value) {
    tiltCardRef.value.addEventListener("mousemove", handleMouseMove);
    tiltCardRef.value.addEventListener("mouseleave", handleMouseLeave);
  }

  // 添加键盘事件监听
  document.addEventListener("keydown", handleKeydown);
});

// 组件卸载时
onUnmounted(() => {
  // 移除事件监听
  if (tiltCardRef.value) {
    tiltCardRef.value.removeEventListener("mousemove", handleMouseMove);
    tiltCardRef.value.removeEventListener("mouseleave", handleMouseLeave);
  }
  document.removeEventListener("keydown", handleKeydown);
});
</script>

<style scoped>
.logoImg {
  width: 700px;
  height: auto;
  margin: 20px;
}
.animated-background {
  width: 100vw;
  height: 100vh;
  background-image: url("@/assets/images/loginBack.png");
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  position: fixed;
  top: 0;
  left: 0;
  z-index: -1;
}

.login-card {
  width: 420px;
  border-radius: 5px;
  overflow: hidden;
  background: rgba(190, 194, 229, 0.67);
  position: relative;
  transition: transform 0.3s ease;
}

.glass-content {
  position: relative;
  z-index: 3;
  padding: 2rem;
  color: white;
}

.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
}

/* Login form styles */
.login-form {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.form-group {
  display: flex;
  flex-direction: column;
  gap: 0.1rem;
}

.form-group label {
  font-size: 0.9rem;
  font-weight: 500;
  color: rgba(255, 255, 255, 0.9);
}

.form-control {
  padding: 0.75rem 1rem;
  border-radius: 8px;
  border: 1px solid rgba(255, 255, 255, 0.8);
  background-color: rgba(255, 255, 255, 0.05);
  color: white;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.form-control:focus {
  outline: none;
  border-color: rgba(255, 255, 255, 1);
  background-color: rgba(255, 255, 255, 0.15);
  box-shadow: 0 0 0 3px rgba(255, 255, 255, 0.1);
}

.form-control::placeholder {
  color: rgb(255, 255, 255);
}

/* 主按钮样式 */
.btn {
  padding: 0.75rem 0.5rem;
  border-radius: 12px;
  border: none;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #ffffff;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 1rem;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
  position: relative;
  overflow: hidden;
}

.btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
  background: linear-gradient(135deg, #764ba2 0%, #667eea 100%);
}

.btn:active:not(:disabled) {
  transform: translateY(0);
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

.btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
  transform: none;
  background: linear-gradient(135deg, #a0aec0 0%, #718096 100%);
}

.form-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 0.3rem;
  font-size: 0.85rem;
}

.form-footer a {
  color: #667eea;
  text-decoration: none;
  transition: color 0.2s ease;
}

.form-footer a:hover {
  color: #764ba2;
  text-decoration: underline;
}

.error-message {
  color: #ff6b6b;
  font-size: 0.9rem;
  margin-top: 0rem;
}

.login-title {
  margin-bottom: 1.6rem;
}

.login-title h2 {
  margin: 0;
  font-size: 1.6rem;
  font-family: "Inter", sans-serif;
  font-weight: 600;
  color: white;
}

.login-title p {
  margin: 0.5rem 0 0;
  font-size: 0.8rem;
  color: rgba(255, 255, 255, 0.9);
}

/* 弹窗样式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.6);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  opacity: 0;
  visibility: hidden;
  transition: all 0.3s ease;
}

.modal-overlay.active {
  opacity: 1;
  visibility: visible;
}

.modal-content {
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(20px);
  border-radius: 24px;
  padding: 2rem 1rem 1rem;
  width: 480px;
  max-width: 90vw;
  box-shadow: 0 25px 50px rgba(0, 0, 0, 0.15),
    0 0 0 1px rgba(255, 255, 255, 0.3);
  position: relative;
  color: #2d3748;
  text-align: center;
  transform: scale(0.9) translateY(20px);
  transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275);
  border: 1px solid rgba(255, 255, 255, 0.8);
}

.modal-overlay.active .modal-content {
  transform: scale(1) translateY(0);
}

.modal-icon {
  margin-bottom: 1.5rem;
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-icon svg {
  display: block;
}

.modal-icon.info {
  color: #667eea;
}

.modal-header {
  margin-bottom: 1.5rem;
}

.modal-title {
  margin: 0;
  font-size: 2rem;
  font-weight: 700;
  color: #2d3748;
  letter-spacing: -0.5px;
}

.modal-body {
  margin-bottom: 2.5rem;
  line-height: 1.7;
}

.modal-body p {
  margin: 1rem 0;
  color: #4a5568;
  font-size: 1.15rem;
}

.modal-body strong {
  color: #2d3748;
  font-weight: 600;
}

.hint {
  font-size: 1rem !important;
  color: #718096 !important;
  font-style: italic;
  margin-top: 1.5rem !important;
}

.modal-close {
  position: absolute;
  top: 1.5rem;
  right: 1.5rem;
  background: rgba(113, 128, 150, 0.08);
  border: none;
  color: #718096;
  font-size: 1.75rem;
  width: 40px;
  height: 40px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.2s ease;
  font-weight: 300;
}

.modal-close:hover {
  background: rgba(113, 128, 150, 0.15);
  color: #4a5568;
  transform: rotate(90deg);
}

.forgottenImg {
  margin: 0 auto;
  border-radius: 10px;
  display: block;
  height: 300px;
}

/* 响应式设计 */
@media (max-width: 480px) {
  .modal-content {
    padding: 2.5rem 2rem 2rem;
    margin: 1rem;
  }

  .modal-title {
    font-size: 1.75rem;
  }

  .modal-body p {
    font-size: 1.05rem;
  }
}

/* 按钮点击效果 */
.btn::before {
  content: "";
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.2);
  transform: translate(-50%, -50%);
  transition: width 0.3s ease, height 0.3s ease;
}

.btn:active::before {
  width: 100px;
  height: 100px;
}
</style>
