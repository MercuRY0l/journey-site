document.addEventListener("DOMContentLoaded", () => {
  const overlay = document.getElementById("modalOverlay");
  const openBtns = document.querySelectorAll(".openModalBtn");
  const closeBtn = document.getElementById("closeModal");
  const form = document.getElementById("feedbackForm");

  openBtns.forEach(btn => {
    btn.addEventListener("click", () => {
      overlay.classList.add("active");
    });
  });

  closeBtn.addEventListener("click", () => {
    overlay.classList.remove("active");
    form.reset();
  });

  overlay.addEventListener("click", (e) => {
    if (e.target === overlay) {
      overlay.classList.remove("active");
      form.reset();
    }
  });

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const formData = new FormData(form);
    const data = Object.fromEntries(formData);

    try {
      const res = await fetch("/feedback", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data)
      });

      if (res.ok) {
        alert("Сообщение отправлено!");
        overlay.classList.remove("active");
        form.reset();
      } else {
        alert("Ошибка отправки");
      }
    } catch {
      alert("Ошибка соединения");
    }
  });
});
