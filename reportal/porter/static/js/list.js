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
            "defaultContent": '<div class="btn-group dropright" id="btn-dropdown">' + 
            '<button class="btn btn-md dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"><span class="fa fa-edit"></span></button>' + 
            '<div class="dropdown-menu" aria-labelledby="dropdownMenuButton">' + 
            '<a class="dropdown-item" id="btn-submit" href="#"><span class="fa fa-save"></span> Submit</a>' + 
            '<a class="dropdown-item" id="btn-download" href="#"><span class="fa fa-download"></span> Download</a>' + 
            '</div></div>'
        }
    ],
});

let id = 0;

$('#datatables tbody').on('click', 'a', function () {
    let data = table.row($(this).parents('tr')).data();
    id = data['id'];

    let id_name = $(this).attr("id");
    if (id_name == 'btn-submit') {
        // Go to Submit page for that report
        window.location = location.origin + '/submission/' + id + '/'; 
    } else if (id_name == 'btn-download') {
        // DUPLICATE button
        window.location = location.origin + '/download/' + id + '/'; 
    }
});


$('#previous').on('click', function (e) {
    window.location = location.origin;
});