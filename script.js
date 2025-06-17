async function askQuestion() {
  const url = document.getElementById("url").value;
  const question = document.getElementById("question").value;

  const response = await fetch("https://langchain-yt.onrender.com", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ url, question })
  });

  const data = await response.json();
  document.getElementById("result").innerText = `Answer: ${data.answer}`;
}
