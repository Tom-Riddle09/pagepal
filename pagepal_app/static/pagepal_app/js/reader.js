document.addEventListener("DOMContentLoaded", function() {
    // Dark mode toggle
    document.getElementById("theme-toggle").addEventListener("click", () => {
        let reader = document.body;
        reader.classList.toggle("night-mode");
    });
});
