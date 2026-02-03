<script setup lang="ts">
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useReviewStore } from '../../stores/review'
import { ElMessage, ElMessageBox } from 'element-plus'

const router = useRouter()
const store = useReviewStore()

onMounted(() => {
  store.fetchTodayReviews()
})

// 完成复习
async function handleComplete(reviewId: number) {
  try {
    await ElMessageBox.confirm('确认已完成此题的复习吗？', '确认完成', {
      confirmButtonText: '确认',
      cancelButtonText: '取消',
      type: 'success',
    })
    await store.completeReview(reviewId)
    ElMessage.success('复习完成！')
  } catch (error) {
    // 取消操作
  }
}

// 查看题目详情
function goToDetail(problemId: number) {
  router.push(`/problems/${problemId}`)
}

// 打开 LeetCode
function openLeetCode(problem: any) {
  const slug = problem.title.toLowerCase().replace(/ /g, '-')
  window.open(`https://leetcode.cn/problems/${slug}/`, '_blank')
}

// 获取难度样式类
const getDifficultyClass = (difficulty: string) => {
  return `difficulty-${difficulty?.toLowerCase()}`
}

// 格式化日期
function formatDate(dateStr: string) {
  const date = new Date(dateStr)
  const now = new Date()
  const diffDays = Math.floor((date.getTime() - now.getTime()) / (1000 * 60 * 60 * 24))
  
  if (diffDays === 0) return '今天'
  if (diffDays === 1) return '明天'
  if (diffDays === -1) return '昨天'
  if (diffDays < -1) return `${Math.abs(diffDays)} 天前`
  return `${diffDays} 天后`
}

// 获取复习轮次文本
function getRoundText(round: number) {
  const texts = ['第一轮', '第二轮', '第三轮', '第四轮', '第五轮']
  return texts[round - 1] || `第${round}轮`
}
</script>

