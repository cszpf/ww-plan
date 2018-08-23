<template>
    <div id="pageView">
      <el-form label-width="80px" class="screen">
        <el-form-item label="日期 :">
          <el-date-picker :clearable="clearablebl" :picker-options="pickerOptions0" v-model="date" type="daterange" placeholder="选择日期" size="small" value-format="yyyy-MM-dd" format="yyyy-MM-dd" @change="dateData">
          </el-date-picker>
        </el-form-item>
      </el-form>
      <div class="table-overflow">
        <table>
            <thead>
                <tr>
                    <th>日期</th>
                    <th v-for="(item, index) in titelList" :key="index">{{item}}</th>
                </tr>
            </thead>
        </table>        
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
      shopList: null,
      titelList: []
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
      console.log(this.date)
    },
    loadData () {
      axios({method: 'post', url: 'http://localhost:5000/api/table_export', data: this.postData})
        .then(response => {
          console.log(response)
          console.log(response.data)
          this.shopList = response.data.splice(0, 1)
          this.titelList = this.shopList[0]._data
          console.log(this.shopList)
          console.log(typeof this.shopList)
          console.log(this.shopList[0]._data)
        })
        .catch(function (error) {
          console.log(error)
        })
    }
  }
}
</script>
<style scoped>
.table-overflow {
    width: 1000px;
    overflow: auto
}
</style>
