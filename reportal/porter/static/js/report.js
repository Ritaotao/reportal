let url_array = window.location.pathname.split('/');
console.log(url_array);
let spk = "";
let pk = "";
if (url_array.length == 5) {
    spk = url_array[url_array.length-3];
    pk = url_array[url_array.length-2];
} else {
    spk = url_array[url_array.length-2];
}

console.log(spk, pk);
// query_param for drf, form_param for form
let current = '/report/'
let qp = "?report_set=" + spk;
let fp = current + spk + '/';

let table = $('#datatables').DataTable({
    "ajax": {
        "url": location.origin + '/api' + current + qp,
        "type": "GET",
        "dataSrc": ""
    },
    "columns": [
        {"title": "id", "data": "id"},
        {"title": "name", "data": "name"},
        {"title": "method", "data": "method"},
        {"title": "templates", "data": "templates"},
        {"title": "create_date", "data": "create_date"},
        {"title": "create_by", "data": "create_by.username"},
        {"title": "last_modify_date", "data": "last_modify_date"},
        {
            "title": "action", 
            "data": null,
            "defaultContent": '<div class="btn-group dropright" id="btn-dropdown">' + 
            '<button class="btn btn-info btn-sm dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Option</button>' + 
            '<div class="dropdown-menu" aria-labelledby="dropdownMenuButton">' + 
            '<a class="dropdown-item" id="btn-go" href="#">Detail</a>' + 
            '<a class="dropdown-item" id="btn-edit" href="#">Edit</a>' + 
            '<a class="dropdown-item" id="btn-delete"href="#">Delete</a>' +
            '</div></div>'
        }
    ],
});

let id = 0;

$('#datatables tbody').on('click', 'a', function () {
    let data = table.row($(this).parents('tr')).data();
    id = data['id'];
    console.log(data['templates']);
    let id_name = $(this).attr("id");
    if (id_name == 'btn-go') {
        // GO button
        // window.location = location.origin + '/quality/' + spk + '/' + id; 
    } else if (id_name == 'btn-edit') {
        // EDIT button
        $('#id_name').val(data['name']);
        $('#id_method').val(data['method']);
        $('#id_templates').val(data['templates']);
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
    $('#id_method').val('');
    $('#id_templates').val('');
    $('#modal-form').attr('action', fp);
    $('#modal_title').text('NEW');
    $("#myModal").modal();
});

$('#previous').on('click', function (e) {
    window.location = location.origin + '/reportset/';
});