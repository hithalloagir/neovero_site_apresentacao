const AGGridHelper = (function () {
    'use strict';

    /**
     * Configuracao de selecao de linhas (API moderna do AG-Grid)
     * @param {Object} config - Configuracao de selecao
     * @param {boolean} config.multiple - Permitir selecao multipla (default: false)
     * @param {boolean} config.checkboxes - Mostrar checkboxes (default: true quando multiple=true)
     * @param {boolean} config.headerCheckbox - Mostrar checkbox no header (default: true quando multiple=true)
     * @param {boolean} config.enableClickSelection - Permitir selecao ao clicar na linha (default: true)
     * @returns {Object} Objeto com propriedade rowSelection configurada
     */
    function getRowSelectionConfig(config = {}) {
        const multiple = !!config.multiple;
        const checkboxes = config.checkboxes !== undefined ? config.checkboxes : multiple;
        const headerCheckbox = config.headerCheckbox !== undefined ? config.headerCheckbox : multiple;
        const enableClickSelection = config.enableClickSelection ?? true;

        return {
            rowSelection: {
                mode: multiple ? 'multiRow' : 'singleRow',
                enableClickSelection,
                checkboxes,
                headerCheckbox
            }
        };
    }


    function normalizeColumnDefs(columnDefs = []) {
        if (!Array.isArray(columnDefs)) return columnDefs;
        return columnDefs.map(col => {
            const copy = { ...col };
            delete copy.checkboxSelection;
            delete copy.headerCheckboxSelection;
            return copy;
        });
    }

    /**
     * Configurações padrão
     */
    const defaultGridOptions = {
        pagination: true,
        paginationPageSize: 20,
        paginationPageSizeSelector: [10, 20, 50, 100],
        animateRows: true,

        defaultColDef: {
            sortable: true,
            filter: true,
            resizable: true,
            flex: 1,
            minWidth: 100,
            // menuTabs: ['generalMenuTab', 'filterMenuTab', 'columnsMenuTab']
        },

        // Seleção padrão
        ...getRowSelectionConfig(),

        localeText: window.AG_GRID_LOCALE_PT_BR || {}
    };

    const themes = {
        quartz: 'ag-theme-quartz',
        alpine: 'ag-theme-alpine',
        balham: 'ag-theme-balham',
        material: 'ag-theme-material'
    };

    /**
     * Cria grid
     */
    function createGrid(config) {
        if (!config || !config.container) throw new Error('Container é obrigatório');
        if (!config.rowData) throw new Error('rowData é obrigatório');
        if (!config.columnDefs) throw new Error('columnDefs é obrigatório');

        const container =
            typeof config.container === 'string'
                ? document.querySelector(config.container)
                : config.container;

        if (!container) throw new Error('Container não encontrado');

        // Aplicar tema
        const theme = themes[config.theme] || themes.quartz;
        if (!container.classList.contains(theme)) container.classList.add(theme);

        container.style.height = config.height || '500px';

        // Auto-size columns
        let autoSizeStrategy;
        if (config.autoSizeColumns !== false) {
            autoSizeStrategy =
                typeof config.autoSizeColumns === 'object'
                    ? config.autoSizeColumns
                    : { type: 'fitCellContents', defaultMinWidth: 100 };
        }

        const gridOptions = {
            ...defaultGridOptions,
            ...getRowSelectionConfig(config.rowSelection),
            rowData: config.rowData,
            columnDefs: normalizeColumnDefs(config.columnDefs),
            ...(autoSizeStrategy && { autoSizeStrategy }),
            ...(config.gridOptions || {})
        };

        // Criar grid
        const gridApi = agGrid.createGrid(container, gridOptions);

        // API simplificada
        return {
            api: gridApi,

            setData(newData) {
                if (typeof gridApi.setRowData === 'function') {
                    gridApi.setRowData(newData);
                }
            },

            updateData(transaction) {
                return gridApi.applyTransaction(transaction);
            },

            getSelectedRows() {
                return gridApi.getSelectedRows();
            },

            getAllData() {
                const all = [];
                gridApi.forEachNode(node => all.push(node.data));
                return all;
            },

            exportToCsv(filename) {
                gridApi.exportDataAsCsv({ fileName: filename || 'export.csv' });
            },

            quickFilter(text) {
                gridApi.setGridOption('quickFilterText', text);
            },

            clearFilters() {
                gridApi.setFilterModel(null);
            },

            autoSizeColumns() {
                if (gridApi.columnApi?.autoSizeAllColumns) {
                    gridApi.columnApi.autoSizeAllColumns();
                } else if (typeof gridApi.sizeColumnsToFit === 'function') {
                    gridApi.sizeColumnsToFit();
                }
            },

            destroy() {
                gridApi.destroy();
            }
        };
    }

    /**
     * Formatadores de coluna
     */
    const columnFormatters = {
        currency: {
            valueFormatter: p =>
                p.value == null
                    ? ''
                    : new Intl.NumberFormat('pt-BR', { style: 'currency', currency: 'BRL' }).format(p.value)
        },
        date: {
            valueFormatter: p => {
                if (!p.value) return '';
                const [year, month, day] = p.value.split('-');
                return new Date(year, month - 1, day).toLocaleDateString('pt-BR');
            }
        },
        datetime: {
            valueFormatter: p =>
                !p.value ? '' : new Date(p.value).toLocaleString('pt-BR')
        },
        percentage: {
            valueFormatter: p => (p.value == null ? '' : `${p.value}%`)
        },
        number: {
            valueFormatter: p =>
                p.value == null ? '' : new Intl.NumberFormat('pt-BR').format(p.value)
        },
        boolean: {
            valueFormatter: p =>
                p.value == null ? '' : p.value ? 'Sim' : 'Não'
        }
    };

    return { createGrid, columnFormatters, themes, defaultGridOptions };
})();

window.AGGridHelper = AGGridHelper;
