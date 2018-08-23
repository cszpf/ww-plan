<template>
    <div id="commodityCouponsDetails">
      <screenData></screenData>
    </div>
</template>
<script>
import screenData from '../components/screenData.vue'
export default {
  name: 'commodityCouponsDetails',
  data () {
    return {
      name: 'commodityCouponsDetails'
    }
  },
  components: {
    'screenData': screenData
  }
}
</script>
