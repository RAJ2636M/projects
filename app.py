import streamlit as st
import networkx as nx
import pandas as pd
import matplotlib.pyplot as plt

st.title("Hospital Referral Network Model")
st.divider()

if 'nodes' not in st.session_state:
    st.session_state.nodes = []
if 'referrals' not in st.session_state:
    st.session_state.referrals = []

st.header("Add Data")
new_node = st.text_input("Enter Doctor Name:", placeholder="e.g. Dr.A")
if st.button("Add Doctor"):
    if new_node and new_node not in st.session_state.nodes:
        st.session_state.nodes.append(new_node)
        st.rerun()
st.divider()
if len(st.session_state.nodes) >= 2:
    s = st.selectbox("From:",st.session_state.nodes)
    t = st.selectbox("To:",st.session_state.nodes)
    if st.button("Add Referral"):
        if (s,t) not in st.session_state.referrals:
            st.session_state.referrals.append((s,t))
            st.rerun()
st.divider()
if st.button("Reset Network"):
    st.session_state.nodes = []
    st.session_state.referrals = []
    st.rerun()

if st.session_state.nodes:
    G = nx.DiGraph()
    G.add_nodes_from(st.session_state.nodes)
    G.add_edges_from(st.session_state.referrals)
st.subheader("📊 Centrality Analysis")
if len(st.session_state.referrals) > 0:
    deg = nx.degree_centrality(G)
    bet = nx.betweenness_centrality(G)
    clo = nx.closeness_centrality(G)
    
    df = pd.DataFrame({
        "Doctor": st.session_state.nodes,
        "Degree": [f"{deg.get(n, 0):.3f}" for n in st.session_state.nodes],
        "Betweenness": [f"{bet.get(n, 0):.3f}" for n in st.session_state.nodes],
        "Closeness": [f"{clo.get(n, 0):.3f}" for n in st.session_state.nodes]
    })
    st.table(df)
    st.subheader("Meaning of Results")

    st.write("""
    - **Degree Centrality**: Shows how many direct connections a doctor has.
    Higher value means the doctor handles more referrals.

    - **Betweenness Centrality**: Shows how often a doctor acts as a bridge between others.
    Higher value means the doctor connects different doctors.

    - **Closeness Centrality**: Shows how close a doctor is to all others.
    Higher value means faster access to other doctors.
    """)
    st.subheader("🕸️ Live Graph View")
    fig, ax = plt.subplots(figsize=(8, 6))
    pos = nx.circular_layout(G) 
    nx.draw(G, pos, with_labels=True,node_color='lightblue',node_size=2000,arrowsize=20,font_weight='bold',ax=ax)
    st.pyplot(fig)
    top_degree = max(deg, key=deg.get)
    top_betweenness = max(bet, key=bet.get)
    top_closeness = max(clo, key=clo.get)

    st.subheader("📌 Key Insights")

    st.write(f"1. {top_degree} - has the highest number of connections (most referrals).")

    st.write(f"2. {top_betweenness} - acts as a bridge doctor connecting other doctors.")

    st.write(f"3. {top_closeness} - is centrally located and can reach other doctors quickly.")
else:
    st.info("Add referrals to see centrality metrics.")
