document.getElementById("signupBtn").addEventListener("click", async () => {
    const username = document.getElementById("username").value.trim();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();
    const confirm_password = document.getElementById("confirm_password").value.trim();
    const messageDiv = document.getElementById("message");

    // Basic validation
    if (!username || !email || !password || !confirm_password) {
        messageDiv.style.color = "red";
        messageDiv.textContent = "Please fill in all fields!";
        return;
    }

    // Check if password and confirm password match
    if (password !== confirm_password) {
        messageDiv.style.color = "red";
        messageDiv.textContent = "Passwords do not match!";
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:5000/signup", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ username, email, password, confirm_password })
        });

        const data = await response.json();
        
        if (response.status === 201) {
            messageDiv.style.color = "green";
            messageDiv.textContent = data.msg + " Redirecting to login...";
            setTimeout(() => { window.location.href = "login.html"; }, 1500);
        } else {
            messageDiv.style.color = "red";
            messageDiv.textContent = data.msg || "Signup failed!";
        }
    } catch (error) {
        console.error(error);
        messageDiv.style.color = "red";
        messageDiv.textContent = "Server error. Try again later.";
    }
});
