let url_array = window.location.pathname.split('/');

let rspk = '';
let spk = '';
let pk = '';
if (url_array.length == 6) {
    rspk = url_array[url_array.length-4];
    spk = url_array[url_array.length-3];
    pk = url_array[url_array.length-2];
} else {
    rspk = url_array[url_array.length-3];
    spk = url_array[url_array.length-2];
}

// query_param for drf, form_param for form
let current = '/field/'
let qp = '?template=' + spk;
let fp = current + rspk + '/' + spk + '/';

let table = $('#datatables').DataTable({
    "ajax": {
        "url": location.origin + '/api' + current + qp,
        "type": "GET",
        "dataSrc": ""
    },
    "columns": [
        {"title": "id", "data": "id"},
        {"title": "name", "data": "name"},
        {"title": "data_type", "data": "dtype"},
        {
            "title": "option", 
            "data": null,
            "defaultContent": '<div class="btn-group dropright" id="btn-dropdown">' + 
            '<button class="btn btn-md dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"><span class="fa fa-edit"></span></button>' + 
            '<div class="dropdown-menu" aria-labelledby="dropdownMenuButton">' + 
            '<a class="dropdown-item" id="btn-edit" href="#"><span class="fa fa-pencil"></span> Edit</a>' + 
            '<a class="dropdown-item" id="btn-delete"href="#"><span class="fa fa-trash-o"></span> Delete</a>' +
            '</div></div>'
        }
    ],
});

let id = 0;

$('#datatables tbody').on('click', 'a', function () {
    let data = table.row($(this).parents('tr')).data();
    id = data['id'];

    let id_name = $(this).attr("id");
    if (id_name == 'btn-edit') {
        // EDIT button
        $('#id_name').val(data['name']);
        $('#id_dtype').val(data['dtype']);
        $('#modal_title').text('EDIT');
        // bind item id to url
        $('#modal-form').attr('action', fp + id + '/');
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
        url: location.origin + '/api' + current + id + '/' + qp,
        method: 'DELETE',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        },
        success: function (data, textStatus, jqXHR) {
            window.location = location.origin + fp; 
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.log(jqXHR);
        },
    });
});

$('#new').on('click', function (e) {
    $('#id_name').val('');
    $('#id_dtype').val('');
    $('#modal-form').attr('action', fp);
    $('#modal_title').text('NEW');
    $("#myModal").modal();
});

$('#import').on('click', function (e) {
    $('#modal_title').text('IMPORT');
    $("#importModal").modal();
});

$('#previous').on('click', function (e) {
    window.location = location.origin + '/template/' + rspk;
});