const cursor = document.querySelector('.cursor');
document.addEventListener('mousemove', (e) => {
    cursor.style.left = e.clientX + 'px';
    cursor.style.top = e.clientY + 'px';
})

window.addEventListener("pageshow", ()=>{
    document.querySelector('.transition-div').style.visibility = 'hidden'
    document.querySelector('.transition-div').classList.remove('transition-active')
}, false);

for (navLink of document.querySelectorAll('.nav-link')){
    navLink.addEventListener('mouseover', ()=>{
        cursor.classList.add('cursor-hover-100')
    })
    navLink.addEventListener('mouseout', ()=>{
        cursor.classList.remove('cursor-hover-100')
    })
}

function showNav(elem){
    elem.style.display = 'none'
    document.querySelector('#hide-navbar-button').style.display = 'block'
    document.querySelector('.navbar-mobile-bg').classList.add('navbar-mobile-bg-show')
            
    let navLinks = document.querySelectorAll('.nav-link')

    function showNavLink(){
        let i = 1
        function myLoop() {         //  create a loop function
            setTimeout(()=> {   //  call a 3s setTimeout when the loop is called                     //  increment the counter
                if (i < navLinks.length) {           //  if the counter < 10, call the loop function
                    navLinks[i].classList.add('opacity-visible')
                    myLoop();             
                } 
                i++                     
            }, 100)
        }
        navLinks[0].classList.add('opacity-visible')
        myLoop()
    }
    for (navLink of navLinks){
        navLink.style.display = 'block'
    }
    showNavLink()
}

function hideNav(elem){
    elem.style.display = 'none'
    document.querySelector('#show-navbar-button').style.display = 'block'
    document.querySelector('.navbar-mobile-bg').classList.remove('navbar-mobile-bg-show')
        
    for (navLink of document.querySelectorAll('.nav-link')){
        navLink.style.display = 'none'
        navLink.classList.remove('opacity-visible')
    }
}

function hoverSmallWhite(elem){
    elem.addEventListener('mouseover', ()=>{
        cursor.classList.add('small-cursor')
        cursor.classList.remove('color-cursor')
        cursor.style.zIndex = '1'
    })
    elem.addEventListener('mouseout', ()=>{
        cursor.classList.remove('small-cursor')
        cursor.classList.add('color-cursor')
        cursor.style.removeProperty('z-index')
    })
}

function hoverUp(elem){
    elem.addEventListener('mouseover', ()=>{
        cursor.classList.add('cursor-up')
    })
    elem.addEventListener('mouseout', ()=>{
        cursor.classList.remove('cursor-up')
    })
}


function hoverSmallColor(elem){
    elem.addEventListener('mouseover', ()=>{
        cursor.classList.add('small-cursor')
        cursor.classList.add('color-cursor')
    })
    elem.addEventListener('mouseout', ()=>{
        cursor.classList.remove('small-cursor')
        cursor.classList.remove('color-cursor')
    })
}

function hover100(elem){
    elem.addEventListener('mouseover', ()=>{
        cursor.classList.add('cursor-hover-100')
    })
    elem.addEventListener('mouseout', ()=>{
        cursor.classList.remove('cursor-hover-100')
    })
}
function hover300(elem){
    elem.addEventListener('mouseover', ()=>{
        cursor.classList.add('cursor-hover-300')
    })
    elem.addEventListener('mouseout', ()=>{
        cursor.classList.remove('cursor-hover-300')
    })
}
function hover500(elem){
    elem.addEventListener('mouseover', ()=>{
        cursor.classList.add('cursor-hover-500')
    })
    elem.addEventListener('mouseout', ()=>{
        cursor.classList.remove('cursor-hover-500')
    })
}

function hoverShowBehind(elem){
    elem.addEventListener('mouseenter',()=>{
        elem.style.zIndex = '99'
    })
    elem.addEventListener('mouseleave',()=>{
        elem.style.removeProperty('z-index')
    })
}

function changeWindow(url, color){
    const transitionDiv = document.querySelector('.transition-div')
    let time = 600
    if (color == 'white'){
        transitionDiv.style.background = 'white'
    } else {
        transitionDiv.style.background = 'var(--color)'
    }
    if (url.includes("quizz") || url.includes("training") || url.includes('typing') || url.includes('learning')) {
        time = 500
    }
    transitionDiv.style.visibility = 'visible'
    if (event.touches) {
        transitionDiv.style.left = event.touches[0].clientX + 'px';
        transitionDiv.style.top = event.touches[0].clientY + 'px';
      } else {
        transitionDiv.style.left = event.clientX + 'px';
        transitionDiv.style.top = event.clientY + 'px';
      }
    transitionDiv.classList.toggle('transition-active')
    
    setTimeout(() => {
        window.location.href = url
    }, time);
}