/*!
* Start Bootstrap - Shop Homepage v5.0.6 (https://startbootstrap.com/template/shop-homepage)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-shop-homepage/blob/master/LICENSE)
*/
// This file is intentionally blank
// Use this file to add JavaScript to your project
const paymentData = {
    public_key: "{{ flutterwave_public_key|safe }}",
    tx_ref: "txref-test-" + Date.now(),
    amount: 100.00,  // Hardcoded
    email: "test@example.com",  // Hardcoded
    name: "Test User"  // Hardcoded
};