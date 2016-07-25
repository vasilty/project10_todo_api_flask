'use strict';

angular.module('todoListApp')
    .factory('AuthService',
        ['$q', '$timeout', '$http', function($q, $timeout, $http) {

    // create user variable
    var user = null;

    // return available functions for use in controllers
    return ({
      isLoggedIn: isLoggedIn,
      login: login,
      logout: logout,
      register: register,
      getToken: getToken
    });

    function isLoggedIn() {
      if(user) {
        return true;
      } else {
        return false;
      }
    }
      
    function login(username, password) {

      // create a new instance of deferred
      var deferred = $q.defer();

      // send a get request to the server to get a token
      $http.defaults.headers.common['Authorization'] = 'Basic ' +
          window.btoa(username + ':' + password);
      $http.get('/api/v1/users/token')
        // handle success
        .success( function (data, status) {
          if(status === 200 && data.token) {
            console.log(data.token);
            // Define a new http header
            $http.defaults.headers.common['Authorization'] = 'Token ' + data.token;
            window.localStorage['jwtToken'] = data.token;
            user = true;
            deferred.resolve();
          } else {
            user = false;
            deferred.reject();
          }
        })
        // handle error
        .error(function (data) {
          user = false;
          deferred.reject();
        });

      // return promise object
       return deferred.promise;

    }

    function logout() {

        // create a new instance of deferred
        var deferred = $q.defer();

        // Delete authorization http header
        delete $http.defaults.headers.common['Authorization'];
        window.localStorage.removeItem('jwtToken');

        user = false;
        deferred.resolve();

        // return promise object
        return deferred.promise;

    }

    function register(username, password, verify_password) {

      // create a new instance of deferred
      var deferred = $q.defer();

      // send a post request to the server
      $http.post('/api/v1/users',
          {username: username, password: password, verify_password: verify_password})
        // handle success
        .success(function (data, status) {
          if(status === 201 && data.username){
            deferred.resolve();
          } else {
            deferred.reject();
          }
        })
        // handle error
        .error(function (data) {
            deferred.reject(data.error);
        });

      // return promise object
      return deferred.promise;

    }

    function getToken() {
        return window.localStorage['jwtToken'];
    }


  }]);
