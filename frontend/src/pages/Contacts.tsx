import React, { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";

const API_BASE_URL =
  window.location.hostname === "localhost"
    ? "http://localhost:8000"
    : "http://backend:8000";

interface Contact {
  id: number;
  name: string;
  email: string;
  phone: string;
  group: string;
  next_contact_date: string;
}

const Contacts: React.FC = () => {
  const [contacts, setContacts] = useState<Contact[]>([]);
  const [filteredContacts, setFilteredContacts] = useState<Contact[]>([]);
  const [selectedContacts, setSelectedContacts] = useState<Set<number>>(new Set());
  const [groups, setGroups] = useState<string[]>([]);
  const [search, setSearch] = useState("");
  const [groupFilter, setGroupFilter] = useState("");
  const [sortKey, setSortKey] = useState<keyof Contact>("name");
  const [sortAsc, setSortAsc] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) {
      navigate("/login");
      return;
    }

    fetch(`${API_BASE_URL}/contacts`, {
      headers: { Authorization: `Bearer ${token}` },
    })
      .then((response) => response.json())
      .then((data) => {
        if (Array.isArray(data)) {
          setContacts(data);
          setFilteredContacts(data);
          const uniqueGroups = Array.from(new Set(data.map((contact) => contact.group))).sort();
          setGroups(uniqueGroups);
        }
      })
      .catch((error) => console.error("Error fetching contacts:", error));
  }, [navigate]);

  useEffect(() => {
    let newContacts = contacts.filter(
      (contact) =>
        contact.name.toLowerCase().includes(search.toLowerCase()) &&
        (groupFilter === "" || contact.group === groupFilter)
    );

    newContacts.sort((a, b) => {
      const valA = a[sortKey];
      const valB = b[sortKey];
      return sortAsc ? String(valA).localeCompare(String(valB)) : String(valB).localeCompare(String(valA));
    });

    setFilteredContacts(newContacts);
  }, [contacts, search, groupFilter, sortKey, sortAsc]);

  const toggleSelectContact = (id: number) => {
    setSelectedContacts((prev) => {
      const newSelection = new Set(prev);
      newSelection.has(id) ? newSelection.delete(id) : newSelection.add(id);
      return newSelection;
    });
  };

  const selectAllContacts = (selectAll: boolean) => {
    if (selectAll) {
      setSelectedContacts(new Set(filteredContacts.map((contact) => contact.id)));
    } else {
      setSelectedContacts(new Set());
    }
  };

  const sendEmail = () => {
    if (selectedContacts.size === 0) {
      alert("No contacts selected.");
      return;
    }

    const token = localStorage.getItem("token");
    if (!token) {
      alert("You must be logged in to send emails.");
      return;
    }

    fetch(`${API_BASE_URL}/send-email`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${token}`,
      },
      body: JSON.stringify({ contact_ids: Array.from(selectedContacts) }),
    })
      .then((response) => response.json())
      .then((data) => alert(data.message))
      .catch((error) => console.error("Error sending email:", error));
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold mb-4">Contacts</h1>

      {/* Search & Filter */}
      <div className="flex space-x-4 mb-4">
        <input
          type="text"
          placeholder="Search contacts..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          className="p-2 border rounded w-full"
        />
        <select
          value={groupFilter}
          onChange={(e) => setGroupFilter(e.target.value)}
          className="p-2 border rounded"
        >
          <option value="">All Groups</option>
          {groups.map((group) => (
            <option key={group} value={group}>
              {group}
            </option>
          ))}
        </select>
      </div>

      {/* Actions */}
      <div className="flex justify-between mb-2">
        <input
          type="checkbox"
          onChange={(e) => selectAllContacts(e.target.checked)}
          className="w-5 h-5"
        />
        <button
          onClick={sendEmail}
          className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
        >
          Send Email
        </button>
      </div>

      {/* Contacts Table */}
      <table className="w-full border-collapse border border-gray-300">
        <thead>
          <tr className="bg-gray-200">
            <th className="p-3">Select</th>
            <th className="p-3 cursor-pointer" onClick={() => setSortKey("name")}>
              Name {sortKey === "name" && (sortAsc ? "↑" : "↓")}
            </th>
            <th className="p-3 cursor-pointer" onClick={() => setSortKey("email")}>
              Email {sortKey === "email" && (sortAsc ? "↑" : "↓")}
            </th>
            <th className="p-3 cursor-pointer" onClick={() => setSortKey("phone")}>
              Phone {sortKey === "phone" && (sortAsc ? "↑" : "↓")}
            </th>
            <th className="p-3 cursor-pointer" onClick={() => setSortKey("group")}>
              Group {sortKey === "group" && (sortAsc ? "↑" : "↓")}
            </th>
          </tr>
        </thead>
        <tbody>
          {filteredContacts.map((contact, index) => (
            <tr key={contact.id} className={index % 2 === 0 ? "bg-gray-100" : "bg-white"}>
              <td className="p-3 text-center">
                <input
                  type="checkbox"
                  checked={selectedContacts.has(contact.id)}
                  onChange={() => toggleSelectContact(contact.id)}
                  className="w-5 h-5"
                />
              </td>
              <td className="p-3">{contact.name}</td>
              <td className="p-3">{contact.email}</td>
              <td className="p-3">{contact.phone || "No phone"}</td>
              <td className="p-3">{contact.group || "No group"}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default Contacts;