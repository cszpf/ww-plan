<template>
  <div id="amendTicket">
    <div class="activeStores-title"><span>修改券数</span></div>
    <el-form label-width="80px" class="screen">
      <el-form-item label="日期 :">
        <el-date-picker :clearable="clearablebl" :picker-options="pickerOptions0" v-model="date" type="daterange" placeholder="选择日期" size="small" value-format="yyyy-MM-dd" format="yyyy-MM-dd" @change="dateData">
        </el-date-picker>
        <!-- <el-button class="guidetable" type="success" size="small" @click="gotoData">导表</el-button> -->
      </el-form-item>
    </el-form>
    <div class="stroetop" v-loading="loading" element-loading-text="拼命加载中" element-loading-spinner="el-icon-loading" element-loading-background="rgba(250, 250, 250, 1)">
      <div class="stroetop-table" v-for="(item, index) in dataList" :key="index">
        <div class="stroetop-td stroetop-boeder">{{item._key}}</div>
        <div class="stroetop-td" v-for="(items, indexs) in item._data" :key="indexs">{{items}}</div>
      </div>
    </div>
  </div>
</template>
<script>
import axios from 'axios'
export default {
  name: 'amendTicket',
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
        ids: 'xgq',
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
      loading: true,
      dataList: []
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
    _download (data, ids) {
      let url = window.URL.createObjectURL(new Blob([data.data]))
      let link = document.createElement('a')
      link.style.display = 'none'
      link.href = url
      link.setAttribute('download', '' + ids + '.xlsx')
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
    },
    gotoData () {
      axios({method: 'post', url: this.$store.state.url + '/api/export', data: this.postData, responseType: 'blob'})
        .then(response => {
          this._download(response, this.postData['ids'])
        })
        .catch(function (error) {
          console.log(error)
        })
    },
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
      this.dataList = []
      axios({method: 'post', url: this.$store.state.url + '/api/table_export', data: this.postData})
        .then(response => {
          if (response.data) {
            this.loading = false
          }
          console.log(response)
          console.log(response.data)
          response.data.splice(0, 1)
          this.dataList = response.data
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
#amendTicket {
  font-size: 14px;
  height: 100vh;
  width: 100%;
  padding:15px;
}
.stroetop {
  width: 100%;
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: flex-start;
  min-height: 300px;
}
.stroetop-table {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  width: 17%;
  min-width: 140px;
}
.stroetop-td {
  height: 40px;
  /* line-height: 40px; */
  /* min-width: 80px; */
  width: 100%;
  word-wrap:break-word;
  text-align: center;
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  padding: 5px;
}
.td-border {
  border-right: 1px solid #dddddd
}
.stroetop-boeder {
  border-bottom: 1px solid #dddddd;
}
.guidetable {
  float: right;
  margin-right: 50px;
}
</style>
