<template>
  <div class="output">
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
      <el-col :span="1">
        <el-button
          icon="el-icon-view"
          type="primary"
          :disabled="item.status === 2 || item.status == 3 ? false: true"
          circle
          @click="viewResult(item.id)"
        />
      </el-col>
      <el-col :span="1">
        <el-button
          icon="el-icon-delete"
          type="danger"
          circle
          @click="deleteJob(item.id)"
        />
      </el-col>
    </el-row></div>
</template>

<script>
import { getJobs, deleteJob } from '@/api/table'
export default {
  name: 'Output',
  data() {
    return {
      jobList: [],
      c: null
    }
  },
  created() {
    this.fetch()
    this.c = setInterval(this.fetch(), 5000)
  },
  beforeDestroy() {
    clearInterval(this.c)
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
    deleteJob(jobId) {
      deleteJob(jobId).then(response => {
        console.log(response)
      }).catch(err => {
        console.log(err)
      })
    },
    viewResult(jobId) {
      this.$router.push({ path: '/output/job', query: { job_id: jobId }})
    },
    fetch() {
      console.log('fetch')
      getJobs().then(response => {
        this.jobList = { ...response.data.data }
      }).catch(err => {
        console.log(err)
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.output {
        margin: 30px;
}
</style>
