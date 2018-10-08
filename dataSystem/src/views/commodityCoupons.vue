<template>
    <div id="commodityCoupons">
      <screenData v-on:fullConditions='loadData' :storeAttributes="attribute" :sogo="merchant" :shop="outlet"></screenData>
      <div class="box" v-loading="loading" element-loading-text="拼命加载中" element-loading-spinner="el-icon-loading" element-loading-background="rgba(250, 250, 250, 1)">
        <div class="box-flex" v-if="shopList.length!=0">
          <div v-for="(item, index) in shopList" :key="index">
            <div class="box-list box-birder">{{item._key}}</div>
            <div class="box-list" v-for="(items, indexs) in item._data" :key="indexs">{{items}}</div>
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
</template>
<script>
import screenData from '../components/screenData.vue'
import axios from 'axios'
export default {
  name: 'commodityCoupons',
  data () {
    return {
      name: 'commodityCoupons',
      merchant: false,
      outlet: false,
      attribute: false,
      dataList: [],
      shopList: [],
      dataPageList: [],
      tableList: false,
      page: 0,
      pageright: true,
      loading: true
    }
  },
  components: {
    'screenData': screenData
  },
  methods: {
    loadData (data) {
      this.loading = true
      this.page = 0
      console.log(data)
      this.shopList = []
      this.dataList = []
      this.dataPageList = []
      axios({method: 'post', url: this.$store.state.url + '/api/table_export', data: data})
        .then(response => {
          if (response.data) {
            this.loading = false
            this.$store.commit('increment', false)
            console.log('aaa' + this.$store.state.path)
          }
          console.log(response)
          console.log(response.data)
          response.data.splice(1, 5)
          this.shopList = response.data.splice(0, 1)
          console.log(this.shopList)
          this.dataList = response.data
          console.log(this.dataList)
          this.dataPageList = response.data.slice(this.page * 10, 10)
          console.log(this.dataPageList)
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
      if (this.dataPageList.length < 10 || (this.page + 1) * 10 > this.dataList.length) {
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
#commodityCoupons {
  padding: 15px;
  font-size: 14px;
}
.box {
  /* width: 90%; */
  /* margin: 15px; */
  /* min-width: 1000px; */
  min-height: 300px;
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
  word-wrap:break-word;
  display: flex;
  flex-direction: row;
  justify-content: center;
  align-items: center;
}
.box-list1 {
  word-wrap: break-word;
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
}
.box-left:hover {
  opacity: 0.7;
  background: #dddddd;
}
.box-right:hover {
  opacity: 0.7;
  background: #dddddd;
}
</style>
