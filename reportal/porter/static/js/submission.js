let url_array = window.location.pathname.split('/');

let rpk = url_array[url_array.length-2];

// query_param for drf, form_param for form
let current = '/submission/'
let qp = "?report=" + rpk;

let table = $('#datatables').DataTable({
    "ajax": {
        "url": location.origin + '/api' + current + qp,
        "type": "GET",
        "dataSrc": ""
    },
    "columns": [
        {"title": "id", "data": "id"},
        {"title": "uid", "data": "uid"},
        {"title": "group", "data": "report.report_set.group.name"},
        {"title": "report_set", "data": "report.report_set.name"},
        {"title": "report", "data": "report.name"},
        {"title": "template", "data": "template.name"},
        {"title": "submit_date", "data": "submitted_date"},
        {"title": "submit_by", "data": "submitted_by"},
        {"title": "clean", "data": "is_clean"},
    ],
});

$('#new').on('click', function (e) {
    $('#modal-form').attr('action', '/submission/');
    $('#modal_title').text('NEW');
    $("#myModal").modal();
})

$('#previous').on('click', function (e) {
    window.location = location.origin + '/list/';
});