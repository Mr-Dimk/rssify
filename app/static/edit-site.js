// edit-site.js — логика редактирования сайта через модальное окно и AJAX

document.addEventListener('DOMContentLoaded', function () {
  // Открытие модального окна и заполнение формы
  document.querySelectorAll('.edit-site-btn').forEach(function (btn) {
    btn.addEventListener('click', function (e) {
      e.preventDefault();
      const siteId = btn.getAttribute('data-site-id');
      const row = document.getElementById('site-row-' + siteId);
      if (!row) return;
      const site = JSON.parse(row.getAttribute('data-site'));
      // Заполнить форму
      document.getElementById('edit-site-id').value = site.id;
      document.getElementById('edit-site-name').value = site.name || '';
      document.getElementById('edit-site-url').value = site.url || '';
      document.getElementById('edit-site-selector').value = site.selector || '';
      document.getElementById('edit-site-title_selector').value =
        site.title_selector || '';
      document.getElementById('edit-site-desc_selector').value =
        site.desc_selector || '';
      document.getElementById('edit-site-link_selector').value =
        site.link_selector || '';
      document.getElementById('edit-site-description').value =
        site.description || '';
      document.getElementById('edit-site-is_active').checked = !!site.is_active;
      document.getElementById('edit-site-check_interval').value =
        site.check_interval || 10;
      document.getElementById('editSiteError').style.display = 'none';
      document.getElementById('editSiteModal').style.display = 'flex';
    });
  });
  // Закрытие модального окна
  document.getElementById('closeEditModal').onclick = function () {
    document.getElementById('editSiteModal').style.display = 'none';
  };
  // Сохранение изменений через AJAX
  document.getElementById('editSiteForm').onsubmit = function (e) {
    e.preventDefault();
    const siteId = document.getElementById('edit-site-id').value;
    const data = {
      name: document.getElementById('edit-site-name').value,
      url: document.getElementById('edit-site-url').value,
      selector: document.getElementById('edit-site-selector').value,
      title_selector: document.getElementById('edit-site-title_selector').value,
      desc_selector: document.getElementById('edit-site-desc_selector').value,
      link_selector: document.getElementById('edit-site-link_selector').value,
      description: document.getElementById('edit-site-description').value,
      is_active: document.getElementById('edit-site-is_active').checked,
      check_interval: parseInt(
        document.getElementById('edit-site-check_interval').value,
        10
      ),
    };
    fetch('/api/sites/' + siteId, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        Accept: 'application/json',
      },
      body: JSON.stringify(data),
    })
      .then((response) => {
        if (!response.ok)
          return response.json().then((data) => {
            throw new Error(data.detail || 'Ошибка обновления');
          });
        return response.json();
      })
      .then((site) => {
        // Обновить строку таблицы
        const row = document.getElementById('site-row-' + site.id);
        if (row) {
          row.setAttribute('data-site', JSON.stringify(site));
          row.children[1].textContent = site.name;
          row.children[2].querySelector('a').textContent = site.url;
          row.children[2].querySelector('a').href = site.url;
          row.children[3].textContent = site.description || '';
          row.children[4].textContent = site.is_active ? 'Да' : 'Нет';
          row.children[5].textContent = site.posts ? site.posts.length : '0';
          row.children[6].textContent = site.last_check
            ? new Date(site.last_check).toLocaleString('ru-RU').slice(0, 16)
            : '-';
          row.children[7].innerHTML = site.last_error
            ? '<span style="color:red;" title="' +
              site.last_error +
              '">Ошибка</span>'
            : '-';
        }
        document.getElementById('editSiteModal').style.display = 'none';
      })
      .catch((err) => {
        const errDiv = document.getElementById('editSiteError');
        errDiv.textContent = err.message;
        errDiv.style.display = 'block';
      });
  };
  // Клик вне модального окна — закрыть
  document
    .getElementById('editSiteModal')
    .addEventListener('click', function (e) {
      if (e.target === this) this.style.display = 'none';
    });
});
