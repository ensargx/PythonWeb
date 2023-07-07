
// create new Todo type
type Todo = {
    id: number;
    title: string;
    description: string;
    completed: boolean;
    owner_id: number;
};

// create function to fetch todos from backend and return as json
const getTodos = async () => {
    // if token is not present, alert user that they are not logged in
    if(!check_token()) {
        return;
    }
    const response = await fetch("http://localhost:8000/todo/", {
        headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
        },
    });
    const todos = await response.json();
    return todos;
};

// create function to render todos to page using todo-list id, add title, description, delete button to each todo
const renderTodos = async () => {
    const todos = await getTodos();
    const todosDiv = document.getElementById("todo_list");
    if (!todosDiv) return;
    todosDiv.innerHTML = "";
    todos.forEach((todo: Todo) => {
        const todoDiv = document.createElement("div");
        todoDiv.id = `todo_${todo.id}`;
        todoDiv.className = "todo";
        
        if(todo.completed) {
            var completed = "checked";
        } else {
            var completed = "";
        }

        todoDiv.innerHTML = `
            <h3>${todo.title}</h3>
            <p>${todo.description}</p>
            <input type="checkbox" onclick="completeTodo(${todo.id}); return false;" ${completed}>Completed</checkbox>
            <button class="delete" onclick="deleteTodo(${todo.id}); return false;">Delete</button>
        `;
        todosDiv.appendChild(todoDiv);
    }
    );
};

// create function to delete todo by its id make the button work
const deleteTodo = async (id: number) => {
    const response = await fetch(`http://localhost:8000/todo/${id}`, {
        method: "DELETE",
        headers: {
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
        },
    });
    const data = await response.json();
    console.log(data);
    if(data.status !== "success") {
        alert("Failed to delete todo.\nDetail: " + data.detail);
        return;
    }
    // delete todo with id from page
    const todoList = document.getElementById("todo_list") as HTMLDivElement;
    // select todo_id div from todo_list
    const todo = todoList.querySelector(`#todo_${id}`) as HTMLDivElement;
    todo.remove();
    return data;
}

// create function to add new todo to backend
const addTodo = async () => {
    // get title and description from input fields
    const form = document.getElementById("todo_form") as HTMLFormElement;
    const title = form.todo_title.value;
    const description = form.todo_description.value;

    // clear input fields
    form.todo_title.value = "";
    form.todo_description.value = "";

    // send title and description to backend
    const response = await fetch("http://localhost:8000/todo/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
        },
        body: JSON.stringify({ title, description, owner_id: 1 }),
    });
    const data = await response.json();

    // if response_status_code is 400, alert user that todo was not added
    if(!response.ok) {
        alert("Failed to add todo.\nDetail: " + data.detail);
        console.log(data);
        return;
    }

    // get todo deails from response
    const todo = data as Todo;

    // add todo to page
    const todosDiv = document.getElementById("todo_list");
    if (!todosDiv) return;
    const todoDiv = document.createElement("div");
    todoDiv.id = `todo_${todo.id}`;
    todoDiv.className = "todo";
    todoDiv.innerHTML = `
        <h3>${todo.title}</h3>
        <p>${todo.description}</p>
        <input type="checkbox" onclick="completeTodo(${todo.id}); return false;" ${todo.completed}>Completed</checkbox>
        <button class="delete" onclick="deleteTodo(${todo.id}); return false;">Delete</button>
    `;
    todosDiv.appendChild(todoDiv);

};

// create function to complete todo by its id
const completeTodo = async (id: number) => {
    // check if todo is completed
    const todo = document.getElementById(`todo_${id}`) as HTMLDivElement;
    const checkbox = todo.querySelector("input[type=checkbox]") as HTMLInputElement;
    const completed = checkbox.checked;

    // lock the checkbox
    checkbox.disabled = true;

    // update todo
    const response = await updateTodo(id, { completed });
    
    if(!response) {
        alert("Failed to update todo.");
        checkbox.disabled = false;
        checkbox.checked = !completed;
        return;
    }

    checkbox.checked = completed;
    checkbox.disabled = false;
};

const updateTodo = async (id: number, values: Todo | any) => {
    const response = await fetch(`http://localhost:8000/todo/${id}`, {
        method: "PUT",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem("access_token")}`,
        },
        body: JSON.stringify(values),
    });
    const data = await response.json();
    if(!response.ok) {
        console.log(data);
        return 0;
    }
    return 1;
};

const check_token = async () => {
    // get token from local storage
    const token = localStorage.getItem("access_token");
    if(!token) {
        return false
    }
    return true;
}

type UserToken = {
    access_token: string;
    token_type: string;
};

const login = async () => {
    // get username and password from input fields
    const form = document.getElementById("login_form") as HTMLFormElement;
    const username = form.username.value;
    const password = form.password.value;

    // clear input fields
    form.username.value = "";
    form.password.value = "";

    // send username and password to backend
    const response = await fetch("http://localhost:8000/user/login", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
        },
        body: JSON.stringify({ username, password }),
    });
    const data = await response.json();

    // if response_status_code is 400, alert user that todo was not added
    if(!response.ok) {
        alert("Failed to login.\nDetail: " + data.detail);
        console.log(data);
        return;
    }

    // get token from response
    const token = data as UserToken;

    // save token to local storage
    localStorage.setItem("access_token", token.access_token);
    localStorage.setItem("token_type", token.token_type);

    // delete login form
    const loginForm = document.getElementById("login_form") as HTMLFormElement;
    loginForm.remove();

    // fetch todos from backend
    const todos = await renderTodos();
    

    // create logout button
    const logoutButton = document.createElement("button");
    logoutButton.id = "logout_button";
    logoutButton.innerHTML = "Logout";
    logoutButton.onclick = logout;
    document.body.appendChild(logoutButton);

}

const create_login_form = () => {
    // if exists, delete logout button
    const logoutButton = document.getElementById("logout_button");
    if(logoutButton) logoutButton.remove();
    
    // create login form into div with id "login_form"
    const loginForm = document.createElement("form");
    loginForm.id = "login_form";
    loginForm.innerHTML = `
        <label for="username">Username</label>
        <input type="text" name="username" id="username" required>
        <label for="password">Password</label>
        <input type="password" name="password" id="password" required> 
        <button type="submit">Login</button>
    `;
    loginForm.onsubmit = (e) => {
        e.preventDefault();
        login();
    };
    document.body.appendChild(loginForm);
}


const logout = async () => {
    // delete token from local storage
    localStorage.removeItem("access_token");
    localStorage.removeItem("token_type");

    // delete logout button
    const logoutButton = document.getElementById("logout_button");
    if(!logoutButton) return;
    logoutButton.remove();
    create_login_form();

    // remove todos from page
    const todosDiv = document.getElementById("todo_list");
    if(!todosDiv) return;
    todosDiv.innerHTML = "";
}

const create_logout_button = () => {
    // if exists, delete login form
    const loginForm = document.getElementById("login_form");
    if(loginForm) loginForm.remove();

    // create logout button
    const logoutButton = document.createElement("button");
    logoutButton.id = "logout_button";
    logoutButton.innerHTML = "Logout";
    logoutButton.onclick = logout;
    document.body.appendChild(logoutButton);
}

window.onload = () => {
    console.log("loaded");
    renderTodos();
    // check if token exists
    const token = localStorage.getItem("access_token");
    if(!token) {
        console.log("no token");
        create_login_form();
    }
    else {
        console.log("token exists");
        create_logout_button();
    }
}