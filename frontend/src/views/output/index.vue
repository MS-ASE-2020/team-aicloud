<template>
  <div>
    <el-row v-for="item in jobList" :key="item.id" :gutter="20">
      <el-col :span="2">
        <p>{{ 'JOB ' + String(item.id) }}</p>
      </el-col>
      <el-col :span="16">
        <el-progress
          :text-inside="true"
          :stroke-width="40"
          :percentage="Percent(item.status)"
        />
      </el-col>
      <el-col :span="4">
        <el-button
          icon="el-icon-view"
          type="primary"
          :disabled="item.status === 2 || item.status == 3 ? false: true"
          circle
          @click="viewResult(item.id)"
        />
      </el-col>
    </el-row></div>
</template>

<script>
import { getJobs } from '@/api/table'
export default {
  data() {
    return {
      jobList: []
    }
  },
  created() {
    this.fetchdata()
  },
  methods: {
    Percent(status) {
      if (status === 0 || status === 4) {
        return 0
      } else if (status === 1) {
        return 50
      } else {
        return 100
      }
    },
    viewResult(jobId) {
      this.$router.push({ path: '/output/job', query: { job_id: jobId }})
    },
    fetchdata() {
      getJobs().then(response => {
        this.jobList = { ...response.data.data }
      }).catch(err => {
        console.log(err)
      })
    }
  }
}
</script>
