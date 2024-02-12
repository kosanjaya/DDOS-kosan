'use strict';

// Information
const allInfoAtk = document.querySelectorAll('.info-attack-type');

// Button
const containerAtkBtn = document.querySelector('.segmented-btn-container');
const allAtkBtn = document.querySelectorAll('.segmented-button');
const btnSynFlood = document.querySelector('.segmented-button-syn-flood');
const btnUdpFlood = document.querySelector('.segmented-button-udp-flood');
const btnSlowloris = document.querySelector('.segmented-button-slowloris');

// Inputs
const inputTargetIp = document.querySelector('.target-ip');
const inputPortNumber = document.querySelector('.port-number');
const inputTimePause = document.querySelector('.time-pause');
const inputAttackDuration = document.querySelector('.attack-duration');
const inputTotalRequest = document.querySelector('.total-request');

const inputs = document.querySelectorAll('input');
// console.log(inputs)

// select container for removing flex child
const containerInput = document.querySelector('.field-wrapper');

// Input Fields
const fieldTargetIp = document.getElementById('target-ip-field');
const fieldPortNumber = document.getElementById('port-number-field');
const fieldTimePause = document.getElementById('time-pause-field');
const fieldAttackDuration = document.getElementById('attack-duration-field');
const fieldTotalRequest = document.getElementById('total-request-field');

// Images
const allImgAtk = document.querySelectorAll('.img-input');
const bannerResult = document.querySelector('.img-banner-result');

// select button for attack and stop from flooding
const btnStartAttack = document.querySelector('.start-attack');
const btnStopFlooding = document.querySelector('.stop-flooding');

// Flooding result
const textResult = document.querySelector('.text-result');
const textResultSlowloris = document.querySelector('.text-result-slowloris');
const loadingAnimation = document.querySelector('.lds-dual-ring');

// remove init banner from text-result
bannerResult.remove()

// remove init inputs from DOM 
const removeInitInputs = [
    inputTimePause,
    inputTotalRequest
]

removeInitInputs.forEach(input => input.remove());

// Input for Attack Types
const initialAtkInputs = [
        inputTargetIp,
        inputPortNumber,
        inputTimePause,
        inputTotalRequest,
        inputAttackDuration,
    ]

const synFloodInputs = [
        inputTargetIp,
        inputPortNumber,
        inputAttackDuration,
    ]

const udpFloodInputs = [
        inputTargetIp,
        inputPortNumber,
        inputTimePause,
        inputAttackDuration,
    ]

const slowlorisInputs = [
        inputTargetIp,
        inputPortNumber,
        inputTotalRequest,
        inputAttackDuration,
    ]



// Handle API DDOS 
const attack = {
    loopStart: async function(objField) {
        const url = "http://127.0.0.1:5000/loop";
        try {
            const responseLoop = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(objField),
            });
            const data = await responseLoop.text();
            console.log(data);
            // menampilkan hasil serangan
            textResult.textContent = ''
            textResult.appendChild(bannerResult);
        } catch(error) {
            console.error(error)
        }
    },

    handleStart: function(objField) {
        console.log(objField);
        this.loopStart(objField);
    },

    // properti for slowloris
    loopSlowlorisStart: async function(objField) {
        const url = "http://127.0.0.1:5000/loop";
        try {
            const responseLoop = await fetch(url, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(objField),
            });
            const data = await responseLoop.text();
            console.log(data);
            // menampilkan hasil serangan
            textResultSlowloris.innerHTML = data
            loadingAnimation.classList.remove('display-none');

        } catch(error) {
            console.error(error)
        }
    },

    handleSlowlorisStart: function(objField) {
        console.log(objField);
        this.loopSlowlorisStart(objField);
    }
}

// Menghentikan serangan
const loopAttackStop = async function() {
    const url = "http://127.0.0.1:5000/loopattackstop";
    try {
        const responseLoop = await fetch(url, {
            method: 'POST',
            dataType: 'text',
            body: "stop"
        });
        
        const data = await responseLoop.text();
        console.log(data);
        // menampilkan hasil serangan
        textResult.textContent = data
        textResultSlowloris.textContent = data
        
    } catch(error) {
        console.error(error)
    }
};

const handleStop = function() {
    loopAttackStop();
};

// removes value from input field
const removeInputFields = function() {
    inputs.forEach(input => input.value = '');
} 
removeInputFields()

