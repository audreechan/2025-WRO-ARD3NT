let diagram = document.getElementById("interactive-diagram");
let locked = null;
Array.from(diagram.getElementsByClassName("diagram-controller")).forEach(controller => {
    controller.addEventListener("mouseover", () => {
        // Toggle the active class on the hovered controller
        controller.classList.toggle("active");
        let targetDiagram = controller.parentNode.querySelector(`.diagram-text`);

        if (targetDiagram) {
            // Toggle visibility of the target diagram
            targetDiagram.classList.toggle("visible");
        }
    });
    //hide when mouse leaves
    controller.addEventListener("mouseout", () => {
        controller.classList.remove("active");
        let targetDiagram = controller.parentNode.querySelector(`.diagram-text`);
        if (targetDiagram) {
            // Hide the target diagram when mouse leaves
            targetDiagram.classList.remove("visible");
        }
    });
    controller.addEventListener("click", () => {
        // Toggle the active class on click
        controller.classList.toggle("active");
        let targetDiagram = controller.parentNode.querySelector(`.diagram-text`);

        if (targetDiagram) {
            // If we have a locked diagram and it's not the one we clicked, unlock it
            if (locked && locked !== targetDiagram) {
                locked.classList.remove("lock-visible");
                locked.classList.remove("visible");
                // Remove active class from the previous controller
                let previousController = locked.previousElementSibling;
                if (previousController) {
                    previousController.classList.remove("active");
                }
                locked = null; // Clear the locked state
            }
            // Toggle visibility of the target diagram on click
            targetDiagram.classList.toggle("lock-visible");
            if(targetDiagram.classList.contains("lock-visible")) {
                // If the diagram is locked, we need to remember which one it is
                locked = targetDiagram;
            }
        }
    });
});
diagram.addEventListener("click", (event) => {
    // If the click is outside of any controller, hide all diagrams
    if (!event.target.classList.contains("diagram-controller")) {
        Array.from(diagram.getElementsByClassName("diagram-text")).forEach(text => {
            text.classList.remove("visible");
            text.classList.remove("lock-visible");
        });
        // Remove active class from all controllers
        Array.from(diagram.getElementsByClassName("diagram-controller")).forEach(controller => {
            controller.classList.remove("active");
        });
        // Clear the locked state if we clicked outside
        locked = null;
    }
});
function toggleAllDiagramText() {
    //unlock locked if it exists
    if (locked) {
        locked.classList.remove("lock-visible");
        locked.classList.remove("visible");
        // Remove active class from the previous controller
        let previousController = locked.previousElementSibling;
        if (previousController) {
            previousController.classList.remove("active");
        }
        locked = null; // Clear the locked state
    }
    Array.from(diagram.getElementsByClassName("diagram-text")).forEach(text => {
        text.classList.toggle("lock-visible");
    });
    Array.from(diagram.getElementsByClassName("diagram-controller")).forEach(controller => {
        controller.classList.toggle("active");
    });
}