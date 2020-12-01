<template>
  <div>
    <h1 style="margin: 20px">Set Each Series</h1>
    <el-table
      :data="series"
      style="width: 100%"
    >
      <el-table-column type="expand">
        <template slot-scope="props">
          <series-set :id="props.row.ts_id" :features="features" @setDone="setDone(arguments)" />
        </template>
      </el-table-column>
      <el-table-column
        label="Series_Id"
        prop="ts_id"
      />
      <el-table-column
        :label="groupby_key_name"
        prop="groupby_val"
      />
      <el-table-column
        label="Setting Count"
        prop="count"
      />
    </el-table>
    <el-button type="primary" style="display:block;margin:20px auto" @click="onSubmit">Submit</el-button>
  </div>
</template>

<script>
import { postSeries, fetchSeries } from '@/api/model'
import SeriesSet from './components/SeriesSet'

export default {
  components: {
    SeriesSet
  },
  data() {
    return {
      min_ts_id: 0,
      jobId: '',
      series: [],
      groupby_key_name: '',
      features: [],
      filters: [],
      seriesSettings: []
    }
  },
  created() {
    this.jobId = this.$route.query.job_id
    this.fetchData()
  },
  methods: {
    DisableSub() {
      let disable = false
      for (var i = 0; i < this.series.length; i++) {
        disable = (this.series[i].count === 0)
      }
      return disable
    },
    minId() {
      let tmpmin = this.series[0]['ts_id']
      this.series.forEach(element => {
        tmpmin = element.ts_id < tmpmin ? element.ts_id : tmpmin
      }
      )
      this.min_ts_id = tmpmin
    },
    createName(arr) {
      console.log(arr)
      arr.forEach(element => {
        this.groupby_key_name = this.groupby_key_name + String(element) + ' '
      })
    },
    fetchData() {
      // fetch all series
      this.createName(this.filters)
      fetchSeries(this.jobId).then(response => {
        this.features = response.data.features
        this.series = response.data.ts_details
        // Add count
        for (let i = 0; i < this.series.length; i++) {
          this.series[i]['count'] = 0
          this.series[i]['metrics'] = []
        }
        this.filters = response.data.groupby_key
        this.createName(this.filters)
        this.minId()
      }).catch(err => {
        console.log(err)
      })
    },
    setDone(params) {
      const id = params[0]
      const applyAll = params[1]
      const settings = params[2]
      if (applyAll) {
        const len = this.series.length
        for (let i = 0; i < len; i++) {
          const tmp = { ...settings }
          tmp['ts_id'] = this.series[i].ts_id
          const row = this.series[i]
          row.count = row.count + 1
          this.$set(this.series, i, row)
          this.seriesSettings.push(tmp)
        }
      } else {
        settings['ts_id'] = id
        const idx = id - this.min_ts_id
        const row = this.series[idx]
        row.count = row.count + 1
        this.$set(this.series, idx, row)
        this.seriesSettings.push(settings)
      }
    },
    onSubmit() {
      if (!this.DisableSub()) {
        postSeries(this.jobId, this.seriesSettings).then(response => {
          this.$message('Submit!')
          this.$router.push({ path: '/output', query: { job_id: this.jobId }})
        }).catch(err => {
          console.log(err)
        })
      } else {
        alert('EVERY SERIES NEED SETTINGS')
      }
    }
  }
}
</script>

<style scoped>
.line{
  text-align: center;
}
</style>
