<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { problemApi, progressApi, noteApi, tagApi } from '../../api'
import { useProblemStore } from '../../stores/problem'
import { ElMessage, ElMessageBox } from 'element-plus'

const route = useRoute()
const router = useRouter()
const store = useProblemStore()

const problemId = computed(() => Number(route.params.id))
const loading = ref(true)
const problem = ref<any>(null)
const note = ref<any>({
  approach: '',
  code: '',
  language: 'python',
  time_complexity: '',
  space_complexity: '',
  key_points: '',
})
const saving = ref(false)
const completing = ref(false)

// 标签管理
const selectedTagId = ref<number | undefined>(undefined)

// 高级选项（手动调整状态）
const showAdvanced = ref(false)
const manualStatus = ref('not_started')
const manualMastery = ref(0)

const languageOptions = [
  { label: 'Python', value: 'python' },
  { label: 'JavaScript', value: 'javascript' },
  { label: 'TypeScript', value: 'typescript' },
  { label: 'Java', value: 'java' },
  { label: 'C++', value: 'cpp' },
  { label: 'Go', value: 'go' },
]

onMounted(async () => {
  await Promise.all([
    fetchProblem(),
    fetchNote(),
    store.fetchTags(),
  ])
  loading.value = false
})

// 获取题目详情
async function fetchProblem() {
  try {
    problem.value = await problemApi.getDetail(problemId.value)
    manualStatus.value = problem.value.progress?.status || 'not_started'
    manualMastery.value = problem.value.progress?.mastery_level || 0
  } catch (error) {
    ElMessage.error('获取题目失败')
    router.push('/problems')
  }
}

// 获取笔记
async function fetchNote() {
  try {
    const res = await noteApi.get(problemId.value)
    if (res) {
      note.value = res
    }
  } catch (error) {
    // 没有笔记，使用默认值
  }
}

// 保存笔记
async function saveNote() {
  saving.value = true
  try {
    await noteApi.save({
      problem_id: problemId.value,
      ...note.value,
    })
    ElMessage.success('笔记保存成功')
  } catch (error) {
    ElMessage.error('保存失败')
  } finally {
    saving.value = false
  }
}

// 一键完成
async function handleComplete() {
  if (problem.value?.progress?.status === 'mastered') {
    ElMessage.info('该题目已掌握')
    return
  }

  try {
    await ElMessageBox.confirm(
      '确认已完成本题的练习吗？',
      '标记完成',
      {
        confirmButtonText: '确认完成',
        cancelButtonText: '取消',
        type: 'success',
      }
    )

    completing.value = true
    await progressApi.complete(problemId.value)
    ElMessage.success('已完成！系统已自动生成复习计划')
    await fetchProblem()
  } catch (error: any) {
    if (error !== 'cancel') {
      ElMessage.error('操作失败')
    }
  } finally {
    completing.value = false
  }
}

// 手动更新进度（高级选项）
async function updateProgressManually() {
  try {
    await progressApi.update(problemId.value, {
      status: manualStatus.value,
      mastery_level: manualMastery.value,
    })
    ElMessage.success('状态已手动更新')
    showAdvanced.value = false
    await fetchProblem()
  } catch (error) {
    ElMessage.error('更新失败')
  }
}

// 添加标签
async function addTag() {
  if (!selectedTagId.value) return
  try {
    await tagApi.addToProblem(problemId.value, selectedTagId.value)
    ElMessage.success('标签添加成功')
    selectedTagId.value = undefined
    await fetchProblem()
  } catch (error) {
    ElMessage.error('添加失败')
  }
}

// 移除标签
async function removeTag(tagId: number) {
  try {
    await tagApi.removeFromProblem(problemId.value, tagId)
    ElMessage.success('标签已移除')
    await fetchProblem()
  } catch (error) {
    ElMessage.error('移除失败')
  }
}

// 打开 LeetCode
function openLeetCode() {
  if (problem.value?.url) {
    window.open(problem.value.url, '_blank')
  }
}

// 返回列表
function goBack() {
  router.push('/problems')
}

// 获取可添加的标签（排除已有的）
const availableTags = computed(() => {
  const existingIds = new Set(problem.value?.tags?.map((t: any) => t.id) || [])
  return store.tags.filter(t => !existingIds.has(t.id))
})

