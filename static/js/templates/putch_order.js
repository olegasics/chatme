function clickSave(order_id) {
    var $projectName = $('#project-name-' + order_id)
    var $invoice = $('#invoice-' + order_id)
    var $ttn = $('#ttn-' + order_id)
    var $saveBtn = $('#save-order-' + order_id)
    var $editBtn = $('#edit-order-' + order_id)
    var $cargo = $('#cargo-' + order_id)
    // alert(projectName + invoice + ttn);

    $.ajax({
        type: "PATCH",
        url: "/orders/" + order_id,
        data: {
            'name': $projectName.val(),
            'invoice': $invoice.val(), 
            'ttn': $ttn.val(),
            'cargo': $cargo.val()
        },
        
        success: function(response) {
            $projectName.prop('disabled', true)
            $invoice.prop('disabled', true)
            $ttn.prop('disabled', true)
            $cargo.prop('disabled', true)
            $saveBtn.prop('hidden', true)
            $editBtn.prop('hidden', false)

        },
        error: function(error) {
            console.log(error);
        }
    });
    
    
}
    
function clickEdit(order_id) {
    var $projectName = $('#project-name-' + order_id)
    var $invoice = $('#invoice-' + order_id)
    var $ttn = $('#ttn-' + order_id)
    var $editBtn = $('#edit-order-' + order_id)
    var $saveBtn = $('#save-order-' + order_id)
    var $cargo = $('#cargo-' + order_id)

    $projectName.prop('disabled', false)
    $invoice.prop('disabled', false)
    $ttn.prop('disabled', false)
    $cargo.prop('disabled', false)
    $editBtn.prop('hidden', true)
    $saveBtn.prop('hidden', false)


}

