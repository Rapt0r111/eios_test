function setTheme(themeName) {
    localStorage.setItem('theme', themeName);
    document.documentElement.className = themeName;

}

// Функция для переключения темы
function toggleTheme() {
    localStorage.setItem('switch', document.getElementById('switch').checked);
  if (localStorage.getItem('theme') === 'theme-dark'){
      setTheme('theme-light');
  } else {
      setTheme('theme-dark');
  }
}

// Функция для установки темы при начальной загрузке
(function () {
  if (localStorage.getItem('theme') === 'theme-light') {
      setTheme('theme-light');
  } else {
      setTheme('theme-dark');
  }
  }
)();
function load_checkbox(){
    document.getElementById('switch').checked = localStorage.getItem('switch') === 'true'
}