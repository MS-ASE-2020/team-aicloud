<template>
  <div class="output">
    <el-row v-for="item in jobList" :key="item.id" :gutter="20" justify="center">
      <el-col :span="2">
        <p>{{ 'JOB ' + String(item.id) }}</p>
      </el-col>
      <el-col :span="18">
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
          :disabled="item.status === 3 ? false: true"
          circle
          @click="viewResult(item.id)"
        />
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
      number: null
    }
  },
  created() {
    this.fetch()
  },
  beforeDestroy() {
    clearInterval(this.number)
  },
  methods: {
    stopPolling() {
      console.log(this.number)
      clearInterval(this.number)
    },
    Percent(status) {
      if (status === 0 || status === 4) {
        return 0
      } else if (status === 1 || status === 2) {
        return 50
      } else {
        return 100
      }
    },
    deleteJob(jobId) {
      deleteJob(jobId).then(response => {
        getJobs().then(res => {
          this.jobList = { ...res.data.data }
        }).catch(err => {
          console.log(err)
        })
      }).catch(err => {
        console.log(err)
      })
    },
    viewResult(jobId) {
      this.$router.push({ path: '/output/job', query: { job_id: jobId }})
    },
    fetch() {
      getJobs().then(response => {
        this.jobList = { ...response.data.data }
        var vm = this
        vm.number = setInterval(function() {
          getJobs().then(res => {
            const newdata = res.data.data
            for (var i = 0; i < vm.jobList.length; i++) {
              if (vm.jobList[i].status !== newdata[i].status) {
                vm.$set(vm.jobList, i, newdata[i])
              }
            }
            if (newdata.length > vm.jobList.length) {
              for (i = vm.jobList.length; i < newdata.length; i++) {
                vm.$set(vm.jobList, i, newdata[i])
              }
            } else {
              vm.stopPolling()
            }
          }).catch(err => {
            console.log(err)
          })
        }, 1000 * 5)
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
