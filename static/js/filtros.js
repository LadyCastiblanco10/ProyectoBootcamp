$(document).ready(function () {

    const tabla = $('#tablaDatos').DataTable({
        initComplete: function () {
            let api = this.api();

            // Función para cargar cualquier filtro dinámico
            function cargarFiltro(columnaIndex, elementoID) {
                let select = $(elementoID);

                api.column(columnaIndex).data().unique().sort().each(function (d) {
                    if (d !== null && d !== undefined && d !== "")
                        select.append(`<option value="${d}">${d}</option>`);
                });

                select.on("change", function () {
                    let val = $.fn.dataTable.util.escapeRegex($(this).val());
                    api.column(columnaIndex)
                        .search(val ? '^' + val + '$' : '', true, false)
                        .draw();
                });
            }

            // Asignación de filtros dinámicos
            cargarFiltro(2, "#filtroSexoVictima"); // columna sexo víctima
            cargarFiltro(4, "#filtroAgresor");     // columna relación agresor
        }
    });
});
