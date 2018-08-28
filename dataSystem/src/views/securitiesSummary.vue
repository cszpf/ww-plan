<template>
  <div id="securitiesSummary">
    <screenData v-on:fullConditions='loadData' :storeAttributes="attribute" :sogo="merchant" :shop="outlet"></screenData>
  </div>
</template>

<script>
import screenData from '../components/screenData.vue'
import axios from 'axios'
export default {
  name: 'securitiesSummary',
  data () {
    return {
      merchant: false,
      outlet: false,
      adminiStrative: [],
      attribute: false
    }
  },
  created () {},
  mounted () {},
  components: {
    'screenData': screenData
  },
  methods: {
    loadData (data) {
      console.log(data)
      axios({method: 'post', url: this.$store.state.url + '/api/table_export', data: data})
        .then(response => {
          // if (response.data) {
          //   this.loading = false
          //   this.$store.commit('increment', false)
          // }
          console.log(response)
          console.log(response.data)
          // this.dataList = response.data
          // console.log(this.dataList)
          // if (this.dataList.length <= 10) {
          //   this.pageright = false
          //   this.dataPageList = response.data
          // } else {
          //   this.dataPageList = response.data.slice(this.page * 10, 10)
          //   this.pageright = true
          //   console.log(this.dataPageList)
          // }
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
