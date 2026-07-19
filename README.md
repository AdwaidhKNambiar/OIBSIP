# Oasis Infobyte SIP — Python Development Intern Roadmap

This repository hosts the software engineering solutions completed during the Oasis Infobyte Summer Internship Program (OIBSIP). Both applications have been structurally upgraded to meet the **Advanced Tier** requirements.

---

## 🛠️ Project Portfolio Architecture

### Task 1: Desktop Voice Assistant (Advanced Tier)
An automated desktop environment assistant utilizing semantic speech synthesis and a localized rule-based parser.
* **Core Logic:** Natural Language Intent Parsing (processes free-form variations rather than simple keyword matches).
* **Automation Engines:** Built-in email pipeline dispatch via secure `smtplib`, system timers with terminal alerts, and interactive mathematical equation evaluation.
* **API Integration:** Real-time atmospheric metrics parsing over secure OpenWeatherMap endpoints.
* **Configuration Controls:** External command macro definitions managed via modular JSON schemas (`assistant_config.json`).

### Task 2: Advanced BMI Health Analytics Suite (Advanced Tier)
A biometric analytical system tracking historical health trends over an embedded transaction database.
* **Interface Design:** Desktop Graphical User Interface (GUI) engineered completely through native `tkinter`.
* **Smart Validation Engines:** Multi-level exception handling that catches letters, negative values, and automatically converts height measurements entered in centimeters to meters natively.
* **Data Persistence Layer:** Persistent storage managed locally via an optimized `sqlite3` transactional architecture supporting multi-user profile querying.
* **Data Visualization Framework:** Generates data telemetry trend lines dynamically across highlighted classification zones using `matplotlib`.

---

## 🔒 Privacy & Compliance Disclosures
* **Data Collection Scope:** The Voice Assistant operates strictly through localized volatile runtime triggers. Audited voice command flows are mapped entirely inside `privacy_audit.log`. No long-term microphonic raw streams are cached on disk.
* **Database Privacy Metrics:** The BMI Analytics tracking suite retains historical rows inside a localized database file (`bmi_records.db`) isolated completely to the host machine with zero cloud sync overhead.

---

## 🚀 Execution Instructions

### Installation of Core Dependencies
Initialize your host python execution sandbox and pull down required external integrations by executing:
```bash
pip install requests matplotlib psutil