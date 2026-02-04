import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { problemApi, progressApi, tagApi } from '../api'

export interface Progress {
  status: string
  attempt_count: number
  mastery_level: number
  completed_reviews: number
  total_reviews: number
}

export interface Problem {
  id: number
  leetcode_id: number
  title: string
  title_cn: string
  difficulty: string
  category: string
  url: string
  progress: Progress | null
  tags: Array<{
    id: number
    name: string
    color: string
  }>
}

export interface Tag {
  id: number
  name: string
  color: string
}

export const useProblemStore = defineStore('problem', () => {
  // 状态
  const problems = ref<Problem[]>([])
  const total = ref(0)
  const loading = ref(false)
  const categories = ref<string[]>([])
  const tags = ref<Tag[]>([])

  // 筛选条件
  const filters = ref({
    difficulty: '',
    category: '',
    status: '',
    search: '',
    tag_id: undefined as number | undefined,
    sort_by: 'default' as 'default' | 'leetcode_id',  // default=官方顺序, leetcode_id=题号
  })

  // 计算属性
  const completedCount = computed(() =>
    problems.value.filter(p => p.progress?.status !== 'not_started').length
  )

  // 获取题目列表
  async function fetchProblems() {
    loading.value = true
    try {
      const params: Record<string, any> = {}
      if (filters.value.difficulty) params.difficulty = filters.value.difficulty
      if (filters.value.category) params.category = filters.value.category
      if (filters.value.status) params.status = filters.value.status
      if (filters.value.search) params.search = filters.value.search
      if (filters.value.tag_id) params.tag_id = filters.value.tag_id
      if (filters.value.sort_by) params.sort_by = filters.value.sort_by

      const res: any = await problemApi.getList(params)
      problems.value = res.items
      total.value = res.total
    } finally {
      loading.value = false
    }
  }

  // 获取分类列表
  async function fetchCategories() {
    const res: any = await problemApi.getCategories()
    categories.value = res.categories
  }

  // 获取标签列表
  async function fetchTags() {
    const res: any = await tagApi.getList()
    tags.value = res
  }

  // 一键完成（推荐使用）
  async function markComplete(problemId: number) {
    const res: any = await progressApi.complete(problemId)
    // 更新本地状态
    const problem = problems.value.find(p => p.id === problemId)
    if (problem) {
      problem.progress = {
        status: res.status,
        attempt_count: res.attempt_count,
        mastery_level: res.mastery_level,
        completed_reviews: res.completed_reviews,
        total_reviews: res.total_reviews,
      }
    }
    return res
  }

  // 手动更新进度（高级选项）
  async function updateProgress(problemId: number, status: string, masteryLevel: number) {
    const res: any = await progressApi.update(problemId, { status, mastery_level: masteryLevel })
    // 更新本地状态
    const problem = problems.value.find(p => p.id === problemId)
    if (problem) {
      problem.progress = {
        status: res.status,
        attempt_count: res.attempt_count,
        mastery_level: res.mastery_level,
        completed_reviews: res.completed_reviews || 0,
        total_reviews: res.total_reviews || 5,
      }
    }
  }

  // 重置筛选
  function resetFilters() {
    filters.value = {
      difficulty: '',
      category: '',
      status: '',
      search: '',
      tag_id: undefined,
      sort_by: 'default',
    }
  }

  return {
    problems,
    total,
    loading,
    categories,
    tags,
    filters,
    completedCount,
    fetchProblems,
    fetchCategories,
    fetchTags,
    markComplete,
    updateProgress,
    resetFilters,
  }
})
