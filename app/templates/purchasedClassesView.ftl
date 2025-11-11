<!DOCTYPE html>
<html lang="en">
<head>
    <title>Purchased Classes</title>
    <link rel="stylesheet" type="text/css" href="/css/style.css">
</head>
<body>
<div class="container">
    <#include "headerView.ftl">
    <h1>Your Classes In Processing</h1>
    <table>
        <thead>
        <tr>
            <th>Name</th>
            <th>Description</th>
            <th>Start Time</th>
            <th>End Time</th>
            <th>Instructor</th>
            <th>Price</th>
        </tr>
        </thead>
        <tbody>
        <#list pendingClasses as pendingClass>
            <tr>
                <td>${pendingClass.name}</td>
                <td>${pendingClass.description}</td>
                <td>${pendingClass.startTime}</td>
                <td>${pendingClass.endTime}</td>
                <td>${pendingClass.instructorName}</td>
                <td>${pendingClass.price}</td>
            </tr>
        </#list>
        </tbody>
    </table>
    <p class="center"><a href="/fitnessClasses">View other classes</a></p>
</div>
</body>
</html>