'use strict';

angular.module('todoListApp')
.controller('todoCtrl', function($scope, Todo, flash, $http, $timeout) {
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
            function(response) {
                flash("TODO successfully deleted.");
                $timeout(function() {flash([])}, 2000);
                $scope.todos.splice(index, 1);
            // error
            }, function (error) {
                if(error.status === 401) {
                    var errorMessage = error.data;
                } else {
                    var errorMessage = error.data.message;
                }
                flash('error', errorMessage);
                $timeout(function() {flash([])}, 2000);
            }
        );
    };


    $scope.saveTodos = function() {
        $scope.setToken();

        var filteredTodos = $scope.todos.filter(function(todo){
            if(todo.edited) {
                return todo;
            }
        });

        var errorMessage = '';

        filteredTodos.forEach(function(todo) {
            if (todo.id) {
                todo.$update(
                    // success
                    function(response){
                    },
                    // error
                    function (error) {
                        if(error.status === 401) {
                            errorMessage = error.data;
                        } else {
                            errorMessage = error.data.message;
                        }
                        flash('error', errorMessage);
                        $timeout(function() {flash([])}, 2000);
                    });

            } else {
                todo.$save(
                    // success
                    function(response){
                    },
                    // error
                    function (error) {
                        if(error.status === 401) {
                            errorMessage = error.data;
                        } else {
                            errorMessage = error.data.message;
                        }
                        flash('error', errorMessage);
                        $timeout(function() {flash([])}, 2000);
                    }
                );
            }
        });

    };

});