// Clicked Segmented Button
containerAtkBtn.addEventListener('click', function(e) {
    const clicked = e.target.closest('.segmented-button');

    // Guard Clause
    if (!clicked) return;
    if (!clicked.dataset.attack) return;

    // Remove Active Classes & add 'display-none' to all info and images
    allAtkBtn.forEach(btn => btn.classList.remove('segmented-button-active'));
    allInfoAtk.forEach(info => {
        info.classList.add('display-none');
        info.classList.remove('fade-in');
    });
    allImgAtk.forEach(img => {
        img.classList.add('display-none');
        img.classList.remove('fade-in');
    });
    initialAtkInputs.forEach(input => input.classList.remove('fade-in'));

    // Add Active Classes
    clicked.classList.add('segmented-button-active');

    // Activate All Content
    document
        .querySelector(`.${clicked.dataset.attack}-split`)
        .classList.remove('display-none');

    document
        .querySelector(`.${clicked.dataset.attack}-img`)
        .classList.remove('display-none');

    // Add Fade in
    document
        .querySelector(`.${clicked.dataset.attack}-split`)
        .classList.add('fade-in');

    document
        .querySelector(`.${clicked.dataset.attack}-img`)
        .classList.add('fade-in');

    // Handle inputs that match to the dataset
    initialAtkInputs.forEach(input => input.remove());

    const handleInputs = function(i) {
        i.classList.add('fade-in');
        i.classList.remove('display-none');
        containerInput.appendChild(i)
        removeInputFields()
    } 

    if (clicked.dataset.attack === 'syn-flood') {
        synFloodInputs.forEach(input => handleInputs(input))

        btnUdpFlood.classList.remove('segmented-button-active');
        btnSlowloris.classList.remove('segmented-button-active');
        
        textResult.classList.remove('display-none');
        textResultSlowloris.classList.add('display-none');
    };

    if (clicked.dataset.attack === 'udp-flood') {
        udpFloodInputs.forEach(input => handleInputs(input))

        btnSynFlood.classList.remove('segmented-button-active');
        btnSlowloris.classList.remove('segmented-button-active');

        textResult.classList.remove('display-none');
        textResultSlowloris.classList.add('display-none');
    };
    
    if (clicked.dataset.attack === 'slowloris') {
        slowlorisInputs.forEach(input => handleInputs(input))

        btnSynFlood.classList.remove('segmented-button-active');
        btnUdpFlood.classList.remove('segmented-button-active');

        textResultSlowloris.classList.remove('display-none');
        textResult.classList.add('display-none');
    };
});

// Button Click to Consume API DDOS & scroll into view btn
let countDown = 0;

btnStartAttack.addEventListener('click', (e) => {
    // Scroll Into View
    const id = e.target.getAttribute('href');
    document.querySelector(id).scrollIntoView({ behavior: 'smooth' });
    console.log(bannerResult.classList)

    // API Start Operations
    const fieldTargetIpValue = fieldTargetIp.value
    const fieldPortNumberValue = fieldPortNumber.value
    const fieldTimePauseValue = fieldTimePause.value
    const fieldTotalRequestValue = fieldTotalRequest.value
    const fieldAttackDurationValue = fieldAttackDuration.value
    // init countdown attack duration
    countDown = fieldAttackDurationValue * 1000

    if (btnSynFlood.classList.contains('segmented-button-active')) {
        const fieldSyn = {
            type: "syn",
            url: fieldTargetIpValue,
            port: fieldPortNumberValue,
            attackduration: fieldAttackDurationValue,
        }
        if (fieldSyn.url === '' && fieldSyn.port === '') textResult.textContent = 'Input Kosong'
        if (fieldSyn.url && fieldSyn.port) {
            attack.handleStart(fieldSyn);
            setTimeout(()=> {
                btnStopFlooding.click();
            }, countDown)
        }
        removeInputFields
    };

    if (btnUdpFlood.classList.contains('segmented-button-active')) {
        const fieldUdp = {
            type: "udp",
            url: fieldTargetIpValue,
            port: fieldPortNumberValue,
            timepause: fieldTimePauseValue,
            attackduration: fieldAttackDurationValue,
        }
        if (fieldUdp.url === '' && fieldUdp.port === '') textResult.textContent = 'Input Kosong'
        if (fieldUdp.url && fieldUdp.port) {
            attack.handleStart(fieldUdp);
            setTimeout(()=> {
                btnStopFlooding.click();
            }, countDown)
        }
        removeInputFields
    };
    

    if (btnSlowloris.classList.contains('segmented-button-active')) {
        const fieldSlowloris = {
            type: "slowloris",
            url: fieldTargetIpValue,
            port: fieldPortNumberValue,
            totalrequest: fieldTotalRequestValue,
            attackduration: fieldAttackDurationValue,
        }
        if (fieldSlowloris.url === '' && fieldSlowloris.port === '') textResultSlowloris.textContent = 'Input Kosong'
        if (fieldSlowloris.url && fieldSlowloris.port) {
            attack.handleSlowlorisStart(fieldSlowloris);
            textResultSlowloris.textContent = 'Menyiapkan Serangan Slowloris'
            setTimeout(()=>{
                setTimeout(()=> {
                    btnStopFlooding.click();
                }, countDown)
            }, 10000) // 10 Sec for preparing slowloris attack
        }
        removeInputFields
    };
})

btnStopFlooding.addEventListener('click', () => {
    handleStop();
    loadingAnimation.classList.add('display-none')
    bannerResult.remove()
    removeInputFields()
});


