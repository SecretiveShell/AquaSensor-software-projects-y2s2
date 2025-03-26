const darkModeToggle = document.getElementById('dark-mode-toggle');

const currentTheme = localStorage.getItem('theme');
if (currentTheme === 'dark') {
    document.body.classList.add('dark-mode');
    darkModeToggle.checked = true;
} else if (currentTheme === 'light') {
    document.body.classList.remove('dark-mode');
    darkModeToggle.checked = false;
}

darkModeToggle.addEventListener('change', function() {
    if (this.checked) {
        document.body.classList.add('dark-mode');
        localStorage.setItem('theme', 'dark');
    } else {
        document.body.classList.remove('dark-mode');
        localStorage.setItem('theme', 'light');
    }
});

const prefersDarkScheme = window.matchMedia('(prefers-color-scheme: dark)');

// Only apply system preference if no theme is set in localStorage
if (prefersDarkScheme.matches && !localStorage.getItem('theme')) {
    document.body.classList.add('dark-mode');
    darkModeToggle.checked = true;
    localStorage.setItem('theme', 'dark');
}

prefersDarkScheme.addEventListener('change', (e) => {
    // Only respond to system changes if no theme is set in localStorage
    if (!localStorage.getItem('theme')) {
        if (e.matches) {
            document.body.classList.add('dark-mode');
            darkModeToggle.checked = true;
            localStorage.setItem('theme', 'dark');
        } else {
            document.body.classList.remove('dark-mode');
            darkModeToggle.checked = false;
            localStorage.setItem('theme', 'light');
        }
    }
});