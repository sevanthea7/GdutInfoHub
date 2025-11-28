<template>
  <div class="notice-page">
    <!-- 顶部导航 -->
    <div class="nav-bar">
      <div class="title-group">
        <div class="title-with-icon">
          <img
            src="@/assets/images/通知公告1.png"
            alt="通知公告图标"
            class="notice-icon"
          />
          <h2>通知公告</h2>
        </div>
      </div>
      <div class="nav-tabs">
        <button
          v-for="(tab, index) in tabList"
          :key="index"
          :class="{ active: activeTab === index }"
          @click="switchTab(index)"
        >
          {{ tab.name }}
        </button>
      </div>
    </div>

    <!-- 分割线 -->
    <div class="divider"></div>

    <!-- 通知列表容器 -->
    <div class="notice-container">
      <!-- 加载中提示 -->
      <div v-if="loading" class="empty-tip">加载中...</div>

      <!-- 无数据提示 -->
      <div v-else-if="currentPageData.length === 0" class="empty-tip">
        暂无相关通知
      </div>

      <!-- 通知列表 -->
      <div class="notice-list" v-else>
        <div
          class="notice-item"
          v-for="(item, index) in currentPageData"
          :key="item.url"
        >
          <div class="notice-content-wrapper">
            <!-- 标题区域（可跳转） -->
            <a
              :href="item.url"
              target="_blank"
              class="notice-title"
              @click.stop
            >
              <span class="bullet">•</span>
              <span>{{ item.title }}</span>
            </a>

            <!-- 通知内容（显示部分） -->
            <div class="notice-content">
              {{ getPreviewContent(item.content) }}
            </div>
          </div>

          <div class="notice-meta">
            <span class="date">{{ item.date }}</span>
            <span class="department">{{ item.department }}</span>
          </div>

          <!-- 条目分割线 -->
          <div
            class="item-divider"
            v-if="index < currentPageData.length - 1"
          ></div>
        </div>
      </div>
    </div>

    <!-- 动态分页控件 -->
    <div class="pagination" v-if="totalPages > 0">
      <button @click="prevPage" :disabled="currentPage <= 1">上页</button>
      <button
        v-for="page in visiblePages"
        :key="page"
        :class="{ active: page === currentPage, ellipsis: page === '...' }"
        @click="goToPage(page)"
        :disabled="page === '...'"
      >
        {{ page }}
      </button>
      <button @click="nextPage" :disabled="currentPage >= totalPages">
        下页
      </button>
      <span class="page-info">
        共 {{ totalItems }} 条，第 {{ currentPage }}/{{ totalPages }} 页
      </span>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from "vue";
// 导入API函数
import { getNoticeList } from "@/api/noticeApi";

// 每页显示条数
const PAGE_SIZE = ref(6);

// 动态选项卡数据（与后端label对应）
const tabList = ref([
  { name: "校园通知", label: "校园通知" },
  { name: "学术活动", label: "学术活动" },
  { name: "行政通知", label: "行政通知" },
  { name: "社区公告", label: "社区公告" },
]);

// 当前激活的选项卡索引
const activeTab = ref(0);

// 所有通知数据（从接口获取）
const allNoticeData = ref([]);
// 加载状态
const loading = ref(false);

// 获取通知数据
const fetchNoticeData = async () => {
  try {
    loading.value = true;
    const result = await getNoticeList(); // 调用API函数
    if (result.code === 200) {
      allNoticeData.value = result.data.items || [];
    } else {
      console.error("获取通知失败:", result.msg);
      allNoticeData.value = [];
    }
  } catch (error) {
    console.error("接口请求失败:", error);
    allNoticeData.value = [];
  } finally {
    loading.value = false;
  }
};

// 页面挂载时获取数据
onMounted(() => {
  fetchNoticeData();
});

// 获取内容预览（截取前100个字符）
const getPreviewContent = (content) => {
  if (!content) return "";
  // 去除换行符
  const plainText = content.replace(/\n/g, " ");
  // 截取前100个字符并添加省略号
  if (plainText.length > 100) {
    return plainText.substring(0, 100) + "...";
  }
  return plainText;
};

// 当前分类的所有通知数据（通过label筛选）
const filteredNotices = computed(() => {
  const currentLabel = tabList.value[activeTab.value].label;
  return allNoticeData.value.filter((notice) => notice.label === currentLabel);
});

// 总数据条数
const totalItems = computed(() => filteredNotices.value.length);

// 总页数
const totalPages = computed(() =>
  Math.ceil(totalItems.value / PAGE_SIZE.value)
);

// 当前页码
const currentPage = ref(1);

// 当前页显示的数据
const currentPageData = computed(() => {
  const startIndex = (currentPage.value - 1) * PAGE_SIZE.value;
  const endIndex = startIndex + PAGE_SIZE.value;
  return filteredNotices.value.slice(startIndex, endIndex);
});

// 可见页码
const visiblePages = computed(() => {
  const pages = [];
  const total = totalPages.value;
  const current = currentPage.value;

  if (total <= 5) {
    for (let i = 1; i <= total; i++) {
      pages.push(i);
    }
    return pages;
  }

  pages.push(1);

  if (current > 3) {
    pages.push("...");
  }

  const start = Math.max(2, current - 1);
  const end = Math.min(total - 1, current + 1);

  for (let i = start; i <= end; i++) {
    pages.push(i);
  }

  if (current < total - 2) {
    pages.push("...");
  }

  pages.push(total);

  return pages;
});

// 切换选项卡
const switchTab = (index) => {
  activeTab.value = index;
  currentPage.value = 1;
};

// 上一页
const prevPage = () => {
  if (currentPage.value > 1) {
    currentPage.value--;
  }
};

