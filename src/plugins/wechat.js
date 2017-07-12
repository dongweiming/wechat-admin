import Vue from 'vue'

function checkStatus(res, options = {}) {
    let { r, msg } = res.data;
    let type, message;
    if (r !== 0) {
        type = 'error';
        message = msg;
    } else {
        type = 'success';
        message = '提交成功';
    }
    this.$message({
        message: message,
        type: type
    });
}

function eventSourceListener() {
    let source = new EventSource(`${API_URL}/stream`);
    let self = this;
    source.addEventListener('login', function(event) {
        let data = JSON.parse(event.data);
        if (data.type == 'scan_qr_code') {
            self.uuid = data.uuid;
            self.qrCode = `${API_URL}/static/img/qr_code.png`;
        } else if (data.type == 'confirm_login') {
            self.sub_title = 'Scan successful';
            self.sub_desc = 'Confirm login on mobile WeChat';
            self.qrCode = data.extra;
        } else if (data.type == 'logged_in') {
            sessionStorage.setItem('user', JSON.stringify(data.user));
            self.$router.push({ path: '/main' });
        } else if (data.type == 'logged_out') {
            sessionStorage.removeItem('user');
            self.$router.push('/login');
        }
    }, false);

    source.addEventListener('notification', function(event) {
        let data = JSON.parse(event.data);
        self.notificationCount = data.count;
    }, false);

    source.addEventListener('error', function(event) {
        console.log("Failed to connect to event stream");
    }, false);
}

export default {
    install(Vue, defaultOptions = {}) {
        Vue.mixin({
            data: function() {
                return {
                    uuid: '',
                    qrCode: `${API_URL}/static/img/qr_code.gif`,
                    sub_title: 'Scan to log in to WeChat',
                    sub_desc: 'Log in on phone to use WeChat on Web',
                    notificationCount: 0
                }
            }
        }),
        Vue.prototype.$checkStatus = checkStatus;
        Vue.prototype.$eventSourceListener = eventSourceListener;
    }
}
