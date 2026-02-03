import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'Dashboard',
      component: () => import('../views/Dashboard/index.vue'),
      meta: { title: '仪表盘' }
    },
    {
      path: '/problems',
      name: 'Problems',
      component: () => import('../views/Problems/index.vue'),
      meta: { title: '题目列表' }
    },
    {
      path: '/problems/:id',
      name: 'ProblemDetail',
      component: () => import('../views/ProblemDetail/index.vue'),
      meta: { title: '题目详情' }
    },
    {
      path: '/review',
      name: 'Review',
      component: () => import('../views/Review/index.vue'),
      meta: { title: '复习计划' }
    },
    {
      path: '/stats',
      name: 'Stats',
      component: () => import('../views/Stats/index.vue'),
      meta: { title: '统计分析' }
    },
  ]
})

// 路由标题
router.beforeEach((to, _from, next) => {
  document.title = `${to.meta.title || 'LeetCode'} - LeetCode Hot 100`
  next()
})

export default router
