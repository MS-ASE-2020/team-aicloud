<template>
  <div class="dashboard-container">
    <el-table
      :data="Datasets"
      border
    >
      <el-table-column
        prop="id"
        label="ID"
      />
      <el-table-column
        prop="name"
        label="Name"
      />
      <el-table-column
        prop="time_created"
        label="Create Time"
      />
      <el-table-column
        label="Operate"
      >
        <template slot-scope="scope">
          <el-button type="text" size="small" @click="DeleteDataSet(scope.row.id)">Delete</el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-upload class="upload" drag action="/invalid" accept=".csv" :on-success="onSuccess" :auto-upload="true" :before-upload="BeforeUpload" :http-request="UploadData" style="margin:30px auto">
      <i class="el-icon-upload" />
      <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
      <div slot="tip" class="el-upload__tip">只能上传csv文件</div>
    </el-upload>
  </div>
</template>

<script>
import {
  mapGetters
} from 'vuex'
import {
  input
} from '@/api/input'
import { getDataSets, deleteDataSets } from '@/api/column'

export default {
  name: 'Dashboard',
  data() {
    return {
      Datasets: []
    }
  },
  computed: {
    ...mapGetters([
      'name'
    ])
  },
  created() {
    this.fetchData()
  },
  methods: {
    DeleteDataSet(id) {
      deleteDataSets(id).then(response => {
        this.fetchData()
      }).catch(err => {
        console.log(err)
      })
    },
    fetchData() {
      getDataSets().then(response => {
        this.$set(this.Datasets, response.data)
        this.Datasets = response.data
      }).catch(err => {
        console.log(err)
      })
    },
    newJob() {
      this.$router.push({ path: '/job' })
    },
    onSuccess(response) {
      console.log(response)
    },
    BeforeUpload(file) {
      // console.log(file)
    },
    UploadData(f) {
      console.log(f)
      const data = new FormData()
      data.append('upload', f.file)
      data.append('name', f.file.name)
      input(data).then(response => {
        // this.$message('Success!')
        this.fetchData()
      }).catch(err => {
        console.log(err)
      })
    }
  }
}
</script>

<style lang="scss" scoped>
.dashboard {
    &-container {
        margin: 30px;
    }

    &-text {
        font-size: 30px;
        line-height: 46px;
    }
}
</style>
