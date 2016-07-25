'use strict';

var todoListApp = angular.module('todoListApp', ['ngResource', 'ngRoute', 'flash']);

todoListApp.config(['$routeProvider', function ($routeProvider) {
  $routeProvider
    .when('/', {
      templateUrl: 'static/templates/home.html',
      access: {restricted: false}
    })
    .when('/login', {
      templateUrl: 'static/templates/login.html',
      controller: 'loginController',
      access: {restricted: false}
    })
    .when('/logout', {
      controller: 'logoutController',
      access: {restricted: false}
    })
    .when('/register', {
      templateUrl: 'static/templates/register.html',
      controller: 'registerController',
      access: {restricted: false}
    })
    .otherwise({
      redirectTo: '/'
    })
}]);