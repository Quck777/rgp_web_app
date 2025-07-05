async function move(direction) {
    const response = await fetch(`/move/${direction}`, { method: "POST" });
    const data = await response.json();
    location.reload(); // Простая перезагрузка, можно заменить на динамическое обновление
}
