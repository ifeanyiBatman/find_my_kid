## 👁️‍🗨️ Find My Kid — WIP Dashboard for Daycare Monitoring

**Find My Kid** is a prototype dashboard that allows parents to monitor their children in daycare via real-time location and live video feeds. Built for a hackathon, it simulates what a future production-ready parental control platform might look like—merging safety, visibility, and control.

> ⚠️ This is a **work-in-progress** project, built quickly as an MVP. The current state is functional but limited, with mocked GPS data and test IP cam feeds.
> Test it out here  [lynk](https://lynk-8dcm.onrender.com)

---

### 🎯 Concept

Give parents **real-time access** to:

* Their child’s current location on a map
* A live video stream from the daycare center
* A unified dashboard with lightweight UI (no bloat, just signal)

---

### 🛠 Tech Stack

* Backend: **FastAPI**
* Frontend: **HTMX + TailwindCSS**
* Video Feed: **IP Webcam app** (used for local streaming)
* Map: **Leaflet.js** with a static lat/lon point

---

### 🧪 Current State

* [x] Map embedded via Leaflet showing a fixed point
* [x] IP video stream rendered on dashboard (simulated phone cam)
* [x] FastAPI serves HTML and streams feed
* [ ] No authentication / OTP / role separation
* [ ] GPS is hardcoded, no live device sync
* [ ] Layout is basic and not responsive

---

### 🚧 Limitations

* ❌ Not production-grade: no user management, encryption, or scalable backend
* 🔐 No security policies in place
* 🛰️ GPS data is static—not linked to real devices yet
* 🧱 Built quickly as an experiment with limited refactor time

---

### 📍 Vision (If Continued)

* Mobile app for caregiver side (stream GPS and video)
* Role-based access for parents, admins, and daycare workers
* Real-time GPS sync from phone/device
* Emergency alert trigger and historical route tracking

---

### 📂 Running It Locally (Dev Only)

```bash
git clone https://github.com/yourusername/find-my-kid.git
cd find-my-kid
pip install -r requirements.txt
uvicorn main:app --reload
```

Then:

* Launch your IP Webcam app on a phone
* Set the IP stream URL in the `.env` or config
* Navigate to `http://localhost:8000` in your browser

---

### 🔓 License

MIT

---
