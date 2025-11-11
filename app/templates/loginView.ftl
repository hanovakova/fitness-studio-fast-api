<!DOCTYPE html>
<html lang="en">
<head>
    <title>Login</title>
    <link rel="stylesheet" type="text/css" href="/css/style.css">
</head>
<body>
<div class="container">
    <#include "headerView.ftl">
    <form class="styled-form" action="/login" method="post">
        <h2>Login</h2>

        <label for="username">Username:
            <input type="text" id="username" name="username" required>
        </label>

        <label for="password">Password:
            <input type="password" id="password" name="password" required>
            <#if error??>
                <span class="err">${error}</span>
            </#if>
        </label>
        <button class="styled-button" type="submit">Login</button>
    </form>
</div>
</body>
</html>