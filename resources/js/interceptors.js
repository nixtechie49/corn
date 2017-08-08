import Vue from "vue";

export default function init() {
    Vue.http.interceptors.push((request, next) => {
        console.log(request);
        next((response) => {
            if (response.status < 400) {
                let msg = response.body;
                if (msg && msg.code !== 1) {
                    console.log(msg);
                }
            } else {
                console.log('请求异常:' + response.status + '' + '=' + response.statusText);
                console.log('url : ' + request.url);
            }
            if (response.status === 401) {
                console.log('login false');
            } else {
                console.log('login true');
            }
            if (response.status === 407) {
                console.log('forbidden true');
            } else {
                console.log('forbidden false');
            }
        });
    })
}