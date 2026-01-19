function readJsonScript(id) {
  const el = document.getElementById(id);
  if (!el) return null;
  return JSON.parse(el.textContent);
}

function baseOptions() {
  return {
    responsive: true,
    maintainAspectRatio: false,
    plugins: {
      legend: { display: false },
      tooltip: { enabled: true }
    },
    scales: {
      x: {
        grid: { color: "rgba(255,255,255,0.20)" },
        ticks: { color: "#fff" },
        border: { display: false }
      },
      y: {
        grid: { color: "rgba(255,255,255,0.20)" },
        ticks: { color: "#fff" },
        border: { display: false }
      }
    }
  }
}

document.addEventListener("DOMContentLoaded", () => {
  // Pega dados do Django
  const dailyLabels = readJsonScript("daily_sales_labels");
  const dailyData   = readJsonScript("daily_sales_data");

  const emailLabels = readJsonScript("email_labels");
  const emailData   = readJsonScript("email_data");

  const tasksLabels = readJsonScript("tasks_labels");
  const tasksData   = readJsonScript("tasks_data");

  // Se não estiver nessa página, não faz nada
  const elDaily = document.getElementById("chartDailySales");
  const elEmail = document.getElementById("chartEmail");
  const elTasks = document.getElementById("chartTasks");
  if (!elDaily || !elEmail || !elTasks) return;

  // 1) Line - Daily Sales
  new Chart(elDaily, {
    type: "line",
    data: {
      labels: dailyLabels,
      datasets: [{
        data: dailyData,
        borderColor: "#fff",
        backgroundColor: "rgba(255,255,255,0.15)",
        fill: true,
        tension: 0.35,
        pointRadius: 4,
        pointBackgroundColor: "#fff",
        pointBorderWidth: 0
      }]
    },
    options: baseOptions()
  });

  // 2) Bar - Email Subscriptions
  new Chart(elEmail, {
    type: "bar",
    data: {
      labels: emailLabels,
      datasets: [{
        data: emailData,
        backgroundColor: "rgba(255,255,255,0.9)",
        borderWidth: 0,
        borderRadius: 6
      }]
    },
    options: baseOptions()
  });

  // 3) Line - Completed Tasks
  new Chart(elTasks, {
    type: "line",
    data: {
      labels: tasksLabels,
      datasets: [{
        data: tasksData,
        borderColor: "#fff",
        backgroundColor: "rgba(255,255,255,0.15)",
        fill: true,
        tension: 0.35,
        pointRadius: 4,
        pointBackgroundColor: "#fff",
        pointBorderWidth: 0
      }]
    },
    options: baseOptions()
  });
});