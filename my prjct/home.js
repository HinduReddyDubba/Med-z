// Validate User Details Form
document.querySelector("form").addEventListener("submit", function(event) {
    const name = document.getElementById("name").value.trim();
    const dob = document.getElementById("dob").value.trim();
    const weight = document.getElementById("weight").value.trim();
    const height = document.getElementById("height_feet").value.trim();

    if (!name || !dob || !weight || !height) {
        alert("Please fill in all fields.");
        event.preventDefault();  // Prevent form submission if validation fails
        return;
    }
});

// Handle User Login
document.getElementById("loginForm").addEventListener("submit", function(event) {
    event.preventDefault();

    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();

    if (!username || !password) {
        alert("Please enter both username and password.");
        return;
    }

    fetch('/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === "Login successful!") {
            window.location.href = "home.html";
        } else {
            alert("Invalid credentials");
        }
    })
    .catch(error => console.error("Error:", error));
});

// Handle Medication Addition
document.getElementById("addMedicationForm").addEventListener("submit", function(event) {
    event.preventDefault();

    const name = document.getElementById("medication-name").value.trim();
    const dosage = document.getElementById("medication-dosage").value.trim();
    const frequency = document.getElementById("medication-frequency").value.trim();

    if (!name || !dosage || !frequency) {
        alert("Please fill in all medication details.");
        return;
    }

    fetch('/add_medication', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ name, dosage, frequency })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.status);
        window.location.reload();
    })
    .catch(error => console.error("Error:", error));
});