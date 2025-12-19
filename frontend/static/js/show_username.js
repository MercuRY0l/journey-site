document.addEventListener("DOMContentLoaded", () => {
    const userGreeting = document.getElementById("userGreeting");
    const loginButton = document.getElementById("auth_btn");

    const username = localStorage.getItem("username");

    if (username) {
        userGreeting.textContent = username;
        loginButton.textContent = "Выйти";

        loginButton.removeAttribute("href"); 
        loginButton.addEventListener("click", (e) => {
            e.preventDefault();

            fetch("/auth/logout", {
                method: "POST",
                credentials: "include"
            })
            .then(response => {
                if (response.ok) {
                    
                    localStorage.removeItem("username");
                    userGreeting.textContent = "";
                    loginButton.textContent = "Войти / зарегистрироваться";
                    loginButton.href = "/auth/login";
                    window.location.href = "/";
                } else {
                    alert("Ошибка при выходе");
                }
            })
            .catch(() => alert("Ошибка соединения с сервером"));
        });
    } else {
        userGreeting.textContent = "";
        loginButton.textContent = "Войти / зарегистрироваться";
        loginButton.href = "/auth/login";
    }
});
