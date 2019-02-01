let url_array = window.location.pathname.split('/');

let rpk = url_array[url_array.length-2];

// query_param for drf, form_param for form
let current = '/submission/'
let qp = "?report=" + rpk + '&is_clean=true';
let fp = current + rpk + '/';

let table = $('#datatables').DataTable({
    "ajax": {
        "url": location.origin + '/api' + current + qp,
        "type": "GET",
        "dataSrc": ""
    },
    "columns": [
        {"title": "id", "data": "id"},
        {"title": "template", "data": "template.name"},
        {"title": "file", "data": "name"},
        {"title": "submit_date", "data": "submitted_date"},
        {"title": "submit_by", "data": "submitted_by.username"},
        {
            "title": "option", 
            "data": null,
            "defaultContent": '<button class="btn btn-info btn-sm" type="button" id="btn-download">Download</button>'
        },
    ],
});

$('#datatables tbody').on('click', 'button', function () {
    let data = table.row($(this).parents('tr')).data();
    id = data['id'];

    let id_name = $(this).attr("id");
    if (id_name == 'btn-download') {
        // Download button
        window.location = location.origin + '/download/' + rpk + '/' + id + '/'; 
    }
});

$('#previous').on('click', function (e) {
    window.location = location.origin + '/list/';
});

