window.addEventListener('pageshow', ()=>{
    for (navLink of document.querySelectorAll('.nav-link')){
        navLink.classList.add('nav-link-white')
    }
})