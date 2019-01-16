let url_array = window.location.pathname.split('/');
console.log(url_array);
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

console.log(spk, pk);
// query_param for drf, form_param for form
let current = '/ruleset/'
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
        {"title": "field", "data": "field.name"},
        {"title": "rule", "data": "rule.name"},
        {"title": "argument", "data": "argument"},
        {"title": "action", "data": "action"},
        {"title": "error_message", "data": "error_message"},
        {"title": "field_id", "data": "field.id"},
        {"title": "rule_id", "data": "rule.id"},
        {
            "title": "option", 
            "data": null,
            "defaultContent": '<div class="btn-group dropright" id="btn-dropdown">' + 
            '<button class="btn btn-info btn-sm dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Option</button>' + 
            '<div class="dropdown-menu" aria-labelledby="dropdownMenuButton">' + 
            '<a class="dropdown-item" id="btn-edit" href="#">Edit</a>' + 
            '<a class="dropdown-item" id="btn-duplicate" href="#">Duplicate</a>' + 
            '<a class="dropdown-item" id="btn-delete"href="#">Delete</a>' +
            '</div></div>'
        }
    ],
    "columnDefs": [
        // hide ID columns
        {
            "targets": [ 6 ],
            "visible": false,
            "searchable": false
        },
        {
            
            "targets": [ 7 ],
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
    if (id_name == 'btn-edit') {
        // EDIT button
        $('#id_field').val(data['field']['id']);
        $('#id_rule').val(data['rule']['id']);
        $('#id_argument').val(data['argument']);
        $('#id_action').val(data['action']);
        $('#id_error_message').val(data['error_message']);
        // bind item id to url
        $('#modal-form').attr('action', fp + id + '/');
        $('#myModal').modal();
    } else if (id_name == 'btn-duplicate') {
        // DUPLICATE button
        $('#id_field').val(data['field']['id']);
        $('#id_rule').val(data['rule']['id']);
        $('#id_argument').val(data['argument']);
        $('#id_action').val(data['action']);
        $('#id_error_message').val(data['error_message']);
        // do not bind item id to create a new record with same values
        $('#modal-form').attr('action', fp);
        $('#modal-form').submit();        
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
    $('#id_field').val('');
    $('#id_rule').val('');
    $('#id_argument').val('');
    $('#id_action').val('');
    $('#id_error_message').val('');
    $('#modal-form').attr('action', fp);
    $('#modal_title').text('NEW');
    $("#myModal").modal();
});

$('#import').on('click', function (e) {
    $('#import_modal_title').text('IMPORT');
    $("#importModal").modal();
});

$('#previous').on('click', function (e) {
    window.location = location.origin + '/template/' + rspk;
});