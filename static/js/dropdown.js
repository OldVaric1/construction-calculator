console.log('Dropdown script loaded');

document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM fully loaded');
    
    // Принудительно закрываем все меню при загрузке
    document.querySelectorAll('.dropdown-menu').forEach(menu => {
        menu.classList.remove('show');
        console.log('Reset menu state:', menu);
    });
    
    const dropdownToggles = document.querySelectorAll('.dropdown-toggle');
    console.log('Found dropdown toggles:', dropdownToggles.length);

    dropdownToggles.forEach((toggle, index) => {
        console.log(`Setting up toggle ${index}:`, toggle);
        
        toggle.addEventListener('click', function(e) {
            console.log('Dropdown clicked:', this);
            e.preventDefault();
            e.stopPropagation();
            
            const menu = this.nextElementSibling;
            if (!menu || !menu.classList.contains('dropdown-menu')) {
                console.log('No valid dropdown menu found for:', this);
                return;
            }
            console.log('Target menu:', menu);

            console.log('Current .show state:', menu.classList.contains('show'));
            if (menu.classList.contains('show')) {
                console.log('Closing menu');
                menu.classList.remove('show');
                console.log('Menu after close:', window.getComputedStyle(menu).display, window.getComputedStyle(menu).opacity, menu.classList);
            } else {
                console.log('Opening menu - about to add .show');
                // Закрываем другие
                document.querySelectorAll('.dropdown-menu.show').forEach(openMenu => {
                    console.log('Closing other menu:', openMenu);
                    openMenu.classList.remove('show');
                });
                menu.classList.add('show');
                console.log('Added .show. Classes now:', menu.classList);
                console.log('Computed styles after add:', window.getComputedStyle(menu).opacity, window.getComputedStyle(menu).visibility);
            }
        });
    });

    // Закрыть меню при клике вне
    document.addEventListener('click', function(e) {
        console.log('Document clicked, target:', e.target);
        document.querySelectorAll('.dropdown-menu.show').forEach(menu => {
            const toggle = menu.previousElementSibling;
            if (!menu.contains(e.target) && !toggle.contains(e.target)) {
                console.log('Closing menu on outside click:', menu);
                menu.classList.remove('show');
            }
        });
    });
});