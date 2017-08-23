<template>
    <div class="content-wrapper content-main" ref="mainContent">
        <section class="content-header">
            <h1>
                选择连接
                <small>:</small>
            </h1>
            <ol class="breadcrumb">
                <li><a href="#"><i class="fa fa-dashboard"></i> Home</a></li>
                <li><a href="#">Layout</a></li>
                <li class="active">Top Navigation</li>
            </ol>
        </section>
        <section class="content">
            <template v-for="c in conn">
                <div class="col-lg-3 col-xs-4">
                    <div class="small-box bg-green">
                        <div class="inner" @click="go(c.id)" style="cursor: pointer">
                            <span class="client-head">{{ c.name }}</span>
                            <p>Redis Cluster</p>
                        </div>
                        <div class="icon" @click="go(c.id)" style="cursor: pointer">
                            <i class="fa fa-play-circle"></i>
                        </div>
                        <a href="#" class="small-box-footer">
                            <b>修改</b>&nbsp;<i class="fa fa-gear"></i>
                        </a>
                    </div>
                </div>
            </template>
            <div class="col-lg-3 col-xs-4">
                <div class="small-box bg-yellow">
                    <div class="inner" @click="add()" style="cursor: pointer">
                        <span class="client-head">添加</span>
                        <p>添加一个新的连接</p>
                    </div>
                    <div class="icon" @click="add()" style="cursor: pointer">
                        <i class="fa fa-plus-circle"></i>
                    </div>
                    <a href="javascript:void(0)" @click="add()" class="small-box-footer">
                        &nbsp;
                    </a>
                </div>
            </div>
        </section>
    </div>
</template>
<script>
    module.exports = {
        data:function(){
            return {
                conn:{}
            }
        },
        methods: {
            go: function (id) {
                this.$router.push({path: '/' + id})
            },
            add: function () {
                this.$router.push({path: '/connection'})
            },
            listConn: function () {
                let v = this;
                let url = '/connection';
                v.$http.get(url, {headers: {'Content-Type': 'application/json;charset=utf-8'}}).then(
                    function (response) {
                        let res = response.body;
                        if (res.code === 1) {
                            v.conn = res.data;
                        }
                    }, function (response) {
                        console.log(response);
                    }
                );
            }
        },
        mounted: function () {
            this.listConn();
            let ref = this.$refs;
            let height = document.documentElement.clientHeight;
            ref.mainContent.style.height = (height - 101) + 'px';
        }
    }
</script>