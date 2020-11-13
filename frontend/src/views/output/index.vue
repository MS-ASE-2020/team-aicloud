<template>
  <div>
    <el-collapse v-model="activeRow">
      <el-collapse-item
        v-for="item in datalists"
        :key="item.ts_id"
        :title="'TimeStamp'+String(item.ts_id)"
        :name="item.ts_id"
        style="font-size:100%"
      >
        <series-table :results="item.results" />
      </el-collapse-item>
    </el-collapse>
  </div>
</template>

<script>
import SeriesTable from './components/SeriesTable'
import { getList } from '@/api/table'
export default {
  components: {
    SeriesTable
  },
  data() {
    return {
      activeRow: [],
      job_id: '',
      datalists: [],
      listLoading: true,
      retval: null
    }
  },
  created() {
    this.listLoading = true
    this.job_id = this.$route.query.job_id
    this.fetchdata()
  },
  methods: {
    fetchdata() {
      var resdata
      getList(this.job_id).then(response => {
        resdata = { ...response.data }
        console.log(resdata.status)
        if (resdata.status === 3) {
          this.datalists = resdata.results
          this.listLoading = false
        }
      })
    }
  }
}
</script>
