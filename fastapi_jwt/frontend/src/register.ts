

const register = async () => {
    const name = document.getElementById('name') as HTMLInputElement;
    const username = document.getElementById('username') as HTMLInputElement;
    const password = document.getElementById('password') as HTMLInputElement;

    const response = await fetch(`${API_URI}/user/register`, {
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