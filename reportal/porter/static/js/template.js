let api_url = "/api" + window.location.pathname;
var url = $(location).attr('href');
var split_url = url.split("/"); // revise this part or find better ways to direct filter
console.log(split_url[1]);
console.log(api_url);
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
        window.location = location + data['id'] + '/'
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