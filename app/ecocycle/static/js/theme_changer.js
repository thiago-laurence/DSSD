document.addEventListener('DOMContentLoaded', (event) => {
  const themeCheckbox = document.getElementById('theme-checkbox');
  
  // Load the saved theme from localStorage
  const savedTheme = localStorage.getItem('theme');
  if (savedTheme) {
    themeCheckbox.checked = savedTheme === 'dark';
  }

  // Save the theme to localStorage when the checkbox changes
  themeCheckbox.addEventListener('change', () => {
    const theme = themeCheckbox.checked ? 'dark' : 'light';
    localStorage.setItem('theme', theme);
  });
});