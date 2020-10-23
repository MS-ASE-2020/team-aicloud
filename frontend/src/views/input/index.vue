<template>
  <div class="dashboard-container">
    <el-upload
      class="upload-demo"
      drag
      action="/invalid"
      accept=".csv"
      :http-request="UploadData"
    >
      <i class="el-icon-upload"></i>
      <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
      <div slot="tip" class="el-upload__tip">只能上传csv文件，且不超过500kb</div>
    </el-upload> 
  </div>
</template>

<script>
import { mapGetters } from 'vuex'
import { input } from '@/api/input'

export default {
  name: 'Dashboard',
  computed: {
    ...mapGetters([
      'name'
    ])
  },
  methods: {
    onSuccess(response) {
      console.log(response)
    },
    BeforeUpload(file) {
      console.log(file)
    },
    UploadData(f) {
<<<<<<< HEAD
      console.log(f)
      const form = new FormData()
      form.append('file', f.file)
      input({"file": form}).then((result) => {
        console.log(result.code)
      }).catch((err) => {
        err.log()
      });
=======
      input(f.file)
>>>>>>> 32f9159fbbfc8fdc7af66d19e07cb476775db3fa
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
