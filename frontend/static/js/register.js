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
      return;
    }

    try {
      const response = await fetch("/auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
      });

      const result = await response.json();

      if (!response.ok) {
        handleErrors(result);
        return;
      }

      if (result.success) {
        localStorage.setItem("username", result.username);
        localStorage.setItem("email", result.email);

        showToast("Регистрация прошла успешно!", "success");
        form.reset();

        setTimeout(() => {
          window.location.href = "/";
        }, 1500);
      }

    } catch (error) {
      console.error(error);
      showToast("Ошибка соединения с сервером", "error");
    }
  });
});

function handleErrors(result) {
  if (!result || !result.detail) {
    showToast("Ошибка при регистрации", "error");
    return;
  }


  if (typeof result.detail === "string") {
    showToast(result.detail, "error");
    return;
  }


  if (Array.isArray(result.detail)) {
    result.detail.forEach(err => {
      if (err.msg) {
        showToast(err.msg, "error");
      } else if (err.loc) {
        showToast(`${err.loc.join(".")}: ${err.msg}`, "error");
      } else {
        showToast(JSON.stringify(err), "error");
      }
    });
    return;
  }

 
  if (typeof result.detail === "object") {
    Object.entries(result.detail).forEach(([field, msg]) => {
      showToast(`${field}: ${msg}`, "error");
    });
    return;
  }


  showToast(JSON.stringify(result.detail), "error");
}

  
function showToast(message, type = "success") {
  const toast = document.createElement("div");

  Object.assign(toast.style, {
    position: "fixed",
    top: "20px",
    right: "20px",
    padding: "12px 18px",
    backgroundColor:
      type === "success"
        ? "rgba(40, 167, 69, 0.9)"
        : "rgba(220, 53, 69, 0.9)",
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

  setTimeout(() => (toast.style.opacity = "1"), 50);

  setTimeout(() => {
    toast.style.opacity = "0";
    toast.addEventListener("transitionend", () => toast.remove());
  }, 3000);
}
