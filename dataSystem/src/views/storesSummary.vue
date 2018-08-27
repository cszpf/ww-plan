<template>
  <div id="storesSummary">
    <screenData v-on:fullConditions='loadData' :storeAttributes="attribute" :sogo="merchant" :shop="outlet"></screenData>
      <div class="overflow-height" v-loading="loading" element-loading-text="拼命加载中" element-loading-spinner="el-icon-loading" element-loading-background="rgba(250, 250, 250, 1)">
        <div class="box" v-if="dataPageList.length!=0">
          <div class="box-flex">
            <div class="box-list box-birder">指标</div>
            <div class="box-list">新增门店数</div>
            <div class="box-list">累计门店数</div>
            <div class="box-list">累计评估收入</div>
            <div class="box-list">累计运营流水</div>
            <div class="box-list">累计流水占比</div>
            <div class="box-list">户均评估收入</div>
            <div class="box-list">户均运营收入</div>
            <div class="box-list">户均流水占比</div>
            <div class="box-list">
              <a class="box-font" v-bind:href="url" target="_blank">活跃门店数量</a>
            </div>
            <div class="box-list">活跃门店占比</div>
            <div class="box-list  box-font">
              <a class="box-font" v-bind:href="url1" target="_blank">沉默门店数量</a>
            </div>
            <div class="box-list  box-font">
              <a class="box-font" v-bind:href="url2" target="_blank">异动商户数量</a>
            </div>
            <div class="box-list  box-font">
              <a class="box-font" v-bind:href="url3" target="_blank">流失商户数量</a>
            </div>
          </div>
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
</template>

<script>
import screenData from '../components/screenData.vue'
import axios from 'axios'
export default {
  data () {
    return {
      number: 0,
      url: '#/activeStores',
      url1: '#/silenceStores',
      url2: '#/businessesLost',
      url3: '#/lossMerchants',
      dataName: [
        { name: '新增门店数' },
        { name: '累计门店数' },
        { name: '累计评估收入' },
        { name: '累计运营流水' },
        { name: '累计流水占比' },
        { name: '户均评估收入' },
        { name: '户均运营收入' },
        { name: '户均流水占比' },
        { name: '活跃门店数量' },
        { name: '活跃门店占比' },
        { name: '沉默门店数量' },
        { name: '异动商户数量' },
        { name: '流失商户数量' }
      ],
      dataDate: [
        {date: '20180825', amount: [{ a: '1527' }, { a: '1528' }, { a: '1529' }, { a: '1530' }, { a: '1531' }, { a: '1532' }, { a: '1533' }, { a: '1534' }, { a: '15235' }, { a: '1536' }, { a: '1537' }, { a: '1538' }, { a: '1234' }]},
        {date: '20180827', amount: [{ a: '1527' }, { a: '1528' }, { a: '1529' }, { a: '1530' }, { a: '1531' }, { a: '1532' }, { a: '1533' }, { a: '1534' }, { a: '15235' }, { a: '1536' }, { a: '1537' }, { a: '1538' }, { a: '1234' }]},
        {date: '20180813', amount: [{ a: '1527' }, { a: '1528' }, { a: '1529' }, { a: '1530' }, { a: '1531' }, { a: '1532' }, { a: '1533' }, { a: '1534' }, { a: '15235' }, { a: '1536' }, { a: '1537' }, { a: '1538' }, { a: '1234' }]},
        {date: '20180843', amount: [{ a: '1527' }, { a: '1528' }, { a: '1529' }, { a: '1530' }, { a: '1531' }, { a: '1532' }, { a: '1533' }, { a: '1534' }, { a: '15235' }, { a: '1536' }, { a: '1537' }, { a: '1538' }, { a: '1234' }]},
        {date: '20180863', amount: [{ a: '1527' }, { a: '1528' }, { a: '1529' }, { a: '1530' }, { a: '1531' }, { a: '1532' }, { a: '1533' }, { a: '1534' }, { a: '15235' }, { a: '1536' }, { a: '1537' }, { a: '1538' }, { a: '1234' }]},
        {date: '20180823', amount: [{ a: '1527' }, { a: '1528' }, { a: '1529' }, { a: '1530' }, { a: '1531' }, { a: '1532' }, { a: '1533' }, { a: '1534' }, { a: '15235' }, { a: '1536' }, { a: '1537' }, { a: '1538' }, { a: '1234' }]},
        {date: '20180868', amount: [{ a: '1527' }, { a: '1528' }, { a: '1529' }, { a: '1530' }, { a: '1531' }, { a: '1532' }, { a: '1533' }, { a: '1534' }, { a: '15235' }, { a: '1536' }, { a: '1537' }, { a: '1538' }, { a: '1234' }]},
        {date: '20180878', amount: [{ a: '1527' }, { a: '1528' }, { a: '1529' }, { a: '1530' }, { a: '1531' }, { a: '1532' }, { a: '1533' }, { a: '1534' }, { a: '15235' }, { a: '1536' }, { a: '1537' }, { a: '1538' }, { a: '1234' }]},
        {date: '20180809', amount: [{ a: '1527' }, { a: '1528' }, { a: '1529' }, { a: '1530' }, { a: '1531' }, { a: '1532' }, { a: '1533' }, { a: '1534' }, { a: '15235' }, { a: '1536' }, { a: '1537' }, { a: '1538' }, { a: '1234' }]},
        {date: '20180872', amount: [{ a: '1527' }, { a: '1528' }, { a: '1529' }, { a: '1530' }, { a: '1531' }, { a: '1532' }, { a: '1533' }, { a: '1534' }, { a: '15235' }, { a: '1536' }, { a: '1537' }, { a: '1538' }, { a: '1234' }]}
      ],
      merchant: false,
      outlet: false,
      attribute: false,
      pageNumber: 1,
      pageSize: 20,
      total: 0,
      adminiStrative: [],
      dataList: [],
      shopList: [],
      dataPageList: [],
      tableList: false,
      page: 0,
      pageright: true,
      loading: true
    }
  },
  created () {},
  mounted () {},
  components: {
    'screenData': screenData
  },
  methods: {
    loadData (data) {
      console.log(data)
      axios({method: 'post', url: 'http://localhost:5000/api/table_export', data: data})
        .then(response => {
          if (response.data) {
            this.loading = false
            this.$store.commit('increment', false)
          }
          console.log(response)
          console.log(response.data)
          this.dataList = response.data
          console.log(this.dataList)
          if (this.dataList.length <= 10) {
            this.pageright = false
            this.dataPageList = response.data
          } else {
            this.dataPageList = response.data.slice(this.page * 10, 10)
            this.pageright = true
            console.log(this.dataPageList)
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
#storesSummary {
  font-size: 12px;
}
.box-font {
  color: #FF9800;
  cursor: pointer;
  text-decoration: underline;
}
.overflow-height {
  min-height: 300px;
}
.box {
  /* width: 90%; */
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
  width: 9%;
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
#storesSummary {
  margin: 15px 20px;
}
.stores-table {
  width: 100%;
}
.stores-pagination {
  float: right;
  margin: 10px 0;
}
</style>
