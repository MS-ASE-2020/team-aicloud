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
