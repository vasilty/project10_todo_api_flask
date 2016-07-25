angular.module('todoListApp')
    .controller('registerController',
      ['$scope', '$location', 'AuthService', 'flash',
      function ($scope, $location, AuthService, flash) {
    
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