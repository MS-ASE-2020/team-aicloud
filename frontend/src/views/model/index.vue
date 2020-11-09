<template>
  <div class="app-container">
    <el-table
      :data="series"
      style="width: 100%"
    >
      <el-table-column type="expand">
        <template slot-scope="props">
          <series-set :id="props.row.ts_id" :features="features" v-on:setDone="setDone"></series-set>
        </template>
      </el-table-column>
      <el-table-column
        lable="Series ID"
        prop="ts_id"
      >
      </el-table-column>
      <el-table-column
        label=groupby_key_name
        prop="groupby_val"
      >
      </el-table-column>
      <el-table-column
        label="Apply All"
      >
        <template slot-scope="props">
          <el-button size="mini" @click="ApplyAll(props.rows.id)">Apply</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-button type="primary" @click="onSubmit">Submit</el-button>
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
      jobId: 1,
      series: [
     {
         "ts_id": 1,
         "groupby_val": "('asiasoutheast', 'FS')"
     },
     {
         "ts_id": 2,
         "groupby_val": "('ussouth', 'A')"
     }
 ],
      groupby_key_name: '',
      features: [1,2,3],
      filters: [4,5],
      seriesSettings: []
    }
  },
  created() {
    this.fetchData()
  },
  methods: {
    createName(arr) {
      arr.forEach(element => {
        groupby_key_name = groupby_key_name + String(element) + ','
      });
    },
    fetchData() {
      fetchSeries(this.jobId).then( response => {
        // this.features = response.data.features
        // this.series = response.data.ts_details
        // this.filters = response.data.groupby_key
        // this.createName(this.filters)
      }).catch( err => {
        console.log(err)
      })
    },
    setDone(settings) {
      this.seriesSettings.push(settings)
    },
    onSubmit() {
      postSeries(this.jobId, this.seriesSettings).then( response => {
        console.log(response.status)
      }).catch( err => {
        console.log(err)
      })
    }
  }
}
</script>

<style scoped>
.line{
  text-align: center;
}
</style>
