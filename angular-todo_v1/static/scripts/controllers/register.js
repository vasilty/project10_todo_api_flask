angular.module('todoListApp')
    .controller('registerController',
      ['$scope', '$location', 'AuthService', 'flash', '$timeout',
      function ($scope, $location, AuthService, flash, $timeout) {
    
        $scope.register = function () {
    
          // initial values
          $scope.error = false;
          $scope.disabled = true;
    
          // call register from service
          var register = AuthService.register($scope.registerForm.username,
                               $scope.registerForm.password,
                               $scope.registerForm.verify_password);
            // handle success
            register.then(function () {
              flash("You have been successfully registered!"); 
              $location.path('/login');
              $timeout(function() {flash([])}, 2000);
              $scope.disabled = false;
              $scope.registerForm = {};
            })
            // handle error
            .catch(function (error) {
              $scope.error = true;
              $scope.errorMessage = error;
              $scope.disabled = false;
              $scope.registerForm = {};
            });
    
        };

}]);