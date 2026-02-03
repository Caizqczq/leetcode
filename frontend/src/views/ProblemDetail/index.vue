<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { problemApi, progressApi, noteApi, tagApi } from '../../api'
import { useProblemStore } from '../../stores/problem'
import { ElMessage } from 'element-plus'

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

// 状态编辑
const status = ref('not_started')
const masteryLevel = ref(0)

// 标签管理
const selectedTagId = ref<number | undefined>(undefined)

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
    status.value = problem.value.progress?.status || 'not_started'
    masteryLevel.value = problem.value.progress?.mastery_level || 0
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

// 更新进度
async function updateProgress() {
  try {
    await progressApi.update(problemId.value, {
      status: status.value,
      mastery_level: masteryLevel.value,
    })
    ElMessage.success('状态更新成功')
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
    'attempted': '已尝试',
    'reviewing': '复习中',
    'mastered': '已掌握',
  }
  return map[status] || status
}
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

      <!-- 进度状态 -->
      <div class="card progress-section">
        <h3 class="card-title">刷题状态</h3>
        <el-form :inline="true">
          <el-form-item label="当前状态">
            <el-select v-model="status" style="width: 140px">
              <el-option label="未开始" value="not_started" />
              <el-option label="已尝试" value="attempted" />
              <el-option label="复习中" value="reviewing" />
              <el-option label="已掌握" value="mastered" />
            </el-select>
          </el-form-item>
          <el-form-item label="掌握程度">
            <el-rate v-model="masteryLevel" />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="updateProgress">更新状态</el-button>
          </el-form-item>
        </el-form>
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
