import Vue from 'vue'

export default {
    install(Vue, defaultOptions = {}) {
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
        Vue.checkStatus = Vue.prototype.$checkStatus = checkStatus;
    }
}
