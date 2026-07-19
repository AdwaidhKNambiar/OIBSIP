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

### Task 3: Cryptographically Secure Password Architect (Advanced Tier)
A security compliance desktop utility generating mathematically safe authentication tokens.
* **Security Subsystem:** Replaces predictable pseudo-random seeds by compiling strings via the cryptographically secure `secrets` module.
* **Algorithmic Inclusion Guard:** Guarantees structural parity by ensuring at least one character from every active checkbox set is embedded into the string.
* **Clipboard Automation:** Built-in hooks natively pass completed tokens directly into the host machine's physical clipboard via `pyperclip`.
* **Volatile Session Buffer:** Displays a localized tracking history pane summarizing the last 5 tokens generated in the active window lifecycle (erased completely on application exit).

### Task 5: Advanced Multi-Room Live Chat Engine (Advanced Tier)
A real-time TCP socket communication room network with relational tracking features.
* **Network Infrastructure:** Powered by a customized multithreaded architecture handling socket connections over local loops (`127.0.0.1`).
* **Persistent Session Stores:** User profiles, credential checks, and historic chat room streams are fully preserved using an embedded relational transaction file (`chat_system.db`).
* **Text Processing Pipeline:** Includes an integrated text engine parser mapping classic emoji shortcodes (e.g., `:smile:`, `:fire:`) directly into standard Unicode representations.
* **🛡️ Security Transparency Disclosure:** 
  * **Password Protection:** User keys are securely hashed using cryptographic standard SHA-256 before hitting persistent storage disks.
  * **Unencrypted Vectors:** Chat packet row data contents are streamed dynamically across local loops and stored inside the database rows as raw unencrypted cleartext string characters. This ensures immediate performance parsing for local execution sandboxes.
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

