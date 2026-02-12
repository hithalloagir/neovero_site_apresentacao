document.addEventListener('DOMContentLoaded', function() {
    
    // ==========================================
    // 1. GRÁFICO DE PASSIVO (BACKLOG)
    // ==========================================
    const backlogCtx = document.getElementById('backlogChart');
    
    // Verifica se o elemento e os dados existem no HTML
    const backlogLabelsTag = document.getElementById('backlog-labels');
    const backlogDataTag = document.getElementById('backlog-data');

    if (backlogCtx && backlogLabelsTag && backlogDataTag) {
        
        // Converte o texto JSON do Django para Array JS real
        const labels = JSON.parse(backlogLabelsTag.textContent);
        const data = JSON.parse(backlogDataTag.textContent);

        // Só cria o gráfico se houver dados
        if (labels.length > 0) {
            new Chart(backlogCtx, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'OS Planejadas Acumuladas',
                        data: data,
                        borderColor: '#dc3545',
                        backgroundColor: 'rgba(220, 53, 69, 0.15)',
                        borderWidth: 3,
                        pointBackgroundColor: '#fff',
                        pointBorderColor: '#dc3545',
                        pointRadius: 5,
                        pointHoverRadius: 7,
                        fill: true,
                        tension: 0.3
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    interaction: { mode: 'index', intersect: false },
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    return context.raw + ' pendências acumuladas';
                                }
                            }
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            grid: { borderDash: [2, 2] }
                        },
                        x: { grid: { display: false } }
                    }
                }
            });
        }
    }

    // ==========================================
    // 2. Pendencias de manutenção corretiva
    // ==========================================
    const backlogCorretivasChart = document.getElementById('backlogCorretivasChart');
    
    // Verifica se o elemento e os dados existem no HTML
    const labels_backlog_corretivas = document.getElementById('labels_backlog_corretivas');
    const data_backlog_corretivas = document.getElementById('data_backlog_corretivas');

    if (backlogCorretivasChart && labels_backlog_corretivas && data_backlog_corretivas) {
        
        // Converte o texto JSON do Django para Array JS real
        const labels = JSON.parse(labels_backlog_corretivas.textContent);
        const data = JSON.parse(data_backlog_corretivas.textContent);

        // Só cria o gráfico se houver dados 
        if (labels.length > 0) {
            new Chart(backlogCorretivasChart, {
                type: 'line',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'OS Planejadas Acumuladas',
                        data: data,
                        borderColor: '#dc3545',
                        backgroundColor: 'rgba(220, 53, 69, 0.15)',
                        borderWidth: 3,
                        pointBackgroundColor: '#fff',
                        pointBorderColor: '#dc3545',
                        pointRadius: 5,
                        pointHoverRadius: 7,
                        fill: true,
                        tension: 0.3
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    interaction: { mode: 'index', intersect: false },
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    return context.raw + ' corretivas acumuladas';
                                }
                            }
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            grid: { borderDash: [2, 2] }
                        },
                        x: { grid: { display: false } }
                    }
                }
            });
        }
    }

    // ==========================================
    // 3. Total de serviços realizados
    // ==========================================
    const backlogTotalServicosChart = document.getElementById('backlogTotalServicosChart');
    
    // Verifica se o elemento e os dados existem no HTML
    const labels_backlog_total_servicos = document.getElementById('labels_backlog_total_servicos');
    const data_backlog_total_servicos = document.getElementById('data_backlog_total_servicos');

    if (backlogTotalServicosChart && labels_backlog_total_servicos && data_backlog_total_servicos) {
        
        // Converte o texto JSON do Django para Array JS real
        const labels = JSON.parse(labels_backlog_total_servicos.textContent);
        const data = JSON.parse(data_backlog_total_servicos.textContent);

        // Só cria o gráfico se houver dados 
        if (labels.length > 0) {
            new Chart(backlogTotalServicosChart, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Total de OS Realizadas',
                        data: data,
                        backgroundColor: '#28a745', // Verde (sucesso/concluído)
                        borderRadius: 5
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    interaction: { mode: 'index', intersect: false },
                    plugins: {
                        legend: { display: false },
                        tooltip: {
                            callbacks: {
                                label: function(context) {
                                    return context.raw + ' serviços realizados';
                                }
                            }
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            grid: { borderDash: [2, 2] }
                        },
                        x: { grid: { display: false } }
                    }
                }
            });
        }
    }

    // ==========================================
    // 4. Ag Grid Equipamentos Parados
    // ==========================================
    const gridDiv = document.querySelector('#myGrid');
    const dataTag = document.getElementById('data-equipamentos-parados');
    if (gridDiv && dataTag) {
        const rowData = JSON.parse(dataTag.textContent);

        // Definição das Colunas
        const columnDefs = [
            { field: "os", headerName: "OS", sortable: true, filter: true, width: 110, pinned: 'left' },
            { field: "empresa", headerName: "Empresa", sortable: true, filter: true, width: 100 },
            { field: "tag", headerName: "Tag", sortable: true, filter: true, width: 120 },
            { field: "modelo", headerName: "Modelo", sortable: true, filter: true, width: 150 },
            { 
                field: "data_parada_fmt", 
                headerName: "Data Parada", 
                sortable: true, 
                width: 150 
            },
            { 
                field: "dias_parado", 
                headerName: "Dias Parado", 
                sortable: true, 
                filter: 'agNumberColumnFilter',
                width: 130,
                // Colorir vermelho se > 30 dias
                cellStyle: params => {
                    if (params.value > 30) {
                        return {color: 'white', backgroundColor: '#dc3545', fontWeight: 'bold'};
                    }
                    return {fontWeight: 'bold', color: '#dc3545'};
                }
            },
            { field: "tipomanutencao", headerName: "Tipo Manutenção", sortable: true, filter: true, width: 150 },
            { field: "situacao", headerName: "Situação", sortable: true, filter: true, width: 120 }
        ];

        // Configurações do Grid
        const gridOptions = {
            columnDefs: columnDefs,
            rowData: rowData,
            pagination: true,
            paginationPageSize: 10,
            defaultColDef: {
                flex: 1, // Faz as colunas ocuparem a largura total
                minWidth: 100,
                resizable: true,
            },
            // Tradução para PT-BR (Opcional, mas recomendado)
            localeText: {
                page: 'Página',
                more: 'Mais',
                to: 'a',
                of: 'de',
                next: 'Próximo',
                last: 'Último',
                first: 'Primeiro',
                previous: 'Anterior',
                loadingOoo: 'Carregando...',
                noRowsToShow: 'Nenhum equipamento parado encontrado.',
                filterOoo: 'Filtrar...',
            }
        };

        // Inicializa o Grid
        new agGrid.Grid(gridDiv, gridOptions);
    }

    // ==========================================
    // 5. Ag Grid Equipamentos Criticos Indisponíveis
    // ==========================================
    const gridDivIndisponiveis = document.querySelector('#myGridIndisponiveis');
    const dataTagIndisponiveis = document.getElementById('lista_equipamentos_criticos_indisponiveis');
    if (gridDivIndisponiveis && dataTagIndisponiveis) {
        const rowData = JSON.parse(dataTagIndisponiveis.textContent);

        // Definição das Colunas
        const columnDefs = [
            { field: "os", headerName: "OS", sortable: true, filter: true, width: 110, pinned: 'left' },
            { field: "empresa", headerName: "Empresa", sortable: true, filter: true, width: 100 },
            { field: "tag", headerName: "Tag", sortable: true, filter: true, width: 120 },
            { field: "prioridade", headerName: "Prioridade", sortable: true, filter: true, width: 120 },
            { field: "modelo", headerName: "Modelo", sortable: true, filter: true, width: 150 },
            { 
                field: "data_parada_fmt", 
                headerName: "Data Parada", 
                sortable: true, 
                width: 150 
            },
            { 
                field: "dias_parado", 
                headerName: "Dias Parado", 
                sortable: true, 
                filter: 'agNumberColumnFilter',
                width: 130,
                // Colorir vermelho se > 30 dias
                cellStyle: params => {
                    if (params.value > 30) {
                        return {color: 'white', backgroundColor: '#dc3545', fontWeight: 'bold'};
                    }
                    return {fontWeight: 'bold', color: '#dc3545'};
                }
            },
            { field: "tipomanutencao", headerName: "Tipo Manutenção", sortable: true, filter: true, width: 150 },
            { field: "situacao", headerName: "Situação", sortable: true, filter: true, width: 120 }
        ];

        // Configurações do Grid
        const gridOptionsIndisponiveis = {
            columnDefs: columnDefs,
            rowData: rowData,
            pagination: true,
            paginationPageSize: 10,
            defaultColDef: {
                flex: 1, // Faz as colunas ocuparem a largura total
                minWidth: 100,
                resizable: true,
            },
            // Tradução para PT-BR (Opcional, mas recomendado)
            localeText: {
                page: 'Página',
                more: 'Mais',
                to: 'a',
                of: 'de',
                next: 'Próximo',
                last: 'Último',
                first: 'Primeiro',
                previous: 'Anterior',
                loadingOoo: 'Carregando...',
                noRowsToShow: 'Nenhum equipamento parado encontrado.',
                filterOoo: 'Filtrar...',
            }
        };

        // Inicializa o Grid
        new agGrid.Grid(gridDivIndisponiveis, gridOptionsIndisponiveis);
    }
});