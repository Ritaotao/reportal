let url_array = window.location.pathname.split('/');

let spk = "";
let pk = "";
if (url_array.length == 5) {
    spk = url_array[url_array.length-3];
    pk = url_array[url_array.length-2];
} else {
    spk = url_array[url_array.length-2];
}

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
        {"title": "templates", "data": "templates[, ].name"},
        {"title": "create_date", "data": "create_date"},
        {"title": "create_by", "data": "create_by.username"},
        {"title": "last_modify_date", "data": "last_modify_date"},
        {"title": "template_ids", "data": "templates[, ].id"},
        {
            "title": "option", 
            "data": null,
            "defaultContent": '<div class="btn-group dropright" id="btn-dropdown">' + 
            '<button class="btn btn-md dropdown-toggle" type="button" id="dropdownMenuButton" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false"><span class="fa fa-edit"></span></button>' + 
            '<div class="dropdown-menu" aria-labelledby="dropdownMenuButton">' + 
            '<a class="dropdown-item" id="btn-edit" href="#"><span class="fa fa-pencil"></span> Edit</a>' + 
            '<a class="dropdown-item" id="btn-dup" href="#"><span class="fa fa-copy"></span> Duplicate</a>' + 
            '<a class="dropdown-item" id="btn-delete"href="#"><span class="fa fa-trash-o"></span> Delete</a>' +
            '</div></div>'
        }
    ],
    "columnDefs": [
        {
            // hide Tempalte IDs
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
    if (id_name == 'btn-delete') {
        // DELETE button
        $('#confirm').modal();
    } else {
        // get template ids for manytomany field
        var template_ids = [];
        var templates = data['templates'];
        for (var i = 0; i < templates.length; i++) {
            template_ids.push(templates[i]['id']);
        }
        // fill form  
        $('#id_method').val(data['method']);
        $('#id_templates').val(template_ids);   
        if (id_name == 'btn-edit') {
            // edit: bind pk to url
            $('#id_name').val(data['name']);
            $('#modal-form').attr('action', fp + id + '/');
            $('#modal_title').text('EDIT');
            $('#myModal').modal();
        } else {
            // duplicate: submit form without id
            var dt = new Date().getTime();
            $('#id_name').val(data['name'] + '_' + dt);
            $('#modal-form').attr('action', fp);
            $('#modal-form').submit();
        }
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