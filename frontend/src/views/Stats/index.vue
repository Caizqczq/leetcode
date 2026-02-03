<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { PieChart, BarChart, LineChart } from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
} from 'echarts/components'
import VChart from 'vue-echarts'
import { statsApi } from '../../api'

// 注册 ECharts 组件
use([
  CanvasRenderer,
  PieChart,
  BarChart,
  LineChart,
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
])

const loading = ref(true)
const stats = ref<any>(null)

onMounted(async () => {
  await fetchStats()
  loading.value = false
})

async function fetchStats() {
  try {
    stats.value = await statsApi.get()
  } catch (error) {
    console.error('获取统计失败', error)
  }
}

// 完成率饼图配置
const completionPieOption = computed(() => {
  if (!stats.value) return {}
  const completed = stats.value.completed_count
  const remaining = stats.value.total_problems - completed
  
  return {
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} ({d}%)'
    },
    legend: {
      bottom: '5%',
      left: 'center'
    },
    series: [
      {
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: true,
          formatter: '{b}\n{c}题'
        },
        data: [
          { value: completed, name: '已完成', itemStyle: { color: '#67C23A' } },
          { value: remaining, name: '未完成', itemStyle: { color: '#DCDFE6' } },
        ]
      }
    ]
  }
})

// 难度分布饼图配置
const difficultyPieOption = computed(() => {
  if (!stats.value) return {}
  
  return {
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} ({d}%)'
    },
    legend: {
      bottom: '5%',
      left: 'center'
    },
    series: [
      {
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: true,
          formatter: '{b}\n{c}题'
        },
        data: [
          { value: stats.value.difficulty_stats.easy, name: '简单', itemStyle: { color: '#67C23A' } },
          { value: stats.value.difficulty_stats.medium, name: '中等', itemStyle: { color: '#E6A23C' } },
          { value: stats.value.difficulty_stats.hard, name: '困难', itemStyle: { color: '#F56C6C' } },
        ]
      }
    ]
  }
})

// 状态分布饼图配置
const statusPieOption = computed(() => {
  if (!stats.value) return {}
  
  return {
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} ({d}%)'
    },
    legend: {
      bottom: '5%',
      left: 'center'
    },
    series: [
      {
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: true,
          formatter: '{b}\n{c}题'
        },
        data: [
          { value: stats.value.status_stats.not_started, name: '未开始', itemStyle: { color: '#909399' } },
          { value: stats.value.status_stats.attempted, name: '已尝试', itemStyle: { color: '#409EFF' } },
          { value: stats.value.status_stats.reviewing, name: '复习中', itemStyle: { color: '#E6A23C' } },
          { value: stats.value.status_stats.mastered, name: '已掌握', itemStyle: { color: '#67C23A' } },
        ]
      }
    ]
  }
})

// 分类完成率柱状图配置
const categoryBarOption = computed(() => {
  if (!stats.value || !stats.value.category_stats) return {}
  
  const categories = stats.value.category_stats.map((c: any) => c.category)
  const totals = stats.value.category_stats.map((c: any) => c.total)
  const completeds = stats.value.category_stats.map((c: any) => c.completed)
  
  return {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    legend: {
      data: ['已完成', '总数']
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: categories,
      axisLabel: {
        rotate: 45
      }
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        name: '已完成',
        type: 'bar',
        stack: 'total',
        itemStyle: { color: '#67C23A' },
        data: completeds
      },
      {
        name: '总数',
        type: 'bar',
        stack: 'total',
        itemStyle: { color: '#DCDFE6' },
        data: totals.map((t: number, i: number) => t - completeds[i])
      }
    ]
  }
})

