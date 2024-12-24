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

document.addEventListener("DOMContentLoaded", () => {
  launchConfetti();

  const reservation = {
    firstName: "John",
    lastName: "Doe",
    tickets: 3,
    seats: ["A1", "A2", "A3"],
    cinema: "Cinema 1",
    movie: "Avengers: Endgame",
  };
  const reservationTable = document.getElementById("reservation-data");
  const row = document.createElement("tr");

  row.innerHTML = `
    <td>${reservation.firstName}</td>
    <td>${reservation.lastName}</td>
    <td>${reservation.tickets}</td>
    <td>${reservation.seats.join(", ")}</td>
    <td>${reservation.cinema}</td>
    <td>${reservation.movie}</td>
  `;

  reservationTable.appendChild(row);

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
