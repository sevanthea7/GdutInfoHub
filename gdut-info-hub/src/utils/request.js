import axios from 'axios'
//import { useUserStore } from '@/stores'
import { ElMessage } from 'element-plus'
import router from '@/router'

axios.defaults.headers['Content-Type'] = 'application/json;charset=utf-8'
const instance = axios.create({
  // TODO 1. 基础地址，超时时间
  baseURL: import.meta.env.VITE_APP_URL, //请求URL = baseURL + apiURL
  timeout: 10000,
})
// 请求拦截器
instance.interceptors.request.use(
  (config) => {
    return config
  },
  (err) => Promise.reject(err)
)

// 响应拦截器
instance.interceptors.response.use(
  (res) => {
    // 先检查 res.data 是否存在
    if (res.data && res.data.code === 200) {
      return Promise.resolve(res.data)
    } else {
      // 如果 res.data 不符合预期，给出错误提示
      ElMessage.error(res.data?.message || '服务异常')
      return Promise.reject(res.data)
    }
  },
  (err) => {
    // 错误对象检查：确保 err.response 存在
    if (err.response) {
      // 处理 401 错误，跳转到登录
      if (err.response.status === 401) {
        router.push('/login')
      }

      // 给出错误提示
      ElMessage.error(err.response.data?.message || '服务异常')
    } else {
      // 如果没有 response，可能是网络错误等情况
      ElMessage.error('请求失败，网络错误或服务器没有响应')
    }
    return Promise.reject(err)
  }
)

export default instance
