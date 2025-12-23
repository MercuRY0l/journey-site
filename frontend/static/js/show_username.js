document.addEventListener("DOMContentLoaded", () => {
    const userGreeting = document.getElementById("userGreeting");
    const loginButton = document.getElementById("auth_btn");
    const userWrapper = document.querySelector(".user-menu-wrapper");

    const username = localStorage.getItem("username");

    if (username) {
        userGreeting.textContent = username;
        userWrapper.style.display = "inline-flex";
        loginButton.style.display = "none";       

    } else {
        
        userWrapper.style.display = "none";        
        loginButton.style.display = "inline-block"; 
    }

    const logoutLink = document.getElementById("logoutLink");
    if (logoutLink) {
        logoutLink.addEventListener("click", (e) => {
            e.preventDefault();
            fetch("/auth/logout", { method: "POST", credentials: "include" })
                .then(res => {
                    if (res.ok) {
                        localStorage.removeItem("username");
                        userWrapper.style.display = "none";       
                        loginButton.style.display = "inline-block"; 
                        window.location.href = "/";
                    } else {
                        alert("Ошибка при выходе");
                    }
                })
                .catch(() => alert("Ошибка соединения"));
        });
    }
});

function showToast(message, type="success") {
  const toast = document.createElement("div");
  Object.assign(toast.style, {
    position: "fixed",
    top: "20px",
    right: "20px",
    padding: "12px 18px",
    backgroundColor: type === "success" ? "rgba(40, 167, 69, 0.9)" : "rgba(220, 53, 69, 0.9)",
    color: "#fff",
    fontSize: "14px",
    borderRadius: "4px",
    boxShadow: "0 2px 8px rgba(0,0,0,0.2)",
    opacity: "0",
    transition: "opacity 0.4s ease",
    zIndex: "9999"
  });
  toast.textContent = message;
  document.body.appendChild(toast);
  setTimeout(() => toast.style.opacity = "1", 50);
  setTimeout(() => {
    toast.style.opacity = "0";
    toast.addEventListener("transitionend", () => toast.remove());
  }, 3000);
}
