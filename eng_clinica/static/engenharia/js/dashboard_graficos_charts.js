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
    const labelsAtendimento = readJsonScript("labels_atendimento");
    const dataAtendimento = readJsonScript("data_atendimento");

    // --- 2. Tempo de Reparo x Tempo de Atendimento ---
    const scatterData = readJsonScript("dados_scatter");
    

    // --- 3. Tempo médio de reparo por unidade(dia) ---
    const labelsReparo = readJsonScript("labels_reparo");
    const dataReparo = readJsonScript("data_reparo");

    // --- 4. Taxa de cumprimento de Prev, Calib, Quali e TSE ---
    const labels_taxa_cumprimento_medio = readJsonScript("labels_taxa_cumprimento_medio");
    const data_taxa_cumprimento_medio = readJsonScript("data_taxa_cumprimento_medio");
    const taxa_cumprimento_metadados = readJsonScript("taxa_cumprimento_metadados");

    // --- 5. Quantidade de OS por Tipo de Manutenção ---
    const labels_tipo_manutencao_os = readJsonScript("labels_tipo_manutencao_os");
    const data_tipo_manutencao_os = readJsonScript("data_tipo_manutencao_os");

    // Elementos do DOM
    const elAtendimentoMedio = document.getElementById("chartAtendimentoMedio");
    const elScatter = document.getElementById("chartScatterReparo");
    const elReparoMedio = document.getElementById("chartReparoMedio");
    const elCumprimentoMedio = document.getElementById("chartCumprimentoPrev");
    const elOsPorTipoManutencao = document.getElementById("chartOsPorTipoManutencao");
 
    // -------------------------------------------------------
    // 1) Tempo Médio de Atendimento por Unidade (h)
    // -------------------------------------------------------
    new Chart(elAtendimentoMedio, {
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
            }]
        },
        options: {
            ...baseOptions(), // Suas opções padrão
            scales: {
                x: {
                    title: { display: true, text: 'Tempo de Reparo (Dias)', font: {weight: 'bold'} },
                    grid: { display: false } // Opcional: manter limpo
                },
                y: {
                    title: { display: true, text: 'Tempo de Atendimento (Horas)', font: { weight: 'bold' } },
                    grid: { color: "#f3f4f6" }
                },
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
    // 3) Tempo Médio de Reparo por Unidade (dia)
    // -------------------------------------------------------
    new Chart(elReparoMedio, {
        type: "bar",    
        data: {
            labels: labelsReparo, // Nomes das Oficinas
            datasets: [{
                label: "Média (Dias)",
                data: dataReparo, // Valores calculados
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
                            return context.raw + ' dias'; // Adiciona 'dias' no tooltip
                        }
                    }
                }
            }
        }
    });


    // -------------------------------------------------------
    // 4) Taxa de Cumprimento Médio (%)
    // -------------------------------------------------------
    new Chart(elCumprimentoMedio, {
        type: "bar",
        data: {
            labels: labels_taxa_cumprimento_medio,
            datasets: [{
                label: "Taxa de Cumprimento (%)",
                data: data_taxa_cumprimento_medio,
                // Cor dinâmica: Verde se 100%, Amarelo se < 80%, etc. (Opcional, aqui pus azul padrão)
                backgroundColor: "#0d6efd", 
                borderRadius: 4,
                barPercentage: 0.6,
            }]
        },
        options: {
            ...baseOptions(),
            scales: {
                x: {
                    grid: { display: false },
                    ticks: { font: { size: 11 } }
                },
                y: {
                    beginAtZero: true,
                    max: 105, // Deixa um respiro acima do 100%
                    grid: { color: "#f3f4f6" },
                    ticks: {
                        callback: function(value) { return value + "%" } // Eixo Y com %
                    }
                }
            },
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const index = context.dataIndex;
                            const taxa = context.raw;

                            const detalhes = (taxa_cumprimento_metadados && taxa_cumprimento_metadados[index]) 
                                 ? taxa_cumprimento_metadados[index] : null;
                            
                            if (detalhes) {
                                return[
                                    `Taxa: ${taxa}%`,
                                    `Fechadas: ${detalhes.fechada}`,
                                    `Total OS: ${detalhes.total}`
                                ]; 
                            } else {
                                return `Taxa: ${taxa}%`;
                            }
                        }
                    }
                }
            }
        }
    });

    // -------------------------------------------------------
    // 5) Quantidade de OS por Tipo de Manutenção
    // -------------------------------------------------------
    new Chart(elOsPorTipoManutencao, {
        type: "bar", // Pode mudar para 'doughnut' se preferir pizza
        data: {
            labels: labels_tipo_manutencao_os,
            datasets: [{
                label: "Quantidade de OS",
                data: data_tipo_manutencao_os,
                backgroundColor: [
                    "#0d6efd", "#6610f2", "#6f42c1", "#d63384", "#dc3545", "#fd7e14"
                ],
                borderRadius: 4,
            }]
        },
        options: {
            ...baseOptions(),
            indexAxis: 'y', // <--- ISSO DEIXA A BARRA HORIZONTAL (Melhor para ler nomes longos)
            scales: {
                x: {
                    grid: { display: false },
                    ticks: { font: { size: 11 } }
                },
                y: {
                    grid: { display: false },
                    ticks: { 
                        font: { size: 11, weight: 'bold' },
                        autoSkip: false // Garante que mostre todos os tipos
                    }
                }
            },
            plugins: {
                legend: { display: false }, // Esconde legenda pois os nomes já estão no eixo Y
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `Qtd: ${context.raw} OS`;
                        }
                    }
                }
            }
        }
    });
});