<template>
  <div id="customerSummary">
    <screenData :sogo="merchant" :shop="outlet"></screenData>
  </div>
</template>
<script>
import screenData from '../components/screenData.vue'
export default {
  name: 'customerSummary',
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
<style>
#customerSummary {
  margin: 15px 20px;
}
</style>
