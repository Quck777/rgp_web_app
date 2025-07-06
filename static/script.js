document.addEventListener("DOMContentLoaded", () => {
    // Подсветка кнопки текущей локации (если нужно в будущем)
    highlightCurrentLocation();

    // Анимация появления лога
    const logEntries = document.querySelectorAll(".log ul li");
    logEntries.forEach((entry, index) => {
        setTimeout(() => {
            entry.style.opacity = 1;
        }, index * 100);
    });

    // Скрытие пустых категорий инвентаря
    hideEmptyInventoryCategories();
});

function highlightCurrentLocation() {
    const location = document.querySelector("h1").textContent;
    const buttons = document.querySelectorAll(".actions button");
    buttons.forEach(btn => {
        if (location.includes(btn.textContent.trim())) {
            btn.classList.add("active-location");
        }
    });
}

function hideEmptyInventoryCategories() {
    const categories = document.querySelectorAll(".inventory-category");
    categories.forEach(category => {
        if (category.querySelectorAll(".inventory-item").length === 0) {
            category.style.display = "none";
        }
    });
}
