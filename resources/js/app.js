import Vue from "vue";
import VueResource from "vue-resource";
import VueRouter from "vue-router";
import App from "../template/app.vue";
import Routes from "./routes";
import interceptors from "./interceptors"

Vue.use(VueRouter);
Vue.use(VueResource);
interceptors;

// routing
const router = new VueRouter({
    routes: Routes,
    linkActiveClass: 'active'
});

Vue.filter('time', function (value) {
    return new Date(parseInt(value)).toLocaleString().replace(/年|月/g, "-").replace(/日/g, " ");
});

const app = new Vue({
    router: router,
    render: h => h(App)
}).$mount('#app');