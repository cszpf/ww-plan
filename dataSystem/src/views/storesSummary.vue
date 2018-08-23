<template>
  <div id="storesSummary">
    <screenData :storeAttributes="attribute" :sogo="merchant" :shop="outlet"></screenData>
    <div class="stores-table">
      <div class="box">
        <div class="box-a">
          <div :class="[number == index?'box-title1':'','box-title']" v-for="(item, index) in dataName" :key="item.name">{{item.name}}</div>
        </div>
        <div class="box-b">
          <div class="box-arrows">
            <i class="el-icon-caret-left box-caret"></i>
          </div>
          <!-- <div> -->
            <div class="box-arrows1" v-for="item in dataDate" :key="item.date">
              <div class="box-amount box-amount1">{{item.date}}</div>
              <div class="box-amount" v-for="items in item.amount" :key="items.a">{{items.a}}</div>
            </div>
          <!-- </div> -->
          <div class="box-arrows">
            <i class="el-icon-caret-right box-caret"></i>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import screenData from '../components/screenData.vue'
export default {
  data () {
    return {
      number: 0,
      dataName: [
        { name: '指标' },
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
      adminiStrative: []
    }
  },
  created () {},
  mounted () {},
  components: {
    'screenData': screenData
  },
  methods: {}
}
</script>

<style scoped>
#storesSummary {
  font-size: 12px;
}
.box {
  width: 100%;
  height: 560px;
  /* border: 1px solid #000000; */
  display: flex;
  flex-direction: row;
  font-size: 14px;
}
.box-a {
  width: 10%;
  min-width: 100px;
  height: 100%;
  border-right: 1px solid #dddddd;
}
.box-title1 {
  border-bottom: 1px solid #dddddd;
}
.box-b {
  width: 90%;
  height: 100%;
  display: flex;
  flex-direction: row;
  justify-content: flex-start;
  border-right: 1px solid #dddddd;
}
.box-title {
  height: 40px;
  text-align: center;
  line-height: 40px;
}
.box-arrows {
  width: 5%;
  height: 100%;
  text-align: center;
}
.box-arrows1 {
  width: 9%
}
.box-caret {
  width: 100%;
  cursor: pointer;
  height: 40px;
  line-height: 40px;
  border-bottom: 1px solid #dddddd;
}
.box-caret:hover {
  opacity: 0.7;
  background: #dddddd;
}
.box-amount {
  /* min-width: 120px; */
  line-height: 40px;
  height: 40px;
  text-align: center;
  vertical-align: middle;
}
.box-amount1 {
  border-bottom: 1px solid #dddddd
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
