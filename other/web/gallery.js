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
let gallery = document.getElementById("gallery");
function addCard(data, id){
    let card = document.createElement("div");
    card.className = "card";
    card.dataset.id = id;
    card.innerHTML = `
        <img src="images/gallery/${data.file}" alt="${data.title}">
        <h2>${data.title}</h2>
        <p>${data.description}</p>
    `;
    if(id==0){
        card.style.width = "100%";
    }else{
        card.style.width = "0%";
        card.style.display = "none";
    }
    gallery.appendChild(card);
}
function loadGallery() {
    for(let i = 0; i < all.length; i++) {
        addCard(all[i], i);
    }
}
loadGallery();