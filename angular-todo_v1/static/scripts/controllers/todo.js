'use strict';

angular.module('todoListApp')
.controller('todoCtrl', function($scope, Todo, flash, $http, $q) {
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

    // create a new instance of deferred
    var deferred = $q.defer();

    var filteredTodos = $scope.todos.filter(function(todo){
//      if(todo.edited) {
        return todo;
//      }
    });

    var messages = [];


    // flash("TODOs saved successfully!");

    filteredTodos.forEach(function(todo) {
        if (todo.id) {
            todo.$update(
                // success
                function(data){
                    // flash("TODOs saved successfully!");
                    messages.push('u');
                },
                // error
                function (data) {
                    // flash('error', data.data);
                    messages.push(data.data);

                });

        } else {
            todo.$save(
                // success
                function(data){
                    // flash("TODOs saved successfully!");
                },
                // error
                function (data) {
                    // flash('error', data.data);
                }
            );

            messages.push('s')
        }



    });

    deferred.resolve(messages);
    console.log(deferred.promise.$$state)

  };


});