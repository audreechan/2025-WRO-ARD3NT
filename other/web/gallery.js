const all = [
    {
        "file": "angelzareln.png",
        "title": "Angel Zombie",
        "description": "A zombie with angel wings, a unique blend of horror and divinity. Runs up to other zombies to protect them, transferring incoming damage to itself.",
    },
    {
        "file": "angryheraldzareln.png",
        "title": "Wizard Zombie",
        "description": "A powerful sorceror zombie with a wizard hat and staff, casting spells to control the battlefield. Can summon other zombies to aid in battle.",
    },
    {
        "file": "arsonzareln.png",
        "title": "Arson Zombie",
        "description": "A zombie engulfed in flames, creating fiery explosions and burning nearby enemies. Its fiery aura can ignite other zombies, enhancing their damage.",
    },
    {
        "file": "assassinzareln.png",
        "title": "Assassin Zombie",
        "description": "A stealthy zombie with a hood and daggers, capable of teleporting behind your units and heavily weakening them.",
    },
    {
        "file": "beezareln.png",
        "title": "Bee Zombie",
        "description": "A zombified bee that dies upon attacking, and has a chance to inflict poison. Spawned in swarms by the Hivemind Zombie."
    }
]
let currentChecked = 0;
let gallery = document.getElementById("gallery");
let gallerySelectors = document.getElementById("gallery-selectors");
function addCard(data, id){
    let card = document.createElement("div");
    card.className = "card";
    card.dataset.id = id;
    card.innerHTML = `
        <img src="images/gallery/${data.file}" alt="${data.title}">
        <h2>${data.title}</h2>
        <p>${data.description}</p>
    `;
    card.style.width = "100%";
    card.style.flexShrink = "0";
    card.classList.add("visible");
    card.classList.add("gallery-card");
    gallery.appendChild(card);
    let radio = document.createElement("input");
    radio.type = "radio";
    radio.name = "gallery";
    radio.dataset.id = id;
    radio.id = `gallery-${id}`;
    radio.className = "gallery-radio";
    radio.addEventListener("change", () => {
        if (radio.checked) {
            gallery.children[radio.dataset.id].scrollIntoView({
                behavior: "smooth", block: "nearest"});
            currentChecked = radio.dataset.id;
        }
    });
    if(id==0){
        radio.checked = true;
    }
    let label = document.createElement("label");
    label.htmlFor = `gallery-${id}`;
    label.style.display = "none";
    label.innerText = data.title;
    gallerySelectors.appendChild(radio);
    gallerySelectors.appendChild(label);
}
function next(scroll = true){
    if(currentChecked < all.length - 1){
        currentChecked++;
    } else {
        currentChecked = 0;
    }
    document.getElementById(`gallery-${currentChecked}`).click();
}
function previous(){
    if(currentChecked > 0){
        currentChecked--;
    } else {
        currentChecked = all.length - 1;
    }
    document.getElementById(`gallery-${currentChecked}`).click();
}
function loadGallery() {
    for(let i = 0; i < all.length; i++) {
        addCard(all[i], i);
    }
}
loadGallery();
function nextInterval(){
    //next(false);
}
let interval = setInterval(nextInterval, 5000);