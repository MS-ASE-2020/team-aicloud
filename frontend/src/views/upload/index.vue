<template>
  <div style="margin: 30px">
    <el-table
      class="table"
      :data="Datasets"
      border
      style="width: 100%;margin: 30px auto"
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
    <div style="display: block; margin: 30px auto">
      <h4>UPLOAD</h4>
      <el-upload
        drag
        action="/invalid"
        accept=".csv"
        :on-success="onSuccess"
        :auto-upload="true"
        :before-upload="BeforeUpload"
        :http-request="UploadData"
      >
        <i class="el-icon-upload" />
        <div class="el-upload__text">Drag OR <em>Click</em></div>
        <div slot="tip" class="el-upload__tip">.csv only</div>
      </el-upload>
    </div>
    <div style="width: 50%; margin: 30px 0 0 0"><h4>KUSTO</h4>
      <P>Name</P>
      <el-input
        v-model="Dataname"
        type="textarea"
        autosize
      />
      <p>Query</p>
      <el-input
        v-model="query"
        type="textarea"
        autosize
      />
      <el-button type="primary" style="margin: 30px auto; display: block" @click="UploadKustoQuery()">UPLOAD</el-button>
    </div>
  </div></template>

<script>
import {
  mapGetters
} from 'vuex'
import {
  input
} from '@/api/input'
import { getDataSets, deleteDataSets } from '@/api/column'

export default {
  data() {
    return {
      Datasets: [],
      Dataname: '',
      query: ''
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
    },
    UploadKustoQuery() {

    }
  }
}
</script>
