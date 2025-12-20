document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("registerForm");

  form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const formData = new FormData(form);
    const data = {
      username: formData.get("username"),
      email: formData.get("email"),
      password: formData.get("password"),
      password_repeat: formData.get("password_repeat")
    };

    if (data.password !== data.password_repeat) {
      showToast("Пароли не совпадают!", "error");
      form.reset();
      return;
    }

    try {
      const response = await fetch('/auth/register', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });

      const result = await response.json();

      if (result.success && result.username) {
        localStorage.setItem("username", result.username);
        showToast("Регистрация прошла успешно!", "success");
        form.reset();
        setTimeout(() => window.location.href = "/", 1500);
      } else {
        showToast(result.detail || "Ошибка при регистрации!", "error");
      }

    } catch (error) {
      console.error(error);
      showToast("Ошибка соединения с сервером", "error");
    }
  });
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
