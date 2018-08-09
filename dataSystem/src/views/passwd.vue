<template>
  <div id="passwd">
    <div class="passwd-content">
      <el-form>
        <el-form-item>
          <el-input type="text" placeholder="原密码"></el-input>
        </el-form-item>
        <el-form-item>
          <el-input type="text" placeholder="新密码"></el-input>
        </el-form-item>
        <el-form-item>
          <el-input type="text" placeholder="在输入一次密码"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button class="passwd-button" type="warning">确认</el-button>
        </el-form-item>
        <el-form-item>
          <el-button class="passwd-button" type="info" plain>取消</el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script>
export default {
  name: 'passwd',
  data () {
    return {
      name: ''
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
