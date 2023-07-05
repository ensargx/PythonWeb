"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
// create function to fetch todos from backend and return as json
const getTodos = () => __awaiter(void 0, void 0, void 0, function* () {
    const response = yield fetch("http://localhost:8000/todo/");
    const todos = yield response.json();
    return todos;
});
// create function to render todos to page using todo-list id, add title, description, delete button to each todo
const renderTodos = () => __awaiter(void 0, void 0, void 0, function* () {
    const todos = yield getTodos();
    const todosDiv = document.getElementById("todo_list");
    if (!todosDiv)
        return;
    todosDiv.innerHTML = "";
    todos.forEach((todo) => {
        const todoDiv = document.createElement("div");
        todoDiv.id = `todo_${todo.id}`;
        todoDiv.className = "todo";
        todoDiv.innerHTML = `
            <h3>${todo.title}</h3>
            <p>${todo.description}</p>
            <button class="delete" onclick="deleteTodo(${todo.id}); return false;">Delete</button>
        `;
        todosDiv.appendChild(todoDiv);
    });
});
// create function to delete todo by its id make the button work
const deleteTodo = (id) => __awaiter(void 0, void 0, void 0, function* () {
    console.log(id);
    const response = yield fetch(`http://localhost:8000/todo/${id}`, {
        method: "DELETE",
    });
    const data = yield response.json();
    console.log(data);
    if (data.status !== "success") {
        alert("Failed to delete todo.\nDetail: " + data.detail);
        return;
    }
    // delete todo with id from page
    const todoList = document.getElementById("todo_list");
    // select todo_id div from todo_list
    const todo = todoList.querySelector(`#todo_${id}`);
    todo.remove();
    return data;
});
// create function to add new todo to backend
const addTodo = () => __awaiter(void 0, void 0, void 0, function* () {
    // get title and description from input fields
    const form = document.getElementById("todo_form");
    const title = form.todo_title.value;
    const description = form.todo_description.value;
    // clear input fields
    form.todo_title.value = "";
    form.todo_description.value = "";
    // send title and description to backend
    const response = yield fetch("http://localhost:8000/todo/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ title, description }),
    });
    const data = yield response.json();
    // if response_status_code is 400, alert user that todo was not added
    if (response.status === 400) {
        alert("Failed to add todo.\nDetail: " + data.detail);
        console.log(data);
        return;
    }
    console.log(data);
    // get todo deails from response
    const todo = data;
    // add todo to page
    const todosDiv = document.getElementById("todo_list");
    if (!todosDiv)
        return;
    const todoDiv = document.createElement("div");
    todoDiv.id = `todo_${todo.id}`;
    todoDiv.className = "todo";
    todoDiv.innerHTML = `
        <h3>${todo.title}</h3>
        <p>${todo.description}</p>
        <button class="delete" onclick="deleteTodo(${todo.id}); return false;">Delete</button>
    `;
    todosDiv.appendChild(todoDiv);
});
window.onload = () => {
    console.log("loaded");
    renderTodos();
};
