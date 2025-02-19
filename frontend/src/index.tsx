import "./index.css";

const API_BASE_URL =
  window.location.hostname === "localhost"
    ? "http://localhost:8000"
    : "http://backend:8000";

let contacts: { id: number; name: string; email: string; phone: string; group: string, next_contact_date: string }[] = [];
let selectedContacts: Set<number> = new Set(); // Track selected contacts

document.addEventListener("DOMContentLoaded", () => {
  const loadingEl = document.getElementById("loading")!;
  const contactsTable = document.getElementById("contacts-table")!;
  const searchInput = document.getElementById("search") as HTMLInputElement;
  const groupFilter = document.getElementById("group-filter") as HTMLSelectElement;
  const selectAllCheckbox = document.getElementById("select-all") as HTMLInputElement;
  const sendEmailButton = document.getElementById("send-email") as HTMLButtonElement;
  const headers = document.querySelectorAll("th[data-sort]");

  let sortKey: keyof typeof contacts[0] = "name";
  let sortAsc = true;

  // Fetch contacts
  fetch(`${API_BASE_URL}/contacts`)
    .then(response => response.json())
    .then((data) => {
      if (Array.isArray(data)) {
        contacts.length = 0;
        contacts.push(...data);
      }
      loadingEl.style.display = "none";
      populateGroupFilter();
      renderTable();
    })
    .catch((error) => {
      console.error("Error fetching contacts:", error);
      loadingEl.innerHTML = "<p class='text-red-500'>Failed to load contacts.</p>";
    });

  // Populate group filter dropdown
  function populateGroupFilter() {
    const groups = Array.from(new Set(contacts.map(contact => contact.group))).sort();
    groupFilter.innerHTML = `<option value="">All Groups</option>` + 
      groups.map(group => `<option value="${group}">${group}</option>`).join("");
  }

  // Render table
  function renderTable() {
    let filteredContacts = contacts.filter(contact =>
      contact.name.toLowerCase().includes(searchInput.value.toLowerCase()) &&
      (groupFilter.value === "" || contact.group === groupFilter.value)
    );

    filteredContacts.sort((a, b) => {
      const valA = a[sortKey];
      const valB = b[sortKey];
      return sortAsc ? String(valA).localeCompare(String(valB)) : String(valB).localeCompare(String(valA));
    });

    contactsTable.innerHTML = filteredContacts
      .map((contact, index) => `
        <tr class="${index % 2 === 0 ? "bg-gray-100" : "bg-white"} hover:bg-gray-200 transition">
            <td class="p-3 text-center">
                <input type="checkbox" class="contact-checkbox w-5 h-5" data-id="${contact.id}" ${selectedContacts.has(contact.id) ? "checked" : ""} />
            </td>
            <td class="p-3 font-medium text-text">${contact.name}</td>
            <td class="p-3 text-gray-600">${contact.email}</td>
            <td class="p-3 text-gray-500">${contact.phone || "No phone"}</td>
            <td class="p-3 text-gray-700">${contact.group || "No group"}</td>
        </tr>`)
      .join("");

    attachCheckboxListeners();
}


  // Handle individual checkbox clicks
  function attachCheckboxListeners() {
    document.querySelectorAll(".contact-checkbox").forEach(checkbox => {
      checkbox.addEventListener("change", (event) => {
        const target = event.target as HTMLInputElement;
        const id = Number(target.getAttribute("data-id"));
        if (target.checked) {
          selectedContacts.add(id);
        } else {
          selectedContacts.delete(id);
        }
      });
    });
  }
  

  // Handle "Select All" checkbox
  selectAllCheckbox.addEventListener("change", () => {
    const allCheckboxes = document.querySelectorAll(".contact-checkbox") as NodeListOf<HTMLInputElement>;
    selectedContacts.clear();
    if (selectAllCheckbox.checked) {
      allCheckboxes.forEach(checkbox => {
        checkbox.checked = true;
        selectedContacts.add(Number(checkbox.getAttribute("data-id")));
      });
    } else {
      allCheckboxes.forEach(checkbox => (checkbox.checked = false));
    }
  });

  // Handle sorting
  headers.forEach(header => {
    header.addEventListener("click", () => {
      const key = header.getAttribute("data-sort") as keyof typeof contacts[0];
      if (sortKey === key) {
        sortAsc = !sortAsc;
      } else {
        sortKey = key;
        sortAsc = true;
      }
      renderTable();
    });
  });

  // Handle filtering by group
  groupFilter.addEventListener("change", renderTable);

  // Handle searching
  searchInput.addEventListener("input", renderTable);

  // Handle sending email
  sendEmailButton.addEventListener("click", () => {
    if (selectedContacts.size === 0) {
      alert("No contacts selected.");
      return;
    }

    const selectedContactIds = Array.from(selectedContacts);
    console.log("Sending email to contacts:", selectedContactIds);
    
    fetch(`${API_BASE_URL}/send-email`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ contact_ids: selectedContactIds })
    }).then(response => response.json())
      .then(data => alert(data.message))
      .catch(error => console.error("Error sending email:", error));
  });
});
