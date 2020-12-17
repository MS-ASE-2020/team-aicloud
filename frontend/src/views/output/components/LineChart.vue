<template>
  <div :class="className" :style="{height:height,width:width}" />
</template>

<script>
import echarts from 'echarts'
require('echarts/theme/macarons') // echarts theme
import resize from './mixins/resize'

export default {
  mixins: [resize],
  props: {
    className: {
      type: String,
      default: 'chart'
    },
    width: {
      type: String,
      default: '100%'
    },
    height: {
      type: String,
      default: '350px'
    },
    autoResize: {
      type: Boolean,
      default: true
    },
    chartData: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      chart: null
    }
  },
  watch: {
    chartData: {
      deep: true,
      handler(val) {
        this.setOptions(val)
      }
    }
  },
  mounted() {
    this.$nextTick(() => {
      this.initChart()
    })
  },
  beforeDestroy() {
    if (!this.chart) {
      return
    }
    this.chart.dispose()
    this.chart = null
  },
  methods: {
    initChart() {
      this.chart = echarts.init(this.$el, 'macarons')
      this.setOptions(this.chartData)
    },
    generateSeries() {
      const series = []
      const lists = this.chartData.predictions
      for (var i = 0; i < lists.length; i++) {
        const setting = {
          type: 'line',
          smooth: true
        }
        setting['data'] = lists[i]
        series.push(setting)
      }
      return series
    },
    setOptions({ hisLength, predictions, timestamps } = {}) {
      this.chart.setOption({
        // option中的每个属性是一类组件
        // 如果有多个同类组件 就是一个数组
        xAxis: {
          data: timestamps,
          boundaryGap: false,
          axisTick: {
            show: false
          }
        },
        grid: {
          left: 10,
          right: 10,
          bottom: 20,
          top: 30,
          containLabel: true
        },
        tooltip: {
          trigger: 'axis',
          axisPointer: {
            type: 'cross'
          },
          padding: [5, 10]
        },
        yAxis: {
          axisTick: {
            show: false
          },
          min: function(value) {
            return value.min
          }
        },
        visualMap: {
          show: false,
          dimension: 0,
          pieces: [{
            lte: hisLength,
            color: 'green'
          }, {
            gt: hisLength,
            color: 'red'
          }]
        },
        series: [{
          name: 'Predicitons',
          type: 'line',
          data: predictions
        }]
      })
    }
  }
}
</script>

<style scoped>
.line{
  text-align: center;
}
</style>
