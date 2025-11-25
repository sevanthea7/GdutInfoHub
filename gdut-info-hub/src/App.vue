<script setup>
import { ref } from "vue";

// 管理需要缓存的组件
const cachedComponents = ref(["IndexQuestionAnswer"]);
</script>

<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<style scoped></style>
