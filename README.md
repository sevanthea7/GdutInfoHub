# GdutInfoHub

广工枢纽是一个面向校园生活的智能信息聚合平台，旨在帮助师生快速获取校内的各类通知公告、水电服务、后勤报修、教务信息等内容。

项目通过自动化爬虫定期从学校通知网及相关部门网站抓取信息，构建统一的校园知识库，并结合大语言模型API，实现基于自然语言的智能问答与信息检索。

我们希望让繁杂分散的校园信息实现了自动化聚合与智能化服务，使师生无需频繁浏览多个网站即可快速获取所需内容。



## 1. 安装

### 1）脚本安装

该方式适合 **大多数用户**，无需逐条执行命令，只需运行脚本即可完成依赖安装和项目启动。

#### 1️⃣ 使用前准备

请确保本机已安装以下基础环境：

- Node.js
- Python（建议 3.9+）
- npm（随 Node.js 安装）
- pip（随 Python 安装）

#### 2️⃣ 克隆项目

```bash
git clone https://github.com/sevanthea7/GdutInfoHub.git
```

并在克隆的文件夹中打开cmd。

#### 3️⃣ 运行环境初始化脚本（首次使用时执行）

该脚本用于 **安装前后端所有依赖**，**只需首次运行一次**。

##### Windows

```powershell
scripts\setup.ps1
```

##### Linux / macOS

```bash
bash scripts/setup.sh
```

#### 4️⃣ 启动项目（每次运行项目时使用）

当依赖已安装完成后，使用启动脚本即可运行项目。

##### Windows

```powershell
scripts\start.ps1
```

##### Linux / macOS

```bash
bash scripts/start.sh
```

**启动后访问：http://localhost:5173**

#### 📌 脚本使用说明

| 脚本                   | 作用           | 何时使用                      |
| ---------------------- | -------------- | ----------------------------- |
| `setup.ps1 / setup.sh` | 安装所有依赖   | **首次运行项目 / 更换环境时** |
| `start.ps1 / start.sh` | 启动前后端服务 | **每次启动项目时**            |

------

### 2. 手动安装

该方式适合希望完全理解项目结构或进行调试、学习的用户。

### 1️⃣ 克隆项目

```bash
git clone https://github.com/sevanthea7/GdutInfoHub.git
```

### 2️⃣ 安装依赖（首次使用）

#### 前端依赖

```bash
cd GdutInfoHub/gdut-info-hub
npm install
```

#### 后端依赖

```bash
pip install volcengine-python-sdk[ark] jieba flask
```

### 3️⃣ 启动项目

#### 启动前端

```bash
cd GdutInfoHub/gdut-info-hub
npm run dev
```

#### 启动后端

```bash
python -m src.app.app
```

------

## 3. 项目结构说明

```
GdutInfoHub
├── docs/          	  # 文档文件
├── gdut-info-hub/    # 前端项目
├── scripts/          # 一键部署与启动脚本
├── src/              # 后端源码
├── tests/            # 测试文件
└── README.md
```

------

## 4. 说明

- **推荐普通用户使用脚本方式**，更省时省力
- **手动方式更适合学习和调试**
- 两种方式效果完全一致，仅操作流程不同

欢迎提出 Issue 或 PR，一起完善 GdutInfoHub 🚀