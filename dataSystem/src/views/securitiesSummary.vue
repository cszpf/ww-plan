<template>
  <div id="securitiesSummary">
    <screenData :district='adminiStrative' :sogo="merchant" :shop="outlet"></screenData>
  </div>
</template>

<script>
import axios from 'axios'
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
  mounted () {
    this.loadData('ADMIN_REGION_CODE')
  },
  components: {
    'screenData': screenData
  },
  methods: {
    loadData (idnmae) {
      let _this = this
      console.log(idnmae)
      axios({method: 'post', url: 'http://localhost:5000/api/databind', data: {id: idnmae}})
        .then(function (response) {
          console.log(response.statusText)
          console.log(response.statusText === 'OK')
          if (response.statusText === 'OK') {
            if (idnmae === 'ADMIN_REGION_CODE') {
              _this.adminiStrative = response.data.ADMIN_REGION_CODE ? response.data.ADMIN_REGION_CODE : ''
            }
            console.log(_this.adminiStrative)
          } else {
            _this.$message.error('占无数据')
          }
        })
        .catch(function (error) {
          console.log(error)
        })
    }
  }
}
</script>
<style scoped>
#securitiesSummary {
  margin:15px 20px;
}
</style>
