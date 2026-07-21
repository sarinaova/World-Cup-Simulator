# World-Cup-Simulator
A simple world cup soccer simulation for university project.

### 📌 Key Features

- 🏗️ **Object-Oriented Architecture (OOP):** Modular design featuring dedicated classes for `Team`, `Match`, `Group`, and `WorldCupSimulator`.
- 📊 **Accurate Statistical Modeling:** Uses the Poisson distribution (`NumPy`) based on team attack and defense ratings to determine match goals.
- 🎲 **Standard Draw & Group Standings:** FIFA rank-based seeding, 8-group draw (4 teams each), and complete tie-breaking rules (Points, Goal Difference, Goals Scored, and Random Draw).
- ⚽ **Knockout Stage & Penalty Shootouts:** Realistically simulates extra time and penalty shootouts (5 initial rounds + sudden death) with balanced probability logic.
- 🔄 **Monte Carlo Simulation:** Capability to simulate the entire tournament as many times as desired (e.g., 1,000 iterations) to calculate team championship probabilities.
