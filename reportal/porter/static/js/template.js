let url_array = window.location.pathname.split('/');

let api_url = "/api/template/?report_set=" + url_array[url_array.length-2];

let table = $('#datatables').DataTable({
    "ajax": {
        "url": location.origin + api_url,
        "type": "GET",
        "dataSrc": ""
    },
    "columns": [
        {"data": "id"},
        {"data": "name"},
        {"data": "uid"},
        {"data": "create_date"},
        {"data": "create_by.username"},
        {"data": "last_modify_date"},
        {
            "data": null,
            "defaultContent": '<button type="button" class="btn btn-success">Go</button>' + '&nbsp;&nbsp' + 
                '<button type="button" class="btn btn-info">Edit</button>' + '&nbsp;&nbsp' + 
            '<button type="button" class="btn btn-danger">Delete</button>'
        }
    ],
});

let id = 0;

$('#datatables tbody').on('click', 'button', function () {
    let data = table.row($(this).parents('tr')).data();
    
    let class_name = $(this).attr('class');
    if (class_name == 'btn btn-success') {
        // GO button
        window.location = location.origin + '/field/' + data['id']
    } else if (class_name == 'btn btn-info') {
        // EDIT button
        $('#id_name').val(data['name']);
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
    $('#type').val('new');
    $('#modal_title').text('NEW');
    $("#myModal").modal();
})