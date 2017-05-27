'use strict';

angular.module('loginApp.login', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/login', {
    templateUrl: 'js/login.html',
    controller: 'loginCtrl'

  });

}])

.controller('loginCtrl', [function() {

}]);
