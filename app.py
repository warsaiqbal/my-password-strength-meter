import streamlit as st
import zxcvbn

# Set page configuration
st.set_page_config(page_title="Password Strength Meter", page_icon="🔒")

# Add simple CSS
st.markdown("""
<style>
    .meter { height: 10px; border-radius: 5px; margin: 10px 0 20px 0; }
    .s0 { background: #F25F5C; width: 20%; }
    .s1 { background: #F27A5E; width: 40%; }
    .s2 { background: #F2B05E; width: 60%; }
    .s3 { background: #7DCE82; width: 80%; }
    .s4 { background: #50C878; width: 100%; }
</style>
""", unsafe_allow_html=True)

# Title and input
st.title("Password Strength Meter")
password = st.text_input("Enter your password", type="password")

if password:
    # Analyze password
    result = zxcvbn.zxcvbn(password)
    score = result['score']  # 0-4
    
    # Display results
    labels = ["Very Weak", "Weak", "Fair", "Strong", "Very Strong"]
    st.markdown(f"### Strength: **{labels[score]}**")
    st.markdown(f'<div class="meter s{score}"></div>', unsafe_allow_html=True)
    st.markdown(f"**Time to crack**: {result['crack_times_display']['offline_slow_hashing_1e4_per_second']}")
    
    # Show warnings and suggestions
    if result['feedback']['warning']:
        st.warning(result['feedback']['warning'])
    
    for suggestion in result['feedback']['suggestions']:
        st.info(suggestion)
    
    # Password composition in two columns
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Length", len(password))
        st.metric("Uppercase", sum(1 for c in password if c.isupper()))
    with col2:
        st.metric("Lowercase", sum(1 for c in password if c.islower()))
        st.metric("Numbers/Symbols", sum(1 for c in password if not c.isalpha()))

st.markdown("---")
st.caption("Built with Streamlit and zxcvbn")

