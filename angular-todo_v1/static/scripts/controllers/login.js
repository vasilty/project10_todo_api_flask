angular.module('todoListApp')
    .controller('loginController',
      ['$scope', '$location', 'AuthService', 'flash',
      function ($scope, $location, AuthService, flash) {

        $scope.login = function () {

          // initial values
          $scope.error = false;
          $scope.disabled = true;
            
          // call login from service
          AuthService.login($scope.loginForm.username, $scope.loginForm.password)
            // handle success
            .then(function () {
              flash("You have been successfully logged in!");
              $location.path('/');
              $scope.disabled = false;
              $scope.loginForm = {};
            })
            // handle error
            .catch(function () {
              $scope.error = true;
              $scope.errorMessage = "Invalid username and/or password";
              $scope.disabled = false;
              $scope.loginForm = {};
            });

        };

}]);