let table = $('#datatables').DataTable({
    "processing": true,
    "serverSide": true,
    "ajax": {
        "url": location.origin + "/api/reportset/",
        "type": "GET",  
    },
    "columns": [
        {"data": "id"},
        {"data": "name"},
        {"data": "group.id"},
        {"data": "group.name"},
        {"data": "create_date"},
        {"data": "create_by.username"},
        {"data": "last_modify_date"},
        {
            "data": null,
            "defaultContent": '<button type="button" class="btn btn-info">Edit</button>' + '&nbsp;&nbsp' + 
            '<button type="button" class="btn btn-danger">Delete</button>'
        }
    ],
    "columnDefs": [
        {
            // hide Group ID
            "targets": [ 2 ],
            "visible": false,
            "searchable": false
        }
    ]
});

let id = 0;

$('#datatables tbody').on('click', 'button', function () {
    let data = table.row($(this).parents('tr')).data();
    
    let class_name = $(this).attr('class');
    if (class_name == 'btn btn-info') {
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
function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
$('#confirm').on('click', '#delete', function (e) {
    $.ajax({
        url: location.origin + '/api/reportset/' + id + '/',
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