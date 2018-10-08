import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

export default new Router({
  routes: [
    // 重定向
    {
      path: '/',
      redirect: '/login'
    },
    // 登录
    {
      path: '/login',
      meta: {
        requireAuth: true
      },
      component: resolve => require(['@/views/login'], resolve)
    },
    // 修改密码
    {
      path: '/passwd',
      meta: {
        requireAuth: true
      },
      component: resolve => require(['@/views/passwd'], resolve)
    },
    // 导表页面
    {
      path: '/tableList',
      meta: {
        requireAuth: true
      },
      component: resolve => require(['@/views/tableList'], resolve)
    },
    // 活跃门店数量
    {
      path: '/activeStores',
      meta: {
        requireAuth: true
      },
      component: resolve => require(['@/views/activeStores'], resolve)
    },
    // 沉默门店数量
    {
      path: '/silenceStores',
      meta: {
        requireAuth: true
      },
      component: resolve => require(['@/views/silenceStores'], resolve)
    },
    // 异动商户流失数量
    {
      path: '/businessesLost',
      meta: {
        requireAuth: true
      },
      component: resolve => require(['@/views/businessesLost'], resolve)
    },
    // 流失商户数量
    {
      path: '/lossMerchants',
      meta: {
        requireAuth: true
      },
      component: resolve => require(['@/views/lossMerchants'], resolve)
    },
    // 下线券
    {
      path: '/referralsTicket',
      meta: {
        requireAuth: true
      },
      component: resolve => require(['@/views/referralsTicket'], resolve)
    },
    // 修改券
    {
      path: '/amendTicket',
      meta: {
        requireAuth: true
      },
      component: resolve => require(['@/views/amendTicket'], resolve)
    },
    // 快到期券
    {
      path: '/expiredCoupons',
      meta: {
        requireAuth: true
      },
      component: resolve => require(['@/views/expiredCoupons'], resolve)
    },
    // 主页
    {
      path: '/index',
      meta: {
        requireAuth: true
      },
      component: resolve => require(['@/views/index'], resolve),
      children: [
        // 门店汇总
        {
          path: '/storesSummary',
          component: resolve => require(['@/views/storesSummary'], resolve)
        },
        // 劵汇总
        {
          path: '/securitiesSummary',
          component: resolve => require(['@/views/securitiesSummary'], resolve)
        },
        // 客户汇总
        {
          path: '/customerSummary',
          component: resolve => require(['@/views/customerSummary'], resolve)
        },
        // 商户用劵
        {
          path: '/commodityCoupons',
          component: resolve => require(['@/views/commodityCoupons'], resolve)
        },
        // 商户用劵详情
        {
          path: '/commodityCouponsDetails',
          component: resolve => require(['@/views/commodityCouponsDetails'], resolve)
        },
        // 门店流水
        {
          path: '/storesBill',
          component: resolve => require(['@/views/storesBill'], resolve)
        },
        // 门店流水占比
        {
          path: '/storeBillRatio',
          component: resolve => require(['@/views/storeBillRatio'], resolve)
        },
        // 门店排行
        {
          path: '/storeRanking',
          component: resolve => require(['@/views/storeRanking'], resolve)
        },
        // 券排行
        {
          path: '/topCoupons',
          component: resolve => require(['@/views/topCoupons'], resolve)
        },
        // 点击量
        {
          path: '/pageView',
          component: resolve => require(['@/views/pageView'], resolve)
        }
      ]
    }
  ]
})
