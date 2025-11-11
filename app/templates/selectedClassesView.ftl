<!DOCTYPE html>
<html>
<head>
    <title>Your Classes</title>
    <link rel="stylesheet" type="text/css" href="/css/style.css">
</head>
<body>
<#include "headerView.ftl">

<h1>Classes You Selected</h1>
<table>
    <thead>
    <tr>
        <th>Name</th>
        <th>Description</th>
        <th>Start Time</th>
        <th>End Time</th>
        <th>Instructor</th>
        <th>Price</th>
        <th>Action</th>
    </tr>
    </thead>
    <tbody>
    <#assign totalPrice = 0>
    <#list enrolledClasses as enrolledClass>
        <tr>
            <td>${enrolledClass.name}</td>
            <td>${enrolledClass.description}</td>
            <td>${enrolledClass.startTime}</td>
            <td>${enrolledClass.endTime}</td>
            <td>${enrolledClass.instructorName}</td>
            <td>${enrolledClass.price}</td>
            <td>
                <form class="table-form" action="/user-classes/drop" method="post">
                    <input type="hidden" name="enrolledClassId" value="${enrolledClass.id}"/>
                    <button class="delete-button" type="submit">Delete</button>
                </form>
            </td>
        </tr>
        <#assign totalPrice = totalPrice + enrolledClass.price>
    </#list>

    <tr>
        <td><strong>Total</strong></td>
        <td colspan="4"></td>
        <td><strong>${totalPrice}</strong></td>
        <td></td>
    </tr>
    </tbody>
</table>

<form class="table-form" action="/checkout" method="get">
    <div style="display: flex; justify-content: center">
        <button class="table-button" type="submit"
                <#if !enrolledClasses?has_content>disabled</#if>>
            Check Out
        </button>
    </div>
</form>
<p><a href="/fitnessClasses">View other classes</a></p>
</body>
</html>