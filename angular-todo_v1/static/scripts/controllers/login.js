angular.module('todoListApp')
    .controller('loginController',
      ['$scope', '$location', 'AuthService', 'flash', '$timeout',
      function ($scope, $location, AuthService, flash, $timeout) {

        $scope.login = function () {

          // initial values
          $scope.error = false;
            
          // call login from service
          AuthService.login($scope.loginForm.username, $scope.loginForm.password)
            // handle success
            .then(function () {
              flash("You have been successfully logged in!");
              $timeout(function() {flash([])}, 2000);
              $location.path('/');
              $scope.loginForm = {};
            })
            // handle error
            .catch(function () {
              $scope.error = true;
              $scope.errorMessage = "Invalid username and/or password";
              $scope.loginForm = {};
            });

        };

}]);