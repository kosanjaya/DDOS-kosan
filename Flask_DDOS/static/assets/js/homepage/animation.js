const navBar = document.querySelector('.navbar-links');
const btnNavToggle = document.querySelector('.nav-toggle');
const btnDosAttackService = document.querySelector('.btn-attack-dos');
const btnDDosAttackService = document.querySelector('.btn-attack-ddos');
const overlay = document.querySelector('.overlay');
const allLinksNavbar = document.querySelectorAll('.links');

// Logic navBar
btnNavToggle.addEventListener('click', () => {
    const visibility = navBar.getAttribute('data-visible')

    if (visibility === 'false') {
        navBar.setAttribute('data-visible', true);
        btnNavToggle.setAttribute('aria-expanded', true);
        overlay.classList.remove('display-none')
    } else if (visibility === 'true') {
        navBar.setAttribute('data-visible', false);
        btnNavToggle.setAttribute('aria-expanded', false);
        overlay.classList.add('display-none')
    }
});

allLinksNavbar.forEach(link => {
    link.addEventListener('click', () => {
        navBar.setAttribute('data-visible', false);
        btnNavToggle.setAttribute('aria-expanded', false);
        overlay.classList.add('display-none')
    })
});

// Directing service button 
btnDosAttackService.addEventListener('click', (event) => {
    event.preventDefault()
    const link = event.currentTarget.querySelector('.API-dos-service').getAttribute('href');

    if (!link || link === null) return;

    window.location.href = link
});

// Overlay
overlay.addEventListener('click', () => {
    navBar.setAttribute('data-visible', false);
    btnNavToggle.setAttribute('aria-expanded', false);
    overlay.classList.add('display-none')
})

// Animation 
////////////// Reveal Sections //////////////
const animateSections = document.querySelectorAll('.section-animation');

const animationSection = function (entries) {
    const [entry] = entries;
    
    const leftProperty = entry.target.querySelector('.property-left');
    const rightProperty = entry.target.querySelector('.property-right');

    if (!leftProperty || !rightProperty) return; // Check if elements exist
    
    if (entry.isIntersecting) {
        leftProperty.classList.remove('property-left-hide');
        rightProperty.classList.remove('property-right-hide');
    } else {
        leftProperty.classList.add('property-left-hide');
        rightProperty.classList.add('property-right-hide');
    }

};

const sectionObserver = new IntersectionObserver(animationSection, {
    root: null,
    threshold: 0.4
});

animateSections.forEach(section => {
    const leftProperty = section.querySelector('.property-left');
    const rightProperty = section.querySelector('.property-right');

    if (leftProperty && rightProperty) {
        leftProperty.classList.add('property-left-hide');
        rightProperty.classList.add('property-right-hide');
    }

    sectionObserver.observe(section);
})

// header
const header = document.querySelector('.header');
const leftPropertyHeader = header.querySelector('.property-left-header');
const rightPropertyHeader = header.querySelector('.property-right-header');

const hideHeaderEl = function (entries) {
    const [entry] = entries;

    const leftProperty = entry.target.querySelector('.property-left-header');
    const rightProperty = entry.target.querySelector('.property-right-header');

    if (!leftProperty || !rightProperty) return; // Check if elements exist

    if (entry.isIntersecting) {
        leftProperty.classList.remove('property-left-hide');
        rightProperty.classList.remove('property-right-hide');
    } else {
        leftProperty.classList.add('property-left-hide');
        rightProperty.classList.add('property-right-hide');
        leftProperty.classList.remove('fade-in-from-left');
        rightProperty.classList.remove('fade-in-from-right');
    }
}

const headerObserver = new IntersectionObserver(hideHeaderEl, {
    root: null,
    threshold: 0.5
})

headerObserver.observe(header)

// bottom
const footer = document.querySelector('footer');
const propertyFooter = footer.querySelector('.property-bottom');

const hideFooterEl = function (entries) {
    const [entry] = entries;

    const bottomProperty = entry.target.querySelector('.property-bottom');

    if (!bottomProperty) return;

    if (entry.isIntersecting) {
        bottomProperty.classList.remove('property-bottom-hide')
    } else {
        bottomProperty.classList.add('property-bottom-hide')
    }
}

const footerObserver = new IntersectionObserver(hideFooterEl, {
    root: null,
    threshold: 0.3
})

if (propertyFooter) {
    propertyFooter.classList.add('property-bottom-hide')
}   

footerObserver.observe(footer)