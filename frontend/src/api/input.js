import request from '@/utils/request'

export function input(data) {
  return request({
    url: '/api/project/data',
    method: 'post',
    data: data
  })
}