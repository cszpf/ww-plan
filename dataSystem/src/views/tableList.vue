<template>
  <div id="tableList">
    <div class="titie">
      <div>
        <el-date-picker @change="dateList" class="pocker" type="daterange" v-model="date" start-placeholder="开始日期" end-placeholder="结束日期" value-format="yyyy-MM-dd"></el-date-picker>
        <el-button type="success" plain @click="gotoIndex">高级检索</el-button>
      </div>
      <div class="tableList-button">
          <el-button type="success" class="table-button" @click="allTableData">导出所有表格</el-button>
          <el-button type="success" class="table-button" @click="customerSummaryData">导出客户汇总</el-button>
      </div>
      <div class="tableList-button">
          <el-button type="success" class="table-button" @click="storesSummaryData">导出门店汇总、异动商户</el-button>
          <el-button type="success" class="table-button" @click="storeBillRatioData">导出门店流水占比</el-button>
      </div>
      <div class="tableList-button">
          <el-button type="success" class="table-button" @click="storesBillData">导出门店流水</el-button>
          <el-button type="success" class="table-button" @click="commodityCouponsData">导出商户用券</el-button>
      </div>
      <div class="tableList-button">
          <el-button type="success" class="table-button" @click="securitiesSummaryData">导出劵汇总、到期劵修改劵下线劵详情</el-button>
          <el-button type="success" class="table-button" @click="storeRankingData">导出门店排行</el-button>
      </div>
      <div class="tableList-button">
          <el-button type="success" class="table-button" @click="commodityCouponsDetailsData">导出商户劵详情</el-button>
          <el-button type="success" class="table-button" @click="stocklistData">导出劵排名</el-button>
      </div>
      <div class="tableList-button1">
          <el-button type="success" class="table-button" @click="pageviewData">导出点击量</el-button>
      </div>
    </div>
  </div>
</template>
<script>
import axios from 'axios'
export default {
  data () {
    return {
      date: ''
    }
  },
  methods: {
    dateList () {
      console.log(this.date)
    },
    allTableData () {
      console.log('导出所有表格')
      this.checkDate({'ids': 'all', 'date': this.date})
    },
    customerSummaryData () {
      console.log('导出客户汇总')
      this.checkDate({'ids': 'khhz', 'date': this.date})
    },
    storesSummaryData () {
      console.log('门店汇总、异动商户')
      this.checkDate({'ids': 'mdhz', 'date': this.date})
    },
    storeBillRatioData () {
      console.log('门店流水占比')
      this.checkDate({'ids': 'mdlszb', 'date': this.date})
    },
    storesBillData () {
      console.log('门店流水')
      this.checkDate({'ids': 'mdls', 'date': this.date})
    },
    commodityCouponsData () {
      console.log('商户用劵')
      this.getData({'ids': 'shyq', 'date': this.date})
    },
    securitiesSummaryData () {
      console.log('劵汇总')
      this.checkDate({'ids': 'qhz', 'date': this.date})
    },
    storeRankingData () {
      console.log('门店排行')
      this.checkDate({'ids': 'mdpm', 'date': this.date})
    },
    commodityCouponsDetailsData () {
      console.log('商户用劵详情')
      this.checkDate({'ids': 'shqxq', 'date': this.date})
    },
    stocklistData () {
      console.log('劵排名')
      this.checkDate({'ids': 'qpm', 'date': this.date})
    },
    pageviewData () {
      console.log('点击量')
      this.getData({'ids': 'djl', 'date': this.date})
    },
    gotoIndex () {
      let _this = this
      _this.$router.push({path: '/storesSummary'})
    },
    download (data, ids) {
      let url = window.URL.createObjectURL(new Blob([data.data]))
      let link = document.createElement('a')
      link.style.display = 'none'
      link.href = url
      link.setAttribute('download', '' + ids + '.xlsx')
      document.body.appendChild(link)
      link.click()
      document.body.removeChild(link)
    },
    getData (datas) {
      let _this = this
      axios({method: 'post', url: 'http://localhost:5000/api/export', data: datas, responseType: 'blob'})
        .then(response => {
          this.download(response, datas['ids'])
        })
        .catch(function (error) {
          console.log(error)
        })
    },
    checkDate (datas) {
      let date1 = this.date
      if (date1) {
        let date = new Date()
        let year = date.getUTCFullYear()
        let month = date.getUTCMonth() + 1
        let day = date.getUTCDate()
        let today = year + '-' + month + '-' + day
        if (month < 10) month = '0' + month
        if (day < 10) day = '0' + day
        if (date1[0] > date1[1]) {
          this.$message.error('起始日期不能大于结束日期')
        } else if (date1[1] > today) {
          this.$message.error('结束日期不能超过今天')
        } else {
          this.getData(datas)
        }
      } else {
        this.$message.error('请选择日期')
      }
    }
  }
}
</script>

<style scoped>
  #tableList {
  height: 100vh;
  width: 100%;
  }
  .titie {
    width: 100%;
    margin-top: 100px;
    display: flex;
    flex-direction: column;
    justify-content:flex-start;
    align-items: center;
  }
  .pocker {
    margin-bottom: 25px;
  }
  .tableList {
      margin-top: 50px;
  }
  .tableList-button {
    width:60%;
    display: flex;
    flex-direction: row;
    justify-content: space-between;
  }
  .tableList-button1 {
    width: 60%;
  }
  .table-button {
    background: #259B24;
    width: 45%;
    margin-bottom: 30px;
  }
  .table-button:hover {
    opacity: 0.7;
  }
</style>
