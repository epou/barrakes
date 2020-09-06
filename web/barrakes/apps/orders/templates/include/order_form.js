let orderList = [];
        let total_price = 0.00;

        const input_seat_number = $("#input_seat_number");
        const receipt_seat_number = $("#receipt_seat_number");

        const payment_method = $("input:radio[name='payment-method']");
        const cash_div_input_import = $("div#cash_import");
        const cash_input_import = $("input#cash_import");
        const comment_input = $("textarea#comment")

        const button_send = $("#buttonSend")

        function updateFinishButton() {
            if (check_all_variables()) {
                button_send.prop("disabled", false);
            } else {
                button_send.prop("disabled", "disabled");
            }

        }


        button_send.click(function(event) {
           console.log("form submitted!");
           event.preventDefault();

           let new_order = {
                   seat_number: input_seat_number.val(),
                   payment_method: $("input:radio[name='payment-method']:checked").val(),
                   payment_amount: cash_input_import.val(),
                   comment: comment_input.val(),
                   items: []
           }
           for (let i=0; i < orderList.length; i++) {
               new_order.items.push(
                   {
                       product_id: orderList[i].product.id,
                       quantity: orderList[i].quantity
                   }
               )
           }

           $.ajaxSetup({
                beforeSend: function(xhr) {
                    xhr.setRequestHeader('X-CSRFToken', getCookie("csrftoken"));
                }
            });

           $.ajax({
               url: "{% url 'ajax_new_order' %}",
               type: "POST",
               dataType: 'json',
               data: {order: JSON.stringify(new_order)},
               success: function(json) {
                   console.log("success");
                   window.location.href = json.href;
               },

               error: function(xhr,errmsg,err) {
                    console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
                }
           });
        });

        input_seat_number.keyup(function() {
            $(this).val(parseInt($(this).val(), 10))
            if ($(this).val() > 0) {
                receipt_seat_number.text(parseInt($(this).val(), 10))
                $(this).addClass("is-valid");
                $(this).removeClass("is-invalid");
            } else {
                receipt_seat_number.text("###")
                $(this).removeClass("is-valid");
                $(this).addClass("is-invalid");
            }
            updateFinishButton();
        });

        payment_method.change(function () {
            if ($(this).val() === "cash") {
                cash_div_input_import.slideDown();
            } else {
                cash_div_input_import.slideUp();
            }
            updateFinishButton();
        });

        cash_input_import.keyup(function(){
            if (parseFloat($(this).val()) < total_price) {
                $(this).removeClass("is-valid");
                $(this).addClass("is-invalid");
            } else {
                $(this).removeClass("is-invalid");
                $(this).addClass("is-valid");
            }
            updateFinishButton();
        });

        function check_all_variables() {
            let result = false;

            if (orderList.length > 0 && payment_method.is(':checked') && input_seat_number.val() !== '' && input_seat_number.val() > 0){
                if ($("input:radio[name='payment-method']:checked").val() === "cash") {
                    if (parseFloat(cash_input_import.val()) >= total_price) {
                        result = true;
                    }
                } else {
                    result = true;
                }

            }

            return result;
        }

        $('.counter-btn').click(function(e) {
            e.preventDefault();
            let $btn = $(this);
            $('#output-' + $btn.data('index')).val(function(i, val) {
                val = val * 1 + $btn.data('inc');
                // Disable substract button if val <= 0
                if (val <= 0){
                    $('#btn-substract-' + $btn.data('index')).prop("disabled", "disabled")
                } else {
                    $('#btn-substract-' + $btn.data('index')).prop("disabled", false)
                }

                let price = parseFloat($('#product_price-' + $btn.data('index')).data('value')) * val;
                updateOrderItemArray(
                    {
                        "quantity": val,
                        "product": {
                            "id": $btn.data('index'),
                            "name": $('#product_name-' + $btn.data('index')).text()
                        },
                        "price": price.toFixed(2)
                    }
                );
                updateOrderItemListTable();
                updateFinishButton();
                updateTotalPrice();
                return (val <= 0 ? '0' : val);
            });
        });



        function updateTotalPrice() {
            total_price = orderList.reduce((total, current) => total + parseFloat(current.price), 0).toFixed(2);
            $('#total_price').text(total_price);
        }

        function updateOrderItemArray(obj) {
            const index = orderList.findIndex((e) => e.product.id === obj.product.id);

            if (index === -1) {
                orderList.push(obj)
            } else {
                if (obj.quantity === 0) {
                    orderList.splice(index, 1)
                } else {
                    orderList[index] = obj
                }
            }
        }

        function updateOrderItemListTable(){
            let html = '';
            for (let i=0; i < orderList.length; i++) {
                html +='<tr class="text-center">'
                    +'<td>' + orderList[i].quantity + '</td>'
                    +'<td>' + orderList[i].product.name + '</td>'
                    +'<td>' + orderList[i].price + ' €</td>'
                    +'</tr>';
            }
            $('#orderListTableBody').html(html);
        }