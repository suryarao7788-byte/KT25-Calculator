# ⚔️ Kill Team 2025 Monte Carlo Simulator

A comprehensive combat simulator for Warhammer 40,000: Kill Team (2025 Edition) featuring full shooting and melee mechanics with 10,000-trial Monte Carlo analysis.

![Kill Team Simulator](https://img.shields.io/badge/Warhammer-40K-darkred)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.0+-red)

## 🎯 Features

### Combat Systems
- **Shooting Combat**: Full ranged attack resolution with defense dice and saves
- **Melee Combat**: Interactive turn-based resolution with strategic decision-making
- **Monte Carlo Simulation**: 10,000 trials for statistically accurate probability analysis

### Special Rules Implemented
- ✅ **Lethal 5+** - 5s and 6s count as critical hits
- ✅ **Rending** - Convert normal hit to crit when you have crits
- ✅ **Severe** - Convert normal to crit when you have no crits
- ✅ **Brutal** - Your dice can only be blocked with critical successes
- ✅ **Punishing** - Convert one fail to a hit when you score any crit
- ✅ **Piercing (1/2)** - Reduce enemy defense dice
- ✅ **Piercing (Crits)** - Reduce defense dice only when scoring crits
- ✅ **Cover** (Light/Heavy/Crit) - Additional automatic saves
- ✅ **Obscured** - Converts crits to normals and discards one success

### Melee Strategies
Four distinct AI strategies for melee resolution:
- **Max Damage**: Always prioritize dealing damage
- **Safe Play**: Block threats before attacking
- **Efficient**: Match dice types (normal blocks normal, crit blocks crit)
- **Crit Priority**: Focus on blocking enemy crits only

### Statistical Analysis
- Average, minimum, and maximum damage
- Kill probability percentages
- Complete damage distribution with visual bars
- Mutual kill tracking for melee combat
- Defender damage and counter-kill statistics

## 🚀 Live Demo

**[Try it now!](#)** *(Add your Streamlit Cloud URL here)*

## 📦 Installation

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/yourusername/kt24-simulator.git
cd kt24-simulator
```

2. Install requirements:
```bash
pip install -r requirements.txt
```

3. Run the app:
```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## 🎲 How to Use

### Shooting Combat
1. Select **Shooting** combat type
2. Configure attacker stats (Attacks, BS, Damage)
3. Enable special rules (Lethal, Rending, Brutal, etc.)
4. Configure defender stats (Save, Defense Dice, Wounds)
5. Add defensive modifiers (Cover, Obscured)
6. Click **Run Simulation**

### Melee Combat
1. Select **Melee** combat type
2. Configure both attacker and defender weapons
3. Set wounds for both operatives
4. Choose combat strategies for each side
5. Enable special rules (Brutal, Punishing, etc.)
6. Click **Run Simulation**

## 📊 Understanding Results

### Key Metrics
- **Avg Damage**: Expected damage per attack sequence
- **Min/Max Damage**: Damage range across all simulations
- **Kill %**: Probability of eliminating the target
- **Damage Distribution**: Frequency of each damage outcome

### Melee-Specific Metrics
- **Defender Avg Dmg**: Damage dealt back to the attacker
- **Defender Kills**: Probability defender eliminates attacker
- **Mutual Kills**: Probability both operatives are eliminated

## 🔧 Technical Details

### Technology Stack
- **Python 3.8+**
- **Streamlit** - Web framework
- **Random** - Dice roll simulation
- **Collections** - Statistical analysis

### Simulation Methodology
- 10,000 Monte Carlo trials per simulation
- True random dice rolling using Python's `random` module
- Sequential rule application matching official game order
- Turn-based melee resolution with strategy algorithms

### Rule Implementation
Rules are applied in official Kill Team sequence:
1. Roll attack dice → Apply Lethal/Punishing
2. Apply Obscured modifier
3. Apply Rending/Severe conversions
4. Roll defense dice with Piercing reduction
5. Add Cover auto-saves
6. Match saves vs hits (with Brutal override)
7. Calculate final damage

## 🤝 Contributing

Contributions welcome! Areas for improvement:
- Additional special rules (Sustained Hits, Blast, etc.)
- Operative database with preset profiles
- Save/load functionality for custom operatives
- Graphical damage distribution charts
- Export results to CSV/JSON

## 📝 License

This project is open source and available under the MIT License.

## ⚠️ Disclaimer

This is an unofficial fan-made tool. Warhammer 40,000 and Kill Team are registered trademarks of Games Workshop Limited. This project is not affiliated with, endorsed by, or associated with Games Workshop.

## 🙏 Acknowledgments

- Games Workshop for Kill Team 2024
- The Kill Team community for rules clarification
- Streamlit for the awesome framework

## 📧 Contact

Questions? Suggestions? Open an issue or reach out!

---

**For the Emperor!** ⚔️
```

## Repository Description (Short)
```
⚔️ Kill Team 2024 Monte Carlo combat simulator with full shooting/melee mechanics, special rules (Lethal, Brutal, Punishing), and 10,000-trial statistical analysis. Built with Python & Streamlit.
```

## GitHub Topics/Tags
```
warhammer-40k
kill-team
wargaming
tabletop
simulator
monte-carlo
python
streamlit
dice-simulator
statistics
combat-calculator
```

## .gitignore
```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/

# Streamlit
.streamlit/

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
