import request from '@/utils/request'

export function getList(id) {
  return request({
    url: '/job/' + String(id) + '/job_results/',
    method: 'get'
  })
}