// 下一页
const nextPage = () => {
  if (currentPage.value < totalPages.value) {
    currentPage.value++;
  }
};

// 跳转指定页码
const goToPage = (page) => {
  if (typeof page === "number" && page >= 1 && page <= totalPages.value) {
    currentPage.value = page;
  }
};

// 监听总页数变化
watch(totalPages, () => {
  if (currentPage.value > totalPages.value) {
    currentPage.value = Math.max(1, totalPages.value);
  }
});
</script>

<style scoped>
.notice-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  font-family: "Microsoft YaHei", sans-serif;
}

.nav-bar {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  gap: 20px;
  margin-bottom: 0;
  flex-wrap: wrap;
  padding-bottom: 0;
}

.title-with-icon {
  display: flex;
  align-items: center;
  gap: 8px;
  padding-bottom: 2px;
}

.notice-icon {
  width: 20px;
  object-fit: contain;
  margin-top: 25px;
}

.title-group h2 {
  font-size: 24px;
  color: #0056b3;
  margin: 0;
  font-weight: 600;
  margin-top: 25px;
}

/*选项栏*/

.nav-tabs {
  display: flex;
  gap: 15px;
  border-bottom: none;
  padding-bottom: 0;
  align-items: flex-end;
}

.nav-tabs button {
  background: none;
  border: none;
  padding: 8px 16px 6px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.3s ease;
  outline: none;
  color: #404040;
}

.nav-tabs button:hover:not(.active) {
  color: #0056b3;
  background-color: white;
}

.nav-tabs button.active {
  color: #0056b3;
  font-weight: 600;
  background-color: white;
  border-bottom: 3px solid #0056b3;
  padding-bottom: 6px;
}
/*分割线*/
.divider {
  width: 100%;
  height: 1px;
  background-color: #aeaeb2;
  margin-bottom: 15px;
  margin-top: 0;
}

/*内容框*/

.notice-container {
  border: 2px solid #e6e6e6;
  padding-left: 15px;
  padding-right: 15px;
  padding-top: 3px;
  padding-bottom: 3px;
  background-color: #ffffff;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
  margin-bottom: 30px;
  margin-top: 30px;
  width: 100%;
  box-sizing: border-box;
}

.empty-tip {
  text-align: center;
  padding: 40px 0;
  color: #718096;
  font-size: 14px;
}

.notice-list {
  display: flex;
  flex-direction: column;
}

.notice-item {
  display: flex;
  justify-content: space-between;
  padding: 5px 0;
  position: relative;
}

/* 内容区域 */
.notice-content-wrapper {
  flex: 1;
  margin-right: 10px;
  min-width: 0;
}

/* 标题链接样式 */
.notice-title {
  display: flex;
  align-items: center;
  font-weight: 600;
  font-size: 16px;
  color: #404040;
  line-height: 1.4;
  text-decoration: none;
  cursor: pointer;
}

.notice-title:hover span:not(.bullet) {
  text-decoration: underline; /* 仅文字部分显示下划线 */
}

.notice-title .bullet {
  color: #0056b3;
  margin-right: 8px;
  font-size: 18px;
  flex-shrink: 0;
}

/* 通知内容样式 */
.notice-content {
  color: #b3b3b3;
  font-size: 14px;
  line-height: 1.6;
  margin-left: 14px;
}

/* 右侧元信息区域 */
.notice-meta {
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  justify-content: flex-start;
  width: 180px;
  flex-shrink: 0;
  gap: 5px;
}

.notice-meta .date {
  font-size: 13px;
  color: #595959;
  font-weight: 500;
}

.notice-meta .department {
  font-size: 12px;
  color: #595959;
}

/* 条目分割线 */
.item-divider {
  position: absolute;
  bottom: 0;
  left: 0;
  width: 100%;
  height: 1px;
  background-color: #e6e6e6;
}

/* 分页样式 */
.pagination {
  display: flex;
  justify-content: center;
  gap: 8px;
  align-items: center;
  flex-wrap: wrap;
}

.pagination button {
  padding: 6px 12px;
  border: 1px solid #e2e8f0;
  background: #ffffff;
  cursor: pointer;
  border-radius: 4px;
  transition: all 0.3s ease;
  color: #4a5568;
}

.pagination button:hover:not(.active):not(:disabled):not(.ellipsis) {
  border-color: #0056b3;
  color: #0056b3;
}

.pagination button.active {
  background: #0056b3;
  color: #ffffff;
  border-color: #0056b3;
}

.pagination button:disabled {
  cursor: not-allowed;
  opacity: 0.5;
  background: #f7fafc;
  color: #a0aec0;
  border-color: #e2e8f0;
}

.pagination button.ellipsis {
  cursor: default;
  background: transparent;
  border: none;
  padding: 6px 4px;
}

.page-info {
  margin-left: 15px;
  font-size: 12px;
  color: #718096;
}

/* 响应式适配 */
@media (max-width: 768px) {
  .nav-bar {
    flex-direction: column;
    align-items: flex-start;
    padding-bottom: 5px;
  }

  .nav-tabs {
    width: 100%;
    justify-content: flex-start;
    overflow-x: auto;
    padding-bottom: 5px;
  }

  .nav-tabs button.active {
    border-bottom: 2px solid #0056b3;
    margin-bottom: -1px;
  }

  .notice-item {
    flex-direction: column;
    padding: 15px 0;
  }

  .notice-content-wrapper {
    margin-right: 0;
    margin-bottom: 15px;
  }

  .notice-meta {
    width: 100%;
    align-items: flex-start;
    flex-direction: row;
    gap: 15px;
  }

  .page-info {
    margin-left: 0;
    margin-top: 10px;
    width: 100%;
    text-align: center;
  }
}
</style>
