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
    },
    customerSummaryData () {
      console.log('导出客户汇总')
    },
    storesSummaryData () {
      console.log('门店汇总、异动商户')
    },
    storeBillRatioData () {
      console.log('门店流水占比')
    },
    storesBillData () {
      console.log('门店流水')
    },
    commodityCouponsData () {
      console.log('商户用劵')
    },
    securitiesSummaryData () {
      console.log('劵汇总')
    },
    storeRankingData () {
      console.log('门店排行')
    },
    commodityCouponsDetailsData () {
      console.log('商户用劵详情')
    },
    stocklistData () {
      console.log('劵排名')
    },
    pageviewData () {
      console.log('点击量')
    },
    gotoIndex () {
      let _this = this
      _this.$router.push({path: '/storesSummary'})
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
