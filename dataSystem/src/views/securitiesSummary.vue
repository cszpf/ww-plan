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
      outlet: false,
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
#securitiesSummary {
  margin:15px 20px;
}
</style>
