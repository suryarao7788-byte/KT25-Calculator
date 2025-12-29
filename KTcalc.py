import streamlit as st
import random
import json
from collections import Counter

st.set_page_config(page_title="KT25 Calculator", page_icon="⚔️", layout="wide")

# 40K THEME CSS
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #0a0a0a 0%, #1a1a1a 100%);
        color: #d4af37;
    }
    h1 {
        color: #d4af37 !important;
        font-family: 'Courier New', monospace;
        text-transform: uppercase;
        letter-spacing: 3px;
        text-shadow: 2px 2px 4px rgba(212, 175, 55, 0.3);
        border-bottom: 2px solid #8b0000;
        padding-bottom: 10px;
    }
    h2, h3 {
        color: #c0c0c0 !important;
        font-family: 'Courier New', monospace;
        text-transform: uppercase;
        letter-spacing: 2px;
    }
    .stButton>button {
        background: linear-gradient(135deg, #8b0000 0%, #6b0000 100%);
        color: #d4af37;
        border: 2px solid #d4af37;
        font-weight: bold;
        text-transform: uppercase;
        letter-spacing: 1px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.5);
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background: linear-gradient(135deg, #d4af37 0%, #b8941f 100%);
        color: #000000;
        border: 2px solid #8b0000;
        transform: translateY(-2px);
    }
    [data-testid="stMetricValue"] {
        color: #d4af37;
        font-size: 32px;
        font-weight: bold;
        text-shadow: 0 0 10px rgba(212, 175, 55, 0.5);
    }
    [data-testid="stMetricLabel"] {
        color: #c0c0c0 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d0d0d 0%, #1a1a1a 100%);
        border-right: 3px solid #8b0000;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'operative_db' not in st.session_state:
    st.session_state.operative_db = {
        "Deathwatch": {
            "Plasma Gunner": {
                "weapons": {
                    "Plasma Gun": {
                        "attacks": 5,
                        "bs": 3,
                        "dmg_normal": 5,
                        "dmg_crit": 6,
                        "lethal_5": True,
                        "piercing": "Piercing 1",
                        "rending": False,
                        "severe": False,
                        "brutal": False,
                        "punishing": False
                    }
                }
            }
        },
        "Enemies": {
            "Guardsman": {
                "save": 5,
                "defense_dice": 3,
                "wounds": 7
            }
        }
    }

def roll_d6():
    return random.randint(1, 6)

def decide_action(my_normals, my_crits, opp_normals, opp_crits, strategy, opponent_is_brutal=False):
    """Decide action based on strategy. If opponent is brutal, can only block with crits."""
    
    if strategy == "Max Damage":
        if my_crits > 0:
            return "deal_crit"
        elif my_normals > 0:
            return "deal_normal"
    
    elif strategy == "Safe Play":
        # Block enemy crits first
        if opp_crits > 0 and my_crits > 0:
            return "block_crit"
        
        # If opponent is brutal, we can only block their normals with crits
        if opponent_is_brutal:
            if opp_normals > 0 and my_crits > 0:
                return "block_normal_with_crit"
        else:
            # Normal blocking rules
            if opp_normals > 0 and my_normals > 0:
                return "block_normal"
            if opp_normals > 0 and my_crits > 0:
                return "block_normal_with_crit"
        
        # No threats left, deal damage
        if my_crits > 0:
            return "deal_crit"
        elif my_normals > 0:
            return "deal_normal"
    
    elif strategy == "Efficient":
        if opp_crits > 0 and my_crits > 0:
            return "block_crit"
        
        if opponent_is_brutal:
            # Can only block with crits
            if opp_normals > 0 and my_crits > 0:
                return "block_normal_with_crit"
        else:
            if opp_normals > 0 and my_normals > 0:
                return "block_normal"
        
        if my_crits > 0:
            return "deal_crit"
        elif my_normals > 0:
            return "deal_normal"
        
        if not opponent_is_brutal and opp_normals > 0 and my_crits > 0:
            return "block_normal_with_crit"
    
    elif strategy == "Crit Priority":
        if opp_crits > 0 and my_crits > 0:
            return "block_crit"
        if my_crits > 0:
            return "deal_crit"
        elif my_normals > 0:
            return "deal_normal"
    
    # Fallback
    if my_crits > 0:
        return "deal_crit"
    elif my_normals > 0:
        return "deal_normal"
    
    return "deal_normal"

def resolve_melee(att_n, att_c, def_n, def_c, att_dmg_n, att_dmg_c, def_dmg_n, def_dmg_c, 
                  att_strat, def_strat, att_brutal=False, def_brutal=False):
    """Resolve melee with brutal rules"""
    att_normals = att_n
    att_crits = att_c
    def_normals = def_n
    def_crits = def_c
    
    att_damage = 0
    def_damage = 0
    
    current_is_attacker = True
    
    while (att_normals > 0 or att_crits > 0) and (def_normals > 0 or def_crits > 0):
        if current_is_attacker:
            action = decide_action(att_normals, att_crits, def_normals, def_crits, att_strat, def_brutal)
            
            if action == "deal_crit":
                att_damage += att_dmg_c
                att_crits -= 1
            elif action == "deal_normal":
                att_damage += att_dmg_n
                att_normals -= 1
            elif action == "block_crit":
                att_crits -= 1
                def_crits -= 1
            elif action == "block_normal_with_crit":
                att_crits -= 1
                def_normals -= 1
            elif action == "block_normal":
                # Only allowed if defender is not brutal
                if not def_brutal:
                    att_normals -= 1
                    def_normals -= 1
                else:
                    # Can't block, must deal damage instead
                    att_damage += att_dmg_n
                    att_normals -= 1
        else:
            action = decide_action(def_normals, def_crits, att_normals, att_crits, def_strat, att_brutal)
            
            if action == "deal_crit":
                def_damage += def_dmg_c
                def_crits -= 1
            elif action == "deal_normal":
                def_damage += def_dmg_n
                def_normals -= 1
            elif action == "block_crit":
                def_crits -= 1
                att_crits -= 1
            elif action == "block_normal_with_crit":
                def_crits -= 1
                att_normals -= 1
            elif action == "block_normal":
                if not att_brutal:
                    def_normals -= 1
                    att_normals -= 1
                else:
                    def_damage += def_dmg_n
                    def_normals -= 1
        
        current_is_attacker = not current_is_attacker
    
    # Resolve remaining dice
    while att_normals > 0 or att_crits > 0:
        if att_crits > 0:
            att_damage += att_dmg_c
            att_crits -= 1
        elif att_normals > 0:
            att_damage += att_dmg_n
            att_normals -= 1
    
    while def_normals > 0 or def_crits > 0:
        if def_crits > 0:
            def_damage += def_dmg_c
            def_crits -= 1
        elif def_normals > 0:
            def_damage += def_dmg_n
            def_normals -= 1
    
    return (att_damage, def_damage)

# TITLE
st.title("🎲 Kill Team 2024 - Monte Carlo Simulator")
st.markdown("**With Brutal & Punishing rules**")

# Combat type
combat_type = st.radio("Combat Type", ["🎯 Shooting", "⚔️ Melee"], horizontal=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("⚔️ Attacker")
    attacks = st.number_input("Number of attacks", 1, 10, 4, key="att_attacks")
    skill = st.number_input("Skill (hit on X+)", 2, 6, 3, key="att_skill")
    dmg_normal = st.number_input("Normal damage", 1, 10, 3, key="att_dmg_n")
    dmg_crit = st.number_input("Crit damage", 1, 10, 4, key="att_dmg_c")
    
    st.markdown("**Special Rules:**")
    col_a, col_b = st.columns(2)
    with col_a:
        lethal_5 = st.checkbox("Lethal 5+", key="att_lethal")
        rending = st.checkbox("Rending", key="att_rending")
        brutal = st.checkbox("Brutal", help="Dice can only be blocked with crits")
    with col_b:
        severe = st.checkbox("Severe", key="att_severe")
        punishing = st.checkbox("Punishing", help="If any crit, convert 1 fail to hit")
        if combat_type == "🎯 Shooting":
            piercing = st.selectbox("Piercing", ["None", "Piercing 1", "Piercing 2", "P(Crits) 1", "P(Crits) 2"])
    
    if combat_type == "⚔️ Melee":
        attacker_strategy = st.selectbox("Strategy", 
            ["Max Damage", "Safe Play", "Efficient", "Crit Priority"],
            key="att_strat")

with col2:
    st.subheader("🎯 Defender")
    
    if combat_type == "🎯 Shooting":
        defender_save = st.number_input("Save (X+)", 2, 6, 5, key="def_save")
        defense_dice = st.number_input("Defense dice", 0, 5, 3, key="def_dice")
        defender_wounds = st.number_input("Wounds", 1, 30, 7, key="def_wounds")
        
        st.markdown("**Defensive Modifiers:**")
        col_a, col_b = st.columns(2)
        with col_a:
            cover_type = st.selectbox("Cover", ["None", "Light (1 normal)", "Heavy (2 normal)", "Crit (1 crit)"])
        with col_b:
            obscured = st.checkbox("Obscured")
    else:
        def_attacks = st.number_input("Defender Attacks", 1, 10, 4, key="def_attacks")
        def_skill = st.number_input("Defender Skill (X+)", 2, 6, 4, key="def_skill")
        def_dmg_normal = st.number_input("Defender Normal Dmg", 1, 10, 3, key="def_dmg_n")
        def_dmg_crit = st.number_input("Defender Crit Dmg", 1, 10, 4, key="def_dmg_c")
        defender_wounds = st.number_input("Defender Wounds", 1, 30, 18, key="def_wounds")
        attacker_wounds = st.number_input("Attacker Wounds", 1, 30, 18, key="att_wounds")
        
        st.markdown("**Defender Special Rules:**")
        col_a, col_b = st.columns(2)
        with col_a:
            def_brutal = st.checkbox("Defender Brutal", key="def_brutal")
        with col_b:
            def_punishing = st.checkbox("Defender Punishing", key="def_punishing")
        
        defender_strategy = st.selectbox("Defender Strategy",
            ["Max Damage", "Safe Play", "Efficient", "Crit Priority"],
            index=1,
            key="def_strat")

st.markdown("---")

if st.button("🎲 Run Simulation (10,000 trials)", type="primary", use_container_width=True):
    num_trials = 10000
    
    st.success("## 📊 Simulation Results")
    st.caption(f"Based on {num_trials:,} simulated sequences")
    
    total_damage = 0
    total_def_damage = 0
    kill_count = 0
    def_kill_count = 0
    mutual_kills = 0
    damage_outcomes = []
    def_damage_outcomes = []
    
    total_normals = 0
    total_crits = 0
    total_misses = 0
    
    with st.spinner(f"Running {num_trials:,} simulations..."):
        for trial in range(num_trials):
            if combat_type == "🎯 Shooting":
                # SHOOTING SIMULATION
                normal_hits = 0
                crits = 0
                fails = 0
                
                for _ in range(attacks):
                    roll = roll_d6()
                    
                    if lethal_5 and roll >= 5:
                        crits += 1
                        total_crits += 1
                    elif roll == 6:
                        crits += 1
                        total_crits += 1
                    elif roll >= skill:
                        normal_hits += 1
                        total_normals += 1
                    else:
                        fails += 1
                        total_misses += 1
                
                # PUNISHING: If any crit, convert 1 fail to hit
                if punishing and crits >= 1 and fails >= 1:
                    normal_hits += 1
                    fails -= 1
                
                if normal_hits == 0 and crits == 0:
                    damage_outcomes.append(0)
                    continue
                
                # Apply Obscured
                if obscured:
                    normal_hits += crits
                    crits = 0
                    if normal_hits >= 1:
                        normal_hits -= 1
                
                # Apply Rending and Severe
                if rending and crits >= 1 and normal_hits >= 1:
                    crits += 1
                    normal_hits -= 1
                
                if severe and crits == 0 and normal_hits >= 1:
                    crits += 1
                    normal_hits -= 1
                
                if normal_hits == 0 and crits == 0:
                    damage_outcomes.append(0)
                    continue
                
                # Apply Piercing
                actual_defense = defense_dice
                if piercing == "Piercing 1":
                    actual_defense = max(0, defense_dice - 1)
                elif piercing == "Piercing 2":
                    actual_defense = max(0, defense_dice - 2)
                elif piercing == "P(Crits) 1" and crits > 0:
                    actual_defense = max(0, defense_dice - 1)
                elif piercing == "P(Crits) 2" and crits > 0:
                    actual_defense = max(0, defense_dice - 2)
                
                normal_saves = 0
                crit_saves = 0
                
                for _ in range(actual_defense):
                    roll = roll_d6()
                    if roll == 6:
                        crit_saves += 1
                    elif roll >= defender_save:
                        normal_saves += 1
                
                # Add cover
                if cover_type == "Light (1 normal)":
                    normal_saves += 1
                elif cover_type == "Heavy (2 normal)":
                    normal_saves += 2
                elif cover_type == "Crit (1 crit)":
                    crit_saves += 1
                
                # BRUTAL: Normal hits can only be blocked by crits
                if brutal:
                    # Crits can be blocked by crit saves
                    remaining_crits = max(0, crits - crit_saves)
                    leftover_crit_saves = max(0, crit_saves - crits)
                    
                    # Normal hits can only be blocked by leftover crit saves
                    remaining_normals = max(0, normal_hits - leftover_crit_saves)
                else:
                    # Normal blocking rules
                    remaining_crits = max(0, crits - crit_saves)
                    leftover_crit_saves = max(0, crit_saves - crits)
                    total_saves_for_normals = normal_saves + leftover_crit_saves
                    remaining_normals = max(0, normal_hits - total_saves_for_normals)
                
                damage = (remaining_normals * dmg_normal) + (remaining_crits * dmg_crit)
                total_damage += damage
                damage_outcomes.append(damage)
                
                if damage >= defender_wounds:
                    kill_count += 1
            
            else:
                # MELEE SIMULATION
                att_normals = 0
                att_crits = 0
                att_fails = 0
                
                for _ in range(attacks):
                    roll = roll_d6()
                    if lethal_5 and roll >= 5:
                        att_crits += 1
                    elif roll == 6:
                        att_crits += 1
                    elif roll >= skill:
                        att_normals += 1
                    else:
                        att_fails += 1
                
                # Punishing for attacker
                if punishing and att_crits >= 1 and att_fails >= 1:
                    att_normals += 1
                    att_fails -= 1
                
                # Defender rolls
                def_normals = 0
                def_crits = 0
                def_fails = 0
                
                for _ in range(def_attacks):
                    roll = roll_d6()
                    if roll == 6:
                        def_crits += 1
                    elif roll >= def_skill:
                        def_normals += 1
                    else:
                        def_fails += 1
                
                # Punishing for defender
                if def_punishing and def_crits >= 1 and def_fails >= 1:
                    def_normals += 1
                    def_fails -= 1
                
                # Apply Rending and Severe for attacker
                if rending and att_crits >= 1 and att_normals >= 1:
                    att_crits += 1
                    att_normals -= 1
                if severe and att_crits == 0 and att_normals >= 1:
                    att_crits += 1
                    att_normals -= 1
                
                # Resolve melee
                att_dmg, def_dmg = resolve_melee(
                    att_normals, att_crits, def_normals, def_crits,
                    dmg_normal, dmg_crit, def_dmg_normal, def_dmg_crit,
                    attacker_strategy, defender_strategy,
                    brutal, def_brutal
                )
                
                total_damage += att_dmg
                total_def_damage += def_dmg
                damage_outcomes.append(att_dmg)
                def_damage_outcomes.append(def_dmg)
                
                att_killed = att_dmg >= defender_wounds
                def_killed = def_dmg >= attacker_wounds
                
                if att_killed and def_killed:
                    mutual_kills += 1
                elif att_killed:
                    kill_count += 1
                elif def_killed:
                    def_kill_count += 1
    
    # Calculate stats
    avg_damage = total_damage / num_trials
    kill_pct = (kill_count / num_trials) * 100
    min_dmg = min(damage_outcomes) if damage_outcomes else 0
    max_dmg = max(damage_outcomes) if damage_outcomes else 0
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("💥 Avg Damage", f"{avg_damage:.2f}")
    with col2:
        st.metric("📉 Min", f"{min_dmg}")
    with col3:
        st.metric("📈 Max", f"{max_dmg}")
    with col4:
        st.metric("🎯 Kill %", f"{kill_pct:.1f}%")
    
    if combat_type == "⚔️ Melee":
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        avg_def_dmg = total_def_damage / num_trials
        def_kill_pct = (def_kill_count / num_trials) * 100
        mutual_pct = (mutual_kills / num_trials) * 100
        
        with col1:
            st.metric("🔴 Defender Avg Dmg", f"{avg_def_dmg:.2f}")
        with col2:
            st.metric("🔴 Defender Kills", f"{def_kill_pct:.1f}%")
        with col3:
            st.metric("⚔️ Mutual Kills", f"{mutual_pct:.1f}%")
    
    st.markdown("---")
    st.markdown("### 📊 Damage Distribution")
    
    damage_counts = Counter(damage_outcomes)
    
    for dmg in sorted(damage_counts.keys()):
        count = damage_counts[dmg]
        pct = (count / num_trials) * 100
        bar = "█" * min(int(pct * 2), 50)
        
        if dmg >= defender_wounds:
            st.markdown(f"💀 **{dmg} damage:** {pct:.1f}% {bar}")
        else:
            st.write(f"{dmg} damage: {pct:.1f}% {bar}")


st.caption("✅ Full KT24 simulator with Brutal & Punishing!")
