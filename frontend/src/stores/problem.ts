import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { problemApi, progressApi, tagApi } from '../api'

export interface Problem {
  id: number
  leetcode_id: number
  title: string
  title_cn: string
  difficulty: string
  category: string
  url: string
  progress: {
    status: string
    attempt_count: number
    mastery_level: number
  } | null
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

  // 更新进度
  async function updateProgress(problemId: number, status: string, masteryLevel: number) {
    await progressApi.update(problemId, { status, mastery_level: masteryLevel })
    // 更新本地状态
    const problem = problems.value.find(p => p.id === problemId)
    if (problem && problem.progress) {
      problem.progress.status = status
      problem.progress.mastery_level = masteryLevel
      problem.progress.attempt_count += 1
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
    updateProgress,
    resetFilters,
  }
})
