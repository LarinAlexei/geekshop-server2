function recalculate_total_values() {
    TOTAL_FORMS = parseInt($('input[name="orderitems-TOTAL_FORMS"]').val());

    var quantities = [];
    var prices = [];

    for(var i = 0; i < TOTAL_FORMS; i++) {
        _quantity = parseInt($('input[name="orderitems-' + i + '-quantity"]').val());
        _price = parseFloat($('.orderitems-' + i + '-price').text().replace(',', '.'));

        quantities[i] = _quantity;
        if (_price && quantity) {
            prices[i] = _price;
        } else {
            prices[i] = 0;
        }
    }

    order_total_quantity = 0;
    order_total_cost = 0;

    for (var i=0; i < TOTAL_FORMS; i++) {
       order_total_quantity += quantities[i];
       order_total_cost += quantities[i] * prices[i];
   }

   $('.order_total_cost').text(order_total_cost.toFixed(2));
   $('.order_total_quantity').text(order_total_quantity);
}

window.onload = function() {
    $('.order_form input[type="number"]').on('click', recalculate_total_values);
    $('.order_form select').on('change', function(event) {
        var product_id = this.value;
        $.ajax({
            url: "/products/product/" + product_id + "/price",
            success: function (data) {
                $('.orderitems-' + product_id + '-price').text(data.price);
            },
        });
    })
    recalculate_total_values();
}

//function deleteOrderItem() {
//    var target_name= row[0].querySelector('input[type="number"]').name;
//    recalculate_total_values();
//}
