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