// 每日刷题趋势折线图
const dailyLineOption = computed(() => {
  if (!stats.value || !stats.value.daily_stats || stats.value.daily_stats.length === 0) {
    return {
      title: {
        text: '暂无数据',
        left: 'center',
        top: 'middle',
        textStyle: {
          color: '#909399',
          fontSize: 14
        }
      }
    }
  }
  
  const dates = stats.value.daily_stats.map((d: any) => d.date)
  const counts = stats.value.daily_stats.map((d: any) => d.count)
  
  return {
    tooltip: {
      trigger: 'axis'
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      boundaryGap: false,
      data: dates
    },
    yAxis: {
      type: 'value',
      minInterval: 1
    },
    series: [
      {
        name: '刷题数',
        type: 'line',
        smooth: true,
        areaStyle: {
          color: {
            type: 'linear',
            x: 0,
            y: 0,
            x2: 0,
            y2: 1,
            colorStops: [
              { offset: 0, color: 'rgba(64, 158, 255, 0.3)' },
              { offset: 1, color: 'rgba(64, 158, 255, 0.05)' }
            ]
          }
        },
        itemStyle: { color: '#409EFF' },
        data: counts
      }
    ]
  }
})
</script>

<template>
  <div class="stats-page" v-loading="loading">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1 class="page-title">统计分析</h1>
      <p class="page-subtitle">全方位了解你的刷题进度和数据</p>
    </div>

    <template v-if="stats">
      <!-- 概览卡片 -->
      <div class="overview-row">
        <div class="card overview-card">
          <div class="overview-value">{{ stats.total_problems }}</div>
          <div class="overview-label">总题数</div>
        </div>
        <div class="card overview-card">
          <div class="overview-value" style="color: #67C23A">{{ stats.completed_count }}</div>
          <div class="overview-label">已完成</div>
        </div>
        <div class="card overview-card">
          <div class="overview-value" style="color: #409EFF">{{ stats.completion_rate }}%</div>
          <div class="overview-label">完成率</div>
        </div>
        <div class="card overview-card">
          <div class="overview-value" style="color: #E6A23C">{{ stats.status_stats.reviewing }}</div>
          <div class="overview-label">复习中</div>
        </div>
      </div>

      <!-- 图表行1 -->
      <div class="charts-row">
        <div class="card chart-card">
          <h3 class="card-title">完成进度</h3>
          <v-chart :option="completionPieOption" style="height: 300px" />
        </div>
        <div class="card chart-card">
          <h3 class="card-title">难度分布</h3>
          <v-chart :option="difficultyPieOption" style="height: 300px" />
        </div>
        <div class="card chart-card">
          <h3 class="card-title">状态分布</h3>
          <v-chart :option="statusPieOption" style="height: 300px" />
        </div>
      </div>

      <!-- 分类完成率 -->
      <div class="card">
        <h3 class="card-title">分类完成情况</h3>
        <v-chart :option="categoryBarOption" style="height: 400px" />
      </div>

      <!-- 刷题趋势 -->
      <div class="card">
        <h3 class="card-title">最近30天刷题趋势</h3>
        <v-chart :option="dailyLineOption" style="height: 300px" />
      </div>

      <!-- 详细数据表格 -->
      <div class="card">
        <h3 class="card-title">分类详情</h3>
        <el-table :data="stats.category_stats" stripe style="width: 100%">
          <el-table-column prop="category" label="分类" width="180" />
          <el-table-column prop="total" label="题目数" width="100" />
          <el-table-column prop="completed" label="已完成" width="100" />
          <el-table-column label="完成率">
            <template #default="{ row }">
              <div class="table-progress">
                <el-progress
                  :percentage="Math.round(row.completed / row.total * 100)"
                  :stroke-width="10"
                />
              </div>
            </template>
          </el-table-column>
        </el-table>
      </div>
    </template>
  </div>
</template>

<style scoped>
.stats-page {
  max-width: 1400px;
}

.overview-row {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-bottom: 20px;
}

.overview-card {
  text-align: center;
  padding: 24px;
}

.overview-value {
  font-size: 36px;
  font-weight: 700;
  color: var(--text-primary);
}

.overview-label {
  font-size: 14px;
  color: var(--text-secondary);
  margin-top: 8px;
}

.charts-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-bottom: 20px;
}

.chart-card {
  min-height: 360px;
}

.table-progress {
  width: 100%;
}

@media (max-width: 1200px) {
  .charts-row {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 768px) {
  .overview-row {
    grid-template-columns: repeat(2, 1fr);
  }
  
  .charts-row {
    grid-template-columns: 1fr;
  }
}
</style>
