<template>
  <div id="referralsTicket">
    <div class="activeStores-title"><span>下线券数</span></div>
    <el-form label-width="80px" class="screen">
      <el-form-item label="日期 :">
        <el-date-picker :clearable="clearablebl" :picker-options="pickerOptions0" v-model="date" type="daterange" placeholder="选择日期" size="small" value-format="yyyy-MM-dd" format="yyyy-MM-dd" @change="dateData">
        </el-date-picker>
      </el-form-item>
    </el-form>
  </div>
</template>
<script>
import axios from 'axios'
export default {
  name: 'referralsTicket',
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
        ids: 'xxq',
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
      }
    }
  },
  created () {
    let today = new Date()
    let lastMonth = new Date(today.getTime() - 3600 * 1000 * 24 * 30)
    this.date.push(this.formatDate(lastMonth), this.formatDate(today))
    console.log(this.date)
    this.postData.date = this.date
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
      axios({method: 'post', url: this.$store.state.url + '/api/table_export', data: this.postData})
        .then(response => {
        //   if (response.data) {
        //     this.loading = false
        //   }
          console.log(response)
          console.log(response.data)
          console.log(this.shopList)
        //   this.dataList = response.data
        //   console.log(this.dataList)
        //   if (this.dataList.length === 0) {
        //     this.loadBl = true
        //   } else {
        //     if (this.dataList.length <= 10) {
        //       this.pageright = false
        //       this.dataPageList = response.data
        //     } else {
        //       this.dataPageList = response.data.slice(this.page * 10, 10)
        //       this.pageright = true
        //       console.log(this.dataPageList)
        //     }
        //   }
        })
        .catch(function (error) {
          console.log(error)
        })
    }
  }
}
</script>
<style scoped>
.activeStores-title {
  margin-top: 20px;
  margin-bottom: 20px;
  padding-left: 35px;
}
#referralsTicket {
  font-size: 14px;
  height: 100vh;
  width: 100%;
}
</style>
