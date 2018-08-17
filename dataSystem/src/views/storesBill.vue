<template>
    <div id="storesBill">
      <screenData></screenData>
    </div>
</template>
<script>
import screenData from '../components/screenData.vue'
export default {
  name: 'storesBill',
  data () {
    return {
      name: 'storesBill'
    }
  },
  components: {
    'screenData': screenData
  }
}
</script>
