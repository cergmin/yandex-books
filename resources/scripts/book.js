let buyButtons = document.getElementsByClassName('buy_button');
let cartButtons = document.getElementsByClassName('cart_button');

for (let cartButton of cartButtons) {
    cartButton.addEventListener('click', function(e) {
        let buttonAction = e.target.getAttribute('data-action');
        let bookID = e.target.getAttribute('data-book-id');
        
        switch (buttonAction) {
            case 'addToCart':
                e.target.innerText = 'Удалить из корзины';
                e.target.setAttribute('data-action', 'deleteFromCart');
                AJAX(
                    window.location.origin + '/api/cart/' + bookID,
                    '',
                    'PUT',
                    function() {}
                )
                break;
            case 'deleteFromCart':
                e.target.innerText = 'Добавить в корзину';
                e.target.setAttribute('data-action', 'addToCart');
                AJAX(
                    window.location.origin + '/api/cart/' + bookID,
                    '',
                    'DELETE',
                    function() {}
                )
                break;
        }
    });
}

for (let buyButton of buyButtons) {
    buyButton.addEventListener('click', function(e) {
        let bookID = e.target.getAttribute('data-book-id');
        let bookName = e.target.getAttribute('data-book-name');

        if (!confirm("Вы уверены, что хотите купить «" + bookName + "»?")) {
            return
        }
        
        AJAX(
            window.location.origin + '/api/buy/' + bookID,
            '',
            'POST',
            function(json) {
                let data = JSON.parse(json);
                alert(data['message']);

                if (data['is_ok']) {
                    document.location.reload();
                }
            }
        )
    });
}