<template>
  <div class="review-page">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1 class="page-title">复习计划</h1>
      <p class="page-subtitle">基于艾宾浩斯遗忘曲线的智能复习提醒</p>
    </div>

    <div v-loading="store.loading">
      <!-- 逾期未复习 -->
      <div class="card" v-if="store.overdueReviews.length > 0">
        <div class="section-header">
          <h3 class="card-title">
            <el-icon color="#F56C6C"><WarningFilled /></el-icon>
            逾期未复习
          </h3>
          <el-tag type="danger">{{ store.overdueReviews.length }} 道题</el-tag>
        </div>
        
        <div class="review-list">
          <div
            v-for="review in store.overdueReviews"
            :key="review.id"
            class="review-card overdue"
          >
            <div class="review-card-info">
              <div class="review-card-title">
                {{ review.problem?.leetcode_id }}. {{ review.problem?.title_cn }}
              </div>
              <div class="review-card-meta">
                <span class="difficulty-tag" :class="getDifficultyClass(review.problem?.difficulty || '')">
                  {{ review.problem?.difficulty === 'Easy' ? '简单' : review.problem?.difficulty === 'Medium' ? '中等' : '困难' }}
                </span>
                <span>{{ review.problem?.category }}</span>
                <span>{{ getRoundText(review.review_round) }}</span>
                <span class="overdue-text">{{ formatDate(review.scheduled_date) }}</span>
              </div>
            </div>
            <div class="review-card-actions">
              <el-button size="small" @click="goToDetail(review.problem?.id!)">查看</el-button>
              <el-button size="small" @click="openLeetCode(review.problem)">LeetCode</el-button>
              <el-button type="success" size="small" @click="handleComplete(review.id)">完成</el-button>
            </div>
          </div>
        </div>
      </div>

      <!-- 今日待复习 -->
      <div class="card">
        <div class="section-header">
          <h3 class="card-title">
            <el-icon color="#E6A23C"><Clock /></el-icon>
            今日待复习
          </h3>
          <el-tag type="warning">{{ store.todayReviews.length }} 道题</el-tag>
        </div>
        
        <div v-if="store.todayReviews.length === 0" class="empty-state">
          <el-icon size="48" color="#c0c4cc"><CircleCheck /></el-icon>
          <p>今日复习任务已完成！</p>
        </div>
        
        <div class="review-list" v-else>
          <div
            v-for="review in store.todayReviews"
            :key="review.id"
            class="review-card today"
          >
            <div class="review-card-info">
              <div class="review-card-title">
                {{ review.problem?.leetcode_id }}. {{ review.problem?.title_cn }}
              </div>
              <div class="review-card-meta">
                <span class="difficulty-tag" :class="getDifficultyClass(review.problem?.difficulty || '')">
                  {{ review.problem?.difficulty === 'Easy' ? '简单' : review.problem?.difficulty === 'Medium' ? '中等' : '困难' }}
                </span>
                <span>{{ review.problem?.category }}</span>
                <span>{{ getRoundText(review.review_round) }}</span>
              </div>
            </div>
            <div class="review-card-actions">
              <el-button size="small" @click="goToDetail(review.problem?.id!)">查看</el-button>
              <el-button size="small" @click="openLeetCode(review.problem)">LeetCode</el-button>
              <el-button type="success" size="small" @click="handleComplete(review.id)">完成</el-button>
            </div>
          </div>
        </div>
      </div>

      <!-- 即将复习 -->
      <div class="card" v-if="store.upcomingReviews.length > 0">
        <div class="section-header">
          <h3 class="card-title">
            <el-icon color="#409EFF"><Calendar /></el-icon>
            未来 7 天
          </h3>
          <el-tag>{{ store.upcomingReviews.length }} 道题</el-tag>
        </div>
        
        <div class="review-list">
          <div
            v-for="review in store.upcomingReviews"
            :key="review.id"
            class="review-card upcoming"
          >
            <div class="review-card-info">
              <div class="review-card-title">
                {{ review.problem?.leetcode_id }}. {{ review.problem?.title_cn }}
              </div>
              <div class="review-card-meta">
                <span class="difficulty-tag" :class="getDifficultyClass(review.problem?.difficulty || '')">
                  {{ review.problem?.difficulty === 'Easy' ? '简单' : review.problem?.difficulty === 'Medium' ? '中等' : '困难' }}
                </span>
                <span>{{ review.problem?.category }}</span>
                <span>{{ getRoundText(review.review_round) }}</span>
                <span class="upcoming-text">{{ formatDate(review.scheduled_date) }}</span>
              </div>
            </div>
            <div class="review-card-actions">
              <el-button size="small" @click="goToDetail(review.problem?.id!)">查看</el-button>
              <el-button size="small" @click="openLeetCode(review.problem)">LeetCode</el-button>
            </div>
          </div>
        </div>
      </div>

      <!-- 艾宾浩斯说明 -->
      <div class="card info-card">
        <h3 class="card-title">
          <el-icon><InfoFilled /></el-icon>
          艾宾浩斯记忆法
        </h3>
        <p class="info-text">
          根据艾宾浩斯遗忘曲线，系统会在你首次完成一道题后，自动安排 5 轮复习：
        </p>
        <div class="intervals">
          <el-tag>第 1 天</el-tag>
          <el-icon><ArrowRight /></el-icon>
          <el-tag>第 2 天</el-tag>
          <el-icon><ArrowRight /></el-icon>
          <el-tag>第 4 天</el-tag>
          <el-icon><ArrowRight /></el-icon>
          <el-tag>第 7 天</el-tag>
          <el-icon><ArrowRight /></el-icon>
          <el-tag>第 15 天</el-tag>
        </div>
        <p class="info-text">
          坚持复习，让解题思路真正内化为你的知识！
        </p>
      </div>
    </div>
  </div>
</template>

<style scoped>
.review-page {
  max-width: 900px;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.section-header .card-title {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 0;
}

.review-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.review-card {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px;
  border: 1px solid var(--border-color);
  border-radius: 8px;
  transition: all 0.3s;
}

.review-card:hover {
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
}

.review-card.overdue {
  border-color: #fbc4c4;
  background: #fff5f5;
}

.review-card.today {
  border-color: #faecd8;
  background: #fffaf0;
}

.review-card.upcoming {
  border-color: #d9ecff;
  background: #f5faff;
}

.review-card-title {
  font-size: 15px;
  font-weight: 500;
  margin-bottom: 8px;
}

.review-card-meta {
  display: flex;
  align-items: center;
  gap: 12px;
  font-size: 13px;
  color: var(--text-secondary);
}

.overdue-text {
  color: var(--danger-color);
  font-weight: 500;
}

.upcoming-text {
  color: var(--primary-color);
}

.review-card-actions {
  display: flex;
  gap: 8px;
}

.empty-state {
  text-align: center;
  padding: 40px;
  color: var(--text-secondary);
}

.empty-state p {
  margin-top: 12px;
  font-size: 14px;
}

.info-card {
  background: linear-gradient(135deg, #f5f7fa 0%, #e4e7ed 100%);
}

.info-text {
  font-size: 14px;
  color: var(--text-regular);
  margin-bottom: 16px;
  line-height: 1.6;
}

.intervals {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 16px;
  flex-wrap: wrap;
}
</style>
