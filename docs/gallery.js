const all = [
    {
        "file": "voiture.png",
        "title": "Car",
        "description": "Side view of our car",
    },
    /*{
        "file": "test.mp4",
        "title": "Test Video",
        "description": "A test video to demonstrate the gallery functionality. This video is a placeholder and does not represent any actual content.",
        "type": "video"
    },*/
    {
        "file": "jacques-travailler.mp4",
        "title": "Jack Working",
        "description": "A video of Jack working on the project. This video showcases the development process and the effort put into creating the website.",
        "type": "video"
    },
    {
        "file": "emilie-travailler.mp4",
        "title": "Emily Working",
        "description": "A video of Emily working on the project. This video highlights the effort involved in building the website.",
        "type": "video"
    },
    {
        "file": "audrey-travailler.mp4",
        "title": "Audrey Working",
        "description": "A video of Audrey working on the project. This video showcases the dedication and hard work put into the team videos.",
        "type": "video"
    },
    {
        "file": "toutlequipe-travailler.mp4",
        "title": "The Whole Team Working",
        "description": "A video of the whole team working on the project. This video captures the collaborative effort and teamwork involved in creating the project.",
        "type": "video"
    },
    /*{
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
    }*/
]
let currentChecked = 0;
let gallery = document.getElementById("gallery");
let gallerySelectors = document.getElementById("gallery-selectors");
function addCard(data, id) {
    let card = document.createElement("div");
    card.className = "card";
    card.dataset.id = id;
    if (data.type === "image" || !data.type) {
        card.innerHTML = `<img src="images/gallery/${data.file}" alt="${data.title}">`;
    } else if (data.type === "video") {
        card.innerHTML = `<video controls playsinline><source src="images/gallery/${data.file}" type="video/mp4">Your browser does not support the video tag.</video>`;
        if (typeof card.children[0].loop == 'boolean') { // loop supported
            card.children[0].loop = true;
        } else { // loop property not supported
            card.children[0].addEventListener('ended', function () {
                this.currentTime = 0;
                this.play();
            }, false);
        }
    }
    card.innerHTML += `
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
                behavior: "smooth", block: 'nearest',   // Prevent vertical scroll
                inline: 'center'    // Scroll horizontally to center
            });
            // psaus current video if it exists
            if (gallery.children[currentChecked].children[0].pause) {
                gallery.children[currentChecked].children[0].pause();
            }
            if (gallery.children[radio.dataset.id].children[0].play) {
                gallery.children[radio.dataset.id].children[0].play();
            }
            currentChecked = Number(radio.dataset.id);
        }
    });
    if (id == 0) {
        radio.checked = true;
    }
    let label = document.createElement("label");
    label.htmlFor = `gallery-${id}`;
    label.style.display = "none";
    label.innerText = data.title;
    gallerySelectors.appendChild(radio);
    gallerySelectors.appendChild(label);
}
function next(scroll = true) {
    let nextChecked = 0;
    if (currentChecked < all.length - 1) {
        nextChecked = currentChecked + 1;
    } else {
        nextChecked = 0;
    }
    document.getElementById(`gallery-${nextChecked}`).click();
}
function previous(scroll = true) {
    let nextChecked = 0;
    if (currentChecked > 0) {
        nextChecked = currentChecked - 1;
    } else {
        nextChecked = all.length - 1;
    }
    document.getElementById(`gallery-${nextChecked}`).click();
}
function loadGallery() {
    for (let i = 0; i < all.length; i++) {
        addCard(all[i], i);
    }
}
loadGallery();
function nextInterval() {
    //next(false);
}
let interval = setInterval(nextInterval, 5000);