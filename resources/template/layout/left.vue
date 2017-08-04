<template>
    <aside class="main-sidebar">
        <section class="sidebar">
            <div class="sidebar-form">
                <div class="input-group">
                    <input type="text" name="pattern" class="form-control" placeholder="Search..."/>
                    <span class="input-group-btn">
                        <button type="button" name="search" id="search-btn" class="btn btn-flat">
                            <i class="fa fa-search"></i>
                        </button>
                    </span>
                </div>
            </div>
            <input type="hidden" v-model="index"/>
            <ul style="padding-left: 10px">
                <li v-for="k in keys" class="key"><span>{{ k }}</span></li>
            </ul>
        </section>
    </aside>
</template>
<script>

    module.exports = {
        data:function(){
            return {
                index:0,
                keys:[]
            }
        },
        methods: {
            getKeys: function () {
                let v = this;
                let url = '/key';
                v.$http.get(url, {headers: {'Content-Type': 'application/json;charset=utf-8'}}).then(
                    function (response) {
                        let msg = response.body;
                        console.log(msg);
                        v.index = msg[0];
                        v.keys = msg[1];
                    }, function (response) {
                        console.log(response);
                    }
                );
            }
        },
        created:function(){
            this.getKeys();
        }
    }

</script>