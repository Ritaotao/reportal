let api_url = "/api" + window.location.pathname;

let table = $('#datatables').DataTable({
    "ajax": {
        "url": location.origin + api_url,
        "type": "GET",
        "dataSrc": ""
    },
    "columns": [
        {"data": "id"},
        {"data": "name"},
        {"data": "group.name"},
        {"data": "create_date"},
        {"data": "create_by.username"},
        {"data": "last_modify_date"},
        {"data": "group.id"},
        {
            "data": null,
            "defaultContent": '<button type="button" class="btn btn-success">Go</button>' + '&nbsp;&nbsp' + 
                '<button type="button" class="btn btn-info">Edit</button>' + '&nbsp;&nbsp' + 
            '<button type="button" class="btn btn-danger">Delete</button>'
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

$('#datatables tbody').on('click', 'button', function () {
    let data = table.row($(this).parents('tr')).data();
    
    let class_name = $(this).attr('class');
    if (class_name == 'btn btn-success') {
        // GO button
        window.location = location.origin + '/template/' + data['id']
    } else if (class_name == 'btn btn-info') {
        // EDIT button
        $('#id_name').val(data['name']);
        $('#id_group').val(data['group']['id']);
        $('#type').val('edit');
        $('#modal_title').text('EDIT');
        $('#myModal').modal();
    } else {
        // DELETE button
        $('#modal_title').text('DELETE');
        $('#confirm').modal();
    }

    id = data['id'];
});

$('#confirm').on('click', '#delete', function (e) {
    $.ajax({
        url: location.origin + api_url + id + '/',
        method: 'DELETE',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        },
        success: function (data, textStatus, jqXHR) {
            location.reload();
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.log(jqXHR);
        },
    });
});

$('#new').on('click', function (e) {
    $('#id_name').val('');
    $('#id_group').val(1);
    $('#type').val('new');
    $('#modal_title').text('NEW');
    $("#myModal").modal();
})