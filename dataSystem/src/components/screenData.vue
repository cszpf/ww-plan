<template>
    <div id="screenData">
      <div class="screen">
      <el-form ref="form" :model="form" label-width="80px" class="screen">
        <el-form-item label="行政区 :">
          <span :class="[adminiIndex===index?'admini':'','screen-span']" v-for="(item, index) in district" :key="item.id" @click="adminiStrativeData(item, index)">{{ item.name }}</span>
          <el-button class="guidetable" type="success" size="small">导表</el-button>
        </el-form-item>
        <el-form-item label="微区域 :">
          <span :class="[microareaindex===index?'admini':'','screen-span']" v-for="(item, index) in microarea" :key="item.id" @click="microareaData(item,index)">{{ item.name }}</span>
          <!-- <span v-if="microarea.length==0" class="screen-span">暂无数据</span> -->
        </el-form-item>
        <el-form-item label="行业 :">
          <span :class="[tradeindex===index?'admini':'','screen-span']" v-for="(item, index) in trade" :key="item.id" @click="tradeData(item,index)">{{ item.name }}</span>
        </el-form-item>
        <el-form-item label="销售经理 :">
          <span :class="[salesManagerindex===index?'admini':'','screen-span']" v-for="(item, index) in salesManager" :key="item.id" @click="salesManagerData(item,index)">{{ item.name }}</span>
        </el-form-item>
        <el-form-item label="运营经理 :">
          <span :class="[operationManagerindex===index?'admini':'','screen-span']" v-for="(item, index) in operationManager" :key="item.id" @click="operationManagerData(item,index)">{{ item.name }}</span>
        </el-form-item>
        <el-form-item label="商户 :" v-if="sogo">
          <el-input class="sreem-input" v-model="form.name" size="mini" placeholder="输入商户"></el-input>
        </el-form-item>
        <el-form-item label="门店 :" v-if="shop">
          <el-input class="sreem-input" v-model="form.name" size="mini" placeholder="输入门店"></el-input>
        </el-form-item>
        <el-form-item label="门店属性 :" v-if="storeAttributes">
          <span :class="[storeAttributesindex===index?'admini':'','screen-span']" v-for="(item, index) in storeAttributesList" :key="item.id" @click="storeAttributesData(item,index)">{{ item.name }}</span>
        </el-form-item>
        <el-form-item label="日期 :">
          <el-date-picker v-model="date" type="daterange" placeholder="选择日期" size="small" format="yyyy-MM-dd">
          </el-date-picker>
        </el-form-item>
      </el-form>
      </div>
      <el-form class="filtro">
        <el-form-item label="已选择筛选条件 :">
          <el-tag class="screen-tags" v-for="(tag, index) in tags" :key="tag.id" @close="handleClose(tag.type, index)" closable>{{ tag.name }}</el-tag><span class="tag-span">共有0个结果</span>
        </el-form-item>
      </el-form>
    </div>
</template>

