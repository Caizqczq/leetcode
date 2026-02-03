<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useProblemStore } from '../../stores/problem'
import { ElMessage, ElMessageBox } from 'element-plus'

const router = useRouter()
const store = useProblemStore()

// 新状态选项（简化为3种）
const statusOptions = [
  { label: '全部状态', value: '' },
  { label: '未开始', value: 'not_started' },
  { label: '进行中', value: 'in_progress' },
  { label: '已掌握', value: 'mastered' },
]

const difficultyOptions = [
  { label: '全部难度', value: '' },
  { label: '简单', value: 'Easy' },
  { label: '中等', value: 'Medium' },
  { label: '困难', value: 'Hard' },
]

// 加载状态
const completingId = ref<number | null>(null)

onMounted(async () => {
  await Promise.all([
    store.fetchProblems(),
    store.fetchCategories(),
    store.fetchTags(),
  ])
})

// 搜索处理
const handleSearch = () => {
  store.fetchProblems()
}

// 重置筛选
const handleReset = () => {
  store.resetFilters()
  store.fetchProblems()
}

// 查看详情
const goToDetail = (row: any) => {
  router.push(`/problems/${row.id}`)
}

// 一键完成
const handleComplete = async (row: any) => {
  // 如果已掌握，不需要再次完成
  if (row.progress?.status === 'mastered') {
    ElMessage.info('该题目已掌握')
    return
  }

  try {
    await ElMessageBox.confirm(
      `确认已完成 "${row.leetcode_id}. ${row.title_cn}" 的练习吗？`,
      '标记完成',
      {
        confirmButtonText: '确认完成',
        cancelButtonText: '取消',
        type: 'success',
      }
    )

    completingId.value = row.id
    await store.markComplete(row.id)
    ElMessage.success('已完成！系统已自动生成复习计划')
  } catch (error: any) {
    // 用户取消操作不提示错误
    if (error !== 'cancel') {
      ElMessage.error('操作失败')
    }
  } finally {
    completingId.value = null
  }
}

// 获取难度样式类
const getDifficultyClass = (difficulty: string) => {
  return `difficulty-${difficulty.toLowerCase()}`
}

// 获取状态样式类
const getStatusClass = (status: string) => {
  return `status-${status}`
}

// 获取状态文本
const getStatusText = (status: string) => {
  const map: Record<string, string> = {
    'not_started': '未开始',
    'in_progress': '进行中',
    'mastered': '已掌握',
  }
  return map[status] || status
}

// 获取复习进度文本
const getReviewProgress = (progress: any) => {
  if (!progress || progress.status === 'not_started') {
    return ''
  }
  const completed = progress.completed_reviews || progress.mastery_level || 0
  const total = progress.total_reviews || 5
  return `${completed}/${total}轮`
}

// 打开 LeetCode 链接
const openLeetCode = (url: string) => {
  window.open(url, '_blank')
}
</script>

