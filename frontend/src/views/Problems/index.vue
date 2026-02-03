<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useProblemStore } from '../../stores/problem'
import { ElMessage } from 'element-plus'

const router = useRouter()
const store = useProblemStore()

const statusOptions = [
  { label: '全部状态', value: '' },
  { label: '未开始', value: 'not_started' },
  { label: '已尝试', value: 'attempted' },
  { label: '复习中', value: 'reviewing' },
  { label: '已掌握', value: 'mastered' },
]

const difficultyOptions = [
  { label: '全部难度', value: '' },
  { label: '简单', value: 'Easy' },
  { label: '中等', value: 'Medium' },
  { label: '困难', value: 'Hard' },
]

// 状态更新对话框
const statusDialogVisible = ref(false)
const currentProblem = ref<any>(null)
const newStatus = ref('')
const newMastery = ref(0)

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

// 打开状态更新对话框
const openStatusDialog = (row: any) => {
  currentProblem.value = row
  newStatus.value = row.progress?.status || 'not_started'
  newMastery.value = row.progress?.mastery_level || 0
  statusDialogVisible.value = true
}

// 更新状态
const handleUpdateStatus = async () => {
  if (!currentProblem.value) return
  
  try {
    await store.updateProgress(currentProblem.value.id, newStatus.value, newMastery.value)
    ElMessage.success('状态更新成功')
    statusDialogVisible.value = false
    store.fetchProblems()
  } catch (error) {
    ElMessage.error('更新失败')
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
    'attempted': '已尝试',
    'reviewing': '复习中',
    'mastered': '已掌握',
  }
  return map[status] || status
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
        
        <el-table-column label="状态" width="100">
          <template #default="{ row }">
            <span
              class="status-tag"
              :class="getStatusClass(row.progress?.status || 'not_started')"
            >
              {{ getStatusText(row.progress?.status || 'not_started') }}
            </span>
          </template>
        </el-table-column>
        
        <el-table-column label="掌握度" width="140">
          <template #default="{ row }">
            <el-rate
              :model-value="row.progress?.mastery_level || 0"
              disabled
              size="small"
            />
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
            <el-button type="success" link size="small" @click="openStatusDialog(row)">
              更新状态
            </el-button>
            <el-button type="warning" link size="small" @click="openLeetCode(row.url)">
              LeetCode
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 状态更新对话框 -->
    <el-dialog v-model="statusDialogVisible" title="更新刷题状态" width="400px">
      <el-form label-width="80px">
        <el-form-item label="题目">
          <span>{{ currentProblem?.leetcode_id }}. {{ currentProblem?.title_cn }}</span>
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="newStatus" style="width: 100%">
            <el-option label="未开始" value="not_started" />
            <el-option label="已尝试" value="attempted" />
            <el-option label="复习中" value="reviewing" />
            <el-option label="已掌握" value="mastered" />
          </el-select>
        </el-form-item>
        <el-form-item label="掌握度">
          <el-rate v-model="newMastery" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="statusDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="handleUpdateStatus">确定</el-button>
      </template>
    </el-dialog>
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
</style>
