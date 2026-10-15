function handleSlotClick(slotId, floorNumber) {
    const slotEl = document.querySelector(`.slot[data-id='${slotId}']`);
    const modal = document.getElementById("modal");
    const modalTitle = document.getElementById("modal-title");
    const vehicleInput = document.getElementById("vehicle-number");
    const ownerInput = document.getElementById("owner-name");

    // Decide Check-In or Check-Out
    if (slotEl.classList.contains("occupied")) {
        modalTitle.textContent = "Check-Out";
        vehicleInput.style.display = "none";
        ownerInput.style.display = "none";
    } else {
        modalTitle.textContent = "Check-In";
        vehicleInput.style.display = "block";
        ownerInput.style.display = "block";
        vehicleInput.value = "";
        ownerInput.value = "";
    }

    modal.style.display = "flex";

    // Confirm button
    document.getElementById("confirm-btn").onclick = async function () {
        const action = modalTitle.textContent === "Check-In" ? "book" : "checkout";
        const vehicle = vehicleInput.value.trim();
        const owner = ownerInput.value.trim();

        if (action === "book" && (!vehicle || !owner)) {
            showMessage("❌ Please fill Vehicle Number and Owner Name!", "error");
            return;
        }

        const url = action === "book" ? "/book" : "/checkout";

        try {
            const response = await fetch(url, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({
                    slot_id: slotId,
                    floor: floorNumber,
                    vehicle,
                    owner
                })
            });

            let ok = response.ok;
            let payload = null;
            try { payload = await response.json(); } catch(e) { payload = await response.text(); }

            console.log("Server response:", payload);

            if (!ok) {
                showMessage(`❌ Something went wrong`, "error");
                return;
            }

            if (action === "book") {
                animateCarToSlot(slotEl, floorNumber, () => {
                    slotEl.classList.add("occupied");
                    slotEl.innerHTML = "🚗";
                    showMessage("✅ Slot booked successfully", "success");
                    updateCounters();
                });
            } else {
                animateCarExit(slotEl, floorNumber, () => {
                    slotEl.classList.remove("occupied");
                    slotEl.innerHTML = "🅿️";
                    showMessage("🅿️ Slot checked out", "success");
                    updateCounters();
                });
            }

            modal.style.display = "none";

        } catch (err) {
            console.error(err);
            showMessage("❌ Network error", "error");
        }
    };

    document.getElementById("cancel-btn").onclick = function () {
        modal.style.display = "none";
    };
}

// Update slot counters
function updateCounters() {
    const slots = document.querySelectorAll(".slot");
    const total = slots.length;
    let filled = 0;
    slots.forEach(slot => { if (slot.classList.contains("occupied")) filled++; });

    const filledEl = document.getElementById("filled-count");
    const emptyEl = document.getElementById("empty-count");
    const totalEl = document.getElementById("total-count");

    if (filledEl) filledEl.textContent = filled;
    if (emptyEl) emptyEl.textContent = total - filled;
    if (totalEl) totalEl.textContent = total;
}

// Switch floors
function switchFloor(floorNumber) {
    const floors = document.querySelectorAll(".floor");
    floors.forEach(floorEl => {
        floorEl.style.display = floorEl.dataset.floor == floorNumber ? "block" : "none";
    });
    updateCounters();
}

document.addEventListener("DOMContentLoaded", () => { updateCounters(); });

function showMessage(msg, type = "success") {
    const messageBox = document.createElement("div");
    messageBox.className = `toast ${type}`;
    messageBox.textContent = msg;

    const parkingLot = document.getElementById("parking-lot") || document.body;
    parkingLot.appendChild(messageBox);

    setTimeout(() => { messageBox.classList.add("show"); }, 100);
    setTimeout(() => {
        messageBox.classList.remove("show");
        setTimeout(() => messageBox.remove(), 300);
    }, 3000);
}

