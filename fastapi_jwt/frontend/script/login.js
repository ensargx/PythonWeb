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
const check_loggen_in = () => {
    const token = localStorage.getItem('access_token');
    if (token) {
        window.location.href = 'index.html';
    }
};
const login = () => __awaiter(void 0, void 0, void 0, function* () {
    const username = document.getElementById('username');
    const password = document.getElementById('password');
    const response = yield fetch(`${API_URI}/user/login`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ username: username.value, password: password.value })
    });
    const data = yield response.json();
    if (!response.ok) {
        alert(data.detail);
        return;
    }
    localStorage.setItem('access_token', data.access_token);
    localStorage.setItem('token_type', data.token_type);
    window.location.href = 'index.html';
});
window.onload = () => {
    check_loggen_in();
};