// 获取难度样式类
const getDifficultyClass = (difficulty: string) => {
  return `difficulty-${difficulty?.toLowerCase()}`
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

// 获取状态样式类
const getStatusClass = (status: string) => {
  return `status-${status}`
}

// 计算复习进度
const reviewProgress = computed(() => {
  const progress = problem.value?.progress
  if (!progress) return { completed: 0, total: 5, percentage: 0 }
  
  const completed = progress.completed_reviews ?? progress.mastery_level ?? 0
  const total = progress.total_reviews ?? 5
  const percentage = (completed / total) * 100
  
  return { completed, total, percentage }
})

// 是否可以标记完成
const canComplete = computed(() => {
  return problem.value?.progress?.status !== 'mastered'
})
</script>

<template>
  <div class="problem-detail" v-loading="loading">
    <!-- 返回按钮 -->
    <div class="back-btn">
      <el-button @click="goBack">
        <el-icon><ArrowLeft /></el-icon>
        返回列表
      </el-button>
    </div>

    <template v-if="problem">
      <!-- 题目信息 -->
      <div class="card problem-info">
        <div class="problem-header">
          <div class="problem-title-section">
            <h1 class="problem-title">
              {{ problem.leetcode_id }}. {{ problem.title_cn }}
            </h1>
            <p class="problem-title-en">{{ problem.title }}</p>
          </div>
          <el-button type="primary" @click="openLeetCode">
            <el-icon><Link /></el-icon>
            在 LeetCode 中打开
          </el-button>
        </div>

        <div class="problem-meta">
          <span class="difficulty-tag" :class="getDifficultyClass(problem.difficulty)">
            {{ problem.difficulty === 'Easy' ? '简单' : problem.difficulty === 'Medium' ? '中等' : '困难' }}
          </span>
          <el-tag type="info">{{ problem.category }}</el-tag>
          <span class="attempt-info" v-if="problem.progress">
            尝试次数: {{ problem.progress.attempt_count }}
          </span>
        </div>

        <!-- 标签管理 -->
        <div class="tags-section">
          <span class="section-label">标签：</span>
          <el-tag
            v-for="tag in problem.tags"
            :key="tag.id"
            :color="tag.color"
            closable
            style="margin-right: 8px; color: #fff"
            @close="removeTag(tag.id)"
          >
            {{ tag.name }}
          </el-tag>
          <el-select
            v-model="selectedTagId"
            placeholder="添加标签"
            size="small"
            style="width: 120px"
            @change="addTag"
          >
            <el-option
              v-for="tag in availableTags"
              :key="tag.id"
              :label="tag.name"
              :value="tag.id"
            />
          </el-select>
        </div>
      </div>

      <!-- 刷题状态（简化版） -->
      <div class="card progress-section">
        <div class="progress-header">
          <h3 class="card-title">刷题状态</h3>
          <el-button
            v-if="canComplete"
            type="success"
            :loading="completing"
            @click="handleComplete"
          >
            <el-icon><Check /></el-icon>
            标记完成
          </el-button>
          <el-tag v-else type="success" size="large">
            <el-icon><CircleCheck /></el-icon>
            已掌握
          </el-tag>
        </div>

        <!-- 状态显示 -->
        <div class="status-display">
          <div class="status-item">
            <span class="status-label">当前状态</span>
            <span
              class="status-value"
              :class="getStatusClass(problem.progress?.status || 'not_started')"
            >
              {{ getStatusText(problem.progress?.status || 'not_started') }}
            </span>
          </div>
          
          <div class="status-item" v-if="problem.progress?.status !== 'not_started'">
            <span class="status-label">复习进度</span>
            <div class="review-progress-wrapper">
              <el-progress
                :percentage="reviewProgress.percentage"
                :stroke-width="12"
                :status="problem.progress?.status === 'mastered' ? 'success' : undefined"
              >
                <span class="progress-text">{{ reviewProgress.completed }}/{{ reviewProgress.total }} 轮</span>
              </el-progress>
            </div>
          </div>
        </div>

        <!-- 高级选项（手动调整） -->
        <div class="advanced-section">
          <el-link type="info" :underline="false" @click="showAdvanced = !showAdvanced">
            <el-icon><Setting /></el-icon>
            {{ showAdvanced ? '收起' : '手动调整状态' }}
          </el-link>
          
          <el-collapse-transition>
            <div v-if="showAdvanced" class="advanced-form">
              <el-alert
                type="info"
                :closable="false"
                show-icon
              >
                <template #title>
                  手动调整仅在特殊情况下使用，推荐使用"标记完成"按钮
                </template>
              </el-alert>
              <el-form :inline="true" style="margin-top: 16px">
                <el-form-item label="状态">
                  <el-select v-model="manualStatus" style="width: 140px">
                    <el-option label="未开始" value="not_started" />
                    <el-option label="进行中" value="in_progress" />
                    <el-option label="已掌握" value="mastered" />
                  </el-select>
                </el-form-item>
                <el-form-item label="掌握程度">
                  <el-input-number v-model="manualMastery" :min="0" :max="5" />
                </el-form-item>
                <el-form-item>
                  <el-button type="primary" @click="updateProgressManually">保存</el-button>
                </el-form-item>
              </el-form>
            </div>
          </el-collapse-transition>
        </div>
      </div>

      <!-- 笔记编辑 -->
      <div class="card note-section">
        <div class="note-header">
          <h3 class="card-title">题解笔记</h3>
          <el-button type="primary" :loading="saving" @click="saveNote">
            <el-icon><Check /></el-icon>
            保存笔记
          </el-button>
        </div>

        <el-form label-position="top">
          <el-form-item label="解题思路">
            <el-input
              v-model="note.approach"
              type="textarea"
              :rows="4"
              placeholder="记录你的解题思路..."
            />
          </el-form-item>

          <el-row :gutter="20">
            <el-col :span="12">
              <el-form-item label="时间复杂度">
                <el-input v-model="note.time_complexity" placeholder="如 O(n)" />
              </el-form-item>
            </el-col>
            <el-col :span="12">
              <el-form-item label="空间复杂度">
                <el-input v-model="note.space_complexity" placeholder="如 O(1)" />
              </el-form-item>
            </el-col>
          </el-row>

          <el-form-item label="代码">
            <div class="code-header">
              <el-select v-model="note.language" size="small" style="width: 140px">
                <el-option
                  v-for="lang in languageOptions"
                  :key="lang.value"
                  :label="lang.label"
                  :value="lang.value"
                />
              </el-select>
            </div>
            <el-input
              v-model="note.code"
              type="textarea"
              :rows="12"
              placeholder="粘贴你的代码..."
              class="code-input"
            />
          </el-form-item>

          <el-form-item label="关键点 / 易错点">
            <el-input
              v-model="note.key_points"
              type="textarea"
              :rows="3"
              placeholder="记录关键点和易错点..."
            />
          </el-form-item>
        </el-form>
      </div>
    </template>
  </div>
</template>

<style scoped>
.problem-detail {
  max-width: 1000px;
}

.back-btn {
  margin-bottom: 16px;
}

.problem-info {
  margin-bottom: 20px;
}

.problem-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 16px;
}

