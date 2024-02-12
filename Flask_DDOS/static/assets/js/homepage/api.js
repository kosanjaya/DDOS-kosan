const btnAttackDDOS = document.querySelector('.btn-attack-ddos');

const startGUI = async function() {
    const url = "http://127.0.0.1:5000/startGUI";
    try {
        const fetchGUI = await fetch(url, {method: 'POST'});
        const response = await fetchGUI.text();
        console.log(response);
    } catch(error) {
        console.error(error)
    }
}

btnAttackDDOS.addEventListener('click', (event) => {
    const clicked = event.currentTarget.closest('.btn-attack-ddos');

    if (!clicked) return;
    if (clicked) startGUI();
})