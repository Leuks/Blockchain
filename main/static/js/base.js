function addNode(){
    var id = $("#node_id").val();
    if(id) {
        $.post("http://127.0.0.1:8000/p2p/NN/", {id: id});
        $("#new_node_modal").modal('hide');
        $("#node_id").val("");
    }
}

function addTransaction(){
    var from = $("#input_from").val();
    var to = $("#input_to").val();
    var kind = $("#input_kind").val();

    $.post("http://127.0.0.1:8000/p2p/NT/", {from: from, to: to, kind: kind });
        $("#new_transaction_modal").modal('hide')
}
