window.addEventListener("DOMContentLoaded", async () => {
    const userGreeting = document.getElementById("userGreeting");
    const loginButton = document.getElementById("auth_btn");
    const userWrapper = document.querySelector(".user-menu-wrapper");

    async function loadUser() {
        try {
            const res = await fetch("/auth/me", { credentials: "include" });
            if (!res.ok) throw new Error("Пользователь не авторизован");
            const user = await res.json();

            
            userGreeting.textContent = user.username;
            userWrapper.style.display = "inline-flex";
            loginButton.style.display = "none";
        } catch (err) {
            
            userWrapper.style.display = "none";
            loginButton.style.display = "inline-block";
        }
    }

    await loadUser();

    const logoutLink = document.getElementById("logoutLink");
    if (logoutLink) {
        logoutLink.addEventListener("click", async (e) => {
            e.preventDefault();
            try {
                const res = await fetch("/auth/logout", { method: "POST", credentials: "include" });
                if (res.ok) {
                    
                    userWrapper.style.display = "none";
                    loginButton.style.display = "inline-block";
                    window.location.href = "/";
                } else {
                    showToast("Ошибка при выходе", "failed");
                }
            } catch {
                showToast("Ошибка соединения", "failed");
            }
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
