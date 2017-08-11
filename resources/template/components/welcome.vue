<template>
    <div class="content-wrapper" ref="mainContent" style="margin-left: 0;padding: 0 100px 0 100px">
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
            <template>
                <div class="col-lg-3 col-xs-4">
                    <div class="small-box bg-aqua">
                        <div class="inner" @click="go(123)" style="cursor: pointer">
                            <span class="client-head">Darkhouse</span>
                            <p>Redis Cluster</p>
                        </div>
                        <div class="icon" @click="go(123)" style="cursor: pointer">
                            <i class="fa fa-play-circle"></i>
                        </div>
                        <a href="#" class="small-box-footer">
                            <b>修改</b>&nbsp;<i class="fa fa-gear"></i>
                        </a>
                    </div>
                </div>
            </template>
        </section>
    </div>
</template>
<script>
    module.exports = {
        methods: {
            go: function (id) {
                this.$router.push({path: '/' + id})
            }
        },
        mounted: function () {
            let ref = this.$refs;
            let height = document.documentElement.clientHeight;
            ref.mainContent.style.height = (height - 101) + 'px';
        }
    }
</script>