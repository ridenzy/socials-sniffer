# PROJECT TITLE

**Project Name:** socials-sniffer

---

# 0) Project details Analysis

- **IST-Zustand:**  
    Before this project, Instagram audience discovery and profile intelligence relied on:
    
    - Manual inspection of profiles
        
    - Unstructured scraping scripts with fragile sessions
        
    - High account ban risk due to poor session handling
        
    - No lifecycle awareness (sleep, VPS suspend, rate-limit drift)
        
    - No separation between authentication, runtime errors, and shutdown behavior
        
- **Soll-Zustand:**  
    A production-grade Instagram audience discovery engine that:
    
    - Uses **human-like session lifecycles**
        
    - Survives system sleep, VPS suspend, and long runtimes
        
    - Separates **intent**, **policy**, and **action**
        
    - Supports multi-agent rotation
        
    - Produces structured, clean, reusable user datasets
        
- **Anforderungen (fachlich/technisch):**
    
    - Python-based
        
    - instagrapi client
        
    - Persistent sessions per agent
        
    - Centralized error handling
        
    - Heartbeat-based suspend detection
        
    - JSON-based storage (append-safe)
        
    - No automatic logout on risky states
        
    - Manual recovery paths for checkpoints
        
- **Wirtschaftlichkeitsbetrachtung (optional):**
    
    - Low infrastructure cost (single VPS or local machine)
        
    - High leverage: replaces manual research hours
        
    - Scales horizontally with agents, not infrastructure
        
- **Requests (Must-haves & Optionals):**
    
    - Must-have: session safety, account longevity
        
    - Must-have: structured user profiles
        
    - Optional: filters, exports, paid tiers, UI
        

---

# 1) Architecture & Design

#### **1.1 Folder Layout**

```
socials-sniffer/
├── program_env/
│   ├── instagram/
│   │   ├── data_collectors/
│   │   │   ├── collectors/
│   │   │   ├── storage/
│   │   │   │   ├── raw-data/
│   │   │   │   └── filtered-data/
│   ├── utilities/
│   │   ├── agencyUtils.py
│   │   ├── timeUtils.py
│   │   ├── jsonUtils.py
│   │   ├── userDataUtils.py
│   │   └── agents/
│   │       ├── agents.json
│   │       └── sessions/
├── README.md
├── requirements.txt
└── pyproject.toml
```

#### **1.2 System Architecture (End-to-End Flow)**

```
[User Input]
   ↓
[Agent Selection]
   ↓
[Session Load / Login]
   ↓
[Runtime Scraping Loop]
   ↓
[Heartbeat & Error Detection]
   ↓
[Exit Reason Resolution]
   ↓
[Logout / Session Discard Policy]
   ↓
[Persist Agent State]
```

#### **1.3 Core Design Principle**

- **Detection ≠ Decision ≠ Action**
    
- Runtime detects anomalies
    
- Policy layer decides
    
- Session manager executes
    

---

# 2) Build Plan

#### **2.1 Provisions via Interface**

- Instagram agent accounts
    
- agents.json with rotation metadata
    
- Session directory per agent
    

#### **2.2 OS Preparation**

- Python 3.10+
    
- Virtual environment
    
- Time sync enabled (important for heartbeat logic)
    

#### **2.3 Build Steps**

1. Initialize folder structure
    
2. Implement JSON utilities
    
3. Implement agent registry
    
4. Implement session-aware login manager
    
5. Add heartbeat detection
    
6. Introduce ExitReason enum
    
7. Centralize logout policy
    
8. Wire runtime to policy
    
9. Add user data normalization
    
10. Persist results safely
    

---

# 3) Final Tests

#### **3.1 Teststrategie**

- Manual runtime tests
    
- Integration testing via long scraping runs
    
- Fault injection (sleep, suspend, errors)
    

#### **3.2 Testfälle**

|Input|Expected|Result|
|---|---|---|
|Valid session|Continue|Passed|
|Expired session|Silent relogin|Passed|
|System sleep|Session deleted, no logout|Passed|
|Checkpoint|Freeze session|Passed|
|Rate limit|Freeze session|Passed|

#### **3.3 What Happens Under the Hood**

- Heartbeat monitors time gaps
    
- On suspend: intent flagged
    
- Loop exits cleanly
    
- ExitReason resolved
    
- Session deleted if unsafe
    

---

# 4) Dev Notes: Gaps to Close

#### **4.1 Optional Enhancements**

- Session health scoring
    
- Agent reputation
    
- Cooldown timers
    
- Export pipelines
    

#### **4.2 Larger Problems & Workarounds**

- instagrapi version drift → silent session discard
    
- pinned_channels_info error → session corruption handling
    
- VPS suspend → heartbeat-based exit
    

---

# 5) Dev Notes: Explanations

#### **5.1 Why No Auto-Logout**

- Logout is a security event
    
- Silent discard mimics app cache reset
    

#### **5.2 Why instagrapi**

- Mature API coverage
    
- Session replay capability
    
- Header control
    

#### **5.3 Why JSON Storage**

- Append-safe
    
- Human-readable
    
- Easy diffing and recovery
    

---

# 6) Projektergebnisse (Results)

#### **6.1 Ergebnisbeschreibung**

- Fully operational Instagram audience discovery engine
    
- Multi-agent capable
    
- Safe for long runtimes
    

#### **6.2 Abnahme**

- Self-validated (developer-owned project)
    

#### **6.3 Soll-Ist-Vergleich**

- All core goals achieved
    
- Optional features deferred intentionally
    

---

# 7) Fazit und Ausblick

- Learned real-world session lifecycle management
    
- Learned to separate policy from mechanics
    
- Built a system that survives failures gracefully
    

Future:

- SaaS wrapper
    
- Paid tiers
    
- UI dashboard
    

---

# 8) Glossar

- **Session:** Persistent authentication state
    
- **Heartbeat:** Time-gap detector
    
- **ExitReason:** Runtime intent classifier
    
- **Silent discard:** Session deletion without logout
    

---

# 9) Anhang (Appendix)

- Quellcode: agencyUtils.py, timeUtils.py
    
- Diagramme: lifecycle flow
    
- Quellen:
    
    - instagrapi docs
        
    - Instagram behavior research
        
    - Internal experiments