<script setup>
import { onMounted } from "vue"; // 正确的生命周期钩子是 onMounted

// 使用 onMounted 生命周期钩子
onMounted(() => {});
</script>

<template>
  <router-view></router-view>
</template>

<style scoped></style>
