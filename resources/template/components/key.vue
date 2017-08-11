<template>
    <aside class="main-sidebar" ref="mainSide" style="max-height: 100%">
        <section class="sidebar" ref="side" style="padding-bottom: 0">
            <div class="sidebar-form" ref="sideForm">
                <div class="input-group">
                    <input type="text" name="pattern" class="form-control" placeholder="Search | Filter"/>
                    <span class="input-group-btn">
                        <button type="button" name="search" id="search-btn" class="btn btn-flat">
                            <i class="fa fa-search"></i>
                        </button>
                    </span>
                </div>
            </div>
            <input type="hidden" v-model="index"/>
            <ul style="margin-bottom: 0;padding-left:10px; overflow-y:auto; overflow-x:hidden;" ref="innerSide">
                <template v-for="k in keys">
                    <router-link tag="li" class="key" :to="'/'+$route.params.connection+'/value/'+k">
                        <span>{{ k }}</span>
                    </router-link>
                </template>
            </ul>
        </section>
    </aside>
</template>
<script>
    module.exports = {
        data: function () {
            return {
                index: 0,
                keys: []
            }
        },
        methods: {
            getKeys: function () {
                let v = this;
                let url = '/key';
                v.$http.get(url, {headers: {'Content-Type': 'application/json;charset=utf-8'}}).then(
                    function (response) {
                        let msg = response.body;
                        v.index = msg[0];
                        v.keys = msg[1];
                    }, function (response) {
                        console.log(response);
                    }
                );
            }
        },
        mounted: function () {
            let ref = this.$refs;
            let sizeHeight = ref.mainSide.offsetHeight - 50;
            ref.side.style.maxHeight = sizeHeight + 'px';
            let formHeight = ref.sideForm.offsetHeight;
            ref.innerSide.style.maxHeight = (sizeHeight - formHeight - 20) + 'px';
        },
        created: function () {
            this.getKeys();
        }
    }
</script>