function signup(button, event) {
    event.preventDefault();
    const form = button.closest("form");
    const formData = new FormData(form);
    console.log("Form data: ", formData)
    fetch("/fitnessClasses", {
        method: 'POST',
        body: formData
    })
        .then(response => {
            if (!response.ok) {
                throw new Error("Request failed: " + response.status);
            }
            return response.json();
        })
        .then(data => {
            if (data.status === "success") {
                button.disabled = true;
                button.textContent = "Signed Up";
            }
        })
        .catch(error => console.error("Error:", error));
}
