let all = [
    {
        "file": "start-loop.png",
        "title": "Start",
        "description": "When the raspberry pi is turned on, the car will automatically start the python script to run the car.",
    },
    {
        "file": "loop.png",
        "title": "Main Loop",
        "description": "The main loop of the car's software, responsible for processing sensor data and controlling the vehicle's movements. It consists of detecting obstacles and avoiding them, and following the line.",
    },
    {
        "file": "obstacle-detection.png",
        "title": "Obstacle Detection",
        "description": "The car takes a picture of its surroundings with its camera and uses a YOLOv8 nano model to detect any obstacles in it",
    },
    {
        "file": "decision-making.png",
        "title": "Decision Making",
        "description": "The car determines the dominant color of the largest, or closest, detected obstacle. If the color is red, it will steer the car right and if it's green, it will steer left. If the obstacle is too large, it is too close and the car will move backwards",
    },
    {
        "file": "line-following.png",
        "title": "Line Following",
        "description": "The car uses its camera to detect the line on the ground and follows it. The car will try to steer so that it is perpendicular to the line. If the edge of the line is too close to the center, it will make a sharper turn, and if it is too much, it will back up.",
    },
    {
        "file": "turning-around.png",
        "title": "Turning Around",
        "description": "After making 2 full laps, the car will start turning around. It will always turn right when moving forward and left when moving back so it can quickly make the turn.",
    },
    {
        "file": "parking.png",
        "title": "Parking",
        "description": "The car is able to detect a parking space and maneuver itself into the space. It uses donkeycar to do so",
    },
]
let currentChecked = 0;
let schematic = document.getElementById("schematic");
let schematicSelectors = document.getElementById("schematic-selectors");
function addSchematicCard(data, id) {
    let card = document.createElement("div");
    card.className = "card";
    card.dataset.id = id;
    if (data.type === "image" || !data.type) {
        card.innerHTML = `<img src="images/schematic/${data.file}" alt="${data.title}">`;
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
    console.log(data.description);
    card.innerHTML += `
        <h2>${data.title}</h2>
        <p>${data.description}</p>
    `;
    card.style.width = "100%";
    card.style.flexShrink = "0";
    card.classList.add("visible");
    card.classList.add("schematic-card");
    schematic.appendChild(card);
    let radio = document.createElement("input");
    radio.type = "radio";
    radio.name = "schematic";
    radio.dataset.id = id;
    radio.id = `schematic-${id}`;
    radio.className = "schematic-radio";
    radio.addEventListener("change", () => {
        if (radio.checked) {
            schematic.children[radio.dataset.id].scrollIntoView({
                behavior: "smooth", block: 'nearest',   // Prevent vertical scroll
                inline: 'center'    // Scroll horizontally to center
            });
            // psaus current video if it exists
            if (schematic.children[currentChecked].children[0].pause) {
                schematic.children[currentChecked].children[0].pause();
            }
            if (schematic.children[radio.dataset.id].children[0].play) {
                schematic.children[radio.dataset.id].children[0].play();
            }
            currentChecked = Number(radio.dataset.id);
        }
    });
    if (id == 0) {
        radio.checked = true;
    }
    let label = document.createElement("label");
    label.htmlFor = `schematic-${id}`;
    label.style.display = "none";
    label.innerText = data.title;
    schematicSelectors.appendChild(radio);
    schematicSelectors.appendChild(label);
}
function disableButtons() {
    if (currentChecked == 0) {
        document.getElementById("schematic-left").disabled = true;
    } else {
        document.getElementById("schematic-left").disabled = false;
    }
    if (currentChecked == all.length - 1) {
        document.getElementById("schematic-right").disabled = true;
    } else {
        document.getElementById("schematic-right").disabled = false;
    }
}
window.schematicNext = function(scroll = true) {
    let nextChecked = 0;
    if (currentChecked < all.length - 1) {
        nextChecked = currentChecked + 1;
    } else {
        nextChecked = 0;
    }
    document.getElementById(`schematic-${nextChecked}`).click();
    disableButtons();
}
window.schematicPrevious = function(scroll = true) {
    let nextChecked = 0;
    if (currentChecked > 0) {
        nextChecked = currentChecked - 1;
    } else {
        nextChecked = all.length - 1;
    }
    document.getElementById(`schematic-${nextChecked}`).click();
    disableButtons();
}
function loadSchematic() {
    for (let i = 0; i < all.length; i++) {
        addSchematicCard(all[i], i);
    }
    document.getElementById("schematic-left").disabled = true;
}
loadSchematic();
function nextInterval() {
    //next(false);
}
let interval = setInterval(nextInterval, 5000);