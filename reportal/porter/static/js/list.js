let api_url = "/api/report/";

let table = $('#datatables').DataTable({
    "ajax": {
        "url": location.origin + api_url,
        "type": "GET",
        "dataSrc": ""
    },
    "columns": [
        {"title": "id", "data": "id"},
        {"title": "group", "data": "report_set.group.name"},
        {"title": "report_set", "data": "report_set.name"},
        {"title": "report", "data": "name"},
        {"title": "templates", "data": "templates[, ].name"},
        {"title": "create_date", "data": "create_date"},
        {"title": "create_by", "data": "create_by.username"},
        {"title": "last_modify_date", "data": "last_modify_date"},
        {
            "title": "option", 
            "data": null,
            "defaultContent": '<button class="btn btn-info btn-sm" id="btn-go">Go</button>'
        }
    ],
});

$('#datatables tbody').on('click', 'button', function () {
    let data = table.row($(this).parents('tr')).data();
    // GO button
    window.location = location.origin + '/submission/' + data['id'] + '/'; 
});


$('#previous').on('click', function (e) {
    window.location = location.origin;
});