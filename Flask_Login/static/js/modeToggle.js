document.addEventListener('DOMContentLoaded', function() {
    const toggle = document.getElementById('themeToggle');
    const darkTheme = document.getElementById('dark-theme');
    const lightTheme = document.getElementById('light-theme');

    // Get theme from localStorage (this happens immediately after login)
    const savedTheme = localStorage.getItem('theme') || 'dark';

    if (savedTheme === 'light') {
        toggle.classList.add('light');
        darkTheme.disabled = true;
        lightTheme.disabled = false;
    } else {
        toggle.classList.remove('light');
        darkTheme.disabled = false;
        lightTheme.disabled = true;
    }

    toggle.addEventListener('click', function() {
        toggle.classList.toggle('light');
        const isLightTheme = toggle.classList.contains('light');

        darkTheme.disabled = isLightTheme;
        lightTheme.disabled = !isLightTheme;

        localStorage.setItem('theme', isLightTheme ? 'light' : 'dark');
    });
});