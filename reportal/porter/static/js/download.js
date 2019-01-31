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
        {"title": "upload", "data": "upload"},
        {"title": "template", "data": "template.name"},
        {"title": "submit_date", "data": "submitted_date"},
        {"title": "submit_by", "data": "submitted_by.username"},
        {"title": "clean", "data": "is_clean"},
    ],
});

$('#previous').on('click', function (e) {
    window.location = location.origin + '/list/';
});

