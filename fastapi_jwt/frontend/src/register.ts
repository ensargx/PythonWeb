

const register = async () => {
    const name = document.getElementById('name') as HTMLInputElement;
    const username = document.getElementById('username') as HTMLInputElement;
    const password = document.getElementById('password') as HTMLInputElement;

    const response = await fetch('http://127.0.0.1:8000/user/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name: name.value, username: username.value, password: password.value })
    });

    const data = await response.json();

    if (!response.ok) {
        alert(data.detail);
        return;
    }

    window.location.href = 'login.html';
}


window.onload = () => {
    check_loggen_in();
}