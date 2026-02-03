import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
})

// 响应拦截器
api.interceptors.response.use(
  (response) => response.data,
  (error) => {
    console.error('API Error:', error)
    return Promise.reject(error)
  }
)

export default api

// 题目相关 API
export const problemApi = {
  // 获取题目列表
  getList: (params?: {
    difficulty?: string
    category?: string
    status?: string
    search?: string
    tag_id?: number
    page?: number
    page_size?: number
  }) => api.get('/problems', { params }),

  // 获取题目详情
  getDetail: (id: number) => api.get(`/problems/${id}`),

  // 获取所有分类
  getCategories: () => api.get('/problems/categories'),
}

// 进度相关 API
export const progressApi = {
  // 一键完成（推荐使用）
  complete: (problemId: number) => api.post(`/progress/${problemId}/complete`),

  // 手动更新进度（高级选项）
  update: (problemId: number, data: { status: string; mastery_level: number }) =>
    api.put(`/progress/${problemId}`, data),

  // 获取进度
  get: (problemId: number) => api.get(`/progress/${problemId}`),
}

// 笔记相关 API
export const noteApi = {
  // 创建或更新笔记
  save: (data: {
    problem_id: number
    approach?: string
    code?: string
    language?: string
    time_complexity?: string
    space_complexity?: string
    key_points?: string
  }) => api.post('/notes', data),

  // 获取笔记
  get: (problemId: number) => api.get(`/notes/${problemId}`),

  // 删除笔记
  delete: (noteId: number) => api.delete(`/notes/${noteId}`),
}

// 标签相关 API
export const tagApi = {
  // 获取所有标签
  getList: () => api.get('/tags'),

  // 创建标签
  create: (data: { name: string; color: string }) => api.post('/tags', data),

  // 删除标签
  delete: (tagId: number) => api.delete(`/tags/${tagId}`),

  // 为题目添加标签
  addToProblem: (problemId: number, tagId: number) =>
    api.post(`/tags/${problemId}/tags/${tagId}`),

  // 从题目移除标签
  removeFromProblem: (problemId: number, tagId: number) =>
    api.delete(`/tags/${problemId}/tags/${tagId}`),
}

// 复习相关 API
export const reviewApi = {
  // 获取今日待复习
  getToday: () => api.get('/reviews/today'),

  // 获取所有复习计划
  getAll: (completed?: boolean) => api.get('/reviews', { params: { completed } }),

  // 标记复习完成
  complete: (reviewId: number) => api.put(`/reviews/${reviewId}/complete`),
}

// 统计相关 API
export const statsApi = {
  // 获取统计数据
  get: () => api.get('/stats'),
}
