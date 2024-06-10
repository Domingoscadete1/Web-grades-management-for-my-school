const sideMenu = document.querySelector("aside");
const menuBtn = document.querySelector("#menu-btn");
const closeBtn = document.querySelector("#close-btn");
const themeToggler = document.querySelector(".theme-toggler");
const professorCheckbox = document.querySelector('.professor');
const estudanteCheckbox = document.querySelector('.estudante');



// Função para alternar o tema
function toggleTheme() {
    document.body.classList.toggle('dark-theme-variables');
    themeToggler.querySelector('span:nth-child(1)').classList.toggle('active');
    themeToggler.querySelector('span:nth-child(2)').classList.toggle('active');
}

// Mostrar sidebar
menuBtn.addEventListener('click', () => {
    sideMenu.style.display = 'block';
})

// Fechar sidebar
closeBtn.addEventListener('click', () => {
    sideMenu.style.display = 'none';
})

// Mudar o tema
themeToggler.addEventListener('click', () => {
    toggleTheme();
    // Salvar o estado do tema no armazenamento local
    const isDarkTheme = document.body.classList.contains('dark-theme-variables');
    localStorage.setItem('darkTheme', JSON.stringify(isDarkTheme));
})

// Checkbox
function toggleCheckbox(selectedCheckboxId) {
    if (selectedCheckboxId === 'professor') {
        estudanteCheckbox.checked = !professorCheckbox.checked;
    } else if (selectedCheckboxId === 'estudante') {
        professorCheckbox.checked = !estudanteCheckbox.checked;
    }
}

// Recuperar o estado do tema do armazenamento local ao carregar a página
document.addEventListener('DOMContentLoaded', () => {
    const darkThemeEnabled = JSON.parse(localStorage.getItem('darkTheme'));
    if (darkThemeEnabled) {
        toggleTheme();
    }
});


const openModal = document.querySelector('#open-modal');
const closeModal = document.querySelector('.cancel-btn');
const modal = document.querySelector('.modal');

const toggleModal = () => {
    modal.classList.toggle("show");
}

openModal.addEventListener("click", () => toggleModal());
closeModal.addEventListener("click", () => toggleModal());



