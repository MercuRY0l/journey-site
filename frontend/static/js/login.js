document.addEventListener("DOMContentLoaded", () => {
  const form = document.getElementById("loginForm");

  form.addEventListener("submit", async (event) => {
    event.preventDefault();

    const formData = new FormData(form);
    const data = {
      username: formData.get("username"),
      password: formData.get("password"),
    };

    try {
      const response = await fetch('/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
      });

      if (response.redirected) {
        showToast("Успешный вход!", "success");
        form.reset();
        return;
      }

      const result = await response.json();
      showToast(result.detail || "Ошибка при авторизации!", "error");

    } catch (error) {
      console.error(error);
      showToast("Ошибка соединения с сервером", "error");
    }
  });
});
