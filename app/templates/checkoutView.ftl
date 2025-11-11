<!DOCTYPE html>
<html>
<head>
    <title>Checkout</title>
    <link rel="stylesheet" type="text/css" href="/css/style.css">
</head>
<body>
<div class="container">
    <#include "headerView.ftl">
    <form class="styled-form" action="/checkout" method="post">
        <h2>Checkout</h2>
        <table>
            <thead>
            <tr>
                <th>Name</th>
                <th>Price</th>
            </tr>
            </thead>
            <tbody>
            <#assign totalPrice=0>
            <#list enrolledClasses as enrolledClass>
                <tr>
                    <td>${enrolledClass.name}</td>
                    <td>${enrolledClass.price}</td>
                </tr>
                <#assign totalPrice = totalPrice + enrolledClass.price>
            </#list>
            <tr>
                <td><strong>Total</strong></td>
                <td><strong>${totalPrice}</strong></td>
            </tr>
            </tbody>
        </table>

        <label for="fullName">Name On The Card:</label>
        <input type="text" id="fullName" name="fullName" required/>

        <label for="creditCard">Credit Card Number:</label>
        <input type="text"
               id="creditCard"
               name="creditCard"
               required
               maxlength="19"
        inputmode="numeric"
        pattern="\d{4}\s\d{4}\s\d{4}\s\d{4}"
        title="Please enter a 16-digit credit card number in groups of 4" />

        <script>
            document.getElementById('creditCard').addEventListener('input', function (e) {
                let value = e.target.value.replace(/\D/g, '');
                value = value.substring(0, 16);
                e.target.value = value.replace(/(\d{4})(?=\d)/g, '$1 ');
            });
        </script>

        <button class="styled-button" type="submit">Confirm Payment</button>
    </form>
</div>
</body>
</html>