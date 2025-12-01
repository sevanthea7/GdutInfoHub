import { defineConfig, loadEnv } from "vite";
import path from "path";
import vue from "@vitejs/plugin-vue";
import { viteMockServe } from "vite-plugin-mock";

export default defineConfig(({ mode, command }) => {
  const env = loadEnv(mode, process.cwd());
  const { VITE_APP_ENV } = env;

  return {
    base: VITE_APP_ENV === "development" ? "/" : "/",
    plugins: [
      vue(),
      viteMockServe({
        mockPath: "mock",
        enable: command === "serve" && VITE_APP_ENV === "development", // 仅开发环境启用mock
        logger: false, // 关闭mock日志（可选）
      }),
    ],
    server: {
      port: 5173,
      host: true,
      open: true,
      proxy: {
        "/api": {
          target: "http://127.0.0.1:5000",
          changeOrigin: true,
          // 后端接口带/api前缀，无需rewrite！
          // 如果后端接口不带/api，才需要：rewrite: (path) => path.replace(/^\/api/, "")
        },
      },
    },
    resolve: {
      alias: {
        "~": path.resolve(__dirname, "./"),
        "@": path.resolve(__dirname, "./src"),
      },
      extensions: [".mjs", ".js", ".ts", ".jsx", ".tsx", ".json", ".vue"],
    },
  };
});
