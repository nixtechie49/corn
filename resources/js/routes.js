import Main from "../template/components/welcome.vue";
import Value from "../template/components/value.vue";

export default [
    {path: '/', component: Main},
    {path: '/value/:key', component: Value}
]