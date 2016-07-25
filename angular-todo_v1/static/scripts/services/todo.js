'use strict';

angular.module('todoListApp')
    .factory('todoService',
        ['$q', '$timeout', '$http', function($q, $timeout, $http) {

        // return available functions for use in controllers
        return ({
          saveTodos: saveTodos
        });
            
        function saveTodos(filteredTodos) {
            // create a new instance of deferred
            var deferred = $q.defer();        
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
                    console.log("here")
                } else {
                    todo.$save(
                        // success
                        function(data){
                            // flash("TODOs saved successfully!");
                            messages.push('s')
                        },
                        // error
                        function (data) {
                            // flash('error', data.data);
                            messages.push(data.data);
                        }
                    );
                }
            });
        
            deferred.resolve(messages);
            return deferred.promise
            
          }
            
    }]);   