document.getElementById("logoutBtn").addEventListener("click", async () => {
    const token = localStorage.getItem("token"); // get JWT from localStorage

    if (!token) {
        alert("You are not logged in!");
        window.location.href = "login.html";
        return;
    }

    try {
        const response = await fetch("http://127.0.0.1:5000/logout", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}` // send token for authentication
            }
        });

        if (response.ok) {
            localStorage.removeItem("token"); // remove JWT locally
            alert("Logged out successfully!");
            window.location.href = "login.html"; // redirect to login page
        } else {
            alert("Logout failed. Try again.");
        }
    } catch (error) {
        console.error("Logout error:", error);
        alert("Server error. Try again later.");
    }
});
