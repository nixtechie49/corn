<template>
    <div class="content-wrapper content-main" ref="mainContent">
        <section class="content-header">
            <h1>
                &nbsp;
                <small>&nbsp;</small>
            </h1>
            <ol class="breadcrumb">
                <li><router-link to="/"><i class="fa fa-link"></i> 连接管理</router-link></li>
                <li class="active" v-if="connection.id">修改连接</li>
                <li class="active" v-else>添加连接</li>
            </ol>
        </section>
        <section class="content" style="width: 60%">
            <div class="box box-info">
                <div class="box-header with-border">
                    <h3 class="box-title" v-if="connection.id">修改连接</h3>
                    <h3 class="box-title" v-else>添加连接</h3>
                </div>
                <div class="box-body form-horizontal">
                    <div class="form-group">
                        <label for="nameInput" class="col-sm-2 control-label">名称</label>
                        <div class="col-sm-10">
                            <input type="text" class="form-control" :disabled="disable.name" id="nameInput"
                                   v-model="connection.name"
                                   placeholder="Name"/>
                        </div>
                    </div>
                    <div class="form-group">
                        <label for="typeInput" class="col-sm-2 control-label">类型</label>
                        <div class="col-sm-10">
                            <select style="width: 200px" id="typeInput" :disabled="disable.type" class="select2"
                                    v-model="connection.type">
                                <option value="1">Redis</option>
                                <option value="2">Redis Cluster</option>
                                <option value="3">zookeeper</option>
                            </select>
                        </div>
                    </div>
                    <div class="form-group">
                        <label for="pwdInput" class="col-sm-2 control-label">密码</label>
                        <div class="col-sm-10">
                            <input type="password" class="form-control" :disabled="disable.password" id="pwdInput"
                                   v-model="connection.password"
                                   placeholder="Password"/>
                        </div>
                    </div>
                    <div class="form-group">
                        <label for="hostInput" class="col-sm-2 control-label">地址</label>
                        <div class="col-sm-10">
                            <input type="text" class="form-control" :disabled="disable.host" id="hostInput"
                                   v-model="connection.host"
                                   placeholder="Host"/>
                        </div>
                    </div>
                    <div class="form-group">
                        <label for="portInput" class="col-sm-2 control-label">端口</label>
                        <div class="col-sm-10">
                            <input type="number" class="form-control" :disabled="disable.port" id="portInput"
                                   v-model="connection.port"
                                   placeholder="Port"/>
                        </div>
                    </div>
                    <div class="form-group">
                        <label for="dbInput" class="col-sm-2 control-label">库</label>
                        <div class="col-sm-10">
                            <input type="number" class="form-control" :disabled="disable.db" id="dbInput"
                                   v-model="connection.db"
                                   placeholder="DB"/>
                        </div>
                    </div>
                    <div class="form-group">
                        <label for="pathInput" class="col-sm-2 control-label">路径</label>
                        <div class="col-sm-10">
                            <input type="text" class="form-control" :disabled="disable.path" id="pathInput"
                                   v-model="connection.path"
                                   placeholder="Path"/>
                        </div>
                    </div>
                </div>
                <div class="box-footer">
                    <button type="button" class="btn btn-danger pull-left" @click="del()" v-if="connection.id">删除
                    </button>
                    <button type="button" class="btn btn-success pull-right" style="margin-left: 15px"
                            @click="submit()">保存
                    </button>
                    <button type="button" class="btn btn-default pull-right" @click="back()">取消</button>
                </div>
            </div>
        </section>
    </div>
</template>
<script>
    module.exports = {
        data: function () {
            return {
                connection: {
                    id: null,
                    name: null,
                    type: null,
                    password: null,
                    host: null,
                    port: null,
                    db: null,
                    path: null
                }
            }
        },
        computed: {
            disable: function () {
                let type = this.connection.type;
                let disable = {};
                if (type == 1) {
                    disable = {
                        name: false,
                        type: false,
                        password: false,
                        host: false,
                        port: false,
                        db: false,
                        path: true,
                    };
                } else if (type == 2) {
                    disable = {
                        name: false,
                        type: false,
                        password: false,
                        host: false,
                        port: true,
                        db: true,
                        path: true,
                    };
                } else if (type == 3) {
                    disable = {
                        name: false,
                        type: false,
                        password: true,
                        host: false,
                        port: true,
                        db: true,
                        path: false,
                    };
                } else {
                    disable = {
                        name: false,
                        type: false,
                        password: true,
                        host: false,
                        port: true,
                        db: true,
                        path: true,
                    };
                }
                return disable;
            }
        },
        methods: {
            back: function () {
                this.$router.push({path: '/'})
            },
            get: function (id) {
                let v = this;
                let url = '/connection/' + id;
                v.$http.get(url, {headers: {'Content-Type': 'application/json;charset=utf-8'}}).then(
                    (response) => {
                        let res = response.body;
                        if (res.code === 1) {
                            let data = res.data;
                            v.connection = data;
                            $('.select2').val(data.type).trigger('change');
                        }
                    }, (response) => {
                        console.log(response);
                    }
                );
            },
            update: function () {
                let v = this;
                let url = '/connection';
                let data = this.connection;
                v.$http.put(url, data, {headers: {'Content-Type': 'application/json;charset=utf-8'}}).then(
                    function (response) {
                        let res = response.body;
                        if (res.code === 1) {
                            v.$router.push('/');
                        }
                    }, function (response) {
                        console.log(response);
                    }
                );
            },
            save: function () {
                let v = this;
                let url = '/connection';
                let data = this.connection;
                v.$http.post(url, data, {headers: {'Content-Type': 'application/json;charset=utf-8'}}).then(
                    function (response) {
                        let res = response.body;
                        if (res.code === 1) {
                            v.$router.push('/');
                        }
                    }, function (response) {
                        console.log(response);
                    }
                );
            },
            del: function () {
                let v = this;
                let url = '/connection/' + v.connection.id;
                v.$http.delete(url, {headers: {'Content-Type': 'application/json;charset=utf-8'}}).then(
                    function (response) {
                        let res = response.body;
                        if (res.code === 1) {
                            v.$router.push('/');
                        }
                    }, function (response) {
                        console.log(response);
                    }
                );
            },
            submit: function () {
                let id = this.connection.id;
                if (id)
                    this.update();
                else
                    this.save();
            }
        },
        mounted: function () {
            let v = this;
            let id = v.$route.params.connection;
            if (id)
                v.get(id);
            let ref = v.$refs;
            let height = document.documentElement.clientHeight;
            ref.mainContent.style.height = (height - 101) + 'px';
            this.$nextTick(function () {
                let select = $('.select2');
                select.select2({
                    placeholder: "请选择",
                    minimumResultsForSearch: Infinity,
                });
                select.on('select2:select', function (evt) {
                    v.connection.type = evt.target.value;
                });
            });
        }
    }
</script>