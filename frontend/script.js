async function sendAction() {
  const input = document.getElementById("user-input").value;
  const output = document.getElementById("story-output");

  if (!input.trim()) return;

  const response = await fetch("http://localhost:8000/action", {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ text: input })
  });

  const data = await response.json();

  output.innerHTML = `
    <p><strong>Глава ${data.chapter}:</strong> Вы попытались: "${data.action}"</p>
    <p>🎲 Бросок кубика: ${data.dice_roll} (${data.outcome})</p>
    <p>${data.result}</p>
  `;

  document.getElementById("user-input").value = "";
}
