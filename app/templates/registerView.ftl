<!DOCTYPE html>
<html>
<head>
    <title>Registration</title>
    <link rel="stylesheet" type="text/css" href="/css/style.css">
</head>
<body>
<div class="container">
    <#include "headerView.ftl">
    <form class="styled-form" action="/register" method="POST" enctype="multipart/form-data">
        <h2>${registrationTitle}</h2>

        <label>${registrationUsername}
            <input type="text" id="username" name="username"
                   value="${bean.username!}"
                   class="<#if errors.username??>error-input</#if>"
                   required>
            <span class="err">${errors.username!}</span>
        </label>

        <label>${registrationPassword}
            <input type="password" id="password1" name="password1"
                   class="<#if errors.password1??>error-input</#if>"
                   required>
            <span class="err">${errors.password1!}</span>
        </label>

        <label>${registrationRepeatPassword}
            <input type="password" id="password2" name="password2"
                   class="<#if errors.password2??>error-input</#if>"
                   required>
            <span class="err">${errors.password2!}</span>
        </label>

        <label>${registrationFullName}
            <input type="text" id="name" name="name"
                   value="${bean.name!}"
                   class="<#if errors.name??>error-input</#if>"
                   required>
            <span class="err">${errors.name!}</span>
        </label>

        <label>${registrationEmail}
            <input type="text" id="email" name="email"
                   value="${bean.email!}"
                   class="<#if errors.email??>error-input</#if>"
                   required>
            <span class="err">${errors.email!}</span>
        </label>

        <label>${registrationAdvertisement}
            <input type="checkbox" name="advert" value="yes"
                   <#if bean.advert?? && bean.advert>checked</#if>>
        </label>

        <label>Avatar (optional):
            <input type="file" name="avatarFile">
        </label>

        <button class="styled-button" type="submit">
            ${registrationSubmit}
        </button>

        <p style="text-align:center; margin-top: 20px;">
            ${registrationQuestion}
            <a href="/login">${registrationLogin}</a>
        </p>
    </form>
</div>
</body>
</html>