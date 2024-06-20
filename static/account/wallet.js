const seeBtn = document.getElementById("see-more-btn");
const balanceBtn = document.getElementById("see-balance-btn");
const someWithdraws = document.getElementById("some-withdraws");
const allWithdraws = document.getElementById("all-withdraws");
const balance = document.getElementById("balance");

seeBtn.addEventListener("click", () => {
    if (seeBtn.innerHTML == "See more") {
        someWithdraws.hidden = true;
        allWithdraws.hidden = false;
        seeBtn.innerHTML = "See less";
    } else {
        someWithdraws.hidden = false;
        allWithdraws.hidden = true;
        seeBtn.innerHTML = "See more";
    };
});

balanceBtn.addEventListener("click", () => {
    if (balanceBtn.classList.contains("bi-eye-slash")) {
        balanceBtn.classList.remove("bi-eye-slash");
        balanceBtn.classList.add("bi-eye");
    } else {
        balanceBtn.classList.remove("bi-eye");
        balanceBtn.classList.add("bi-eye-slash");
    }
});