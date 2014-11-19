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

redisExplorer.controller('colCtrl', function colCtrl($scope, $http) {
    $http.get("/collection/").success(function (response) {
        $scope.collections = response['collections'];
        $scope.dbs = response['dbs'];
        $scope.collection = response['currentCol'];
        $scope.db = response['currentDB'];
        $scope.$emit('collectionObserver', $scope.collection, $scope.db);
    });
    $scope.change = function (c, d) {
        $scope.$emit('collectionObserver', c, d);
    }
});

redisExplorer.controller('keyCtrl', function keyCtrl($scope, $http) {
    $scope.$on('collectionNotice', function (event, col, db) {
        $http.get("/key/", {params: {target: col, db: db} }).success(function (response) {
            $scope.collection = col;
            $scope.db = db;
            $scope.keys = response;
        });
    });
    $scope.click = function (key) {
        $scope.$emit('valueObserver', key, $scope.collection, $scope.db);
    }
});

redisExplorer.controller('valueCtrl', function valueCtrl($scope, $http) {
    $scope.$on('valueNotice', function (event, key, col, db) {
        $http.get("/value/", {params: {key: key, col: col, db: db} }).success(function (response) {
            $scope.type = response['type'];
            $scope.value = response['value'];
        });
    });
});
