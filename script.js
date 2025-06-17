async function askQuestion() {
  const url = document.getElementById("url").value;
  const question = document.getElementById("question").value;

  const response = await fetch("http://localhost:8000/ask", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url, question })
  });

  const data = await response.json();
  document.getElementById("result").innerText = `Answer: ${data.answer}`;
}