.problem-title {
  font-size: 24px;
  font-weight: 600;
  margin-bottom: 4px;
}

.problem-title-en {
  font-size: 14px;
  color: var(--text-secondary);
}

.problem-meta {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}

.attempt-info {
  font-size: 14px;
  color: var(--text-secondary);
}

.tags-section {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
}

.section-label {
  font-size: 14px;
  color: var(--text-secondary);
}

.progress-section {
  margin-bottom: 20px;
}

.progress-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.progress-header .card-title {
  margin-bottom: 0;
}

.status-display {
  display: flex;
  gap: 40px;
  margin-bottom: 20px;
}

.status-item {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.status-label {
  font-size: 14px;
  color: var(--text-secondary);
}

.status-value {
  font-size: 16px;
  font-weight: 500;
}

.status-value.status-not_started {
  color: var(--text-secondary);
}

.status-value.status-in_progress {
  color: var(--primary-color);
}

.status-value.status-mastered {
  color: var(--success-color);
}

.review-progress-wrapper {
  width: 200px;
}

.progress-text {
  font-size: 14px;
  font-weight: 500;
}

.advanced-section {
  border-top: 1px solid var(--border-color);
  padding-top: 16px;
}

.advanced-form {
  margin-top: 16px;
}

.note-section {
  margin-bottom: 20px;
}

.note-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.note-header .card-title {
  margin-bottom: 0;
}

.code-header {
  margin-bottom: 8px;
}

.code-input :deep(textarea) {
  font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', 'Consolas', monospace;
  font-size: 13px;
  line-height: 1.5;
}
</style>
