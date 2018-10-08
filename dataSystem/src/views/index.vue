<template>
    <div id="index">
      <div class="tite-flex">
       <el-row>
           <el-col class="navTop" :span="24">
               <p class="title-content">运营统计系统</p>
               <div class="offDiv">
                 <span class="titie-span">您好,{{username}}</span>
                 <el-button size="small" type="warning"  @click="passwd" class="operating">修改密码</el-button>
                 <el-button size="small" type="warning" class="operating" @click="logOff">退出登录</el-button>
               </div>
           </el-col>
       </el-row>
       <el-row>
         <el-col>
           <div class="box">
             <el-menu router :default-active="this.$route.path" active-text-color="#FF9800"  mode="horizontal" @select="handleSelect">
               <el-menu-item v-for="item in menu" :index="item.url" :key="item.parentMenuId">{{item.name}}</el-menu-item>
             </el-menu>
           </div>
         </el-col>
       </el-row>
      </div>
      <el-card class="contentView"  v-loading="loading"    element-loading-text="拼命加载中" element-loading-spinner="el-icon-loading" element-loading-background="rgba(250, 250, 250, 1)">
        <router-view></router-view>
      </el-card>
    </div>
</template>

<script>
export default {
  name: 'index',
  data () {
    return {
      activeIndex: '/storesSummary',
      menu: [
        {
          name: '门店汇总',
          url: '/storesSummary',
          parentMenuId: '1'
        },
        {
          name: '劵汇总',
          url: '/securitiesSummary',
          parentMenuId: '2'
        },
        {
          name: '客户汇总',
          url: '/customerSummary',
          parentMenuId: '3'
        },
        {
          name: '商户用劵',
          url: '/commodityCoupons',
          parentMenuId: '4'
        },
        {
          name: '商户劵详情',
          url: '/commodityCouponsDetails',
          parentMenuId: '5'
        },
        {
          name: '门店流水',
          url: '/storesBill',
          parentMenuId: '6'
        },
        {
          name: '门店流水占比',
          url: '/storeBillRatio',
          parentMenuId: '7'
        },
        {
          name: '门店排名',
          url: '/storeRanking',
          parentMenuId: '8'
        },
        {
          name: '劵排名',
          url: '/topCoupons',
          parentMenuId: '9'
        },
        {
          name: '点击量',
          url: '/pageView',
          parentMenuId: '10'
        }
      ],
      username: '',
      loading: true
    }
  },
  created () {
    this.username = sessionStorage.getItem('username')
    this.loadingTime()
  },
  methods: {
    loadingTime () {
      setTimeout(() => {
        this.loading = false
      }, 1500)
    },
    handleSelect (key, keyPath) {
      console.log(key, keyPath)
      if (key === '/storesSummary') { // 门店汇总
        sessionStorage.setItem('id', 'mdhz')
        this.$store.commit('increment', true)
        // this.loading = true
        // this.loadingTime()
      }
      if (key === '/securitiesSummary') { // 券汇总
        sessionStorage.setItem('id', 'qhz')
        this.$store.commit('increment', true)
        // this.loading = true
        // this.loadingTime()
      }
      if (key === '/customerSummary') { // 客户汇总
        sessionStorage.setItem('id', 'khhz')
        this.$store.commit('increment', true)
        // this.loading = true
        // this.loadingTime()
      }
      if (key === '/commodityCoupons') { // 商户用券
        sessionStorage.setItem('id', 'shyq')
        this.$store.commit('increment', true)
        // this.loading = true
        // this.loadingTime()
      }
      if (key === '/commodityCouponsDetails') { // 商户券详情
        sessionStorage.setItem('id', 'shqxq')
        this.$store.commit('increment', true)
        // this.loading = true
        // this.loadingTime()
      }
      if (key === '/storesBill') { // 门店流水
        sessionStorage.setItem('id', 'mdls')
        this.$store.commit('increment', true)
        // this.loading = true
        // this.loadingTime()
      }
      if (key === '/storeBillRatio') { // 门店流水占比
        sessionStorage.setItem('id', 'mdlszb')
        this.$store.commit('increment', true)
        // this.loading = true
        // this.loadingTime()
      }
      if (key === '/storeRanking') { // 门店排名
        sessionStorage.setItem('id', 'mdpm')
        this.$store.commit('increment', true)
        // this.loading = true
        // this.loadingTime()
      }
      if (key === '/topCoupons') { // 券排名
        sessionStorage.setItem('id', 'qpm')
        this.$store.commit('increment', true)
        // this.loading = true
        // this.loadingTime()
      }
      if (key === '/pageView') { // 点击量
        sessionStorage.setItem('id', 'djl')
        this.$store.commit('increment', true)
        // this.loading = true
        // this.loadingTime()
      }
    },
    passwd () {
      this.$router.push({path: '/passwd'})
    },
    logOff () {
      this.$confirm('此操作将退出登录, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        this.$message({
          type: 'success',
          message: '操作成功!'
        })
        sessionStorage.removeItem('username')
        sessionStorage.removeItem('id')
        this.$store.commit('increment', true)
        this.$router.push({path: '/login'})
      }).catch(() => {})
    }
  }
}
</script>

<style scoped>
.title-flex {
  position: fixed;
}
/* 顶部装饰条 */
.navTop {
  height: 60px;
  background: #ff9800;
}
.title-content {
  float: left;
  color: #fff;
  height: 60px;
  line-height: 60px;
  margin: 0;
  margin-left: 20px;
  font-size: 18px;
}
.offDiv {
  float: right;
  margin-right: 10px;
  height: 60px;
  line-height: 60px;
  color: #ffffff;
}
.titie-span {
  margin: 0 15px 0 0;
  text-align: center;
  font-size: 14px;
}
.operating {
  cursor: pointer;
  background: #ed780c !important;
  box-shadow: 2px 2px 2px #ed780c;
  border: #ed780c;
}
.operating:hover {
  opacity: 0.7 !important;
}
.box {
  margin: 0 10px;
}
/* 内容 */
.contentView {
  position: absolute;
  padding-bottom: 20px;
  overflow: auto;
  bottom: 30px;
  top: 121px;
  left: 0;
  right: 0;
  box-shadow: none !important;
  border: none !important;
}
</style>
<style>
#index .el-card__body {
  padding: 10px 5px;
}
/*定义滚动条高宽及背景 高宽分别对应横竖滚动条的尺寸*/
/* ::-webkit-scrollbar
{
  width: 10px;
  height: 100%;
  background-color: #c0c4cc;
}*/
/*定义滚动条轨道 内阴影+圆角*/
/* ::-webkit-scrollbar-track
{
  -webkit-box-shadow: inset 0 0 6px rgba(0,0,0,0.3);
  border-radius: 10px;
  background-color: #c0c4cc;
} */
/*定义滑块 内阴影+圆角*/
/* ::-webkit-scrollbar-thumb
{
  border-radius: 8px;
  -webkit-box-shadow: inset 0 0 6px rgba(0,0,0,.3);
  background-color: #ff9800;
}*/
</style>
