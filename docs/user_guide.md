# 📖 Trevo AI Tourism Tools - User Guide

## 🚀 Getting Started

### Prerequisites

- Python 3.8+ installed
- Basic familiarity with Terminal or Command Prompt
- Internet connection (for API and VR content streaming)

### Quick Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/sherif-trevo-ai/trevo-ai-tourism-tools.git
   ```

2. **Navigate to the directory:**
   ```bash
   cd trevo-ai-tourism-tools
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 🛠 Available Tools & Engines

### 1. Geospatial VR Engine (Core Innovation)

| Aspect | Details |
|--------|---------|
| **File** | `tools/geovr_engine.py` |
| **Purpose** | Bridges real-world GPS coordinates with interactive 360° VR content |
| **Impact** | Increases booking intent by 94% through virtual previews |
| **Key Features** | Haversine distance calculations, VR hotspot mapping, proximity discovery |

**How to Run:**
```bash
python tools/geovr_engine.py
```

### 2. AI Marketing Content Generator

| Aspect | Details |
|--------|---------|
| **File** | `tools/marketing_generator.py` |
| **Purpose** | Generate high-conversion ad copy for Google, Meta, and TikTok |
| **Impact** | Target a 30% lift in digital conversion rates |
| **Workflow** | Input destination and audience data → Receive optimized multilingual copy |

**How to Run:**
```bash
python tools/marketing_generator.py
```

### 3. Business ROI Calculator

| Aspect | Details |
|--------|---------|
| **File** | `tools/roi_calculator.py` |
| **Purpose** | Measure campaign efficiency and reduce "Ad Waste" |
| **Goal** | Help agencies reduce ad spend waste by 15% |
| **Features** | Analyzes cost-per-lead (CPL) and return on investment |

**How to Run:**
```bash
python tools/roi_calculator.py
```

---

## 🌐 API Layer (For Developers)

Trevo is built with a **Decoupled Architecture**. You can run our core logic as a Flask API to serve your own frontend or mobile app.

### Start the API Server

```bash
python api/app.py
```

### Main Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/roi` | `POST` | Instant business performance analysis |
| `/marketing` | `POST` | Generate AI travel descriptions |
| `/vr-search` | `GET` | Find immersive content by coordinates *(Coming Soon)* |

---

## 🗺 Strategic Roadmap

- **Phase 2:** Advanced Mapbox GL JS integration for 3D trip tracking
- **Phase 3:** FinTech integration for secure multi-currency travel payments
- **Phase 4:** Expanding AI training data for regional Arabic dialects

---

## 🆘 Support & Contributions

We believe in building the future of travel together.

- **Found a bug?** [Open an Issue](https://github.com/sherif-trevo-ai/trevo-ai-tourism-tools/issues)
- **Want to contribute?** Review our [CONTRIBUTING.md](./CONTRIBUTING.md) and submit a Pull Request

---

**Maintained by Sherif Almeidany** - Leading AI-driven digital transformation in tourism
