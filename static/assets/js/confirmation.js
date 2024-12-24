document.addEventListener("DOMContentLoaded", () => {
  launchConfetti();

  const reservationDataElement = document.getElementById("reservation-data-json");

  if (reservationDataElement) {
    try {
      const reservationDetails = JSON.parse(reservationDataElement.textContent);

      if (reservationDetails) {
        const reservationTable = document.getElementById("reservation-data");
        const row = document.createElement("tr");

        row.innerHTML = `
          <td>${reservationDetails.name || "N/A"}</td>
          <td>${reservationDetails.family_name || "N/A"}</td>
          <td>${reservationDetails.num_tickets || 0}</td>
          <td>${reservationDetails.seats && reservationDetails.seats.length > 0 ? reservationDetails.seats.join(", ") : "N/A"}</td>
          <td>${reservationDetails.cinema || "N/A"}</td>
          <td>${reservationDetails.movie || "N/A"}</td>
        `;

        reservationTable.appendChild(row);
      }
    } catch (error) {
      console.error("Error parsing reservation details JSON:", error);
    }
  }

  document.getElementById("download-pdf").addEventListener("click", () => {
    const pdfContent = document.querySelector(".confirmation-container");
    html2pdf()
      .set({
        margin: 1,
        filename: "ticket-reservation.pdf",
        html2canvas: { scale: 4 },
        jsPDF: { orientation: "portrait" },
      })
      .from(pdfContent)
      .save();
  });
});

function launchConfetti() {
  const confettiSettings = {
    particleCount: 100,
    startVelocity: 30,
    spread: 360,
    origin: { x: 0.5, y: 0.5 },
    colors: ["#ff0000", "#ffffff", "#000000"],
  };

  setTimeout(() => confetti(confettiSettings), 200);
  setTimeout(() => confetti(confettiSettings), 400);
  setTimeout(() => confetti(confettiSettings), 600);
}
const reservationDataElement = document.getElementById("reservation-data-json");

if (reservationDataElement) {
  try {
    const reservationDetails = JSON.parse(reservationDataElement.textContent.trim());

    if (reservationDetails) {
      const reservationTable = document.getElementById("reservation-data");
      const row = document.createElement("tr");

      row.innerHTML = `
        <td>${reservationDetails.name || "N/A"}</td>
        <td>${reservationDetails.family_name || "N/A"}</td>
        <td>${reservationDetails.num_tickets || 0}</td>
        <td>${reservationDetails.seats && reservationDetails.seats.length > 0 ? reservationDetails.seats.join(", ") : "N/A"}</td>
        <td>${reservationDetails.cinema || "N/A"}</td>
        <td>${reservationDetails.movie || "N/A"}</td>
      `;

      reservationTable.innerHTML = "";
      reservationTable.appendChild(row);
    }
  } catch (error) {
    console.error("Error parsing reservation details JSON:", error);
  }
}

