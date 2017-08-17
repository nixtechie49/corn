import Content from "../template/components/content.vue";
import Connection from "../template/components/connection.vue";
import Welcome from "../template/components/welcome.vue";
import Value from "../template/components/value.vue";

export default [
    {path: '/', component: Welcome},
    {path: '/connection', component: Connection},
    {path: '/connection/:connection', component: Connection},
    {
        path: '/:connection', component: Content,
        children: [
            {path: 'value/:key', components: {content: Value}}
        ],
    }
]