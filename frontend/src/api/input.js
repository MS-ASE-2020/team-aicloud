import request from '@/utils/request'

export function input(data) {
  return request({
    url: '/data/',
    method: 'post',
    data: data
  })
}