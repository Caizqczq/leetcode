import { defineStore } from 'pinia'
import { ref } from 'vue'
import { reviewApi } from '../api'

export interface ReviewPlan {
  id: number
  progress_id: number
  scheduled_date: string
  review_round: number
  completed: boolean
  completed_at: string | null
  problem: {
    id: number
    leetcode_id: number
    title: string
    title_cn: string
    difficulty: string
    category: string
  } | null
}

export const useReviewStore = defineStore('review', () => {
  const todayReviews = ref<ReviewPlan[]>([])
  const overdueReviews = ref<ReviewPlan[]>([])
  const upcomingReviews = ref<ReviewPlan[]>([])
  const loading = ref(false)

  // 获取今日复习
  async function fetchTodayReviews() {
    loading.value = true
    try {
      const res: any = await reviewApi.getToday()
      todayReviews.value = res.today
      overdueReviews.value = res.overdue
      upcomingReviews.value = res.upcoming
    } finally {
      loading.value = false
    }
  }

  // 标记复习完成
  async function completeReview(reviewId: number) {
    await reviewApi.complete(reviewId)
    // 从列表中移除
    todayReviews.value = todayReviews.value.filter(r => r.id !== reviewId)
    overdueReviews.value = overdueReviews.value.filter(r => r.id !== reviewId)
  }

  return {
    todayReviews,
    overdueReviews,
    upcomingReviews,
    loading,
    fetchTodayReviews,
    completeReview,
  }
})
