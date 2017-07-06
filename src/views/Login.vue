<template>
<div class="body">
    <div class="login">
        <div class="login_box">
            <div class="qrcode">
                <img class="img" :src="this.qrCode">
                <div>
                    <p class="sub_title">{{sub_title}}</p>
                    <p class="sub_desc">{{sub_desc}}</p>
                </div>
            </div>
        </div>
    </div>
    <div class="github">
      <a class="lang-item" href="https://github.com/dongweiming/wechat-admin">Github</a>
    </div>
    <div class="copyright">
        <p class="desc">&copy; Wechat-Vue-Admin Team. All Rights </p>
    </div>
</div>
</template>

<script>
  import { requestLogin } from '../api/api';
  export default {
    methods: {
      validate(res) {
          let { msg, r } = res.data;
          if (r !== 0) {
              this.$message({
                  message: msg,
                  type: 'error'
              });
              return false;
          }
          return true;
      },
      login() {
          this.$eventSourceListener();
          requestLogin().then(res => {
              this.validate(res);
          });
      }
    },
    mounted() {
      this.login();
    }
  }
</script>

<style lang="scss">
body, dd, dl, fieldset, h1, h2, h3, h4, h5, h6, ol, p, textarea, ul {
    margin: 0;
}
a, button, input, textarea {
    outline: 0;
}

body, html {
     height: 100%;
} 

body {
    line-height: 1.6;
    font-family: Helvetica Neue,Helvetica,Hiragino Sans GB,Microsoft YaHei,\\5FAE\8F6F\96C5\9ED1,Arial,sans-serif;
//    background: url(../assets/bg2.jpg) no-repeat 50%;
//    background-size: cover;
}

.login {
    height: 100%;
    min-width: 860px;
    min-height: 700px;
    overflow: auto;
    position: relative;
}

.login_box {
    position: absolute;
    top: 50%;
    left: 50%;
    margin-left: -190px;
    margin-top: -270px;
    border-radius: 4px;
    -moz-border-radius: 4px;
    -webkit-border-radius: 4px;
    background-color: #fff;
    width: 380px;
    height: 540px;
    shadow: 0 2px 10px #999;
    .qrcode {
        position: relative;
        text-align: center;
        .img {
            display: block;
            width: 270px;
            height: 270px;
            margin: 42px auto 12px;
        }
        .sub_title {
            text-align: center;
            font-size: 20px;
            color: #353535;
            margin-bottom: 20px;
        }
        .sub_desc {
            text-align: center;
            color: #888;
            font-size: 18px;
        }
    }
}
.github {
    bottom: 60px;
    position: absolute;
    left: 60px;
    a {
        text-decoration: none;
        font-size: 12px;
        color: #d3d3d3;
    }
}
.copyright {
    position: absolute;
    bottom: 60px;
    right: 60px;
    color: #d3d3d3;
    font-size: 12px;
}
</style>