<template>
  <div class="problems-page">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1 class="page-title">题目列表</h1>
      <p class="page-subtitle">LeetCode Hot 100 全部题目，共 {{ store.total }} 题</p>
    </div>

    <!-- 筛选区域 -->
    <div class="card filter-card">
      <el-form :inline="true" class="filter-form">
        <el-form-item label="搜索">
          <el-input
            v-model="store.filters.search"
            placeholder="题号或标题"
            clearable
            style="width: 180px"
            @keyup.enter="handleSearch"
          />
        </el-form-item>
        
        <el-form-item label="难度">
          <el-select v-model="store.filters.difficulty" style="width: 120px" @change="handleSearch">
            <el-option
              v-for="opt in difficultyOptions"
              :key="opt.value"
              :label="opt.label"
              :value="opt.value"
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="分类">
          <el-select v-model="store.filters.category" style="width: 140px" clearable @change="handleSearch">
            <el-option label="全部分类" value="" />
            <el-option
              v-for="cat in store.categories"
              :key="cat"
              :label="cat"
              :value="cat"
            />
          </el-select>
        </el-form-item>
        
        <el-form-item label="状态">
          <el-select v-model="store.filters.status" style="width: 120px" @change="handleSearch">
            <el-option
              v-for="opt in statusOptions"
              :key="opt.value"
              :label="opt.label"
              :value="opt.value"
            />
          </el-select>
        </el-form-item>
        
        <el-form-item>
          <el-button type="primary" @click="handleSearch">
            <el-icon><Search /></el-icon>
            搜索
          </el-button>
          <el-button @click="handleReset">重置</el-button>
        </el-form-item>
      </el-form>
    </div>

    <!-- 题目表格 -->
    <div class="card">
      <el-table
        :data="store.problems"
        v-loading="store.loading"
        stripe
        style="width: 100%"
      >
        <el-table-column prop="leetcode_id" label="题号" width="80" sortable />
        
        <el-table-column label="标题" min-width="280">
          <template #default="{ row }">
            <div class="problem-title">
              <span class="title-cn" @click="goToDetail(row)">{{ row.title_cn }}</span>
              <span class="title-en">{{ row.title }}</span>
            </div>
          </template>
        </el-table-column>
        
        <el-table-column prop="difficulty" label="难度" width="100">
          <template #default="{ row }">
            <span class="difficulty-tag" :class="getDifficultyClass(row.difficulty)">
              {{ row.difficulty === 'Easy' ? '简单' : row.difficulty === 'Medium' ? '中等' : '困难' }}
            </span>
          </template>
        </el-table-column>
        
        <el-table-column prop="category" label="分类" width="120" />
        
        <el-table-column label="状态" width="140">
          <template #default="{ row }">
            <div class="status-cell">
              <span
                class="status-tag"
                :class="getStatusClass(row.progress?.status || 'not_started')"
              >
                {{ getStatusText(row.progress?.status || 'not_started') }}
              </span>
              <span v-if="getReviewProgress(row.progress)" class="review-progress">
                {{ getReviewProgress(row.progress) }}
              </span>
            </div>
          </template>
        </el-table-column>
        
        <el-table-column label="复习进度" width="140">
          <template #default="{ row }">
            <template v-if="row.progress && row.progress.status !== 'not_started'">
              <el-progress
                :percentage="((row.progress.completed_reviews || row.progress.mastery_level || 0) / 5) * 100"
                :stroke-width="8"
                :show-text="false"
                :status="row.progress.status === 'mastered' ? 'success' : undefined"
              />
            </template>
            <span v-else class="no-progress">-</span>
          </template>
        </el-table-column>
        
        <el-table-column label="标签" min-width="160">
          <template #default="{ row }">
            <el-tag
              v-for="tag in row.tags"
              :key="tag.id"
              :color="tag.color"
              size="small"
              style="margin-right: 4px; color: #fff"
            >
              {{ tag.name }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column label="操作" width="180" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="goToDetail(row)">
              详情
            </el-button>
            <el-button
              type="success"
              link
              size="small"
              :loading="completingId === row.id"
              :disabled="row.progress?.status === 'mastered'"
              @click="handleComplete(row)"
            >
              {{ row.progress?.status === 'mastered' ? '已完成' : '完成' }}
            </el-button>
            <el-button type="warning" link size="small" @click="openLeetCode(row.url)">
              LeetCode
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<style scoped>
.problems-page {
  max-width: 1400px;
}

.filter-card {
  margin-bottom: 20px;
}

.filter-form {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.problem-title {
  display: flex;
  flex-direction: column;
}

.title-cn {
  font-weight: 500;
  cursor: pointer;
  color: var(--text-primary);
}

.title-cn:hover {
  color: var(--primary-color);
}

.title-en {
  font-size: 12px;
  color: var(--text-secondary);
  margin-top: 2px;
}

.status-cell {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.review-progress {
  font-size: 12px;
  color: var(--text-secondary);
}

.no-progress {
  color: var(--text-secondary);
}

/* 状态标签样式 */
.status-tag.status-in_progress {
  color: var(--primary-color);
  background: rgba(64, 158, 255, 0.1);
  padding: 2px 8px;
  border-radius: 4px;
  font-size: 12px;
}
</style>
