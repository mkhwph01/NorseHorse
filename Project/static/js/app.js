var app = angular.module('app', ['ngMessages']);
angular.module('getLostApp', ['ngMaterial']).
controller('MainCtrl', function($rootScope, $scope, $mdToast, $animate, $http, $timeout, $q, $log) {
  'use strict';
  // Initialize the scope variables
  $scope.info = {
    origin: {},
    maxfare: {},
    returndate: new Date(),
    departuredate: new Date()
  };

  
  // Helper function to format the date
  function formatDate(date) {
    var d = new Date(date),
      month = '' + (d.getMonth() + 1),
      day = '' + d.getDate(),
      year = d.getFullYear();

    if (month.length < 2) {
      month = '0' + month;
    }
    if (day.length < 2) {
      day = '0' + day;
    }

    return [year, month, day].join('-');
  }

  // Helper functions to show the toast message on success or error
  (function toastHelper() {
    $scope.toastPosition = {
      bottom: false,
      top: true,
      left: false,
      right: true,
      fit: true
    };

    $scope.getToastPosition = function() {
      return Object.keys($scope.toastPosition)
        .filter(function(pos) {
          return $scope.toastPosition[pos];
        })
        .join(' ');
    };

    $scope.showSimpleToast = function(msg) {
      $mdToast.show(
        $mdToast.simple()
        .content(msg)
        .position($scope.getToastPosition())
        .hideDelay(3000)
      );
    };
  })();

});