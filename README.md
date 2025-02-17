# FollowThru

FollowThru is a **simple contact manager** designed for business follow-ups, reminders, and email automation.  
Contacts can belong to groups, have due dates for follow-ups, and receive templated emails.  

The project is designed to be **open-source and flexible**, so others can use it for **personal or business purposes** (e.g., birthday reminders, outreach tracking).  

## 🚀 **Tech Stack**
- **Backend:** Falcon (Python) + PostgreSQL  
- **Frontend:** React (TypeScript) + Webpack  
- **Package Management:** `uv` (Python) + `npm` (JavaScript)  
- **Containerization:** Docker + Docker Compose  

---

## 🔧 **Setup & Running the Project (Development)**
### **1️⃣ Clone the repository**
```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/followthru.git
cd followthru
```

### **2️⃣ Build & Run the Project with Docker**
```bash
make run
```
This will:  
👉 Start the **backend** (`Falcon API + PostgreSQL`)  
👉 Start the **frontend** (`React + Webpack Dev Server`)  
👉 Automatically watch for file changes  

### **3️⃣ Access the App**
- **Backend API**: [http://localhost:8000/](http://localhost:8000/)  
- **Frontend UI**: [http://localhost:3000/](http://localhost:3000/)  

---

## 🔨 **Development Commands**
### **🐍 Backend (Python + Falcon)**
#### **Activate Virtual Environment (If Not Using Docker)**
```bash
uv venv
source .venv/bin/activate  # Mac/Linux
# .venv\Scripts\activate   # Windows
```

#### **Install Dependencies**
```bash
uv pip install --upgrade -r pyproject.toml
```

#### **Lock Dependencies (To Ensure Reproducibility)**
```bash
uv run
```

#### **Run Backend Locally (Without Docker)**
```bash
gunicorn -b 0.0.0.0:8000 app:app
```

---

### **⚛️ Frontend (React + TypeScript)**
#### **Install Dependencies**
```bash
npm install
```

#### **Run Frontend Locally (Without Docker)**
```bash
npm start
```

#### **Build Production Version**
```bash
npm run build
```

---

## 🐳 **Managing Docker Containers**

### **Rebuild Containers (When Dependencies Change)**
```bash
make run
```

### **Stop Containers**
```bash
make stop
```

### **Access Backend Container (For Debugging)**
```bash
make backend_shell
```

---
