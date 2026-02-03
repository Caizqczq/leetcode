<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { statsApi } from '../../api'
import { useReviewStore } from '../../stores/review'

const router = useRouter()
const reviewStore = useReviewStore()

const loading = ref(true)
const stats = ref<any>(null)

onMounted(async () => {
  await Promise.all([
    fetchStats(),
    reviewStore.fetchTodayReviews(),
  ])
  loading.value = false
})

async function fetchStats() {
  try {
    stats.value = await statsApi.get()
  } catch (error) {
    console.error('获取统计失败', error)
  }
}

// 计算待复习总数
const totalReviews = computed(() => {
  return reviewStore.todayReviews.length + reviewStore.overdueReviews.length
})

// 跳转页面
function goToProblems() {
  router.push('/problems')
}

function goToReview() {
  router.push('/review')
}

function goToStats() {
  router.push('/stats')
}

function goToProblem(problemId: number) {
  router.push(`/problems/${problemId}`)
}

// 获取难度样式类
const getDifficultyClass = (difficulty: string) => {
  return `difficulty-${difficulty?.toLowerCase()}`
}
</script>

<template>
  <div class="dashboard" v-loading="loading">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1 class="page-title">欢迎回来！</h1>
      <p class="page-subtitle">继续你的 LeetCode Hot 100 刷题之旅</p>
    </div>

    <!-- 统计卡片 -->
    <div class="stats-row" v-if="stats">
      <div class="card stat-card" @click="goToProblems">
        <div class="stat-icon" style="background: linear-gradient(135deg, #409EFF 0%, #66b1ff 100%)">
          <el-icon size="28"><List /></el-icon>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.completed_count }} / {{ stats.total_problems }}</div>
          <div class="stat-label">已完成题目</div>
        </div>
        <div class="stat-progress">
          <div class="progress-bar">
            <div class="progress-bar-inner" :style="{ width: stats.completion_rate + '%' }"></div>
          </div>
          <span class="progress-text">{{ stats.completion_rate }}%</span>
        </div>
      </div>

      <div class="card stat-card" @click="goToReview">
        <div class="stat-icon" :style="{ background: totalReviews > 0 ? 'linear-gradient(135deg, #E6A23C 0%, #f5c06e 100%)' : 'linear-gradient(135deg, #67C23A 0%, #95d475 100%)' }">
          <el-icon size="28"><Clock /></el-icon>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ totalReviews }}</div>
          <div class="stat-label">待复习题目</div>
        </div>
        <el-tag v-if="reviewStore.overdueReviews.length > 0" type="danger" size="small">
          {{ reviewStore.overdueReviews.length }} 道已逾期
        </el-tag>
        <el-tag v-else-if="totalReviews === 0" type="success" size="small">
          已完成
        </el-tag>
      </div>

      <div class="card stat-card" @click="goToStats">
        <div class="stat-icon" style="background: linear-gradient(135deg, #67C23A 0%, #95d475 100%)">
          <el-icon size="28"><TrendCharts /></el-icon>
        </div>
        <div class="stat-content">
          <div class="stat-value">{{ stats.status_stats.mastered }}</div>
          <div class="stat-label">已掌握题目</div>
        </div>
      </div>
    </div>

    <!-- 主内容区 -->
    <div class="main-row">
      <!-- 今日复习 -->
      <div class="card review-section">
        <div class="card-header">
          <h3 class="card-title">
            <el-icon><Bell /></el-icon>
            今日复习任务
          </h3>
          <el-button type="primary" link @click="goToReview">查看全部</el-button>
        </div>

        <div v-if="totalReviews === 0" class="empty-state">
          <el-icon size="40" color="#67C23A"><CircleCheck /></el-icon>
          <p>太棒了！今日复习任务已完成</p>
        </div>

        <div v-else class="review-list">
          <!-- 逾期题目 -->
          <div
            v-for="review in reviewStore.overdueReviews.slice(0, 3)"
            :key="'overdue-' + review.id"
            class="review-item overdue"
            @click="goToProblem(review.problem?.id!)"
          >
            <div class="review-info">
              <span class="review-title">{{ review.problem?.leetcode_id }}. {{ review.problem?.title_cn }}</span>
              <span class="review-meta">
                <span class="difficulty-tag" :class="getDifficultyClass(review.problem?.difficulty || '')">
                  {{ review.problem?.difficulty === 'Easy' ? '简单' : review.problem?.difficulty === 'Medium' ? '中等' : '困难' }}
                </span>
                <el-tag type="danger" size="small">逾期</el-tag>
              </span>
            </div>
            <el-icon><ArrowRight /></el-icon>
          </div>

          <!-- 今日题目 -->
          <div
            v-for="review in reviewStore.todayReviews.slice(0, 3)"
            :key="'today-' + review.id"
            class="review-item"
            @click="goToProblem(review.problem?.id!)"
          >
            <div class="review-info">
              <span class="review-title">{{ review.problem?.leetcode_id }}. {{ review.problem?.title_cn }}</span>
              <span class="review-meta">
                <span class="difficulty-tag" :class="getDifficultyClass(review.problem?.difficulty || '')">
                  {{ review.problem?.difficulty === 'Easy' ? '简单' : review.problem?.difficulty === 'Medium' ? '中等' : '困难' }}
                </span>
              </span>
            </div>
            <el-icon><ArrowRight /></el-icon>
          </div>
        </div>
      </div>

      <!-- 难度分布 -->
      <div class="card difficulty-section" v-if="stats">
        <h3 class="card-title">
          <el-icon><PieChart /></el-icon>
          题目难度分布
        </h3>
        
        <div class="difficulty-stats">
          <div class="difficulty-item">
            <div class="difficulty-header">
              <span class="difficulty-tag difficulty-easy">简单</span>
              <span class="difficulty-count">{{ stats.difficulty_stats.easy }} 题</span>
            </div>
            <div class="progress-bar">
              <div class="progress-bar-inner easy" :style="{ width: (stats.difficulty_stats.easy / stats.total_problems * 100) + '%' }"></div>
            </div>
          </div>
          
          <div class="difficulty-item">
            <div class="difficulty-header">
              <span class="difficulty-tag difficulty-medium">中等</span>
              <span class="difficulty-count">{{ stats.difficulty_stats.medium }} 题</span>
            </div>
            <div class="progress-bar">
              <div class="progress-bar-inner medium" :style="{ width: (stats.difficulty_stats.medium / stats.total_problems * 100) + '%' }"></div>
            </div>
          </div>
          
          <div class="difficulty-item">
            <div class="difficulty-header">
              <span class="difficulty-tag difficulty-hard">困难</span>
              <span class="difficulty-count">{{ stats.difficulty_stats.hard }} 题</span>
            </div>
            <div class="progress-bar">
              <div class="progress-bar-inner hard" :style="{ width: (stats.difficulty_stats.hard / stats.total_problems * 100) + '%' }"></div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 状态统计 -->
    <div class="card status-section" v-if="stats">
      <h3 class="card-title">
        <el-icon><DataAnalysis /></el-icon>
        刷题状态统计
      </h3>
      
      <div class="status-grid status-grid-3">
        <div class="status-item">
          <div class="status-value">{{ stats.status_stats.not_started }}</div>
          <div class="status-label">未开始</div>
        </div>
        <div class="status-item">
          <div class="status-value" style="color: #409EFF">{{ stats.status_stats.in_progress }}</div>
          <div class="status-label">进行中</div>
        </div>
        <div class="status-item">
          <div class="status-value" style="color: #67C23A">{{ stats.status_stats.mastered }}</div>
          <div class="status-label">已掌握</div>
        </div>
      </div>
    </div>

    <!-- 快捷入口 -->
    <div class="card quick-actions">
      <h3 class="card-title">快捷入口</h3>
      <div class="action-grid">
        <div class="action-item" @click="goToProblems">
          <el-icon size="32" color="#409EFF"><List /></el-icon>
          <span>全部题目</span>
        </div>
        <div class="action-item" @click="goToReview">
          <el-icon size="32" color="#E6A23C"><Calendar /></el-icon>
          <span>复习计划</span>
        </div>
        <div class="action-item" @click="goToStats">
          <el-icon size="32" color="#67C23A"><TrendCharts /></el-icon>
          <span>统计分析</span>
        </div>
        <div class="action-item" @click="router.push('/problems?status=not_started')">
          <el-icon size="32" color="#909399"><Document /></el-icon>
          <span>未做题目</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.dashboard {
  max-width: 1200px;
}

