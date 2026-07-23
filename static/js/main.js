const menuButton = document.getElementById("menu-button");
const mainMenu = document.getElementById("main-menu");

if (menuButton && mainMenu) {
    menuButton.addEventListener("click", function () {
        const isOpen = mainMenu.classList.toggle("menu-open");

        menuButton.setAttribute(
            "aria-expanded",
            String(isOpen)
        );

        menuButton.textContent = isOpen
            ? "Fermer"
            : "Menu";
    });
}


const userDropdownButton =
    document.getElementById("user-dropdown-button");

const userDropdownMenu =
    document.getElementById("user-dropdown-menu");

if (userDropdownButton && userDropdownMenu) {
    userDropdownButton.addEventListener(
        "click",
        function (event) {
            event.stopPropagation();

            const isOpen =
                userDropdownMenu.classList.toggle("open");

            userDropdownButton.setAttribute(
                "aria-expanded",
                String(isOpen)
            );
        }
    );

    document.addEventListener("click", function (event) {
        const clickedInsideMenu =
            userDropdownMenu.contains(event.target);

        const clickedButton =
            userDropdownButton.contains(event.target);

        if (!clickedInsideMenu && !clickedButton) {
            userDropdownMenu.classList.remove("open");

            userDropdownButton.setAttribute(
                "aria-expanded",
                "false"
            );
        }
    });
}


/* =========================
   Traductions des créneaux
========================= */

const translationsElement =
    document.getElementById("appointment-translations");

let appointmentTranslations = null;

if (translationsElement) {
    try {
        appointmentTranslations = JSON.parse(
            translationsElement.textContent
        );
    } catch (error) {
        console.error(
            "Impossible de charger les traductions des créneaux.",
            error
        );
    }
}


/* =========================
   Gestion des créneaux
========================= */

const appointmentDate =
    document.getElementById("appointment-date");

const preferredTime =
    document.getElementById("preferred-time");

const slotsMessage =
    document.getElementById("slots-message");


if (appointmentDate) {
    appointmentDate.min =
        new Date().toISOString().split("T")[0];
}


if (
    appointmentDate &&
    preferredTime &&
    appointmentTranslations
) {
    appointmentDate.addEventListener(
        "change",
        async function () {
            const selectedDate = appointmentDate.value;
            const translations = appointmentTranslations;

            preferredTime.innerHTML = "";
            preferredTime.disabled = true;

            if (slotsMessage) {
                slotsMessage.textContent = "";
            }

            if (!selectedDate) {
                const option =
                    document.createElement("option");

                option.value = "";
                option.textContent =
                    translations.selectDateFirst;

                preferredTime.appendChild(option);
                return;
            }

            const loadingOption =
                document.createElement("option");

            loadingOption.value = "";
            loadingOption.textContent =
                translations.loadingSlots;

            preferredTime.appendChild(loadingOption);

            try {
                const response = await fetch(
                    `/api/creneaux?date=${encodeURIComponent(
                        selectedDate
                    )}`
                );

                if (!response.ok) {
                    throw new Error(
                        "Unable to load available slots"
                    );
                }

                const data = await response.json();

                preferredTime.innerHTML = "";

                if (
                    !data.success ||
                    !Array.isArray(data.slots) ||
                    data.slots.length === 0
                ) {
                    const noSlotOption =
                        document.createElement("option");

                    noSlotOption.value = "";
                    noSlotOption.textContent =
                        translations.noSlots;

                    preferredTime.appendChild(
                        noSlotOption
                    );

                    if (slotsMessage) {
                        slotsMessage.textContent =
                            translations.noSlots;
                    }

                    return;
                }

                const defaultOption =
                    document.createElement("option");

                defaultOption.value = "";
                defaultOption.textContent =
                    translations.chooseSlot;

                preferredTime.appendChild(
                    defaultOption
                );

                data.slots.forEach(function (slot) {
                    const option =
                        document.createElement("option");

                    option.value = slot;
                    option.textContent = slot;

                    preferredTime.appendChild(option);
                });

                preferredTime.disabled = false;
            } catch (error) {
                console.error(
                    "Erreur lors du chargement des créneaux.",
                    error
                );

                preferredTime.innerHTML = "";

                const errorOption =
                    document.createElement("option");

                errorOption.value = "";
                errorOption.textContent =
                    translations.slotsError;

                preferredTime.appendChild(errorOption);

                if (slotsMessage) {
                    slotsMessage.textContent =
                        translations.slotsError;
                }
            }
        }
    );
}
const messageField =
    document.getElementById("message");

const messageCounter =
    document.getElementById("message-counter");

if (messageField && messageCounter) {
    function updateMessageCounter() {
        messageCounter.textContent =
            `${messageField.value.length} / 500`;
    }

    messageField.addEventListener(
        "input",
        updateMessageCounter
    );

    updateMessageCounter();
}
const notifButton =
document.getElementById("notification-button");

const notifMenu =
document.getElementById("notification-menu");

if (notifButton && notifMenu){

    notifButton.addEventListener("click", function(e){

        e.stopPropagation();

        notifMenu.classList.toggle("open");

    });

    document.addEventListener("click", function(){

        notifMenu.classList.remove("open");

    });

}
const chatMessages =
    document.getElementById("chat-messages");

if (chatMessages) {
    chatMessages.scrollTop =
        chatMessages.scrollHeight;
}