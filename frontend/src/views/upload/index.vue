<template>
  <div class="dashboard-container">
    <el-upload class="upload-demo" drag action="/invalid" accept=".csv" :on-success="onSuccess" :auto-upload="true" :before-upload="BeforeUpload" :http-request="UploadData">
      <i class="el-icon-upload" />
      <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
      <div slot="tip" class="el-upload__tip">只能上传csv文件，且不超过500kb</div>
    </el-upload>
    <el-link type="success" @click="newJob()">Create New Job</el-link>
  </div>
</template>

<script>
import {
  mapGetters
} from 'vuex'
import {
  input
} from '@/api/input'

export default {
  name: 'Dashboard',
  computed: {
    ...mapGetters([
      'name'
    ])
  },
  methods: {
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
        this.$message('Success!')
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
