/**
 * Created by rock on 14-11-17.
 */

var redisExplorer = angular.module('redisExplorer', []);
//    .filter(
//    'to_trusted', ['$sce', function ($sce) {
//        return function (text) {
//            return $sce.trustAsHtml(text);
//        }
//    }]);

var COLLECTION_OBSERVER = 'collectionObserver';
var COLLECTION_NOTICE = 'collectionNotice';
var VALUE_OBSERVER = 'valueObserver';
var VALUE_NOTICE = 'valueNotice';
var ALERT_OBSERVER = 'alertObserver';
var CONFIRM_OBSERVER = 'confirmObserver';
var CONFIRM_NOTICE = 'confirmNotice';
var NO_COLLECTION_OBSERVER = 'noCollectionObserver';

redisExplorer.controller('parentCtr', function parentCtr($scope, $http, $window) {
    $scope.alarm = false;
    $scope.choice = false;
    $scope.noCollection = false;
    $scope.$on(COLLECTION_OBSERVER, function (event, col, db) {
        $scope.$broadcast(COLLECTION_NOTICE, col, db);
    });
    $scope.$on(VALUE_OBSERVER, function (event, key) {
        $scope.$broadcast(VALUE_NOTICE, key);
    });
    $scope.$on(ALERT_OBSERVER, function (event, msg) {
        $scope.alarm = true;
        $scope.msg = msg;
    });
    $scope.$on(CONFIRM_OBSERVER, function (event, msg, key) {
        $scope.alarm = true;
        $scope.choice = true;
        $scope.msg = msg;
        $scope.key = key;
    });
    $scope.$on(NO_COLLECTION_OBSERVER, function (event) {
        $scope.noCollection = true;
    });
    $scope.close = function () {
        $scope.alarm = false;
    }
    $scope.yes = function () {
        $scope.alarm = false;
        $scope.choice = false;
        $scope.$broadcast(CONFIRM_NOTICE, 'confirmDel', true, $scope.key);
    }
    $scope.no = function () {
        $scope.alarm = false;
        $scope.choice = false;
        $scope.$broadcast(CONFIRM_NOTICE, 'confirmDel', false, $scope.key);
    }
    $scope.closeInput = function () {
        $scope.noCollection = false;
    }
    $scope.redis = undefined;
    $scope.new_redis = function (redis) {
        $http.post("/collection/", {redis: redis}).success(function (response) {
            if (response['success']) {
                $scope.$emit(ALERT_OBSERVER, '添加成功');
                $scope.closeInput();
            } else {
                $scope.$emit(ALERT_OBSERVER, response['msg']);
            }
        });
    }
});

redisExplorer.controller('colCtrl', function colCtrl($scope, $http) {
    $http.get("/collection/").success(function (response) {
        if (response['success']) {
            $scope.collections = response['collections'];
            $scope.dbs = response['dbs'];
            $scope.collection = response['currentCol'];
            $scope.db = response['currentDB'];
            $scope.$emit(COLLECTION_OBSERVER, $scope.collection, $scope.db);
        } else {
            $scope.$emit(ALERT_OBSERVER, response['msg']);
            $scope.$emit(NO_COLLECTION_OBSERVER);
        }
    }).error(function () {
        $scope.$emit(ALERT_OBSERVER, '服务端未知错误.');
    });
    $scope.change = function (c, d) {
        $scope.$emit(COLLECTION_OBSERVER, c, d);
    }
    $scope.redirect = function () {
        $scope.$emit(NO_COLLECTION_OBSERVER);
    }
});

redisExplorer.controller('keyCtrl', function keyCtrl($scope, $http) {
    $scope.$on(COLLECTION_NOTICE, function (event, col, db) {
        $http.get("/key/", {params: {target: col, db: db}}).success(function (response) {
            if (response['success']) {
                $scope.collection = col;
                $scope.db = db;
                $scope.keys = response['keys'];
            } else {
                $scope.keys = [];
                $scope.$emit(ALERT_OBSERVER, response['msg']);
            }
        }).error(function () {
            $scope.$emit(ALERT_OBSERVER, '服务端未知错误.');
        });
    });
    $scope.click = function (key) {
        $scope.key = key;
        $scope.$emit(VALUE_OBSERVER, key);
    }
});

redisExplorer.controller('valueCtrl', function valueCtrl($scope, $http) {
    $scope.$on(COLLECTION_NOTICE, function (event, col, db) {
        $scope.collection = col;
        $scope.db = db;
    });
    $scope.$on(VALUE_NOTICE, function (event, key) {
        $http.get("/value/", {params: {key: key, col: $scope.collection, db: $scope.db}}).success(function (response) {
            resetPage($scope);
            $scope.type = response['type'];
            $scope.key = response['key'];
            if ($scope.type == 'hash') {
                $scope.hash = response['value'];
            } else if ($scope.type == 'zset') {
                $scope.zset = response['value'];
            } else if ($scope.type == 'list') {
                $scope.list = response['value'];
            } else if ($scope.type == 'set') {
                $scope.set = response['value'];
            } else {
                $scope.string = response['value'];
            }
            if (!response['success']) {
                $scope.$emit(ALERT_OBSERVER, response['msg']);
            }
        }).error(function () {
            $scope.$emit(ALERT_OBSERVER, '服务端未知错误.');
        });
    });
    $scope.$on(CONFIRM_NOTICE, function (event, funcId, choose, key) {
        if (funcId == "confirmDel" && choose) {
            $http.delete("/value/", {
                params: {
                    key: key,
                    col: $scope.collection,
                    db: $scope.db
                }
            }).success(function (response) {
                resetPage($scope);
                if (response['success']) {
                    $scope.$emit(ALERT_OBSERVER, '删除成功');
                    $scope.$emit(COLLECTION_OBSERVER, $scope.collection, $scope.db);
                } else {
                    $scope.$emit(ALERT_OBSERVER, response['msg']);
                }
            }).error(function () {
                $scope.$emit(ALERT_OBSERVER, '服务端未知错误.');
            });
        }
    });
    $scope.del = function (key) {
        if (key == undefined) {
            $scope.$emit(ALERT_OBSERVER, '请选择要删除的键');
            return;
        }
        $scope.$emit(CONFIRM_OBSERVER, '确认删除:  ' + key + '  ?', key);
    }
    $scope.mutilDel = function () {
        $scope.$emit(ALERT_OBSERVER, '待实现');
    }
    $scope.adDel = function () {
        $scope.$emit(ALERT_OBSERVER, '待实现');
    }
    $scope.command = '';
    $scope.execute_command = function (command) {
        $http.post("/command/", {command: command, col: $scope.collection, db: $scope.db}).success(function (response) {
            resetPage($scope);
            if (response['success']) {
                $scope.$emit(ALERT_OBSERVER, '执行成功');
                $scope.$emit(COLLECTION_OBSERVER, $scope.collection, $scope.db);
            } else {
                $scope.$emit(ALERT_OBSERVER, response['msg']);
            }
        });
    }
});

function resetPage(page) {
    page.hash = undefined;
    page.zset = undefined;
    page.list = undefined;
    page.set = undefined;
    page.string = undefined;
    page.type = undefined;
    page.key = undefined;
}
