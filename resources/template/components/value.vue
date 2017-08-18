<template>
    <div>
        <p>key = {{ $route.params.key }}</p>
        <span>value = </span><span v-html="value"></span>
    </div>
</template>
<script>

    module.exports = {
        data: function () {
            return {
                value: {}
            }
        },
        methods: {
            getValue: function () {
                let v = this;
                if (v.$route.params.key) {
                    let url = '/value/' + v.$route.params.key;
                    v.$http.get(url, {headers: {'Content-Type': 'application/json;charset=utf-8'}}).then(
                        (response) => {
                            let res = response.body;
                            if (res.code === 1) {
                                let data = res.data;
                                v.value = bePretty(JSON.stringify(data));
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
        created: function () {
            this.getValue();
        }
    }

</script>