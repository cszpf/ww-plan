<template>
  <div id="storeBillRatio">
    <screenData></screenData>
  </div>
</template>
<script>
import screenData from '../components/screenData.vue'
export default {
  name: 'storeBillRatio',
  data () {
    return {
      name: 'storeBillRatio'
    }
  },
  components: {
    'screenData': screenData
  }
}
</script>
