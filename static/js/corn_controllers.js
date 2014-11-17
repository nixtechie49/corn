/**
 * Created by rock on 14-11-17.
 */

var redisExplorer = angular.module('redisExplorer', []);

redisExplorer.controller('keyController', function keyController($scope, $http) {
    $http.get("/key/", {params: {target: 'sc0', db: '0'} })
        .success(function (response) {
            $scope.keys = response;
        });
});
