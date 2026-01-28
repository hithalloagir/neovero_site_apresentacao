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

    // --- 6. Quantidade de OS Planejadas já Realizadas ---
    const labels_qtde_os_planejadas_realizadas = readJsonScript("labels_qtde_os_planejadas_realizadas");
    const data_qtde_os_planejadas_realizadas = readJsonScript("data_qtde_os_planejadas_realizadas");

    // --- 7. Quantidade de OS Planejadas Não Fechadas ---
    const labels_qtde_os_planejadas_n_realizadas = readJsonScript("labels_qtde_os_planejadas_n_realizadas");
    const data_qtde_os_planejadas_n_realizadas = readJsonScript("data_qtde_os_planejadas_n_realizadas");

    //--- 8. Taxa de Conclusão de OS de Planejamento ---
    const labels_os_taxa_conclusao_planejamento = readJsonScript("labels_os_taxa_conclusao_planejamento");
    const data_os_taxa_conclusao_planejamento = readJsonScript("data_os_taxa_conclusao_planejamento");
    const plan_taxa_metadados = readJsonScript("plan_taxa_metadados");

    //--- 9. Taxa de Disponibilidade Geral dos Equipamentos ---
    const labels_disponibilidade_equipamentos = readJsonScript("labels_disponibilidade_equipamentos");
    const data_disponibilidade_equipamentos = readJsonScript("data_disponibilidade_equipamentos");

    //--- 10. Taxa de Disponibilidade dos Equipamentos Críticos ---

    //--- 11. Quantidade de Equipamentos Cadastrados por Unidade ---
    const labels_equipamentos_unidade = readJsonScript("labels_equipamentos_unidade");
    const data_equipamentos_unidade = readJsonScript("data_equipamentos_unidade");

    //--- 12. Quantidade de Equipamentos Críticos por Unidade ---

    //--- 13. Tempo 1 atendimento equip Critico (h) ---

    //--- 14. Idade dos Equipamentos por Unidade (anos) ---
    const labels_idade_equipamentos_unidade = readJsonScript("labels_idade_equipamentos_unidade");
    const data_idade_equipamentos_unidade = readJsonScript("data_idade_equipamentos_unidade");

    //--- 15. Idade dos Equipamentos por família (anos) ---
    const labels_idade_media_equipamentos_familia = readJsonScript("labels_idade_media_equipamentos_familia");
    const data_idade_media_equipamentos_familia = readJsonScript("data_idade_media_equipamentos_familia");

    

    // Elementos do DOM
    const elAtendimentoMedio = document.getElementById("chartAtendimentoMedio");
    const elScatter = document.getElementById("chartScatterReparo");
    const elReparoMedio = document.getElementById("chartReparoMedio");
    const elCumprimentoMedio = document.getElementById("chartCumprimentoPrev");
    const elOsPorTipoManutencao = document.getElementById("chartOsPorTipoManutencao");
    const elQtdeOsPlanejadasRealizadas = document.getElementById("chartQtdeOSPlanejdasRealizadas");
    const elQtdeOsPlanejadasNFechadas = document.getElementById("chartQtdeOSPlanejdasNFechadas");
    const elPorcentagemOSPlanejadasConcluidas = document.getElementById("chartPorcentagemOSPlanejadasConcluidas");
    const elTaxaDisponibilidadeEquipamentos = document.getElementById("chartTaxaDisponibilidadeEquipamentos");
    const elchartQTDEquipamentosUnidade = document.getElementById("chartQTDEquipamentosUnidade");
    const elchartIdadeMediaEquipamentosUnidade = document.getElementById("chartIdadeMediaEquipamentosUnidade");
    const elchartIdadeFamiliaEquipamentos = document.getElementById("chartIdadeFamiliaEquipamentos");


 
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
                barPercentage: 0.9,
                categoryPercentage: 0.9
            }]
        },
        options: {
            ...baseOptions(),
            indexAxis: 'y',
            interaction: {
                mode: 'nearest',
                axis: 'y',
                intersect: false,
            },
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

    // -------------------------------------------------------
    // 6) Quantidade de OS Planejadas já Realizadas
    // -------------------------------------------------------
    new Chart(elQtdeOsPlanejadasRealizadas, {
        type: "bar",
        data: {
            labels: labels_qtde_os_planejadas_realizadas,
            datasets: [{
                label: "Planejadas Concluídas",
                data: data_qtde_os_planejadas_realizadas,
                backgroundColor: "#198754", // Verde Sucesso
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
                    grid: { color: "#f3f4f6" },
                    ticks: { 
                        font: { size: 11 },
                        beginAtZero: true 
                    }
                }
            },
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `Concluídas: ${context.raw}`;
                        }
                    }
                }
            }
        }
    });

    // -------------------------------------------------------
    // 7) Quantidade de OS Planejadas não fechadas
    // -------------------------------------------------------
    new Chart(elQtdeOsPlanejadasNFechadas, {
        type: "bar",
        data: {
            labels: labels_qtde_os_planejadas_n_realizadas,
            datasets: [{
                label: "Planejadas Não Fechadas",
                data: data_qtde_os_planejadas_n_realizadas,
                backgroundColor: "#198754", // Verde Sucesso
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
                    grid: { color: "#f3f4f6" },
                    ticks: { 
                        font: { size: 11 },
                        beginAtZero: true 
                    }
                }
            },
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `Pendentes: ${context.raw}`;
                        }
                    }
                }
            }
        }
    });

    // -------------------------------------------------------
    // 8) OS Taxa de Conclusão de Planejamento
    // -------------------------------------------------------
    new Chart(elPorcentagemOSPlanejadasConcluidas, {
        type: "bar",
        data: {
            labels: labels_os_taxa_conclusao_planejamento,
            datasets: [{
                label: "Conclusão (%)",
                data: data_os_taxa_conclusao_planejamento,
                backgroundColor: "#0dcaf0", // Azul Ciano (Info)
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
                    max: 105,
                    grid: { color: "#f3f4f6" },
                    ticks: { callback: function(v) { return v + "%" } }
                }
            },
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const index = context.dataIndex;
                            const det = plan_taxa_metadados ? plan_taxa_metadados[index] : null;
                            const pct = context.raw;
                            
                            if (det) {
                                return [
                                    `Taxa: ${pct}%`,
                                    `Realizadas: ${det.fechada}`,
                                    `Total Planejado: ${det.total}`
                                ];
                            }
                            return `Taxa: ${pct}%`;
                        }
                    }
                }
            }
        }
    });

    // -------------------------------------------------------
    // 9) Taxa de Disponibilidade de Equipamentos
    // -------------------------------------------------------
    elTaxaDisponibilidadeEquipamentos.innerHTML = ''; // Limpa conteúdo anterior, se houver

    labels_disponibilidade_equipamentos.forEach((hospital, index) => {
        const valor = data_disponibilidade_equipamentos[index];
        const resto = (100 - valor).toFixed(2);

        const colDiv = document.createElement('div');
        colDiv.className = "col-12 col-md-6 col-lg-3";

        let color = "#198754"; // Verde
        if (valor < 95) color = "#ffc107"; // Amarelo
        if (valor < 50) color = "#dc3545"; // Vermelho

        colDiv.innerHTML = `
            <div class="card border-0 shadow-sm rounded-4 h-100">
                <div class="card-body p-3 text-center">
                    <h6 class="text-muted fw-bold mb-0">${hospital}</h6>
                    <div style="height: 150px; position: relative;">
                        <canvas id="gauge_${index}"></canvas>
                        <div style="position: absolute; top: 60%; left: 0; right: 0; text-align: center;">
                            <span class="h4 fw-bold" style="color: ${color}">${valor}%</span>
                        </div>
                    </div>
                </div>
            </div>
        `;
        elTaxaDisponibilidadeEquipamentos.appendChild(colDiv);

        const ctx = document.getElementById(`gauge_${index}`);
        new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: ['Disponível', 'Indisponível'],
                datasets: [{
                    data: [valor, resto],
                    backgroundColor: [color, '#e9ecef'],
                    borderWidth: 0,
                    cutout: '75%',
                    circumference: 180,
                    rotation: 270,
                }] 
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: { legend: { display: false }, 
                tooltip: { enabled: false } }
            }
            
        });
    }); 

    // -------------------------------------------------------
    // 10) Taxa de Disponibilidade dos Equipamentos Críticos
    // -------------------------------------------------------

    // -------------------------------------------------------
    // 11) Quantidade de Equipamentos Cadastrados por Unidade
    // -------------------------------------------------------
    new Chart(elchartQTDEquipamentosUnidade, {
        type: "doughnut",
        data: {
            labels: labels_equipamentos_unidade,
            datasets: [{
                label: "Quantidade de Equipamentos",
                data: data_equipamentos_unidade,
                backgroundColor: [
                    "#0d6efd", "#6610f2", "#6f42c1", "#d63384", "#dc3545", "#fd7e14", "#198754", "#20c997", "#0dcaf0"
                ],
                borderRadius: 4,
                barPercentage: 0.9,
                categoryPercentage: 0.9
            }]
        },
        options: {
            ...baseOptions(),
            plugins: {
                legend: { display: true, position: 'right', labels: { usePointStyle: true } },   
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const value = context.raw;
                            const total = context.chart._metasets[context.datasetIndex].total;
                            const percentage = ((value / total) * 100).toFixed(1) + "%";
                            return `${context.label}: ${value} (${percentage})`;
                        }
                    }
                }
            }
        }
    });

    // -------------------------------------------------------
    // 12) Quantidade de Equipamentos Críticos por Unidade
    // -------------------------------------------------------

    // -------------------------------------------------------
    // 13) Tempo 1 atendimento equip Critico (h)
    // -------------------------------------------------------

    // -------------------------------------------------------
    // 14) Idade dos Equipamentos por Unidade (anos)
    // -------------------------------------------------------
    new Chart(elchartIdadeMediaEquipamentosUnidade, {
        type: "bar",
        data: {
            labels: labels_idade_equipamentos_unidade,
            datasets: [{
                label: "Idade Média (Anos)",
                data: data_idade_equipamentos_unidade,
                backgroundColor: "#198754",
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
                    grid: { color: "#f3f4f6", borderDash: [5, 5] },
                    ticks: { font: { size: 11 } },
                    title: { display: true, text: 'Anos', font: { weight: 'bold' } }
                }
            },
            plugins: {
                legend: { display: false },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            return `Idade: ${context.raw} anos`;
                        }
                    }
                }
            }
        }
    });

    // -------------------------------------------------------
    // 15) Idade dos Equipamentos por família (anos)
    // -------------------------------------------------------
    new Chart(elchartIdadeFamiliaEquipamentos, {
        type: "bar",
        data: {
            labels: labels_idade_media_equipamentos_familia,
            datasets: [{
                label: "Idade Média (Anos)",
                data: data_idade_media_equipamentos_familia,
                backgroundColor: "#0d6efd",
                borderRadius: 4,
                barPercentage: 0.7,
            }]
        },
        options: {
            ...baseOptions(),
            scales: {
                x: {
                    grid: { display: false },
                    ticks: {
                        font: { size: 11 },
                        autoSkip: false,
                        maxRotation: 45,
                        minRotation: 0
                    }
                },
                y: {
                    beginAtZero: true,
                    grid: {
                        color: "#f3f4f6",
                        borderDash: [5, 5]
                    },
                    title: { display: true, text: 'Anos', }
                }
            }
        },
        plugins: {
            legend: { display: false },
            tooltip: {
                callbacks: {
                    label: function(context) {
                        return `Idade: ${context.raw} anos`;
                    }
                }
            }
        }   
    });
});