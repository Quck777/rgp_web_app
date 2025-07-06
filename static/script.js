// static/script.js

// Переход по локациям через кнопку
document.addEventListener("DOMContentLoaded", function () {
    const locationButtons = document.querySelectorAll(".location-button");

    locationButtons.forEach(button => {
        button.addEventListener("click", function () {
            const location = this.dataset.location;
            window.location.href = `/?location=${location}`;
        });
    });

    // Удаление предмета (если такая кнопка появится)
    document.querySelectorAll(".delete-item").forEach(btn => {
        btn.addEventListener("click", function () {
            const itemName = this.dataset.item;
            fetch(`/delete_item?name=${itemName}`, { method: "POST" })
                .then(() => window.location.reload());
        });
    });

    // Продажа предмета (если такая кнопка появится)
    document.querySelectorAll(".sell-item").forEach(btn => {
        btn.addEventListener("click", function () {
            const itemName = this.dataset.item;
            fetch(`/sell_item?name=${itemName}`, { method: "POST" })
                .then(() => window.location.reload());
        });
    });
});
