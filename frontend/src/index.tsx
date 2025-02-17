const API_BASE_URL =
  window.location.hostname === "localhost"
    ? "http://localhost:8000"
    : "http://backend:8000";

document.addEventListener("DOMContentLoaded", () => {
  const loadingEl = document.getElementById("loading")!;
  const contactsList = document.getElementById("contacts-list")!;

  fetch(`${API_BASE_URL}/contacts`)
    .then((response) => response.json())
    .then((data) => {
      loadingEl.style.display = "none"; // Hide loading message

      if (!data.contacts || data.contacts.length === 0) {
        contactsList.innerHTML = "<p>No contacts found.</p>";
        return;
      }

      contactsList.innerHTML = data.contacts
        .map(
          (contact: { id: number; name: string; email: string; phone: string }) =>
            `<li><strong>${contact.name}</strong> - ${contact.email} - ${contact.phone || "No phone"}</li>`
        )
        .join("");
    })
    .catch((error) => {
      console.error("Error fetching contacts:", error);
      loadingEl.innerHTML = "Failed to load contacts.";
    });
});
