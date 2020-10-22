import axios from 'axios'

export function input(file) {
  const Axios = axios.create({
    method: 'post',//请求方法
    headers: {'Content-Type': 'multiple/form-data'},//请求头 'multiple/form-data'
    baseURL: process.env.VUE_APP_BASE_API, // url = base url + request url
    // withCredentials: true, // send cookies when cross-domain requests
    timeout: 5000 // request timeout
  })

  var fd = new FormData();
  fd.append('file', file);
  Axios.post("/upload/data", fd)
}
