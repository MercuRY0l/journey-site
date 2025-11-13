fetch('/auth/login', {
  method: 'POST',
  body: new FormData(form)
}).then(res => {
  if (res.ok) {
    window.location.href = '/';
  }
});