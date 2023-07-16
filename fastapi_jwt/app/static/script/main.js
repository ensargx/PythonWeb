const update_todo = (id) => {
    var todo = document.getElementById(`todo-${id}`);
    var todo_name = todo.querySelector('h1').innerText;
    var todo_description = todo.querySelector('p').innerText;
    var todo_status = todo.querySelector('[name="status"]').value;
    console.log(todo_name, todo_description, todo_status);
}
