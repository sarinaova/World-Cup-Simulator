# World-Cup-Simulator
A simple world cup soccer simulation for university project.

### 📌 Key Features

- 🏗️ **Modular & Object-Oriented Design:** Clean architecture utilizing dedicated classes (`ClassTeam`, `ClassMatch`, `ClassGroup`, and `WorldCupSimulator`) for clear separation of concerns.
- 📊 **Accurate Statistical Modeling:** Uses the Poisson distribution (`NumPy`) based on team attack and defense ratings to determine match goals.
- 🎲 **Standard Draw & Group Standings:** FIFA rank-based seeding, 8-group draw (4 teams each), and complete tie-breaking rules (Points, Goal Difference, Goals Scored, and Random Draw).
- ⚽ **Knockout Stage & Penalty Shootouts:** Realistically simulates extra time and penalty shootouts (5 initial rounds + sudden death) with balanced probability logic.
- 🔄 **Monte Carlo Simulation:** Capability to simulate the entire tournament as many times as desired (e.g., 1,000 iterations) to calculate team championship probabilities.
  ---

## 🛠️ Tech Stack & Dependencies

Built with **Python 3.6+**.

### External Libraries
- **`numpy`**: High-performance statistical sampling (`np.random.poisson`) written in C for fast execution during large-scale simulations.

### Built-in Modules
- **`csv`**: Parsing initial team data (`teams_2026_worldcup.csv`).
- **`random`**: Fair group draws (Mersenne Twister algorithm) and penalty shootout mechanics.
- **`os`**: File system validation to prevent runtime errors (`FileNotFoundError`).

📂 Project Structure
.
├── ClassTeam.py                # Team class definition and statistics
├── ClassMatch.py               # Match logic & Poisson simulation
├── ClassGroup.py               # Group standings & tie-breaking logic
├── WorldCupSimulator.py        # Main tournament manager class
├── main.py                     # Entry point & CLI menu
├── teams_2026_worldcup.csv     # Input dataset
└── README.md                   # Project documentation
