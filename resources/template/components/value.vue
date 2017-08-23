<template>
    <div style="overflow: auto" ref="content">
        <p>KEY = {{ $route.params.key }}</p>
        <p>TYPE = {{ type }}</p>
        <span>VALUE = </span>
        <span v-html="value"></span>
    </div>
</template>
<script>

    module.exports = {
        data: function () {
            return {
                type: '',
                value: {}
            }
        },
        methods: {
            getValue: function () {
                let v = this;
                if (v.$route.params.key) {
                    let url = '/' + v.$route.params.connection + '/value/' + v.$route.params.key;
                    v.$http.get(url, {headers: {'Content-Type': 'application/json;charset=utf-8'}}).then(
                        (response) => {
                            let res = response.body;
                            if (res.code === 1) {
                                let data = res.data;
                                v.type = data[0];
                                v.value = bePretty(data[1]);
                            }
                        }, (response) => {
                            console.log(response);
                        }
                    );
                }
            }
        },
        updated: function () {
            this.getValue();
        },
        mounted: function () {
            let ref = this.$refs;
            let height = document.documentElement.clientHeight;
            ref.content.style.height = (height - 161) + 'px';
        },
        created: function () {
            this.getValue();
        }
    }

</script>