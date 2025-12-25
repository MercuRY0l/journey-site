window.addEventListener("DOMContentLoaded", async () => {
  async function loadUserData() {
    try {
      const res = await fetch("/auth/me", { credentials: "include" });
      if (!res.ok) throw new Error("Не удалось загрузить данные пользователя");
      const user = await res.json();
      const valueSpans = document.querySelectorAll(".setting-card .value");
      if (valueSpans[0]) valueSpans[0].textContent = user.username;
      if (valueSpans[1]) valueSpans[1].textContent = user.email;
    } catch (err) {
      console.error(err);
      showToast("Ошибка загрузки данных пользователя", "failed");
    }
  }

  await loadUserData();

  document.querySelectorAll(".edit-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      const targetForm = document.getElementById(btn.dataset.target);
      document.querySelectorAll(".edit-form").forEach(f => {
        if (f !== targetForm) f.style.display = "none";
      });
      targetForm.style.display = targetForm.style.display === "block" ? "none" : "block";
    });
  });

  const usernameForm = document.getElementById("username");
  usernameForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const input = usernameForm.querySelector("input");
    const newUsername = input.value.trim();
    if (!newUsername) return showToast("Введите логин", "failed");

    try {
      const res = await fetch("/user/settings/username", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ new_username: newUsername }),
        credentials: "include"
      });
      const result = await res.json();
      if (res.ok) {
        await loadUserData();
        showToast("Логин обновлён", "success");
        usernameForm.style.display = "none";
        input.value = "";
      } else {
        handleErrors(result);
      }
    } catch (err) {
      showToast("Ошибка сети", "failed");
      console.error(err);
    }
  });

  const emailForm = document.getElementById("email");
  emailForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const input = emailForm.querySelector("input");
    const newEmail = input.value.trim();
    if (!newEmail) return showToast("Введите email", "failed");

    try {
      const res = await fetch("/user/settings/email", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ new_email: newEmail }),
        credentials: "include"
      });
      const result = await res.json();
      if (res.ok) {
        await loadUserData();
        showToast("Письмо подтверждения отправлено", "success");
        emailForm.style.display = "none";
        input.value = "";
      } else {
        handleErrors(result);
      }
    } catch (err) {
      showToast("Ошибка сети", "failed");
      console.error(err);
    }
  });

  const passwordForm = document.getElementById("password");
  passwordForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const inputs = passwordForm.querySelectorAll("input");
    const oldPassword = inputs[0].value.trim();
    const newPassword = inputs[1].value.trim();
    const repeatPassword = inputs[2].value.trim();
    if (!oldPassword || !newPassword || !repeatPassword)
      return showToast("Заполните все поля", "failed");
    if (newPassword !== repeatPassword)
      return showToast("Пароли не совпадают", "failed");

    try {
      const res = await fetch("/user/settings/password", {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ old_password: oldPassword, new_password: newPassword }),
        credentials: "include"
      });
      const result = await res.json();
      if (res.ok) {
        showToast("Пароль обновлён", "success");
        passwordForm.reset();
        passwordForm.style.display = "none";
      } else {
        handleErrors(result);
      }
    } catch (err) {
      showToast("Ошибка сети", "failed");
      console.error(err);
    }
  });
});

function handleErrors(result) {
  if (!result || !result.detail) {
    showToast("Ошибка при обновлении", "failed");
    return;
  }
  if (typeof result.detail === "string") {
    showToast(result.detail, "failed");
    return;
  }
  if (Array.isArray(result.detail)) {
    result.detail.forEach(err => {
      if (err.msg) showToast(err.msg, "failed");
      else if (err.loc) showToast(`${err.loc.join(".")}: ${err.msg}`, "failed");
      else showToast(JSON.stringify(err), "failed");
    });
    return;
  }
  if (typeof result.detail === "object") {
    Object.entries(result.detail).forEach(([field, msg]) => showToast(`${field}: ${msg}`, "failed"));
    return;
  }
  showToast(JSON.stringify(result.detail), "failed");
}

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
