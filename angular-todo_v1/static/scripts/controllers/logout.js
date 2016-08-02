angular.module('todoListApp').controller('logoutController',
  ['$scope', '$location', 'AuthService', 'flash', '$timeout',
  function ($scope, $location, AuthService, flash, $timeout) {

    $scope.logout = function () {

      // call logout from service
      AuthService.logout()
        .then(function () {
          flash("You have been successfully logged out!");
          $location.path('/');
          $timeout(function() {flash([])}, 2000);
        });

    };

}]);