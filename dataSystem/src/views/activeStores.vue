<template>
    <div id="activeStores">
     <div class="activeStores-title"><span>活跃门店数量</span></div>
     <el-form label-width="80px" class="screen">
        <el-form-item label="日期 :">
          <el-date-picker :clearable="clearablebl" :picker-options="pickerOptions0" v-model="date" type="daterange" placeholder="选择日期" size="small" value-format="yyyy-MM-dd" format="yyyy-MM-dd" @change="dateData">
          </el-date-picker>
        </el-form-item>
      </el-form>
      <div v-if="loadBl" class="loadBlClass">
          <span>暂无数据</span>
      </div>
      <div class="overflow-height" v-loading="loading" element-loading-text="拼命加载中" element-loading-spinner="el-icon-loading" element-loading-background="rgba(250, 250, 250, 1)">
        <div class="box" v-if="dataPageList.length!=0">
          <div class="box-flex">
            <div v-for="(item, index) in shopList" :key="index">
              <div class="box-list box-birder">{{item._key}}</div>
              <div class="box-list" v-for="(items, indexs) in item._data" :key="indexs">{{items}}</div>
            </div>
          </div>
          <div class="box-border">
            <div class="box-left" v-if="page!=0" @click="leftList">
                <i class="el-icon-caret-left"></i>
            </div>
            <div class="box-flex" v-for="(items, index) in dataPageList" :key="index">
                <div class="box-list1 box-birder">{{items._key}}</div>
                <div class="box-list1" v-for="(itemss, indexs) in items._data" :key="indexs">{{itemss}}</div>
            </div>
            <div class="box-right" @click="rightList" v-if="pageright">
                <i class="el-icon-caret-right"></i>
            </div>
          </div>
        </div>
      </div>
    </div>
</template>
<script>
import axios from 'axios'
export default {
  name: 'activeStores',
  data () {
    return {
      loadBl: false,
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
        ids: 'hymd',
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
      shopList: [{'_key': '', '_data': []}],
      dataPageList: [],
      tableList: false,
      page: 0,
      pageright: true,
      loading: false
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
      this.loadBl = false
      this.loading = true
      this.dataList = []
      this.dataPageList = []
      axios({method: 'post', url: 'http://localhost:5000/api/table_export', data: this.postData})
        .then(response => {
          if (response.data) {
            this.loading = false
          }
          console.log(response)
          console.log(response.data)
          console.log(this.shopList)
          this.dataList = response.data
          console.log(this.dataList)
          if (this.dataList.length === 0) {
            this.loadBl = true
          } else {
            if (this.dataList.length <= 10) {
              this.pageright = false
              this.dataPageList = response.data
            } else {
              this.dataPageList = response.data.slice(this.page * 10, 10)
              this.pageright = true
              console.log(this.dataPageList)
            }
          }
        })
        .catch(function (error) {
          console.log(error)
        })
    },
    rightList () {
      this.page += 1
      console.log(this.page)
      console.log(this.dataList)
      console.log(this.dataPageList)
      this.dataPageList = this.dataList.slice(this.page * 10, this.page * 10 + 10)
      if (this.dataPageList.length < 10 || (this.page + 1) * 10 >= this.dataList.length) {
        this.pageright = false
      } else {
        this.pageright = true
      }
    },
    leftList () {
      this.pageright = true
      this.page -= 1
      console.log(this.page)
      console.log(this.dataList)
      console.log(this.dataPageList)
      this.dataPageList = this.dataList.slice(this.page * 10, this.page * 10 + 10)
    }
  }
}
</script>
<style scoped>
.loadBlClass {
  display: flex;
  flex-direction: row;
  justify-content: center;
  width: 100%;
}
.box-border {
  border-left: 1px solid #dddd;
  border-right: 1px solid #dddd;
  width: 100%;
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: flex-start;
}
.table-overflow {
    width: 100%;
    overflow-x: hidden;
}
table th {
    min-width: 50px;
}
.activeStores-title {
  margin-top: 20px;
  margin-bottom: 20px;
  padding-left: 35px;
}
#lossMerchants {
  font-size: 14px;
  height: 100vh;
  width: 100%;
}
.box {
  width: 100%;
  /* margin: 15px; */
  /* min-width: 1000px; */
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  align-items: flex-start;
}
.box-flex {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  width: 10%;
  min-width: 90px;
}
.box-list {
  height: 40px;
  /* line-height: 40px; */
  /* min-width: 120px; */
  width: 100%;
  border-right: 1px solid #dddddd;
  text-align: center;
  /* word-wrap:break-word; */
  /* word-break:break-all; */
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
  /* margin: 5px; */
}
.box-list1 {
  word-wrap: break-word;
  word-break:break-all;
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
  /* margin: 5px; */
}
.box-birder {
  border-bottom: 1px solid #dddddd;
}
.box-left {
  width: 2%;
  min-width: 10px;
  line-height: 40px;
  height: 40px;
  text-align: center;
  vertical-align: middle;
  border-bottom: 1px solid #dddddd;
  cursor: pointer;
  /* margin: 5px; */
}
.box-right {
  width: 2%;
  min-width: 10px;
  line-height: 40px;
  height: 40px;
  text-align: center;
  vertical-align: middle;
  border-bottom: 1px solid #dddddd;
  cursor: pointer;
  /* margin: 5px; */
}
.box-left:hover {
  opacity: 0.7;
  background: #dddddd;
}
.box-right:hover {
  opacity: 0.7;
  background: #dddddd;
}
.overflow-height {
  min-height: 300px;
  max-height: 500px;
  width: 100%;
  overflow: auto;
}
</style>
