// delete-site.js — удаление сайта через AJAX

document.addEventListener('DOMContentLoaded', function () {
  document.querySelectorAll('.delete-site-btn').forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      const siteId = btn.getAttribute('data-site-id');
      if (!siteId) return;
      if (!confirm('Удалить сайт #' + siteId + '?')) return;
      btn.disabled = true;
      fetch('/api/sites/' + siteId, {
        method: 'DELETE',
        headers: {
          Accept: 'application/json',
        },
      })
        .then((response) => {
          if (response.status === 204) {
            // Удалить строку из таблицы
            const row = document.getElementById('site-row-' + siteId);
            if (row) row.remove();
          } else {
            return response.json().then((data) => {
              throw new Error(data.detail || 'Ошибка удаления');
            });
          }
        })
        .catch((err) => {
          alert('Ошибка: ' + err.message);
          btn.disabled = false;
        });
    });
  });
});
