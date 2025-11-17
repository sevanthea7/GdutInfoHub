import { createRouter, createWebHistory } from "vue-router";

const Index = () => import("@/components/index.vue");
const _404 = () => import("@/view/404.vue");
const NoticeAnnouncement = () => import("@/components/noticeAnnouncement.vue");
const WaterElectricService = () =>
  import("@/components/waterElectricService.vue");
const LogisticsRepair = () => import("@/components/logisticsRepair.vue");
const AcademicInfo = () => import("@/components/academicInfo.vue");

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: "/login", component: () => import("@/view/login/LoginPage.vue") },
    {
      path: "/",
      component: () => import("@/view/layout/Layout.vue"),
      redirect: "/index",
      children: [
        { path: "/index", component: Index },
        { path: "/noticeAnnouncement", component: NoticeAnnouncement },
        { path: "/waterElectricService", component: WaterElectricService },
        { path: "/logisticsRepair", component: LogisticsRepair },
        { path: "/academicInfo", component: AcademicInfo },
      ],
    },
    {
      path: "/:pathMatch(.*)*",
      name: "NotFound",
      component: _404,
    },
  ],
});

router.beforeEach((to, from, next) => {
  const userId = sessionStorage.getItem("userId");
  console.log("userId", userId);
  if (to.path === "/login" && userId) {
    next("/");
  } else if (!userId && to.path !== "/login") {
    next("/login");
  } else {
    next();
  }
});

export default router;
