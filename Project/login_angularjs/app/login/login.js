'use strict';

angular.module('loginApp.login', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/login', {
    templateUrl: 'login/login.html',
    controller: 'loginCtrl'

  });

}])

.controller('loginCtrl', [function() {

}]);