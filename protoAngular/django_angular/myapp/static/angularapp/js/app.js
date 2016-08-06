var module = angular.module("sampleApp", ['ngRoute']);
module.config(function ($interpolateProvider) {
    $interpolateProvider.startSymbol('[[').endSymbol(']]');
})
module.config(['$routeProvider',
    function($routeProvider) {
        $routeProvider.
            when('/route1', {
                templateUrl: static_url + 'angularapp/html/test1.html',
                controller: 'RouteController1'
            }).
            when('/route2', {
                templateUrl: static_url + 'angularapp/html/test2.html',
                controller: 'RouteController2'
            }).
            otherwise({
                redirectTo: '/'
            });
    }]);

module.controller("RouteController1", function($scope) {
    $scope.test="this working test1"
});
module.controller("RouteController2", function($scope) {
    $scope.test="this working test2"
});
