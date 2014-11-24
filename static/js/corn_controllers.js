/**
 * Created by rock on 14-11-17.
 */

var redisExplorer = angular.module('redisExplorer', []);

redisExplorer.controller('parentCtr', function parentCtr($scope) {
    $scope.$on('collectionObserver', function (event, col, db) {
        $scope.$broadcast('collectionNotice', col, db);
    });
    $scope.$on('valueObserver', function (event, key, col, db) {
        $scope.$broadcast('valueNotice', key, col, db);
    });
});

redisExplorer.controller('colCtrl', function colCtrl($scope, $http, $window) {
    $http.get("/collection/").success(function (response) {
        $scope.collections = response['collections'];
        $scope.dbs = response['dbs'];
        $scope.collection = response['currentCol'];
        $scope.db = response['currentDB'];
        $scope.$emit('collectionObserver', $scope.collection, $scope.db);
    }).error(function () {
        alert('服务端未知错误.');
    });
    $scope.change = function (c, d) {
        $scope.$emit('collectionObserver', c, d);
    }
    $scope.redirect = function (url) {
        $window.location.href = url;
    }
});

redisExplorer.controller('keyCtrl', function keyCtrl($scope, $http) {
    $scope.$on('collectionNotice', function (event, col, db) {
        $http.get("/key/", {params: {target: col, db: db}}).success(function (response) {
            if (response['success']) {
                $scope.collection = col;
                $scope.db = db;
                $scope.keys = response['keys'];
            } else {
                $scope.keys = [];
                alert(response['msg']);
            }
        }).error(function () {
            alert('服务端未知错误.');
        });
    });
    $scope.click = function (key) {
        $scope.$emit('valueObserver', key, $scope.collection, $scope.db);
    }
    $scope.mutilDel = function () {
        alert('待实现');
    }
    $scope.adDel = function () {
        alert('待实现');
    }
})
;

redisExplorer.controller('valueCtrl', function valueCtrl($scope, $http) {
    $scope.$on('valueNotice', function (event, key, col, db) {
        $http.get("/value/", {params: {key: key, col: col, db: db}}).success(function (response) {
            clearValuePage($scope);
            $scope.type = response['type'];
            $scope.key = response['key'];
            $scope.col = col;
            $scope.db = db;
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
                alert(response['msg']);
            }
        }).error(function () {
            alert('服务端未知错误.');
        });
    });
    $scope.del = function (key, col, db) {
        if (key == undefined) {
            alert('请选择要删除的键');
            return;
        }
        var c = confirm('确认删除:  ' + key + '  ?');
        if (c) {
            $http.delete("/value/", {params: {key: key, col: col, db: db}}).success(function (response) {
                clearValuePage($scope);
                if (response['success']) {
                    alert('删除成功');
                    $scope.$emit('collectionObserver', col, db);
                } else {
                    alert(response['msg']);
                }
            }).error(function () {
                alert('服务端未知错误.');
            });
        }
    }
    $scope.command = '';
    $scope.execute_command = function (command, col, db) {
        alert(command);
        $http({
            method: 'POST',
            url: "/command/",
            data: {command: command, col: col, db: db},
            headers: {
                'Content-Type': 'application/json;charset=UTF-8'
            }
        }).success(function (response) {
            alert(response);
        });
    }
});

function clearValuePage(page) {
    page.hash = undefined;
    page.zset = undefined;
    page.list = undefined;
    page.set = undefined;
    page.string = undefined;
    page.type = undefined;
    page.key = undefined;
    page.col = undefined;
    page.db = undefined;
}
