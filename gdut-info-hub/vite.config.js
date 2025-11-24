import { defineConfig, loadEnv } from "vite";
import path from "path";
import vue from "@vitejs/plugin-vue";

// https://vitejs.dev/config/
export default defineConfig(({ mode, command }) => {
  const env = loadEnv(mode, process.cwd());
  const { VITE_APP_ENV } = env;
  return {
    // 自定义根路径 例如 "/web/" "/app/"
    base: VITE_APP_ENV === "development" ? "/" : "/",
    plugins: [vue()],
    server: {
      port: 5173,
      host: true,
      open: true,
      proxy: {
        "/api": {
          target: "http://10.21.56.119:30222", //后端目标服务器
          changeOrigin: true, //允许跨域请求
          // rewrite: (path) => path.replace(/^\/api/, ''), //将所有含/api路径的，去掉/api转发给服务器
        },
      },
    },
    resolve: {
      // https://cn.vitejs.dev/config/#resolve-alias
      alias: {
        // 设置路径
        "~": path.resolve(__dirname, "./"),
        // 设置别名
        "@": path.resolve(__dirname, "./src"),
        //__dirname,是一个成员，用来动态获取当前文件模块所属的绝对路径（不包含文件名）
        //__filename，可以动态获取当前文件夹的绝对路径（包含文件名）
      },
      // https://cn.vitejs.dev/config/#resolve-extensions
      extensions: [".mjs", ".js", ".ts", ".jsx", ".tsx", ".json", ".vue"],
    },
  };
});
