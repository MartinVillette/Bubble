window.addEventListener('pageshow', ()=>{
    cursor.classList.add('color-cursor')
    document.querySelector('body').style.background = 'white'
    document.querySelector('.navbar-mobile-bg').style.background = 'var(--color)'
    for (navLink of document.querySelector('.navbar-mobile').querySelectorAll('.nav-link')){
        navLink.style.color = 'white'
    }
    document.querySelector('#hide-navbar-button').style.filter = 'none'
})

let navbarButton = document.querySelector('.navbar-button')
if (navbarButton){
    navbarButton.style.filter = 'invert(62%) sepia(54%) saturate(513%) hue-rotate(195deg) brightness(102%) contrast(101%)'
}
