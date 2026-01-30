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
    const labels_taxa_disponibilidade_equipamentos_criticos = readJsonScript("labels_taxa_disponibilidade_equipamentos_criticos");
    const data_taxa_disponibilidade_equipamentos_criticos = readJsonScript("data_taxa_disponibilidade_equipamentos_criticos");

    //--- 11. Quantidade de Equipamentos Cadastrados por Unidade ---
    const labels_equipamentos_unidade = readJsonScript("labels_equipamentos_unidade");
    const data_equipamentos_unidade = readJsonScript("data_equipamentos_unidade");

    //--- 12. Quantidade de Equipamentos Críticos por Unidade ---
    const labels_equipamentos_criticos_por_unidade = readJsonScript("labels_equipamentos_criticos_por_unidade");
    const data_equipamentos_criticos_por_unidade = readJsonScript("data_equipamentos_criticos_por_unidade");
    
    //--- 13. Tempo 1 atendimento equip Critico (h) ---
    const labels_primeiro_atendimento_equipamento_critico = readJsonScript("labels_primeiro_atendimento_equipamento_critico");
    const data_primeiro_atendimento_equipamento_critico = readJsonScript("data_primeiro_atendimento_equipamento_critico");

    //--- 14. Idade dos Equipamentos por Unidade (anos) ---
    const labels_idade_equipamentos_unidade = readJsonScript("labels_idade_equipamentos_unidade");
    const data_idade_equipamentos_unidade = readJsonScript("data_idade_equipamentos_unidade");

    //--- 15. Idade dos Equipamentos por família (anos) ---
    const labels_idade_media_equipamentos_familia = readJsonScript("labels_idade_media_equipamentos_familia");
    const data_idade_media_equipamentos_familia = readJsonScript("data_idade_media_equipamentos_familia");

    //--- 16. Maiores tempos Reparo equipamentos criticos
    const labels_reparo_tempo_critico = readJsonScript("labels_reparo_tempo_critico");
    const data_reparo_tempo_critico = readJsonScript("data_reparo_tempo_critico");

    //--- 17. Principais Causas Corretivas
    const labels_principais_causas_corretivas = readJsonScript("labels_principais_causas_corretivas");
    const data_principais_causas_corretivas = readJsonScript("data_principais_causas_corretivas");

    //--- 18. Maiores Tempos de parada equipamentos criticos por familia
    const labels_maiores_tempos_parada_criticos_por_familia = readJsonScript("labels_maiores_tempos_parada_criticos_por_familia");
    const data_maiores_tempos_parada_criticos_por_familia = readJsonScript("data_maiores_tempos_parada_criticos_por_familia");

    //--- 19. Tempo Mediano de paradas de equipamentos criticos por unidade
    const labels_tempo_mediano_parada_criticos_por_unidade = readJsonScript("labels_tempo_mediano_parada_criticos_por_unidade");
    const data_tempo_mediano_parada_criticos_por_unidade = readJsonScript("data_tempo_mediano_parada_criticos_por_unidade");


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
    const elchartReparoCritico = document.getElementById("chartReparoCritico");
    const elchartCausasCorretivas = document.getElementById("chartCausasCorretivas");
    const elchartParadaCritica = document.getElementById("elchartParadaCritica");
    const elchartMedianaParadaEquipamentosCriticosUnidade = document.getElementById("chartMedianaParadaEquipamentosCriticosUnidade");
    const elrowDisponibilidadeEquipamentosCriticos = document.getElementById("rowDisponibilidadeEquipamentosCriticos");
    const elchartEquipCriticosPorUnidade = document.getElementById("chartEquipCriticosPorUnidade");
    const elchartPrimeiroAtendimentoEquipCritico = document.getElementById("chartPrimeiroAtendimentoEquipCritico");
    


    // -------------------------------------------------------
    // 1) Tempo Médio de Atendimento por Unidade (h)
    // -------------------------------------------------------
    if (elAtendimentoMedio && labelsAtendimento) {
        new Chart(elAtendimentoMedio, {
            type: "bar",
            data: {
                labels: labelsAtendimento,
                datasets: [{
                    label: "Média (Horas)",
                    data: dataAtendimento,
                    backgroundColor: "#198754",
                    borderRadius: 4,
                    barPercentage: 0.6,
                }]
            },
            options: {
                ...baseOptions(),
                plugins: { ...baseOptions().plugins, tooltip: { callbacks: { label: c => c.raw + ' horas' } } }
            }
        });
    }

    
    // -------------------------------------------------------
    // 2) Tempo de Reparo x Tempo de Atendimento
    // -------------------------------------------------------
    if (elScatter && scatterData) {
        new Chart(elScatter, {
            type: 'scatter',
            data: {
                datasets: [{
                    label: 'Reparo x Atendimento',
                    data: scatterData,
                    backgroundColor: 'rgba(54, 162, 235, 0.6)',
                    borderColor: 'rgba(54, 162, 235, 1)',
                    pointRadius: 5,
                }]
            },
            options: {
                ...baseOptions(),
                scales: {
                    x: { title: { display: true, text: 'Tempo de Reparo (Dias)', font: { weight: 'bold' } }, grid: { display: false } },
                    y: { title: { display: true, text: 'Tempo de Atendimento (Horas)', font: { weight: 'bold' } }, grid: { color: "#f3f4f6" } },
                },
                plugins: {
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const p = context.raw;
                                return [`Empresa: ${p.empresa}`, `Equip: ${p.familia || 'N/A'}`, `Reparo: ${p.x} dias`, `Atend: ${p.y} horas`];
                            }
                        }
                    }
                }
            }
        });
    }


    // -------------------------------------------------------
    // 3) Tempo Médio de Reparo por Unidade (dia)
    // -------------------------------------------------------
    if (elReparoMedio && labelsReparo) {
        new Chart(elReparoMedio, {
            type: "bar",
            data: {
                labels: labelsReparo,
                datasets: [{
                    label: "Média (Dias)",
                    data: dataReparo,
                    backgroundColor: "#198754",
                    borderRadius: 4,
                    barPercentage: 0.6,
                }]
            },
            options: {
                ...baseOptions(),
                plugins: { ...baseOptions().plugins, tooltip: { callbacks: { label: c => c.raw + ' dias' } } }
            }
        });
    }


    // -------------------------------------------------------
    // 4) Taxa de Cumprimento Médio (%)
    // -------------------------------------------------------
    if (elCumprimentoMedio && labels_taxa_cumprimento_medio) {
        new Chart(elCumprimentoMedio, {
            type: "bar",
            data: {
                labels: labels_taxa_cumprimento_medio,
                datasets: [{
                    label: "Taxa (%)",
                    data: data_taxa_cumprimento_medio,
                    backgroundColor: "#0d6efd",
                    borderRadius: 4,
                    barPercentage: 0.6,
                }]
            },
            options: {
                ...baseOptions(),
                scales: {
                    x: { grid: { display: false }, ticks: { font: { size: 11 } } },
                    y: { beginAtZero: true, max: 105, grid: { color: "#f3f4f6" }, ticks: { callback: v => v + "%" } }
                },
                plugins: {
                    legend: { display: false },
                    tooltip: {
                        callbacks: {
                            label: function(context) {
                                const idx = context.dataIndex;
                                const det = taxa_cumprimento_metadados ? taxa_cumprimento_metadados[idx] : null;
                                return det ? [`Taxa: ${context.raw}%`, `Fechadas: ${det.fechada}`, `Total: ${det.total}`] : `Taxa: ${context.raw}%`;
                            }
                        }
                    }
                }
            }
        });
    }

    // -------------------------------------------------------
    // 5) Quantidade de OS por Tipo de Manutenção
    // -------------------------------------------------------
    if (elOsPorTipoManutencao && labels_tipo_manutencao_os) {
        new Chart(elOsPorTipoManutencao, {
            type: "bar",
            data: {
                labels: labels_tipo_manutencao_os,
                datasets: [{
                    label: "Quantidade",
                    data: data_tipo_manutencao_os,
                    backgroundColor: ["#0d6efd", "#6610f2", "#6f42c1", "#d63384", "#dc3545", "#fd7e14"],
                    borderRadius: 4
                }]
            },
            options: {
                ...baseOptions(),
                indexAxis: 'y',
                scales: { x: { grid: { display: false } }, y: { grid: { display: false }, ticks: { font: { weight: 'bold' }, autoSkip: false } } }
            }
        });
    }

    // -------------------------------------------------------
    // 6) Quantidade de OS Planejadas já Realizadas
    // -------------------------------------------------------
    if (elQtdeOsPlanejadasRealizadas && labels_qtde_os_planejadas_realizadas) {
        new Chart(elQtdeOsPlanejadasRealizadas, {
            type: "bar",
            data: {
                labels: labels_qtde_os_planejadas_realizadas,
                datasets: [{ label: "Realizadas", data: data_qtde_os_planejadas_realizadas, backgroundColor: "#198754", borderRadius: 4, barPercentage: 0.6 }]
            },
            options: baseOptions()
        });
    }

    // -------------------------------------------------------
    // 7) Quantidade de OS Planejadas não fechadas
    // -------------------------------------------------------
    if (elQtdeOsPlanejadasNFechadas && labels_qtde_os_planejadas_n_realizadas) {
        new Chart(elQtdeOsPlanejadasNFechadas, {
            type: "bar",
            data: {
                labels: labels_qtde_os_planejadas_n_realizadas,
                datasets: [{ label: "Pendentes", data: data_qtde_os_planejadas_n_realizadas, backgroundColor: "#198754", borderRadius: 4, barPercentage: 0.6 }]
            },
            options: baseOptions()
        });
    }

    // -------------------------------------------------------
    // 8) OS Taxa de Conclusão de Planejamento
    // -------------------------------------------------------
    if (elPorcentagemOSPlanejadasConcluidas && labels_os_taxa_conclusao_planejamento) {
        new Chart(elPorcentagemOSPlanejadasConcluidas, {
            type: "bar",
            data: {
                labels: labels_os_taxa_conclusao_planejamento,
                datasets: [{ label: "Conclusão (%)", data: data_os_taxa_conclusao_planejamento, backgroundColor: "#0dcaf0", borderRadius: 4, barPercentage: 0.6 }]
            },
            options: {
                ...baseOptions(),
                scales: { y: { beginAtZero: true, max: 105, ticks: { callback: v => v + "%" } } }
            }
        });
    }

    // -------------------------------------------------------
    // 9) Taxa de Disponibilidade de Equipamentos
    // -------------------------------------------------------
    if (elTaxaDisponibilidadeEquipamentos && labels_disponibilidade_equipamentos) {
        // ... (Mesma lógica de loop para gauges individuais)
        // Como o container existe, o loop já foi feito no JS antigo ou será feito aqui:
        elTaxaDisponibilidadeEquipamentos.innerHTML = ''; 
        labels_disponibilidade_equipamentos.forEach((hospital, index) => {
            const valor = data_disponibilidade_equipamentos[index];
            const resto = (100 - valor).toFixed(2);
            const colDiv = document.createElement('div');
            colDiv.className = "col-12 col-md-6 col-lg-3";
            let color = valor < 50 ? "#dc3545" : (valor < 95 ? "#ffc107" : "#198754");
            
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
                </div>`;
            elTaxaDisponibilidadeEquipamentos.appendChild(colDiv);
            new Chart(document.getElementById(`gauge_${index}`), {
                type: 'doughnut',
                data: { labels: ['Disp', 'Indisp'], datasets: [{ data: [valor, resto], backgroundColor: [color, '#e9ecef'], borderWidth: 0, cutout: '75%', circumference: 180, rotation: 270 }] },
                options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false }, tooltip: { enabled: false } } }
            });
        });
    }

    // -------------------------------------------------------
    // 10) Taxa de Disponibilidade dos Equipamentos Críticos
    // -------------------------------------------------------
    if (elrowDisponibilidadeEquipamentosCriticos && labels_taxa_disponibilidade_equipamentos_criticos) {
         elrowDisponibilidadeEquipamentosCriticos.innerHTML = "";
         labels_taxa_disponibilidade_equipamentos_criticos.forEach((hospital, index) => {
            const valor = data_taxa_disponibilidade_equipamentos_criticos[index];
            const resto = (100 - valor).toFixed(2);
            let color = valor < 95 ? "#dc3545" : (valor < 98 ? "#ffc107" : "#198754");
            
            const colDiv = document.createElement("div");
            colDiv.className = "col-12 col-md-6 col-lg-3"; 
            colDiv.innerHTML = `
                <div class="card border-0 shadow-sm rounded-4 h-100" style="border-top: 4px solid ${color} !important;">
                    <div class="card-body p-3 text-center">
                        <h6 class="text-muted fw-bold mb-0">${hospital}</h6>
                        <div style="height: 150px; position: relative;">
                            <canvas id="gauge_crit_${index}"></canvas>
                            <div style="position: absolute; top: 60%; left: 0; right: 0; text-align: center;">
                                <span class="h4 fw-bold" style="color: ${color}">${valor}%</span>
                            </div>
                        </div>
                    </div>
                </div>`;
            elrowDisponibilidadeEquipamentosCriticos.appendChild(colDiv);
            new Chart(document.getElementById(`gauge_crit_${index}`), {
                type: 'doughnut',
                data: { labels: ["Disp", "Indisp"], datasets: [{ data: [valor, resto], backgroundColor: [color, "#e9ecef"], borderWidth: 0, cutout: "75%", circumference: 180, rotation: 270 }] },
                options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false }, tooltip: { enabled: false } } }
            });
         });
    }

    // -------------------------------------------------------
    // 11) Quantidade de Equipamentos Cadastrados por Unidade
    // -------------------------------------------------------
    if (elchartQTDEquipamentosUnidade && labels_equipamentos_unidade) {
        new Chart(elchartQTDEquipamentosUnidade, {
            type: "doughnut",
            data: {
                labels: labels_equipamentos_unidade,
                datasets: [{ label: "Qtd", data: data_equipamentos_unidade, backgroundColor: ["#0d6efd", "#6610f2", "#6f42c1", "#d63384", "#dc3545", "#fd7e14", "#198754", "#20c997", "#0dcaf0"], borderWidth: 0 }]
            },
            options: { ...baseOptions(), plugins: { legend: { display: true, position: 'right' } } }
        });
    }

    // -------------------------------------------------------
    // 12) Quantidade de Equipamentos Críticos por Unidade
    // -------------------------------------------------------
    if (elchartEquipCriticosPorUnidade && labels_equipamentos_criticos_por_unidade) {
        new Chart(elchartEquipCriticosPorUnidade, {
            type: "doughnut",
            data: {
                labels: labels_equipamentos_criticos_por_unidade,
                datasets: [{ label: "Qtd", data: data_equipamentos_criticos_por_unidade, backgroundColor: ["#dc3545", "#fd7e14", "#ffc107", "#20c997", "#0d6efd"], borderWidth: 0 }]
            },
            options: { ...baseOptions(), plugins: { legend: { display: true, position: 'right' } } }
        });
    }

    // -------------------------------------------------------
    // 13) Tempo 1 atendimento equip Critico (h)
    // -------------------------------------------------------
    if (elchartPrimeiroAtendimentoEquipCritico && labels_primeiro_atendimento_equipamento_critico) {
        new Chart(elchartPrimeiroAtendimentoEquipCritico, {
            type: "bar",
            data: {
                labels: labels_primeiro_atendimento_equipamento_critico,
                datasets: [{ label: "Horas", data: data_primeiro_atendimento_equipamento_critico, backgroundColor: "#fd7e14", borderRadius: 4, barPercentage: 0.6 }]
            },
            options: baseOptions()
        });
    }

    // -------------------------------------------------------
    // 14) Idade dos Equipamentos por Unidade (anos)
    // -------------------------------------------------------
    if (elchartIdadeMediaEquipamentosUnidade && labels_idade_equipamentos_unidade) {
        new Chart(elchartIdadeMediaEquipamentosUnidade, {
            type: "bar",
            data: {
                labels: labels_idade_equipamentos_unidade,
                datasets: [{ label: "Anos", data: data_idade_equipamentos_unidade, backgroundColor: "#198754", borderRadius: 4, barPercentage: 0.6 }]
            },
            options: { ...baseOptions(), scales: { y: { beginAtZero: true, title: { display: true, text: 'Anos' } } } }
        });
    }

    // -------------------------------------------------------
    // 15) Idade dos Equipamentos por família (anos)
    // -------------------------------------------------------
    if (elchartIdadeFamiliaEquipamentos && labels_idade_media_equipamentos_familia) {
        new Chart(elchartIdadeFamiliaEquipamentos, {
            type: "bar",
            data: {
                labels: labels_idade_media_equipamentos_familia,
                datasets: [{ label: "Anos", data: data_idade_media_equipamentos_familia, backgroundColor: "#0d6efd", borderRadius: 4, barPercentage: 0.7 }]
            },
            options: {
                ...baseOptions(),
                scales: { x: { ticks: { autoSkip: false, maxRotation: 45, minRotation: 0 } }, y: { beginAtZero: true, title: { display: true, text: 'Anos' } } }
            }
        });
    }

    // -------------------------------------------------------
    // 16) Maiores tempos Reparo equipamentos criticos
    // -------------------------------------------------------
    if (elchartReparoCritico && labels_reparo_tempo_critico) {
        new Chart(elchartReparoCritico, {
            type: "bar",
            data: {
                labels: labels_reparo_tempo_critico,
                datasets: [{ label: "Horas", data: data_reparo_tempo_critico, backgroundColor: "#dc3545", borderRadius: 4, barPercentage: 0.6 }]
            },
            options: { ...baseOptions(), scales: { x: { ticks: { autoSkip: false, maxRotation: 45, minRotation: 0 } } } }
        });
    }

    // -------------------------------------------------------
    // 17) Principais Causas Corretivas
    // -------------------------------------------------------
    if (elchartCausasCorretivas && labels_principais_causas_corretivas) {
        new Chart(elchartCausasCorretivas, {
            type: "bar",
            data: {
                labels: labels_principais_causas_corretivas,
                datasets: [{ label: "Ocorrências", data: data_principais_causas_corretivas, backgroundColor: "#fd7e14", borderRadius: 4 }]
            },
            options: { ...baseOptions(), indexAxis: 'y' }
        });
    }

    // -------------------------------------------------------
    // 18) Maiores Tempos de parada equipamentos criticos por familia
    // -------------------------------------------------------
    if (elchartParadaCritica && labels_maiores_tempos_parada_criticos_por_familia) {
         new Chart(elchartParadaCritica, { // ID corrigido no seletor
            type: "bar",
            data: {
                labels: labels_maiores_tempos_parada_criticos_por_familia,
                datasets: [{ label: "Horas Parado", data: data_maiores_tempos_parada_criticos_por_familia, backgroundColor: "#842029", borderRadius: 4, barPercentage: 0.6 }]
            },
            options: { ...baseOptions(), scales: { x: { ticks: { autoSkip: false, maxRotation: 45, minRotation: 0 } } } }
        });
    }

    // -------------------------------------------------------
    // 19) Tempo Mediano de paradas de equipamentos criticos por unidade
    // -------------------------------------------------------
    if (elchartMedianaParadaEquipamentosCriticosUnidade && labels_tempo_mediano_parada_criticos_por_unidade) {
        new Chart(elchartMedianaParadaEquipamentosCriticosUnidade, {
            type: "bar",
            data: {
                labels: labels_tempo_mediano_parada_criticos_por_unidade,
                datasets: [{ label: "Mediana (h)", data: data_tempo_mediano_parada_criticos_por_unidade, backgroundColor: "#6610f2", borderRadius: 4, barPercentage: 0.6 }]
            },
            options: baseOptions()
        });
    }

    // -------------------------------------------------------
    // 20) Horarios que os equipamentos criticos ficaram indisponiveis
    // -------------------------------------------------------
    const cells = document.querySelectorAll('.heatmap-cell');
    if (cells.length > 0) {
        let maxVal = 0;
        cells.forEach(c => {
            const val = parseInt(c.getAttribute('data-value')) || 0;
            if (val > maxVal) maxVal = val;
            c.style.border = "1px solid #fff";
        });
        cells.forEach(c => {
            const val = parseInt(c.getAttribute('data-value')) || 0;
            if (val > 0) {
                const intensity = maxVal > 0 ? (val / maxVal) : 0;
                const alpha = 0.1 + (intensity * 0.9);
                c.style.backgroundColor = `rgba(220, 53, 69, ${alpha})`;
                if (alpha > 0.6) c.style.color = '#fff';
                c.style.cursor = 'pointer'; // Indica que é interativo
            } else {
                c.style.backgroundColor = "#f8f9fa";
                c.style.color = "transparent";
            }
        });
    }
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
      return new bootstrap.Tooltip(tooltipTriggerEl)
    })
});