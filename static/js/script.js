        document.getElementById('title').innerHTML = 'Your content';
        var home = document.getElementById('home');
        var assort = document.getElementById('assortment');
        var createOrder = document.getElementById('createOrder');
        var orders = document.getElementById('orders');
        var contact = document.getElementById('contact');
        var user = document.getElementById('user');

        function DivVisible(ell)
        {
            home.style.display='none';
            assort.style.display='none';
            createOrder.style.display='none';
            orders.style.display= 'none';
            contact.style.display= 'none';
            user.style.display= 'none';

            ell.style.display='block';
        }

