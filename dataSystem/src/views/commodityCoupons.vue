<template>
    <div id="commodityCoupons">
      <screenData :storeAttributes="attribute" :sogo="merchant" :shop="outlet"></screenData>
    </div>
</template>
<script>
import screenData from '../components/screenData.vue'
export default {
  name: 'commodityCoupons',
  data () {
    return {
      name: 'commodityCoupons'
    }
  },
  components: {
    'screenData': screenData
  },
}
</script>
