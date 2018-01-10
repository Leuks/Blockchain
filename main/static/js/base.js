function addNode(){
    var id = $("#node_id").val();
    var version = $("#node_version").val();
    var check = $("#check:checked").length;
    if(id) {
        $.post("http://127.0.0.1:8000/p2p/NN/", {id: id, version: version, hacked : check}, function (data) {
            $("#new_node_modal").modal('hide');
            $("#node_id").val("");
            location.reload();
        });
    }
}

function makeSimulation(){
    var nodes_count = $("#nodes_count").val();
    var transactions_count = $("#transactions_count").val();
    if(nodes_count && transactions_count) {
        $.post("http://127.0.0.1:8000/p2p/NS/", {nodes_count: nodes_count, transactions_count: transactions_count}, function (data) {
            $("#new_simulation_modal").modal('hide');
            $("#nodes_count").val("");
            $("#transactions_count").val("");
            location.reload();
        });
    }
}

function addTransaction(){
    var from = $("#input_from").val();
    var to = $("#input_to").val();
    var kind = $("#input_kind").val();

    $.post("http://127.0.0.1:8000/p2p/NT/", {from: from, to: to, kind: kind.toString() }, function (data) {
        $("#new_transaction_modal").modal('hide')
        location.reload();
    });
}

function clearNetwork(){
    $.post("http://127.0.0.1:8000/p2p/CN/");
    location.reload();
}


