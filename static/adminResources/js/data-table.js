(function ($) {
    'use strict';
    $(function () {
        $('#order-listing').DataTable({
            "aLengthMenu": [
                [5, 10, 15, -1],
                [5, 10, 15, "All"]
            ],
            "iDisplayLength": 10,
            "language": {
                search: ""
            }
        });
        $('#order-listing').each(function () {
            var datatable = $(this);
            // SEARCH - Add the placeholder for Search and Turn this into in-line form control
            var search_input = datatable.closest('.dataTables_wrapper').find('div[id$=_filter] input');
            search_input.attr('placeholder', 'Search');
            search_input.removeClass('form-control-sm');
            // LENGTH - Inline-Form control
            var length_sel = datatable.closest('.dataTables_wrapper').find('div[id$=_length] select');
            length_sel.removeClass('form-control-sm');
        });
    });

    $(document).ready(function () {

        // create a data table
        var table = $('#order-listing').DataTable();

        // add custom listener to draw event on the table
        table.on("draw", function () {
            // get the search keyword
            var keyword = $('#my-table_filter > label:eq(0) > input').val();

            // clear all the previous highlighting
            $('#order-listing').unmark();

            // highlight the searched word
            $('#order-listing').mark(keyword, {});
        });

    });


})(jQuery);

