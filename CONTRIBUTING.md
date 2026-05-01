# 🤝 Contributing to Trevo AI Tourism Tools

First off, thank you for considering contributing to Trevo! It's people like you who will help build the **Operating System for Smart Tourism**.

We are building a scalable, AI-driven infrastructure to empower 6,350+ tourism SMEs in the MENA region to capture their share of the **$950B global experience economy**.

---

## 🏗️ Technical Stack & Structure
Trevo uses a **Decoupled Architecture**:
*   **Backend:** Python / Flask API (`/api/app.py`).
*   **Logic Engines:** Specialized Python modules for Geo-VR and Itinerary Optimization (`/tools/`).
*   **Frontend:** React-based single-page application (`/index.html`).

---

## 🛠️ How to Set Up Your Local Environment
To contribute to the code, you need to run the full-stack environment locally:

1.  **Fork & Clone:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/trevo-ai-tourism-tools.git](https://github.com/YOUR_USERNAME/trevo-ai-tourism-tools.git)
    cd trevo-ai-tourism-tools
    ```

2.  **Install Dependencies:**
    ```bash
    pip install flask flask-cors
    ```

3.  **Run the Backend Engine:**
    ```bash
    python api/app.py
    ```
    *The API will be live at `http://127.0.0.1:5000`.*

4.  **Launch the Frontend:**
    Open `index.html` in your browser. Ensure the status indicator shows **"Engine: Online"**.

---

## 🎯 Priority Contribution Areas
We are currently looking for help in these specific areas (Phase 2 & 3 of our Roadmap):

*   **AI & Logic:** Improving the `ItineraryOptimizer` using advanced algorithms (e.g., Genetic Algorithms).
*   **Geospatial VR:** Integrating **Mapbox GL JS** to visualize 360° previews on interactive maps.
*   **FinTech Layer:** Developing secure API schemas for regional travel payment gateways.
*   **UI/UX:** Enhancing the Dashboard with real-time data visualization.

---

## 📋 Submission Process
1.  **Search** for existing Issues or open a new one to discuss your idea.
2.  **Create a feature branch** (`git checkout -b feature/AmazingFeature`).
3.  **Commit** your changes with clear, descriptive messages.
4.  **Push** to the branch and open a **Pull Request**.

---

## ⚖️ Code of Conduct
By participating, you agree to maintain a professional and respectful environment. We celebrate the diversity of our global community.

---
**Questions?** Open an issue or reach out to the project lead, **Sherif Almeidany**. 🚀