<script>
import axios from 'axios'
export default {
  props: {
    sogo: {
      type: Boolean,
      default: true
    },
    shop: {
      type: Boolean,
      default: true
    },
    storeAttributes: {
      type: Boolean,
      default: true
    },    
  },
  data () {
    return {
      date: '',
      form: {
        name: '',
        date: ''
      },
      district: [], // 行政区
      microarea: [], // 微区域
      trade: [], // 行业
      salesManager: [], // 销售经理
      operationManager: [], // 运营经理
      storeAttributesList: [
        { id: 'active’', name: '活跃门店', type: 'SUBBRANCH_PROP' },
        { id: 'silent’', name: '沉默门店', type: 'SUBBRANCH_PROP' }
      ], // 门店属性
      adminiIndex: '', // 行政区
      microareaindex: '', // 微区域
      tradeindex: '', // 行业
      salesManagerindex: '', // 销售经理
      operationManagerindex: '', // 运营经理
      storeAttributesindex: '', // 门店属性
      tags: [],
      postData: {
        id: 'mdhz',
        opt: {
          'ADMIN_REGION_CODE': '', // 行政区
          'MICRO_REGION_CODE': '', // 微区域
          'SALE_NAME': '', // 销售经理
          'MERCHANT_TYPE': '', // 行业
          'OPERATOR_NAME': '' // 运营经理
        },
        date: ['2017-08-30', '2018-08-17']
      }
    }
  },
  created () {},
  mounted () {
    this.loadData('ADMIN_REGION_CODE') // 行政区
    this.loadData('MERCHANT_TYPE') // 行业
    this.loadData('SALE_NAME') // 销售经理
    this.loadData('OPERATOR_NAME') // 运营经理
    if (this.sogo) {
      this.loadData('MERCHANT_ID') // 商户
    }
    // this.getData()
  },
  methods: {
    getData () {
      // let _this = this
      axios({method: 'post', url: 'http://localhost:5000/api/table_export', data: this.postData})
        .then(function (response) {
          console.log(response)
        })
        .catch(function (error) {
          console.log(error)
        })
    },
    loadData (idnmae) { // 筛选条件
      let _this = this
      console.log(idnmae)
      axios({method: 'post', url: 'http://localhost:5000/api/databind', data: {id: idnmae}})
        .then(function (response) {
          console.log(response.statusText)
          console.log(response.statusText === 'OK')
          if (response.statusText === 'OK') {
            console.log(response)
            if (idnmae === 'ADMIN_REGION_CODE') {
              _this.district = response.data.ADMIN_REGION_CODE ? response.data.ADMIN_REGION_CODE : ''
            }
            if (idnmae === 'MERCHANT_TYPE') {
              _this.trade = response.data.MERCHANT_TYPE
            }
            if (idnmae === 'SALE_NAME') {
              _this.salesManager = response.data.SALE_NAME
            }
            if (idnmae === 'OPERATOR_NAME') {
              _this.operationManager = response.data.OPERATOR_NAME
            }
            if (idnmae === 'SUBBRANCH_PROP') {
              _this.storeAttributes = response.data.SUBBRANCH_PROP
            }
          } else {
            _this.$message.error('占无数据')
          }
        })
        .catch(function (error) {
          console.log(error)
        })
    },
    adminiStrativeData (data, index) {
      // 选择行政区
      let _this = this
      this.adminiIndex = index
      let adminiStrativeBl = false
      let adminiStrativeType = 'ADMIN_REGION_CODE'
      this.screening(adminiStrativeBl, this.tags, data, adminiStrativeType)
      _this.tags.forEach((item, index) => {
        if (item.type === 'MICRO_REGION_CODE') {
          _this.tags.splice(index, 1)
          _this.microareaindex = ''
        }
      })
      console.log(data)
      if (data) {
        _this.microarea = []
        axios({method: 'post', url: 'http://localhost:5000/api/databind', data: {'id': 'MICRO_REGION_CODE', 'opt': {'ADMIN_REGION_CODE': data.id}}})
          .then(function (response) {
            if (response.statusText === 'OK') {
              console.log(response)
              _this.microarea = response.data.MICRO_REGION_CODE
              console.log(_this.microarea)
            } else {
              _this.$message.error('占无数据')
            }
          })
          .catch(function (error) {
            console.log(error)
          })
      }
    },
    microareaData (data, index) {
      // 微区域
      this.microareaindex = index
      let microareaBl = false
      let microareaType = 'MICRO_REGION_CODE'
      console.log(this.tags)
      this.screening(microareaBl, this.tags, data, microareaType)
    },
    tradeData (data, index) {
      // 行业
      this.tradeindex = index
      let tradeBl = false
      let tradeType = 'MERCHANT_TYPE'
      console.log(this.tags)
      this.screening(tradeBl, this.tags, data, tradeType)
    },
    salesManagerData (data, index) {
      // 销售经理
      this.salesManagerindex = index
      let salesManagerBl = false
      let salesManagerType = 'SALE_NAME'
      console.log(this.tags)
      this.screening(salesManagerBl, this.tags, data, salesManagerType)
    },
    operationManagerData (data, index) {
      // 运营经理
      this.operationManagerindex = index
      let operationManagerBl = false
      let operationManagerType = 'OPERATOR_NAME'
      console.log(this.tags)
      this.screening(operationManagerBl, this.tags, data, operationManagerType)
    },
    storeAttributesData (data, index) {
      // 门店属性
      this.storeAttributesindex = index
      let storeAttributesBl = false
      let storeAttributesType = 'SUBBRANCH_PROP'
      console.log(this.tags)
      this.screening(storeAttributesBl, this.tags, data, storeAttributesType)
    },
    screening (judge, tags, data, type) { // 判断值 筛选条件 数据 类型
      if (this.tags.length === 0) {
        this.tags.push(data)
      } else {
        this.tags.forEach((item, index) => {
          if (item.type === type) {
            judge = true
            this.tags.splice(index, 1, data)
            console.log(judge)
          }
        })
        if (!judge) { this.tags.push(data) }
      }
    },
    handleClose (type, index) {
      this.tags.splice(index, 1)
      if (type === 'ADMIN_REGION_CODE') {
        this.adminiIndex = ''
        this.tags.forEach((item, index) => {
          if (item.type === 'MICRO_REGION_CODE') {
            this.tags.splice(index, 1)
            this.microareaindex = ''
            this.microarea = []
          }
        })
      }
      if (type === 'MICRO_REGION_CODE') {
        this.microareaindex = ''
      }
      if (type === 'MERCHANT_TYPE') {
        this.tradeindex = ''
      }
      if (type === 'SALE_NAME') {
        this.salesManagerindex = ''
      }
      if (type === 'OPERATOR_NAME') {
        this.operationManagerindex = ''
      }
      if (type === 'SUBBRANCH_PROP') {
        this.storeAttributesindex = ''
      }
    }
  }
}
</script>
<style scoped>
/* #screenData {
  margin: 20px;
} */
/* .screen-table {
  margin-left: 20px;
} */
.guidetable {
  float: right;
  margin-right: 25px;
}
 /* ddfdf */
.screen-tags {
  margin: 5px;
}
.admini {
  color: #f9980f;
}
.sreem-input {
  width: 320px;
}
.screen-span {
  margin: 5px;
  cursor: pointer;
}
.screen-span:hover {
  color: #f9980f;
}
.filtro {
  margin: 15px 0;
}
.tag-span {
  float: right;
  margin-right: 10px;
}
</style>
<style>
#screenData .el-form-item {
  margin: 3px 0px;
}
#screenData .screen .el-form-item__label {
  color: #BBBBBB;
}
#screenData .el-tag {
  color: #f9980f;
  border: 1px solid #dddddd;
  background: #ffffff;
}
#screenData .el-tag .el-icon-close {
  color: #f9980f;
}
#screenData .el-tag .el-icon-close::before:hover {
  color: #f9980f;
  background: #ffffff;
}
#screenData .el-button--success {
    background: #259B24;
    background-color: #259B24;
}
#screenData .el-tag .el-icon-close:hover{
    background: #ff9800;
    color: #fff;
}
</style>
