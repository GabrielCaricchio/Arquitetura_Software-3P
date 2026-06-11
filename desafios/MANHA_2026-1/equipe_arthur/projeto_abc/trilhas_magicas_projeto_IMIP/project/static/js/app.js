// JS bem simples: fecha mensagens automaticamente para deixar a tela limpa.
document.addEventListener("DOMContentLoaded", () => {
    const flashes = document.querySelectorAll(".flash");
    flashes.forEach((flash) => {
        setTimeout(() => {
            flash.style.transition = "opacity .5s ease, transform .5s ease";
            flash.style.opacity = "0";
            flash.style.transform = "translateY(-6px)";
        }, 5000);
    });
});
