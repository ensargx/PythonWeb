let getTodos = async () => {
    const response = await fetch('http://127.0.0.1:8000/todo/');
    const todos = await response.json();
    return todos;
    }

const renderTodos = async () => {
    const todos = await getTodos();
    const todoList = document.getElementById('todo_list');

    todos.forEach(todo => {
        const todoElement = document.createElement('li');
        title = document.createElement('h3');
        title.innerHTML = todo.title;
        description = document.createElement('p');
        description.innerHTML = todo.description;
        todoElement.appendChild(title);
        todoElement.appendChild(description);
        todoList.appendChild(todoElement);
    });
}

async function addTodo(event) {
    event.preventDefault();
    const todoForm = document.getElementById('todo_form');
    const title = todoForm.title.value;
    const description = todoForm.description.value;
    const todo = {
        title: title,
        description: description
    }
    const response_todo = await postTodo(todo);
    todoForm.reset();
    renderTodos();
    console.log(response_todo);
}

const postTodo = async (todo) => {
    const response = await fetch('http://127.0.0.1:8000/todo/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(todo)
    });
    const data = await response.json();
    return data;
}

window.onload = () => {
    renderTodos();
    const todoForm = document.getElementById('todo_form');
    todoForm.addEventListener('submit', addTodo);
}