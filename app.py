import sys
import os
import traceback
from pathlib import Path

# Force immediate log flushing to Streamlit Cloud console
try:
    sys.stdout.reconfigure(line_buffering=True)
    sys.stderr.reconfigure(line_buffering=True)
except Exception:
    pass

print(">>> [CAF PROBE] app.py starting execution...")

import streamlit as st

st.set_page_config(page_title="CAF Startup Diagnostics", layout="wide")
st.title("🛠️ CAF Deployment Diagnostic Probe")

# 1. Environment & Path Inspection
root_dir = Path(__file__).resolve().parent
if str(root_dir) not in sys.path:
    sys.path.insert(0, str(root_dir))

st.subheader("1. Environment Checks")
col1, col2 = st.columns(2)
with col1:
    st.write(f"**Python Version:** {sys.version.split()[0]}")
    st.write(f"**Working Directory:** `{os.getcwd()}`")
with col2:
    st.write(f"**Root Directory:** `{root_dir}`")
    st.write(f"**`caf` package directory exists:** `{(root_dir / 'caf').is_dir()}`")

print(f">>> [CAF PROBE] sys.path injected: {root_dir}")

# 2. Module Import Test
st.subheader("2. Testing CAF UI Import")
try:
    print(">>> [CAF PROBE] Attempting import: from caf.ui.demo_dashboard import main ...")
    with st.spinner("Importing `caf.ui.demo_dashboard`..."):
        from caf.ui.demo_dashboard import main
    st.success("✅ Successfully imported `caf.ui.demo_dashboard.main`!")
    print(">>> [CAF PROBE] Import succeeded.")
except Exception as e:
    st.error(f"❌ Failed during import: {e}")
    st.code(traceback.format_exc())
    print(f">>> [CAF PROBE] Import failed with exception:\n{traceback.format_exc()}")
    st.stop()

# 3. Execution Test
st.subheader("3. Launching Application")
if st.button("🚀 Run CAF Application Now", type="primary"):
    st.info("Handing control over to `caf.ui.demo_dashboard.main()`...")
    print(">>> [CAF PROBE] Invoking main()...")
    try:
        main()
    except Exception as e:
        st.error(f"❌ Error during main() execution: {e}")
        st.code(traceback.format_exc())
        print(f">>> [CAF PROBE] main() raised exception:\n{traceback.format_exc()}")
else:
    st.caption("Click the button above to execute `main()` and verify execution.")