/* =========================
   Check-In Animation
========================= */
function animateCarToSlot(slotEl, floorNumber, callback) {
    const car = document.getElementById(`car-animation-${floorNumber}`);
    if (!car) { if(callback) callback(); return; }

    const road = slotEl.closest(".parking-layout")?.querySelector(".road");
    if (!road) { if(callback) callback(); return; }

    const orig = {
        display: car.style.display,
        position: car.style.position,
        left: car.style.left,
        top: car.style.top,
        transition: car.style.transition,
        transform: car.style.transform
    };

    car.style.display = "block";
    car.style.position = "fixed";
    car.style.transition = "none";
    car.style.transformOrigin = "center center";
    car.style.transform = "rotate(0deg)";

    const roadRect = road.getBoundingClientRect();
    const slotRect = slotEl.getBoundingClientRect();
    const carRect = car.getBoundingClientRect();

    // Start **at the road start**
    const startLeft = roadRect.left + 0 - carRect.width;
    const startTop = roadRect.top + (roadRect.height - carRect.height)/2;
    car.style.left = `${startLeft}px`;
    car.style.top = `${startTop}px`;

    car.offsetHeight;

    const targetLeft = slotRect.left + (slotRect.width - carRect.width)/2;
    car.style.transition = "left 1.2s linear";
    car.style.left = `${targetLeft}px`;

    setTimeout(() => {
        car.style.transition = "transform 0.3s ease-in-out";
        car.style.transform = "rotate(-90deg)";

        setTimeout(() => {
            const targetTop = slotRect.top + (slotRect.height - carRect.height)/2;
            car.style.transition = "top 0.8s ease-in-out";
            car.style.top = `${targetTop}px`;

            setTimeout(() => {
                car.style.display = orig.display || "none";
                car.style.position = orig.position || "";
                car.style.left = orig.left || "";
                car.style.top = orig.top || "";
                car.style.transition = orig.transition || "";
                car.style.transform = orig.transform || "";
                if(callback) callback();
            }, 850);
        }, 350);
    }, 1250);
}

/* =========================
   Check-Out Animation (always exit right)
========================= */
function animateCarExit(slotEl, floorNumber, callback) {
    const car = document.getElementById(`car-animation-${floorNumber}`);
    if (!car) { if(callback) callback(); return; }

    const road = slotEl.closest(".parking-layout")?.querySelector(".road");
    if (!road) { if(callback) callback(); return; }

    car.style.display = "block";
    car.style.position = "fixed";
    car.style.transition = "none";
    car.style.transformOrigin = "center center";
    car.style.transform = "rotate(-90deg)";

    const slotRect = slotEl.getBoundingClientRect();
    const roadRect = road.getBoundingClientRect();
    let carRect = car.getBoundingClientRect();

    car.style.left = `${slotRect.left + (slotRect.width - carRect.width)/2}px`;
    car.style.top = `${slotRect.top + (slotRect.height - carRect.height)/2}px`;

    car.offsetHeight;

    const reverseDuration = 800;
    const rotateDuration = 400;
    const exitDuration = 1000;

    // STEP 1: Reverse straight to road center
    const roadY = roadRect.top + (roadRect.height - carRect.height)/2;
    car.style.transition = `top ${reverseDuration}ms ease-in-out`;
    car.style.top = `${roadY}px`;

    setTimeout(() => {
        // STEP 2: Rotate to forward
        car.style.transition = `transform ${rotateDuration}ms ease-in-out`;
        car.style.transform = "rotate(0deg)";

        setTimeout(() => {
            carRect = car.getBoundingClientRect();

            // STEP 3: Exit to **road end**, stay within frame
            const exitX = roadRect.left + roadRect.width - carRect.width - 5; // right edge of road
            car.style.transition = `left ${exitDuration}ms linear`;
            car.style.left = `${exitX}px`;

            setTimeout(() => {
                car.style.display = "none";
                if(callback) callback();
            }, exitDuration + 20);

        }, rotateDuration + 20);
    }, reverseDuration + 20);
}
