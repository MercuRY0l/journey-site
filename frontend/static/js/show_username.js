

document.addEventListener("DOMContentLoaded", () => {

const userGreeting = document.getElementById("userGreeting");
const loginButton = document.getElementById("auth_btn");

const username = localStorage.getItem("username")

if (username) {
    userGreeting.textContent = username;
    loginButton.textContent = "Выйти";
    loginButton.href = "/auth/logout";
}
else{
    userGreeting.textContent = "";
    loginButton.textContent = "Войти / зарегистрироваться";
    loginButton.href = "/auth/login"   
}
});
