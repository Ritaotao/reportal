let api_url = "/api/template/"

let url_array = window.location.pathname.split('/');
console.log(url_array);
let rspk = "";
let pk = "";
if (url_array.length == 5) {
    rspk = url_array[url_array.length-3];
    pk = url_array[url_array.length-2];
} else {
    rspk = url_array[url_array.length-2];
}

console.log(rspk, pk);
// query_param for drf
let qp = "?report_set=" + rspk;

let table = $('#datatables').DataTable({
    "ajax": {
        "url": location.origin + api_url + qp,
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
            "defaultContent": '<div class="btn-group dropright" id="btn-dropdown">' + 
            '<button class="btn btn-info btn-sm dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">Option</button>' + 
            '<div class="dropdown-menu" aria-labelledby="dropdownMenuButton">' + 
            '<a class="dropdown-item" id="btn-go" href="#">Go</a>' + 
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

    let id_name = $(this).attr("id");
    if (id_name == 'btn-go') {
        // GO button
        window.location = location.origin + '/field/' + id; 
    } else if (id_name == 'btn-edit') {
        // EDIT button
        $('#id_name').val(data['name']);
        // bind item id to url
        $('#modal-form').attr('action', '/template/' + rspk + '/' + id + '/');
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
        url: location.origin + api_url + id + '/' + qp,
        method: 'DELETE',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        },
        success: function (data, textStatus, jqXHR) {
            window.location = location.origin + '/template/' + rspk + '/'; 
        },
        error: function (jqXHR, textStatus, errorThrown) {
            console.log(jqXHR);
        },
    });
});

$('#new').on('click', function (e) {
    $('#id_name').val('');
    $('#modal-form').attr('action', '/template/' + rspk +'/');
    $('#modal_title').text('NEW');
    $("#myModal").modal();
})