const { createApp } = Vue
const app = createApp({
	data() {
		return {
			message: 'Hello Vue!',
            data: [],
            requested: false
		}
	},
	methods: {
        requestData() {
            this.requested = true
			fetch('http://localhost:3000/api/data')
				.then(response => response.json())
				.then(data => {
					this.data = data.map(d => {
						d[10] = d[10] ? JSON.parse(d[10]) : []
						return d
					})
				})
		},
		makeChart1() {
			var myChart = echarts.init(document.getElementById('chart_1'))

			// 指定图表的配置项和数据
			var option = {
				title: {
					text: 'Top 5 热门国家',
				},
				tooltip: {},
				xAxis: {
					data: ['衬衫', '羊毛衫', '雪纺衫', '裤子', '高跟鞋', '袜子'],
				},
				yAxis: {},
				series: [
					{
						name: '销量',
						type: 'bar',
						data: [5, 20, 36, 10, 10, 20],
					},
				],
			}

			// 使用刚指定的配置项和数据显示图表。
			myChart.setOption(option)
        },
        makeChart2() {
			var myChart = echarts.init(document.getElementById('chart_2'))

			// 指定图表的配置项和数据
			var option = {
				title: {
					text: 'Top 5 热门人物',
				},
				tooltip: {},
				xAxis: {
					data: ['衬衫', '羊毛衫', '雪纺衫', '裤子', '高跟鞋', '袜子'],
				},
				yAxis: {},
				series: [
					{
						name: '销量',
						type: 'bar',
						data: [5, 20, 36, 10, 10, 20],
					},
				],
			}

			// 使用刚指定的配置项和数据显示图表。
			myChart.setOption(option)
        },
        makeChart3() {
			var myChart = echarts.init(document.getElementById('chart_3'))

			// 指定图表的配置项和数据
			var option = {
				title: {
					text: 'Top 5 热门事件',
				},
				tooltip: {},
				xAxis: {
					data: ['衬衫', '羊毛衫', '雪纺衫', '裤子', '高跟鞋', '袜子'],
				},
				yAxis: {},
				series: [
					{
						name: '销量',
						type: 'bar',
						data: [5, 20, 36, 10, 10, 20],
					},
				],
			}

			// 使用刚指定的配置项和数据显示图表。
			myChart.setOption(option)
        },
        makeChart4() {
			var myChart = echarts.init(document.getElementById('chart_4'))

			// 指定图表的配置项和数据
            var option = {
                title: {
					text: '热门趋势图',
				},
                xAxis: {
                    data: ['A', 'B', 'C', 'D', 'E']
                  },
                  yAxis: {},
                  series: [
                    {
                      data: [10, 22, 28, 43, 49],
                      type: 'line',
                      stack: 'x'
                    },
                    {
                      data: [5, 4, 3, 5, 10],
                      type: 'line',
                      stack: 'x'
                    }
                  ]
              };

			// 使用刚指定的配置项和数据显示图表。
			myChart.setOption(option)
        },
        makeCharts() {
            this.makeChart1()
            this.makeChart2()
            this.makeChart3()
            this.makeChart4()
        }
	},
	mounted() {
		this.makeCharts()
	},
})
window.app = app
