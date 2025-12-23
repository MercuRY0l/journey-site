const buttons = document.querySelectorAll('.edit-btn');

buttons.forEach(btn => {
  btn.addEventListener('click', () => {
    const id = btn.dataset.target;
    const form = document.getElementById(id);
    
    document.querySelectorAll('.edit-form').forEach(f => {
      if (f !== form) f.classList.remove('active');
    });

    form.classList.toggle('active');
  });
});
