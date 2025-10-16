import streamlit as st
import py3Dmol
from stmol import showmol
import biotite.structure.io.pdb as pdb
import requests

# Set page config for better mobile display
st.set_page_config(
    page_title="PDB Viewer",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state
if 'pdb_str' not in st.session_state:
    st.session_state.pdb_str = None

def fetch_pdb(pdb_id):
    url = f"https://files.rcsb.org/download/{pdb_id}.pdb"
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return None

def render_mol(pdb_str, style="cartoon", color_option="default", custom_color=None):
    view = py3Dmol.view(width=800, height=600)  # Back to original fixed dimensions
    view.addModel(pdb_str, "pdb")
    
    # Apply style and color
    if color_option == "default":
        view.setStyle({style: {'color': 'spectrum'}})
    else:
        view.setStyle({style: {'color': custom_color}})
    
    view.zoomTo()
    showmol(view, height=600, width=800)  # Back to original fixed dimensions

st.title("🧬 Simple PDB Viewer")

# Sidebar styling options
with st.sidebar:
    st.markdown("## Style Options")
    style = st.selectbox(
        "Select Style",
        ["cartoon", "line", "cross", "stick", "sphere"],
        index=0
    )
    
    color_option = st.radio(
        "Color Option",
        ["Default (Spectrum)", "Custom"],
        index=0
    )
    
    custom_color = None
    if color_option == "Custom":
        custom_color = st.color_picker("Select Color", "#FF0000")

# Create two tabs for different input methods
tab1, tab2 = st.tabs(["Upload PDB", "Enter PDB ID"])

with tab1:
    uploaded_file = st.file_uploader("Upload a PDB file", type=['pdb'])
    if uploaded_file is not None:
        st.session_state.pdb_str = uploaded_file.getvalue().decode('utf-8')
        render_mol(st.session_state.pdb_str, style, 
                  "default" if color_option == "Default (Spectrum)" else "custom", 
                  custom_color)

with tab2:
    pdb_id = st.text_input("Enter PDB ID (e.g., 1AKE)").strip()
    if pdb_id:
        pdb_str = fetch_pdb(pdb_id)
        if pdb_str:
            st.session_state.pdb_str = pdb_str
            render_mol(st.session_state.pdb_str, style, 
                      "default" if color_option == "Default (Spectrum)" else "custom", 
                      custom_color)
        else:
            st.error("Unable to fetch PDB structure. Please check the ID.")

# Instructions
st.sidebar.markdown("""
## Instructions
1. Upload a PDB file or enter a PDB ID
2. The structure will be displayed automatically
3. Use mouse/touch to interact:
   - Left click/one finger: rotate
   - Right click/pinch: zoom
   - Middle click/two fingers: translate
""")
