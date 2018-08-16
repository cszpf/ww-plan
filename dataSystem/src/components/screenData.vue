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
        <el-form-item label="门店属性 :">
          <span :class="[storeAttributesindex===index?'admini':'','screen-span']" v-for="(item, index) in storeAttributes" :key="item.id" @click="storeAttributesData(item,index)">{{ item.name }}</span>
        </el-form-item>
        <el-form-item label="日期 :">
          <el-date-picker v-model="form.date" type="daterange" placeholder="选择日期" size="small" format="yyyy-MM-dd">
          </el-date-picker>
        </el-form-item>
      </el-form>
      </div>
      <el-form class="filtro">
        <el-form-item label="已选择筛选条件 :">
          <el-tag class="screen-tags" v-for="(tag, index) in tags" :key="tag.id" @close="handleClose(tag.type, index)" closable>{{ tag.name }}</el-tag>
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
    district: {
      type: Array,
      default: function () {
        return []
      }
    }
  },
  data () {
    return {
      form: {
        name: '',
        date: ''
      },
      adminiStrative: [
        // 行政区
        { name: '广州市番禺区', id: '1', type: 'adminiStrative' },
        { name: '广州市白云区', id: '2', type: 'adminiStrative' },
        { name: '广州市荔湾区', id: '3', type: 'adminiStrative' }
      ],
      microarea: [], // 微区域
      trade: [], // 行业
      salesManager: [], // 销售经理
      operationManager: [
        // 运营经理
        { name: '小意', id: '22', type: 'operationManager' },
        { name: '小松', id: '23', type: 'operationManager' }
      ],
      storeAttributes: [
        // 门店属性
        { name: '活跃门店', id: '23', type: 'storeAttributes' },
        { name: '沉默门店', id: '24', type: 'storeAttributes' }
      ],
      adminiIndex: '', // 行政区
      microareaindex: '', // 微区域
      tradeindex: '', // 行业
      salesManagerindex: '', // 销售经理
      operationManagerindex: '', // 运营经理
      storeAttributesindex: '', // 门店属性
      tags: []
    }
  },
  created () {},
  mounted () {
    this.loadData('MERCHANT_TYPE') // 行业
    this.loadData('SALE_NAME') // 销售经理
  },
  methods: {
    loadData (idnmae) {
      let _this = this
      console.log(idnmae)
      axios({method: 'post', url: 'http://localhost:5000/api/databind', data: {id: idnmae}})
        .then(function (response) {
          console.log(response.statusText)
          console.log(response.statusText === 'OK')
          if (response.statusText === 'OK') {
            console.log(response)
            if (idnmae === 'MERCHANT_TYPE') {
              _this.trade = response.data.MERCHANT_TYPE
            }
            if (idnmae === 'SALE_NAME') {
              _this.salesManager = response.data.SALE_NAME
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
      let operationManagerType = 'operationManager'
      console.log(this.tags)
      this.screening(operationManagerBl, this.tags, data, operationManagerType)
    },
    storeAttributesData (data, index) {
      // 门店属性
      this.storeAttributesindex = index
      let storeAttributesBl = false
      let storeAttributesType = 'storeAttributes'
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
      if (type === 'operationManager') {
        this.operationManagerindex = ''
      }
      if (type === 'storeAttributes') {
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
