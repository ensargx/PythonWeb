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
const register = () => __awaiter(void 0, void 0, void 0, function* () {
    const name = document.getElementById('name');
    const username = document.getElementById('username');
    const password = document.getElementById('password');
    const response = yield fetch('http://127.0.0.1:8000/user/register', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ name: name.value, username: username.value, password: password.value })
    });
    const data = yield response.json();
    if (!response.ok) {
        alert(data.detail);
        return;
    }
    window.location.href = 'login.html';
});
window.onload = () => {
    check_loggen_in();
};
