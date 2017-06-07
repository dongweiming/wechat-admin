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
      <a class="lang-item" href="github.com/dongweiming/">Github</a>
    </div>
    <div class="copyright">
        <p class="desc">&copy; Wechat-Vue-Admin Team. All Rights </p>
    </div>
</div>
</template>

<script>
  import { requestLogin } from '../api/api';
  export default {
    data() {
      return {
        uuid: '',
        qrCode: 'http://localhost:8100/static/img/qr_code.gif',
        sub_title: 'Scan to log in to WeChat',
        sub_desc: 'Log in on phone to use WeChat on Web'
      };
    },
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
      eventSourceListen() {
          let source = new EventSource("http://localhost:8100/stream");
          let self = this;
          source.addEventListener('login', function(event) {
              let data = JSON.parse(event.data);
              if (data.type == 'scan_qr_code') {
                  self.uuid = data.uuid;
                  self.qrCode = 'http://localhost:8100/static/img/qr_code.png';
              } else if (data.type == 'confirm_login') {
                  self.sub_title = 'Scan successful';
                  self.sub_desc = 'Confirm login on mobile WeChat';
                  self.qrCode = 'http://localhost:8100/static/img/qr_code.gif';
              } else if (data.type == 'logged_in') {
                  sessionStorage.setItem('user', JSON.stringify(data.user));
                  self.$router.push({ path: '/main' });
              }
          }, false);
          source.addEventListener('error', function(event) {
              console.log("Failed to connect to event stream");
          }, false);

      },
      login() {
          this.eventSourceListen();
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
