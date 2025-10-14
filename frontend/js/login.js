document.getElementById("loginBtn").addEventListener("click", async() =>{
    const username = document.getElementById("username").value.trim();
    const password = document.getElementById("password").value.trim();
    const messageDiv = document.getElementById("message");

    if (!username || !password){
        messageDiv.style.color = "red";
        messageDiv.textContent= "Please enter username, email and password"
        return; 
    }
    try{
        const response = await fetch("http://127.0.0.1:5000/login",{
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({username, password})
        });
        const data = await response.json();

        if (response.status===200){
            messageDiv.style.color= "green";
            messageDiv.textContent= "Logged in successfully! Redirecting...";
            localStorage.setItem("token", data.access_token);
            setTimeout(() => { window.location.href = "index.html"; }, 1500);
        } else {
            messageDiv.style.color="red";
            messageDiv.textContent= data.msg || "Login failed!"
        }
    } catch (error){
        console.error(error);
        messageDiv.style.color = "red";
        messageDiv.textContent = "Server error. Try again later.";
    }

})