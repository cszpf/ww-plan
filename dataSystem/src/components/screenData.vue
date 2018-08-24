<template>
    <div id="screenData">
      <div class="screen">
      <el-form ref="form" :model="form" label-width="80px" class="screen">
        <el-form-item label="行政区 :">
          <span :class="[adminiIndex===index?'admini':'','screen-span']" v-for="(item, index) in district" :key="item.id" @click="adminiStrativeData(item, index)">{{ item.name }}</span>
          <el-button class="guidetable" type="success" size="small" @click="gotoData">导表</el-button>
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
          <el-input class="sreem-input" v-model="contact" size="mini" placeholder="输入商户" @blur="loadContact"></el-input>
          <div><span :class="[contactListindex===index?'admini':'','screen-span']" v-for="(item, index) in contactList" :key="item.id" @click="contactListData(item,index)">{{item.name}}</span></div>
        </el-form-item>
        <el-form-item label="门店 :" v-if="shop">
          <span :class="[shopnameListindex===index?'admini':'','screen-span']" v-for="(item, index) in shopnameList" :key="item.id" @click="shopnameData(item,index)">{{item.name}}</span>
        </el-form-item>
        <el-form-item label="门店属性 :" v-if="storeAttributes">
          <span :class="[storeAttributesindex===index?'admini':'','screen-span']" v-for="(item, index) in storeAttributesList" :key="item.id" @click="storeAttributesData(item,index)">{{ item.name }}</span>
        </el-form-item>
        <el-form-item label="日期 :">
          <el-date-picker :clearable="clearablebl" :picker-options="pickerOptions0" v-model="date" type="daterange" placeholder="选择日期" size="small" value-format="yyyy-MM-dd" format="yyyy-MM-dd" @change="dateData">
          </el-date-picker>
        </el-form-item>
      </el-form>
      </div>
      <el-form class="filtro">
        <el-form-item label="已选择筛选条件 :">
          <el-tag class="screen-tags" v-for="(tag, index) in tags" :key="tag.id" @close="handleClose(tag.type, index)" closable>{{ tag.name }}</el-tag>
          <!-- <span class="tag-span">共有0个结果</span> -->
          <el-button :class="[nodisabled?'disabled':'','guidetable']"  type="success" size="small" @click="demand" :disabled="nodisabled">查询</el-button>
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
    }
  },
  data () {
    return {
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
      date: [],
      form: {
        name: '',
        date: ''
      },
      contact: '', // 商户名称
      contactList: [], // 商户列表
      contactListindex: '',
      shopname: '', // 门店名称
      shopnameList: [], // 门店列表
      shopnameListindex: '',
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
        ids: sessionStorage.getItem('id'),
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
      clearablebl: false,
      timeFrame: ''
    }
  },
  computed: {
    nodisabled () {
      return this.$store.state.path
    }
  },
  created () {
    let today = new Date()
    let lastMonth = new Date(today.getTime() - 3600 * 1000 * 24 * 30)
    this.date.push(this.formatDate(lastMonth), this.formatDate(today))
    this.postData.date = this.date
  },
  mounted () {
    this.loadData('ADMIN_REGION_CODE') // 行政区
    this.loadData('MERCHANT_TYPE') // 行业
    this.loadData('SALE_NAME') // 销售经理
    this.loadData('OPERATOR_NAME') // 运营经理
    this.$emit('fullConditions', this.postData)
    // this.getData()
  },
  methods: {
    demand () {
      this.$store.commit('increment', true)
      this.$emit('fullConditions', this.postData)
    },
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
      axios({method: 'post', url: 'http://localhost:5000/api/export', data: this.postData, responseType: 'blob'})
        .then(response => {
          this._download(response, this.postData['ids'])
        })
        .catch(function (error) {
          console.log(error)
        })
    },
    formatDate  (date) { // 日期格式化
      let y = date.getFullYear()
      let m = date.getMonth() + 1
      m = m < 10 ? '0' + m : m
      let d = date.getDate()
      d = d < 10 ? ('0' + d) : d
      return y + '-' + m + '-' + d
    },
    dateData () {
      this.postData.date = this.date
    },
    loadContact () {
      let _this = this
      axios({method: 'post', url: 'http://localhost:5000/api/databind', data: {'id': 'MERCHANT_ID', 'opt': {'MERCHANT_NAME': this.contact}}})
        .then(function (response) {
          _this.contactList = response.data.MERCHANT_ID
        })
        .catch(function (error) {
          console.log(error)
        })
    },
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
      axios({method: 'post', url: 'http://localhost:5000/api/databind', data: {id: idnmae}})
        .then(function (response) {
          if (response.statusText === 'OK') {
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
      if (data) {
        _this.microarea = []
        axios({method: 'post', url: 'http://localhost:5000/api/databind', data: {'id': 'MICRO_REGION_CODE', 'opt': {'ADMIN_REGION_CODE': data.id}}})
          .then(function (response) {
            if (response.statusText === 'OK') {
              _this.microarea = response.data.MICRO_REGION_CODE
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
      this.screening(microareaBl, this.tags, data, microareaType)
      this.postData.opt.MICRO_REGION_CODE = data.id
    },
    tradeData (data, index) {
      // 行业
      this.tradeindex = index
      let tradeBl = false
      let tradeType = 'MERCHANT_TYPE'
      this.screening(tradeBl, this.tags, data, tradeType)
      this.postData.opt.MERCHANT_TYPE = data.id
    },
    salesManagerData (data, index) {
      // 销售经理
      this.salesManagerindex = index
      let salesManagerBl = false
      let salesManagerType = 'SALE_NAME'
      this.screening(salesManagerBl, this.tags, data, salesManagerType)
      this.postData.opt.SALE_NAME = data.id
    },
    operationManagerData (data, index) {
      // 运营经理
      this.operationManagerindex = index
      let operationManagerBl = false
      let operationManagerType = 'OPERATOR_NAME'
      this.screening(operationManagerBl, this.tags, data, operationManagerType)
      this.postData.opt.OPERATOR_NAME = data.id
    },
    storeAttributesData (data, index) {
      // 门店属性
      this.storeAttributesindex = index
      let storeAttributesBl = false
      let storeAttributesType = 'SUBBRANCH_PROP'
      this.screening(storeAttributesBl, this.tags, data, storeAttributesType)
      this.postData.opt.SUBBRANCH_PROP = data.id
    },
    contactListData (data, index) {
      // 商户
      this.contactListindex = index
      let contactListBl = false
      let contactLisType = 'MERCHANT_ID'
      let _this = this
      this.screening(contactListBl, this.tags, data, contactLisType)
      this.postData.opt.MERCHANT_ID = data.id
      axios({method: 'post', url: 'http://localhost:5000/api/databind', data: {'id': ' SUBBRANCH_ID', 'opt': {'MERCHANT_ID': data.id}}})
        .then(function (response) {
          _this.shopnameList = response.data.SUBBRANCH_ID
        })
        .catch(function (error) {
          console.log(error)
        })
    },
    screening (judge, tags, data, type) { // 判断值 筛选条件 数据 类型
      if (this.tags.length === 0) {
        this.tags.push(data)
      } else {
        this.tags.forEach((item, index) => {
          if (item.type === type) {
            judge = true
            this.tags.splice(index, 1, data)
          }
        })
        if (!judge) { this.tags.push(data) }
      }
    },
    shopnameData (data, index) {
      // 门店
      this.shopnameListindex = index
      let shopnameListBl = false
      let shopnameListType = 'SUBBRANCH_ID'
      this.screening(shopnameListBl, this.tags, data, shopnameListType)
      this.postData.opt.SUBBRANCH_ID = data.id
    },
    handleClose (type, index) {
      this.tags.splice(index, 1)
      if (type === 'ADMIN_REGION_CODE') {
        this.adminiIndex = ''
        this.loadData.ADMIN_REGION_CODE = ''
        this.tags.forEach((item, index) => {
          if (item.type === 'MICRO_REGION_CODE') {
            this.tags.splice(index, 1)
            this.microareaindex = ''
            this.loadData.MICRO_REGION_CODE = ''
            this.microarea = []
          }
        })
      }
      if (type === 'MICRO_REGION_CODE') {
        this.microareaindex = ''
        this.loadData.MICRO_REGION_CODE = ''
      }
      if (type === 'MERCHANT_TYPE') {
        this.tradeindex = ''
        this.loadData.MERCHANT_TYPE = ''
      }
      if (type === 'SALE_NAME') {
        this.salesManagerindex = ''
        this.loadData.ALE_NAME = ''
      }
      if (type === 'OPERATOR_NAME') {
        this.operationManagerindex = ''
        this.loadData.OPERATOR_NAME = ''
      }
      if (type === 'SUBBRANCH_PROP') {
        this.storeAttributesindex = ''
        this.loadData.SUBBRANCH_PROP = ''
      }
      if (type === 'MERCHANT_ID') {
        this.contactListindex = ''
        this.loadData.MERCHANT_ID = ''
        this.tags.forEach((item, index) => {
          if (item.type === 'SUBBRANCH_ID') {
            this.tags.splice(index, 1)
            this.shopnameListindex = ''
            this.loadData.SUBBRANCH_ID = ''
            this.shopnameList = []
          }
        })
      }
      if (type === 'SUBBRANCH_ID') {
        this.shopnameListindex = ''
        this.loadData.SUBBRANCH_ID = ''
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
.disabled {
  opacity: 0.7;
}
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
.contactListSpan {
  margin-right: 15px;
}
.contactListSpan:hover {
  color: #f9980f;
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
