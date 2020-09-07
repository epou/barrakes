
    let only_pending = {% if only_pending == 'true' %}true{% else %}false{% endif %}
    let inverse_order = {% if inverse_order == 'true' %}true{% else %}false{% endif %}

    $('#order_container').on("click", 'a.dropdown-item', function(e) {

            // Stop propagation to avoid show the modal.
            if (!e) var e = window.event;
                e.cancelBubble = true;
            if (e.stopPropagation) e.stopPropagation();

            let order_id = $(this).closest(".jquery-btn-status").data("index");
            let new_status = $(this).data('value')

            if (new_status === 'cancelled'){
                let result = confirm("Estàs segur que vols cancel·lar la comanda?")
                if (result === false){
                    return
                }
            }

            request = {
                order_id: order_id,
                status: new_status,
                return_only_pending: only_pending,
                return_inverse_order: inverse_order
            }

            $.ajaxSetup({
                beforeSend: function(xhr) {
                    xhr.setRequestHeader('X-CSRFToken', getCookie("csrftoken"));
                }
            });

           $.ajax({
               url: "{% url 'change_order_status' %}",
               type: "POST",
               dataType: 'json',
               data: {data: JSON.stringify(request)},

               success: function(data) {
                   console.log("success")
                   $('#order_container').html(data.orders)
                   $('#num_finished_orders').html(data.num_finished_orders)
                   $('#num_pending_orders').html(data.num_pending_orders)
               },

               error: function(xhr,errmsg,err) {
                    console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
                }
           });
        });

    $(function(){
        $('#modal_aside_left').modal({
            keyboard: true,
            backdrop: true,
            show: false,
        }).on('show.bs.modal', function(){ //subscribe to show method
            let getIdFromRow = $(event.target).closest('tr').attr('id'); //get the id from tr
            //make your ajax call populate items or what even you need
            $.ajax({
               url: "{% url 'ajax_order_items' %}" + '?order_id=' + getIdFromRow,
               type: "GET",
               dataType: 'json',
               success: function(data) {
                   console.log("success")
                   $('#modal_aside_left').html(data.modal)
               },

               error: function(xhr,errmsg,err) {
                    console.log(xhr.status + ": " + errmsg); // provide a bit more info about the error to the console
                }
           });
            $(this).find("#command_id").text(getIdFromRow)
        });
    });

    function autoloader(){
        let current_search = window.location.search.split("?")[1]
        let query_parameters = [
            'return_only_pending='+only_pending,
            'return_inverse_order='+inverse_order,
            current_search
        ]
        $.ajax({
               url: "{% url 'ajax_order_list' %}" + '?' + query_parameters.join("&"),
               type: "GET",
               dataType: 'json',
               success: function(data) {
                   console.log("success")
                   $('#order_container').html(data.orders)
                   $('#num_finished_orders').html(data.num_finished_orders)
                   $('#num_pending_orders').html(data.num_pending_orders)
               },

               error: function(xhr,errmsg,err) {
                    console.log(xhr.status + ": " + errmsg); // provide a bit more info about the error to the console
                }
           });
    }
    setInterval(function (){
        if (document.hidden === false) {
            autoloader();
        }
    }, 10000)