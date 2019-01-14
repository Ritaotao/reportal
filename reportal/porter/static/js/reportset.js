let api_url = "/api/reportset/";

let table = $('#datatables').DataTable({
    "ajax": {
        "url": location.origin + api_url,
        "type": "GET",
        "dataSrc": ""
    },
    "columns": [
        {"title": "id", "data": "id"},
        {"title": "name", "data": "name"},
        {"title": "group", "data": "group.name"},
        {"title": "create_date", "data": "create_date"},
        {"title": "create_by", "data": "create_by.username"},
        {"title": "last_modify_date", "data": "last_modify_date"},
        {"title": "group_id", "data": "group.id"},
        {
            "title": "action",
            "data": null,
            "defaultContent": '<div class="btn-group dropright" id="btn-dropdown">' + 
            '<button class="btn btn-info btn-sm dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Option</button>' + 
            '<div class="dropdown-menu" aria-labelledby="dropdownMenuButton">' + 
            '<a class="dropdown-item" id="btn-template" href="#">Templates</a>' + 
            '<a class="dropdown-item" id="btn-report" href="#">Reports</a>' + 
            '<a class="dropdown-item" id="btn-edit" href="#">Edit</a>' + 
            '<a class="dropdown-item" id="btn-delete" href="#">Delete</a>' +
            '</div></div>'
        }
    ],
    "columnDefs": [
        {
            // hide Group ID
            "targets": [ 6 ],
            "visible": false,
            "searchable": false
        }
    ]
});

let id = 0;

$('#datatables tbody').on('click', 'a', function () {
    let data = table.row($(this).parents('tr')).data();
    id = data['id'];

    let id_name = $(this).attr("id");
    if (id_name == 'btn-template') {
        // REPORT button
        window.location = location.origin + '/template/' + id + '/'; 
    } else if (id_name == 'btn-report') {
        // TEMPLATE button
        window.location = location.origin + '/report/' + id + '/';
    } else if (id_name == 'btn-edit') {
        // EDIT button
        $('#id_name').val(data['name']);
        $('#id_group').val(data['group']['id']);
        // bind item id to url
        $('#modal-form').attr('action', '/reportset/' + id + '/');
        $('#modal_title').text('EDIT');
        $('#myModal').modal();
    } else {
        // DELETE button
        $('#modal_title').text('DELETE');
        $('#confirm').modal();
    }
});

$('#confirm').on('click', '#delete', function (e) {
    $('#modal-form').attr('action', '');
    $.ajax({
        url: location.origin + api_url + id + '/',
        method: 'DELETE',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        },
        success: function (data, textStatus, jqXHR) {
            window.location = location.origin + '/reportset/'; 
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.log(jqXHR);
        },
    });
});

$('#new').on('click', function (e) {
    $('#id_name').val('');
    $('#id_group').val('');
    $('#modal-form').attr('action', '/reportset/');
    $('#modal_title').text('NEW');
    $("#myModal").modal();
})

$('#previous').on('click', function (e) {
    window.location = location.origin;
});