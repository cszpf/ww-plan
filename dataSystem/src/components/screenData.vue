<template>
    <div id="screenData">
      <div class="screen">
      <el-form ref="form" :model="form" label-width="80px" class="screen">
        <el-form-item label="行政区 :">
          <span :class="[adminiIndex===index?'admini':'','screen-span']" v-for="(item, index) in adminiStrative" :key="item.id" @click="adminiStrativeData(item, index)">{{ item.name }}</span>
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
export default {
  props: {
    sogo: {
      type: Boolean,
      default: true
    },
    shop: {
      type: Boolean,
      default: true
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
      microarea: [
        // 微区域
        { name: '市桥商圈', id: '4', type: 'microarea' },
        { name: '大石商圈', id: '5', type: 'microarea' },
        { name: '万博商圈', id: '6', type: 'microarea' }
      ],
      trade: [
        // 行业
        { name: '加油', id: '6', type: 'trade' },
        { name: '娱乐', id: '7', type: 'trade' },
        { name: '美容', id: '9', type: 'trade' },
        { name: '健身', id: '10', type: 'trade' },
        { name: '汽车', id: '11', type: 'trade' },
        { name: '保健', id: '12', type: 'trade' },
        { name: '宠物', id: '13', type: 'trade' },
        { name: '正餐', id: '14', type: 'trade' },
        { name: '快餐', id: '15', type: 'trade' },
        { name: '茶饮', id: '16', type: 'trade' },
        { name: '甜品', id: '17', type: 'trade' },
        { name: 'ktv', id: '18', type: 'trade' },
        { name: '其他', id: '19', type: 'trade' }
      ],
      salesManager: [
        // 销售经理
        { name: '小超', id: '20', type: 'trasalesManagerde' },
        { name: '小熊', id: '21', type: 'trasalesManagerde' }
      ],
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
  methods: {
    adminiStrativeData (data, index) {
      // 选择行政区
      this.adminiIndex = index
      let adminiStrativeBl = false
      let adminiStrativeType = 'adminiStrative'
      this.screening(adminiStrativeBl, this.tags, data, adminiStrativeType)
    //   if (this.tags.length === 0) {
    //     this.tags.push(data)
    //   } else {
    //     this.tags.forEach((item, index) => {
    //       if (item.type === 'adminiStrative') {
    //         adminiStrativeBl = true
    //         this.tags.splice(index, 1, data)
    //       }
    //     })
    //     if (!adminiStrativeBl) { this.tags.push(data) }
    //   }
    },
    microareaData (data, index) {
      // 微区域
      this.microareaindex = index
      let microareaBl = false
      let microareaType = 'microarea'
      console.log(this.tags)
      this.screening(microareaBl, this.tags, data, microareaType)
    //   if (this.tags.length === 0) {
    //     this.tags.push(data)
    //   } else {
    //     this.tags.forEach((item, index) => {
    //       if (item.type === 'microarea') {
    //         microareaBl = true
    //         this.tags.splice(index, 1, data)
    //         console.log(microareaBl)
    //       }
    //     })
    //     if (!microareaBl) { this.tags.push(data) }
    //   }
    },
    tradeData (data, index) {
      // 行业
      this.tradeindex = index
      let tradeBl = false
      let tradeType = 'trade'
      console.log(this.tags)
      this.screening(tradeBl, this.tags, data, tradeType)
    },
    salesManagerData (data, index) {
      // 销售经理
      this.salesManagerindex = index
      let salesManagerBl = false
      let salesManagerType = 'trasalesManagerde'
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
      if (type === 'adminiStrative') {
        this.adminiIndex = ''
      }
      if (type === 'microarea') {
        this.microareaindex = ''
      }
      if (type === 'trade') {
        this.tradeindex = ''
      }
      if (type === 'trasalesManagerde') {
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
