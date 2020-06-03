
function clickCreateCustomOrder() {

    $.ajax({
        type: "POST",
        url: "/orders/",
        data: {
            'name': $('#custom_order_project').val(),
            'invoice': $('#custom_order_invoice').val(),
            'cargo': $('#custom_order_cargo').val(),
            'status': $('#custom_order_status').val(),
            'sender': $('#custom_order_sender').val(),
            'receiver': $('#custom_order_receiver').val(),
            'document': $('#custom_order_document').val(),
            'carrier': $('#custom_order_carrier').val(),
            'ttn': $('#custom_order_ttn').val()
        },
        
        success: function(response) {
            console.log('success')
    
        },
        error: function(error) {
            console.log(error);
        }
    });
}



function clickCreateManager() {

    $.ajax({
        type: "POST",
        url: "/managers/create",
        data: {
            'name': $('#manager-name').val(),
            'small_name': $('#manager-small-name').val(),
            'number_phone': $('#manager-number-phone').val()
        },
        
        success: function(response) {
            console.log('success')
    
        },
        error: function(error) {
            console.log(error);
        }
    });
}

function clickCreateProject() {

    $.ajax({
        type: "POST",
        url: "/projects/create",
        data: {
            'name': $('#project-name').val(),
            'manager_small_name': $('#manager-small-name').val(),
            'customer': $('#customer').val()
        },
        
        success: function(response) {
            console.log('success')
    
        },
        error: function(error) {
            console.log(error);
        }
    });
}




