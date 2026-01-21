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
    // --- 1. Tempo médio de atendimento por unidade(h) ---
    const labelsAtendimento = readJsonScript("labels_atendimento"); // ID definido no HTML
    const dataAtendimento = readJsonScript("data_atendimento");     // ID definido no HTML

    // --- 2. Tempo de Reparo x Tempo de Atendimento ---
    const scatterData = readJsonScript("dados_scatter");
    

    // --- 3. Tempo de Reparo x Tempo de Atendimento ---
    const emailLabels = readJsonScript("email_labels");
    const emailData = readJsonScript("email_data");

    const tasksLabels = readJsonScript("tasks_labels");
    const tasksData = readJsonScript("tasks_data");

    // Elementos do DOM
    const elDaily = document.getElementById("chartDailySales");
    const elScatter = document.getElementById("chartScatterReparo");

    const elEmail = document.getElementById("chartEmail");
    const elTasks = document.getElementById("chartTasks");

    // Verificação de segurança
    // if (!elDaily || !elEmail || !elTasks) return;

    // -------------------------------------------------------
    // 1) Tempo Médio de Atendimento por Unidade (h)
    // -------------------------------------------------------
    new Chart(elDaily, {
        type: "bar",    
        data: {
            labels: labelsAtendimento, // Nomes das Oficinas
            datasets: [{
                label: "Média (Horas)",
                data: dataAtendimento, // Valores calculados
                backgroundColor: "#198754", // Verde Bootstrap
                borderRadius: 4,
                barPercentage: 0.6,
            }]
        },
        options: {
            ...baseOptions(),
            plugins: {
                ...baseOptions().plugins,
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return context.raw + ' horas'; // Adiciona 'horas' no tooltip
                        }
                    }
                }
            }
        }
    });

    // -------------------------------------------------------
    // 2) Tempo de Reparo x Tempo de Atendimento)
    // -------------------------------------------------------

    new Chart(elScatter, {
        type: 'scatter',
        data: {
            datasets: [{
                label: 'Reparo x Atendimento',
                data: scatterData, // Chart.js entende a estrutura {x: ..., y: ...}
                backgroundColor: 'rgba(54, 162, 235, 0.6)', // Azul transparente
                borderColor: 'rgba(54, 162, 235, 1)',
                pointRadius: 5,
                pointHoverRadius: 7
            }]
        },
        options: {
            ...baseOptions(), // Suas opções padrão
            scales: {
                x: {
                    title: { display: true, text: 'Tempo de Reparo (Dias)' },
                    grid: { display: false } // Opcional: manter limpo
                },
                y: {
                    title: { display: true, text: 'Tempo de Atendimento (Horas)' },
                    grid: { color: "#f3f4f6" }
                }
            },
            plugins: {
                tooltip: {
                    callbacks: {
                        // AQUI É A MÁGICA DO TOOLTIP CUSTOMIZADO
                        label: function(context) {
                            const ponto = context.raw; // Acessa o objeto original {x, y, empresa, familia}
                            
                            // Retorna um array de strings (cada string é uma linha no tooltip)
                            return [
                                `Empresa: ${ponto.empresa}`,
                                `equipamento: ${ponto.familia || 'N/A'}`,
                                `Reparo: ${ponto.x} dias`,
                                `Atendimento: ${ponto.y} horas`
                            ];
                        }
                    }
                }
            }
        }
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