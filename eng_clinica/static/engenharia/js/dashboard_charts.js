function readJsonScript(id) {
    const el = document.getElementById(id);
    if (!el) return null;
    return JSON.parse(el.textContent);
}

// Configurações globais para estilo "Clean/Moderno"
// Chart.defaults.font.family = "'Inter', system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif";
// Chart.defaults.color = "#6c757d"; // Cor de texto padrão (text-muted do Bootstrap)

function baseOptions() {
    return {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: { display: false },
            tooltip: {
                backgroundColor: 'rgba(0, 0, 0, 0.8)',
                padding: 12,
                titleFont: { size: 13 },
                bodyFont: { size: 13 },
                cornerRadius: 8,
                displayColors: false // Remove o quadradinho de cor no tooltip para ficar mais limpo
            }
        },
        scales: {
            x: {
                grid: {
                    display: false, // Remove grades verticais para limpar o visual
                    drawBorder: false
                },
                ticks: {
                    color: "#9ca3af", // Cinza suave
                    font: { size: 11 }
                },
                border: { display: false }
            },
            y: {
                grid: {
                    color: "#f3f4f6", // Cinza muito claro para as linhas horizontais
                    borderDash: [5, 5], // Linhas pontilhadas (estilo moderno)
                    drawBorder: false
                },
                ticks: {
                    color: "#9ca3af",
                    font: { size: 11 },
                    padding: 10
                },
                border: { display: false }
            }
        },
        interaction: {
            mode: 'index',
            intersect: false,
        }
    }
}

document.addEventListener("DOMContentLoaded", () => {
    // Pega dados do Django
    const dailyLabels = readJsonScript("daily_sales_labels");
    const dailyData = readJsonScript("daily_sales_data");

    const emailLabels = readJsonScript("email_labels");
    const emailData = readJsonScript("email_data");

    const tasksLabels = readJsonScript("tasks_labels");
    const tasksData = readJsonScript("tasks_data");

    // Elementos do DOM
    const elDaily = document.getElementById("chartDailySales");
    const elEmail = document.getElementById("chartEmail");
    const elTasks = document.getElementById("chartTasks");

    // Verificação de segurança
    if (!elDaily || !elEmail || !elTasks) return;

    // -------------------------------------------------------
    // 1) Line - Daily Sales (Tema: Success/Verde)
    // -------------------------------------------------------
    // Criando um gradiente suave para o preenchimento
    let ctxDaily = elDaily.getContext("2d");
    let gradientDaily = ctxDaily.createLinearGradient(0, 0, 0, 300);
    gradientDaily.addColorStop(0, 'rgba(25, 135, 84, 0.2)'); // Bootstrap Success
    gradientDaily.addColorStop(1, 'rgba(25, 135, 84, 0.0)');

    new Chart(elDaily, {
        type: "line",
        data: {
            labels: dailyLabels,
            datasets: [{
                label: "Vendas",
                data: dailyData,
                borderColor: "#198754", // Bootstrap Success
                backgroundColor: gradientDaily,
                borderWidth: 2,
                fill: true,
                tension: 0.4, // Curva suave
                pointRadius: 0, // Remove pontos (aparecem só no hover)
                pointHoverRadius: 6,
                pointBackgroundColor: "#198754",
                pointBorderColor: "#fff",
                pointBorderWidth: 2
            }]
        },
        options: baseOptions()
    });

    // -------------------------------------------------------
    // 2) Bar - Email Subscriptions (Tema: Warning/Laranja)
    // -------------------------------------------------------
    new Chart(elEmail, {
        type: "bar",
        data: {
            labels: emailLabels,
            datasets: [{
                label: "Inscritos",
                data: emailData,
                backgroundColor: "#ffc107", // Bootstrap Warning
                hoverBackgroundColor: "#ffca2c",
                borderRadius: 4, // Barras arredondadas
                borderSkipped: false, // Arredonda em baixo também se quiser, ou tire essa linha
                barPercentage: 0.6, // Barras mais finas
                categoryPercentage: 0.8
            }]
        },
        options: baseOptions()
    });

    // -------------------------------------------------------
    // 3) Line - Completed Tasks (Tema: Danger/Vermelho)
    // -------------------------------------------------------
    let ctxTasks = elTasks.getContext("2d");
    let gradientTasks = ctxTasks.createLinearGradient(0, 0, 0, 300);
    gradientTasks.addColorStop(0, 'rgba(220, 53, 69, 0.2)'); // Bootstrap Danger
    gradientTasks.addColorStop(1, 'rgba(220, 53, 69, 0.0)');

    new Chart(elTasks, {
        type: "line",
        data: {
            labels: tasksLabels,
            datasets: [{
                label: "Tarefas",
                data: tasksData,
                borderColor: "#dc3545", // Bootstrap Danger
                backgroundColor: gradientTasks,
                borderWidth: 2,
                fill: true,
                tension: 0.4,
                pointRadius: 0,
                pointHoverRadius: 6,
                pointBackgroundColor: "#dc3545",
                pointBorderColor: "#fff",
                pointBorderWidth: 2
            }]
        },
        options: baseOptions()
    });
});