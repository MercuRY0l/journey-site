async function isAuthorized() {
  try {
    const res = await fetch("/auth/me", {
      method: "GET",
      credentials: "include"
    });

    return res.ok;
  } catch {
    return false;
  }
}


document.addEventListener("DOMContentLoaded", () => {
  const overlay = document.getElementById("modalOverlay");
  const openBtns = document.querySelectorAll(".openModalBtn");
  const closeBtn = document.getElementById("closeModal");
  const form = document.getElementById("feedbackForm");

  openBtns.forEach(btn => {
  btn.addEventListener("click", async (e) => {
    const authorized = await isAuthorized();

    if (!authorized) {
      e.preventDefault();
      showToast(
        "Для этого действия необходимо войти или зарегистрироваться",
        "failed"
      );
      return;
    }

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
        showToast("Сообщение отправлено!");
        overlay.classList.remove("active");
        form.reset();
      } else {
        showToast("Сообщение не отправлено!", "failed");
      }
    } catch {
      showToast("Сообщение не отправлено!", "failed");

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
