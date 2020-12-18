import request from '@/utils/request'

export function getList(id) {
  return request({
    url: '/job/' + String(id) + '/job_results/',
    method: 'get'
  })
}

export function getJobs() {
  return request({
    url: '/job/',
    method: 'get'
  })
}

export function deleteJob(id) {
  return request({
    url: '/job/' + String(id) + '/',
    method: 'delete'
  })
}

export function download(modelId) {
  return request({
    url: '/job/' + String(modelId) + '/export_model/',
    method: 'get'
  })
}

export function downloadsetting(modelId) {
  return request({
    url: '/job/' + String(modelId) + '/export_settings/',
    method: 'get'
  })
}
