import request from '@/utils/request'

export function getList(params) {
  return request({
    url: '/result/1',
    method: 'get',
    params
  })
}
