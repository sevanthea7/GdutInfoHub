# 软工小组作业

### 1、前端项目拉取与启动步骤
克隆项目到本地
git clone https://github.com/sevanthea7/GdutInfoHub.git

进入项目目录
cd GdutInfoHub/gdut-info-hub
安装依赖
```bash
# 如果使用 npm
npm install

# 如果使用 yarn
yarn install

# 如果使用 pnpm
pnpm install
```

启动开发 npm run dev, 启动成功后，控制台会显示访问地址, 在浏览器中打开该地址即可查看项目。

前端项目结构说明
```bash
GdutInfoHub/
├── src/                 # 源代码目录
│   ├── assets/         # 静态资源
│   ├── components/     # Vue 组件
│   ├── views/          # 页面组件
│   ├── router/         # 路由配置
│   ├── store/          # 状态管理
│   └── main.js         # 入口文件
├── public/             # 公共资源
├── package.json        # 项目配置和依赖
└── vite.config.js      # Vite 构建配置
```


2. 后端相关库安装

**环境配置**
```bash
pip install volcengine-python-sdk[ark]
pip install jieba
```


**接口测试**
```bash
python -m src.app.app
```
正常启动时会输出类似下方内容。
```text
Flask starting...
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on http://127.0.0.1:5000
```


python的端口测试命令
```bash
python -m src.app.test_app
```
