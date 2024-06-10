const modalU = document.querySelector(".create-user");
const closeUserModal = document.querySelector(".close-modal");
const openModal = document.querySelector(".open-modal");
const modal = document.querySelector(".create-user");

closeUserModal.addEventListener('click', ()=>{
  
   let att = modalU.classList.contains("show-create-user")
   if(att){
        modalU.classList.remove('show-create-user')
        modalU.classList.add('close-create-user')
   }else{
    modalU.classList.add('show-create-user')
    modalU.classList.remove('close-create-user')
   }
})

openModal.addEventListener('click', () => {
    modal.classList.toggle("show");
})
