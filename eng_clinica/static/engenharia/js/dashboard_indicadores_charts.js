function readJsonScript(id) {
    const el = document.getElementById(id);
    if (!el) return null;
    try {
        return JSON.parse(el.textContent);
    } catch (e) {
        console.warn(`Erro ao ler JSON de ${id}`, e);
        return [];
    }
}

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
                displayColors: false 
            }
        },
        scales: {
            x: {
                grid: { display: false, drawBorder: false },
                ticks: { color: "#9ca3af", font: { size: 11 } },
                border: { display: false }
            },
            y: {
                grid: { color: "#f3f4f6", borderDash: [5, 5], drawBorder: false },
                ticks: { color: "#9ca3af", font: { size: 11 }, padding: 10 },
                border: { display: false }
            }
        },
        interaction: { mode: 'index', intersect: false }
    }
}

document.addEventListener("DOMContentLoaded", () => {
    // --- 1. Quantidade de Equipamentos Cadastrados ---
    const labels_equipamentos_cadastrados = readJsonScript("labels_equipamentos_cadastrados");
    const data_equipamentos_cadastrados = readJsonScript("data_equipamentos_cadastrados");

    // Elementos do DOM
    const elchartQtdEquipamentosCadastrados = document.getElementById("chartQtdEquipamentosCadastrados");

    // -------------------------------------------------------
    // 1) Quantidade de Equipamentos Cadastrados
    // -------------------------------------------------------
    if (elchartQtdEquipamentosCadastrados && labels_equipamentos_cadastrados) {
        new Chart(elchartQtdEquipamentosCadastrados, {
            type: "bar",
            data: {
                labels: labels_equipamentos_cadastrados,
                datasets: [{
                    label: "Quantidade",
                    data: data_equipamentos_cadastrados,
                    backgroundColor: "#198754",
                    borderRadius: 4,
                    barPercentage: 0.6,
                }]
            },
            options: {
                ...baseOptions(),
                plugins: { ...baseOptions().plugins, tooltip: { callbacks: { label: c => c.raw + ' Equipamentos' } } }
            }
        });
    }
});