<template>
  <div id="securitiesSummary">
    <screenData :sogo="merchant" :shop="outlet"></screenData>
  </div>
</template>

<script>
import screenData from '../components/screenData.vue'
export default {
  name: 'securitiesSummary',
  data () {
    return {
      merchant: false,
      outlet: false
    }
  },
  components: {
    'screenData': screenData
  }
}
</script>
<style scoped>
#securitiesSummary {
  margin:15px 20px;
}
</style>
