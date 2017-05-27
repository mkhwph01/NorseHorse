'use strict';

angular.module('loginApp.version', [
  'loginApp.version.interpolate-filter',
  'loginApp.version.version-directive'
])

.value('version', '0.1');
