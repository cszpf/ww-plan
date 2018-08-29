<template>
  <div id="storeRanking">
    <el-form label-width="80px" class="screen">
      <el-form-item label="日期 :">
        <el-date-picker :clearable="clearablebl" :picker-options="pickerOptions0" v-model="date" type="daterange" placeholder="选择日期" size="small" value-format="yyyy-MM-dd" format="yyyy-MM-dd" @change="dateData">
        </el-date-picker>
      </el-form-item>
    </el-form>
    <div class="stroetop">
      <div :class="[item._boeder == 2?'td-border':'','stroetop-table']" v-for="(item, index) in dataList" :key="index">
        <div class="stroetop-td">{{item._key}}</div>
        <div></div>
      </div>
    </div>
  </div>
</template>
<script>
import axios from 'axios'
export default {
  name: 'pageView',
  data () {
    return {
      clearablebl: false,
      date: [],
      pickerOptions0: {
        disabledDate (time) {
          return time.getTime() > Date.now() - 8.64e6
        },
        shortcuts: [
          {
            text: '最近一周',
            onClick (picker) {
              const end = new Date()
              const start = new Date()
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 7)
              picker.$emit('pick', [start, end])
            }
          },
          {
            text: '最近一个月',
            onClick (picker) {
              const end = new Date()
              const start = new Date()
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 30)
              picker.$emit('pick', [start, end])
            }
          },
          {
            text: '最近三个月',
            onClick (picker) {
              const end = new Date()
              const start = new Date()
              start.setTime(start.getTime() - 3600 * 1000 * 24 * 90)
              picker.$emit('pick', [start, end])
            }
          }
        ]
      },
      postData: {
        ids: sessionStorage.getItem('id'),
        opt: {
          'ADMIN_REGION_CODE': '', // 行政区
          'MICRO_REGION_CODE': '', // 微区域
          'SALE_NAME': '', // 销售经理
          'MERCHANT_TYPE': '', // 行业
          'OPERATOR_NAME': '', // 运营经理
          'MERCHANT_ID': '', // 商户
          'SUBBRANCH_ID': '' // 门店
        },
        date: [],
        page: 0,
        columns: 10
      },
      dataList: [],
      tableList: false,
      page: 0,
      pageright: true,
      loading: true
    }
  },
  created () {
    let today = new Date()
    let lastMonth = new Date(today.getTime() - 3600 * 1000 * 24 * 30)
    this.date.push(this.formatDate(lastMonth), this.formatDate(today))
    console.log(this.date)
    this.postData.date = this.date
  },
  mounted () {
    this.loadData()
  },
  methods: {
    formatDate  (date) {
      let y = date.getFullYear()
      let m = date.getMonth() + 1
      m = m < 10 ? '0' + m : m
      let d = date.getDate()
      d = d < 10 ? ('0' + d) : d
      return y + '-' + m + '-' + d
    },
    dateData () {
      this.postData.date = this.date
      this.loadData()
    },
    loadData () {
      this.loading = true
      this.page = 0
      this.dataList = []
      axios({method: 'post', url: this.$store.state.url + '/api/table_export', data: this.postData})
        .then(response => {
          if (response.data) {
            this.loading = false
          }
          console.log(response)
          console.log(response.data)
          // this.shopList = response.data.splice(0, 1)
          // console.log(this.shopList)
          this.dataList = response.data
          this.dataList.forEach((item, index) => {
            item['_boeder'] = 1
            if (index === 0) {
              item['_boeder'] = 2
            }
            if (index === 2) {
              item['_boeder'] = 2
            }
            if (index === 4) {
              item['_boeder'] = 2
            }
            if (index === 7) {
              item['_boeder'] = 2
            }
            if (index === 9) {
              item['_boeder'] = 2
            }
            console.log(item)
          })
          // console.log(this.dataList)
          // this.dataPageList = response.data.slice(this.page * 10, 10)
          // console.log(this.dataPageList)
        })
        .catch(function (error) {
          console.log(error)
        })
    }
  }
}
</script>
<style scoped>
#storeRanking {
  width: 100%;
  height: 100vh;
}
.stroetop {
  width: 100%;
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: flex-start;
}
.stroetop-table {
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: flex-start;
  padding: 10px;
}
stroetop-td {
  padding: 5px;
}
.td-border {
  border-right: 1px solid #dddddd
}
</style>
