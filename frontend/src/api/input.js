import request from '@/utils/request'

export function input(data) {
  return request({
    url: '/upload/data',
    method: 'post',
    data
  })
}
