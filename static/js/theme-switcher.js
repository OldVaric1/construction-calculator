document.addEventListener('DOMContentLoaded', function() {
  const themeSwitch = document.getElementById('theme-switch');
  const currentTheme = localStorage.getItem('theme');

  // Применяем сохранённую тему при загрузке
  if (currentTheme) {
    document.documentElement.classList.toggle('dark-theme', currentTheme === 'dark');
    themeSwitch.checked = currentTheme === 'dark';
  }

  // Обработчик переключения темы
  themeSwitch.addEventListener('change', function() {
    if (this.checked) {
      document.documentElement.classList.add('dark-theme');
      localStorage.setItem('theme', 'dark');
    } else {
      document.documentElement.classList.remove('dark-theme');
      localStorage.setItem('theme', 'light');
    }
  });

  // Автоматическое определение системной темы (если пользователь не выбирал тему)
  if (!currentTheme && window.matchMedia) {
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)');
    if (prefersDark.matches) {
      document.documentElement.classList.add('dark-theme');
      themeSwitch.checked = true;
      localStorage.setItem('theme', 'dark');
    }

    // Отслеживаем изменение системных настроек
    prefersDark.addEventListener('change', (e) => {
      if (!localStorage.getItem('theme')) {
        document.documentElement.classList.toggle('dark-theme', e.matches);
        themeSwitch.checked = e.matches;
      }
    });
  }
});

document.addEventListener('DOMContentLoaded', function() {
    const dropdowns = document.querySelectorAll('.dropdown');

    dropdowns.forEach(dropdown => {
        const menu = dropdown.querySelector('.dropdown-menu');

        dropdown.addEventListener('mouseenter', () => {
            if (menu) menu.classList.add('show');
        });

        dropdown.addEventListener('mouseleave', () => {
            if (menu) menu.classList.remove('show');
        });
    });
});

document.addEventListener('DOMContentLoaded', function() {
  const dropdowns = document.querySelectorAll('.dropdown');

  dropdowns.forEach(dropdown => {
    const menu = dropdown.querySelector('.dropdown-menu');

    // Показываем меню при наведении на родительский блок
    dropdown.addEventListener('mouseenter', () => {
      if (menu) {
        menu.classList.add('show');
      }
    });

    // Скрываем меню при уходе курсора с родительского блока
    dropdown.addEventListener('mouseleave', () => {
      if (menu) {
        menu.classList.remove('show');
      }
    });
  });
});


