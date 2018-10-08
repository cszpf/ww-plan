<template>
  <div id="passwd">
    <div class="passwd-content">
      <el-form>
        <el-form-item>
          <el-input type="password" placeholder="原密码" v-model='oldpwd'>{{ oldpwd }}</el-input>
        </el-form-item>
        <el-form-item>
          <el-input type="password" placeholder="新密码" v-model='newpwd'>{{ newpwd }}</el-input>
        </el-form-item>
        <el-form-item>
          <el-input type="password" placeholder="请确认密码" v-model='twice'>{{ twice }}</el-input>
        </el-form-item>
        <el-form-item>
          <el-button class="passwd-button" type="warning" @click="submitForm">确认</el-button>
        </el-form-item>
        <el-form-item>
          <el-button class="passwd-button" type="info" plain @click="cancel">取消</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>
<script>
import axios from 'axios'
export default {
  name: 'passwd',
  data () {
    return {
      name: '',
      oldpwd: '',
      newpwd: '',
      twice: ''
    }
  },
  methods: {
    submitForm () {
      const path = this.$store.state.url + '/api/pwd'
      axios.post(path, {'oldpwd': this.oldpwd, 'newpwd': this.newpwd, 'twice': this.twice})
        .then(response => {
          console.log(response)
          if (response.statusText === 'OK') {
            this.$message({message: '修改成功', type: 'success'})
            this.$router.push({path: '/login'})
          } else {
            this.$message.error(response.data.status)
          }
        })
        .catch(function (error) {
          console.log(error)
        })
    },
    cancel () {
      this.$router.push({path: '/storesSummary'})
    }
  }
}

</script>

<style scoped>
#passwd {
    height: 100vh;
    width: 100%;
}
#passwd .passwd-content {
  width: 360px;
  position: absolute;
  left:50%; top:50%;
  transform:translate(-50%,-50%);
}
#passwd .passwd-button {
  width: 100%;
}
</style>
