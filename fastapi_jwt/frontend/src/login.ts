
const check_loggen_in = () => {
    const token = localStorage.getItem('access_token');
    if (token) {
        window.location.href = 'index.html';
    }
}

const login = async () => {
    const username = document.getElementById('username') as HTMLInputElement;
    const password = document.getElementById('password') as HTMLInputElement;

    const response = await fetch('http://localhost:8000/user/login', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username: username.value, password: password.value })
    });

    const data = await response.json();

    if (!response.ok) {
        alert(data.detail);
        return;
    }

    localStorage.setItem('access_token', data.access_token);
    localStorage.setItem('token_type', data.token_type);
    window.location.href = 'index.html';
}

window.onload = () => {
    check_loggen_in();
}