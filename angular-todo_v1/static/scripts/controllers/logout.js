angular.module('todoListApp').controller('logoutController',
  ['$scope', '$location', 'AuthService', 'flash',
  function ($scope, $location, AuthService, flash) {

    $scope.logout = function () {

      // call logout from service
      AuthService.logout()
        .then(function () {
          flash("You have been successfully logged out!");
          $location.path('/');
        });

    };

}]);