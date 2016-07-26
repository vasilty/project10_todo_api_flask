'use strict';

angular.module('todoListApp')
.controller('todoCtrl', function($scope, Todo, flash, $http) {
  $scope.setToken = function () {
    var token = window.localStorage['jwtToken'];
    if(token) {
        $http.defaults.headers.common['Authorization'] = 'Token ' + token;
    }
  };

  $scope.deleteTodo = function(todo, index) {
    $scope.setToken();
    todo.$delete(
        // success
        function(data) {
          flash("TODO successfully deleted.");
          $scope.todos.splice(index, 1);
        // error    
        }, function (data) {
          flash('error', data.data);
        });
  };


  $scope.saveTodos = function() {
    $scope.setToken();

    var filteredTodos = $scope.todos.filter(function(todo){
//      if(todo.edited) {
        return todo;
//      }
    });

    flash("TODOs saved successfully!");

    filteredTodos.forEach(function(todo) {
        if (todo.id) {
            todo.$update(
                // success
                function(data){
                    // flash("TODOs saved successfully!");
                },
                // error
                function (data) {
                    flash('error', data.data);
                });

        } else {
            todo.$save(
                // success
                function(data){
                    // flash("TODOs saved successfully!");
                },
                // error
                function (data) {
                    flash('error', data.data);
                }
            );
        }
    });

  };

});