.stats-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-bottom: 20px;
}

.stat-card {
  display: flex;
  align-items: center;
  gap: 16px;
  cursor: pointer;
  transition: all 0.3s;
}

.stat-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
}

.stat-icon {
  width: 56px;
  height: 56px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
}

.stat-content {
  flex: 1;
}

.stat-value {
  font-size: 24px;
  font-weight: 700;
  color: var(--text-primary);
}

.stat-label {
  font-size: 13px;
  color: var(--text-secondary);
  margin-top: 4px;
}

.stat-progress {
  display: flex;
  align-items: center;
  gap: 8px;
}

.stat-progress .progress-bar {
  width: 60px;
}

.progress-text {
  font-size: 13px;
  color: var(--text-secondary);
}

.main-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.card-header .card-title {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 0;
}

.review-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.review-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px;
  border-radius: 8px;
  background: #f5f7fa;
  cursor: pointer;
  transition: all 0.3s;
}

.review-item:hover {
  background: #e4e7ed;
}

.review-item.overdue {
  background: #fef0f0;
}

.review-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.review-title {
  font-size: 14px;
  font-weight: 500;
}

.review-meta {
  display: flex;
  align-items: center;
  gap: 8px;
}

.empty-state {
  text-align: center;
  padding: 30px;
  color: var(--text-secondary);
}

.empty-state p {
  margin-top: 12px;
}

.difficulty-section .card-title {
  display: flex;
  align-items: center;
  gap: 8px;
}

.difficulty-stats {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.difficulty-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.difficulty-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.difficulty-count {
  font-size: 13px;
  color: var(--text-secondary);
}

.progress-bar-inner.easy {
  background: linear-gradient(90deg, #67C23A 0%, #95d475 100%);
}

.progress-bar-inner.medium {
  background: linear-gradient(90deg, #E6A23C 0%, #f5c06e 100%);
}

.progress-bar-inner.hard {
  background: linear-gradient(90deg, #F56C6C 0%, #f89898 100%);
}

.status-section .card-title {
  display: flex;
  align-items: center;
  gap: 8px;
}

.status-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  text-align: center;
}

.status-grid.status-grid-3 {
  grid-template-columns: repeat(3, 1fr);
}

.status-value {
  font-size: 32px;
  font-weight: 700;
  color: var(--text-primary);
}

.status-label {
  font-size: 14px;
  color: var(--text-secondary);
  margin-top: 4px;
}

.quick-actions .action-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.action-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 20px;
  border-radius: 8px;
  background: #f5f7fa;
  cursor: pointer;
  transition: all 0.3s;
}

.action-item:hover {
  background: #e4e7ed;
  transform: translateY(-2px);
}

.action-item span {
  font-size: 14px;
  color: var(--text-regular);
}

@media (max-width: 992px) {
  .stats-row {
    grid-template-columns: 1fr;
  }
  
  .main-row {
    grid-template-columns: 1fr;
  }
  
  .status-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .quick-actions .action-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
