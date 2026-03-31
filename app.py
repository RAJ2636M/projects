import streamlit as st
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt
import base64


def set_bg():
    with open("bg.webp", "rb") as f:
        data = f.read()
    encoded = base64.b64encode(data).decode()

    st.markdown(f"""
    <style>
    .stApp {{
        background-image: url("data:image/webp;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}

    /* Dark overlay for readability */
    .stApp::before {{
        content: "";
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.6);
        z-index: -1;
    }}
    </style>
    """, unsafe_allow_html=True)

set_bg()

st.markdown("""
<style>
.block-container {
    background: rgba(0, 0, 0, 0.55);
    padding: 2rem;
    border-radius: 15px;
    backdrop-filter: blur(10px);
}
</style>
""", unsafe_allow_html=True)

st.title("🏥 Hospital Referral Network Model")
st.divider()

st.subheader("📘 About This Application")

st.write("""
This application models a **Hospital Referral Network** using graph theory.

- Each **Doctor** is represented as a node.
- Each **Referral** (A → B) means Doctor A refers a patient to Doctor B.
- The system analyzes relationships between doctors using network metrics.
""")

st.subheader("🧑‍💻 How to Use")

st.write("""
1. **Add Doctors**  
   Enter doctor names and click *Add Doctor*.

2. **Create Referrals**  
   Select two doctors and create a referral connection.

3. **View Analysis**  
   Once referrals are added:
   - A table will show centrality values.
   - A graph will visualize the network.
   - Insights will highlight important doctors.

4. **Reset Network**  
   Click reset to start fresh.
""")

st.subheader("📊 What the Data Means")

st.write("""
- **Degree Centrality**  
  Shows how many direct connections a doctor has.  
  👉 Higher value = handles more referrals.

- **Betweenness Centrality**  
  Shows how often a doctor connects others.  
  👉 Higher value = acts as a bridge.

- **Closeness Centrality**  
  Shows how quickly a doctor can reach others.  
  👉 Higher value = more centrally located.
""")

# Session State Initialization
if 'nodes' not in st.session_state:
    st.session_state.nodes = []
if 'referrals' not in st.session_state:
    st.session_state.referrals = []

# -------------------- ADD DOCTORS --------------------
st.header("➕ Add Data")
new_node = st.text_input("Enter Doctor Name:", placeholder="e.g. Dr. A")

if st.button("Add Doctor"):
    if new_node and new_node not in st.session_state.nodes:
        st.session_state.nodes.append(new_node)
        st.success(f"{new_node} added successfully!")
        

st.divider()

# -------------------- ADD REFERRALS --------------------
if len(st.session_state.nodes) >= 2:
    s = st.selectbox("From:", st.session_state.nodes)
    t = st.selectbox("To:", st.session_state.nodes)

    if st.button("Add Referral"):
        if s == t:
            st.warning("⚠️ Doctor cannot refer to themselves!")
        elif (s, t) not in st.session_state.referrals:
            st.session_state.referrals.append((s, t))
            st.success(f"Referral added: {s} → {t}")
            st.rerun()

st.divider()

# -------------------- RESET --------------------
if st.button("Reset Network"):
    st.session_state.nodes = []
    st.session_state.referrals = []
    st.rerun()

# -------------------- GRAPH --------------------
if st.session_state.nodes:
    G = nx.DiGraph()
    G.add_nodes_from(st.session_state.nodes)
    G.add_edges_from(st.session_state.referrals)

# -------------------- CENTRALITY --------------------
st.subheader("📊 Centrality Analysis")

if len(st.session_state.referrals) > 0:
    deg = nx.degree_centrality(G)
    bet = nx.betweenness_centrality(G)
    clo = nx.closeness_centrality(G)

    df = pd.DataFrame({
        "Doctor": st.session_state.nodes,
        "Degree": [round(deg.get(n, 0), 3) for n in st.session_state.nodes],
        "Betweenness": [round(bet.get(n, 0), 3) for n in st.session_state.nodes],
        "Closeness": [round(clo.get(n, 0), 3) for n in st.session_state.nodes]
    })

    st.table(df)

    # -------------------- BAR CHART --------------------
    st.subheader("📊 Centrality Comparison Chart")
    st.bar_chart(df.set_index("Doctor"))

    # -------------------- MEANING --------------------
    st.subheader("📖 Meaning of Results")
    st.write("""
    - **Degree Centrality**: Number of direct connections (referrals handled).
    - **Betweenness Centrality**: Acts as a bridge between doctors.
    - **Closeness Centrality**: How quickly a doctor can reach others.
    """)

    # -------------------- GRAPH VISUAL --------------------
    st.subheader("🕸️ Live Graph View")

    fig, ax = plt.subplots(figsize=(8, 6))

    # Improved layout
    pos = nx.spring_layout(G)

    # Find top nodes
    top_degree = max(deg, key=deg.get)
    top_betweenness = max(bet, key=bet.get)
    top_closeness = max(clo, key=clo.get)

    # Node coloring
    node_colors = []
    for node in G.nodes():
        if node == top_degree:
            node_colors.append('green')      # Most connections
        elif node == top_betweenness:
            node_colors.append('orange')     # Bridge
        elif node == top_closeness:
            node_colors.append('red')        # Central
        else:
            node_colors.append('lightblue')

    nx.draw(
        G, pos,
        with_labels=True,
        node_color=node_colors,
        node_size=2000,
        arrowsize=20,
        font_weight='bold',
        ax=ax
    )

    st.pyplot(fig)

    # -------------------- INSIGHTS --------------------
    st.subheader("📌 Key Insights")

    st.write(f"🟢 {top_degree} - has the highest number of connections (most referrals).")
    st.write(f"🟠 {top_betweenness} - acts as a bridge doctor connecting others.")
    st.write(f"🔴 {top_closeness} - is centrally located and can reach others quickly.")

else:
    st.info("ℹ️ Add referrals to see centrality metrics.")
