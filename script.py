import streamlit as st

# --- PAGE SETUP ---
st.set_page_config(page_title="Mochi Health | Birth Control Finder", page_icon="🩹", layout="centered")

# --- STATE MANAGEMENT ---
if "started" not in st.session_state:
    st.session_state.started = False
if "consultation" not in st.session_state:
    st.session_state.consultation = False
if "show_recommendations" not in st.session_state:
    st.session_state.show_recommendations = False

# --- LANDING PAGE ---
if not st.session_state.started:
    st.image(
        "https://framerusercontent.com/images/vt0oTlMyqYk9mI52IAtKqT28EYA.png?width=198&height=88", 
        width=160, 
    )
    st.title("Mochi Health Birth Control Finder")
    st.write("Welcome to Mochi! This quick quiz will help you find which of our **birth control methods** best fit your lifestyle, preferences, and medical needs.")
    st.write("---")

    st.markdown(
        """
        **💊 How it works:**
        1. Answer 4 short questions
        2. View personalized birth control recommendations that may be right for you  
        3. Discuss your options with a Mochi provider
        """
    )
    if st.button("Start Quiz"):
        st.session_state.started = True
        st.rerun()

# --- QUIZ PAGE ---
elif st.session_state.started:
    # --- QUIZ PAGE ---
    st.image(
        "https://framerusercontent.com/images/vt0oTlMyqYk9mI52IAtKqT28EYA.png?width=198&height=88", 
        width=160, 
    )
    st.title("Mochi Health Birth Control Finder")
    st.write("Answer a few quick questions to discover which of our birth control options may fit your lifestyle and health best.")
    st.write("---")

    # --- QUESTIONS ---
    st.header("Step 1: Your Priorities")
    priorities = st.multiselect(
        "What are you looking for when it comes to choosing birth control?",
        [
            "Low maintenance",
            "Hormone-free",
            "Regulating periods",
            "Improving acne or mood",
            "Short-term flexibility",
            "Cost"
        ]
    )

    st.header("Step 2: Lifestyle")
    lifestyle = st.radio(
        "How consistent are you with daily routines (like taking pills)?",
        [
            "Very consistent — I can take something daily",
            "Somewhat consistent — weekly or monthly is okay",
            "Not consistent — I’d prefer long-term, low-effort options"
        ]
    )

    st.header("Step 3: Medical Considerations")
    
    # Check for estrogen contraindications
    st.write("Please answer the following questions to help us determine safe and effective options for you:")
    
    smoker_over_35 = st.checkbox("I am over 35 years old and smoke cigarettes")
    migraine_aura = st.checkbox("I have migraines with aura (visual disturbances, blind spots, or flashing lights)")
    vte_risk = st.checkbox("I have a personal or family history of blood clots (VTE/DVT/PE)")
    bmi_over_30 = st.checkbox("My BMI is over 30")
    
    # Determine if estrogen is contraindicated
    estrogen_contraindicated = smoker_over_35 or migraine_aura or vte_risk

    st.header("Step 4: Future Plans")
    plans = st.radio(
        "Are you planning to get pregnant in the next 1–2 years?",
        ["Yes", "No", "Maybe / Not sure"]
    )

    st.write("---")

    # --- VISUAL CARD FUNCTION ---
    def display_card(icon, title, description):
        st.markdown(
            f"""
            <div style='padding:1em;border-radius:12px;border:1px solid #ddd;margin-bottom:0.8em;box-shadow:2px 2px 8px rgba(0,0,0,0.05);background-color:#f9fafb;'>
                <h4 style='margin-bottom:0.3em;'>{icon} {title}</h4>
                <p style='margin-top:0em;font-size:15px;color:#444;'>{description}</p>
            </div>
            """,
            unsafe_allow_html=True
        )

    # --- RESULTS ---
    # Validation for required questions
    validation_errors = []
    
    if not priorities:
        validation_errors.append("Please select at least one priority in Step 1!")
    
    if validation_errors:
        for error in validation_errors:
            st.write(f"• {error}")
        st.stop()
  
    if st.button("Show My Recommendations"):
        st.session_state.show_recommendations = True
        st.rerun()
        
    if st.session_state.show_recommendations:
        st.subheader("Your Personalized Recommendations")

        recs = []

        # Check if user wants to avoid daily pills
        avoid_daily_pills = ("Low maintenance" in priorities or 
                           lifestyle == "Somewhat consistent — weekly or monthly is okay" or 
                           lifestyle == "Not consistent — I'd prefer long-term, low-effort options")

        # Hormone-free options
        if "Hormone-free" in priorities:
            recs.append(("🧡 Paragard (Copper IUD)", "Non-hormonal IUD that lasts 10-12 years. Copper prevents fertilization."))

        # Convenience / low-maintenance
        if "Low maintenance" in priorities or lifestyle == "Not consistent — I'd prefer long-term, low-effort options":
            if "Hormone-free" not in priorities and not estrogen_contraindicated:
                recs.append(("💉 DMPA (Depo-Provera Injection)", "Progestin-only injection given every 3 months."))
            recs.append(("🧡 Paragard (Copper IUD)", "Non-hormonal IUD that lasts 10-12 years. Copper prevents fertilization."))

        # Daily consistency users
        if lifestyle == "Very consistent — I can take something daily" and not avoid_daily_pills:
            if "Improving acne or mood" in priorities and not estrogen_contraindicated and "Hormone-free" not in priorities:
                recs.append(("💊 Yaz (Combined Pill)", "Daily pill containing estrogen and drospirenone. May help with acne and mood."))
            elif "Regulating periods" in priorities and not estrogen_contraindicated and "Hormone-free" not in priorities:
                recs.append(("💊 Aviane (Combined Pill)", "Daily pill containing estrogen and progestin. Helps regulate periods."))
            elif "Hormone-free" not in priorities:
                recs.append(("💊 Micronor (Progestin-Only Pill)", "Daily pill with only progestin."))

        # Weekly/monthly routine users
        if lifestyle == "Somewhat consistent — weekly or monthly is okay":
            if not estrogen_contraindicated and "Hormone-free" not in priorities:
                recs.append(("💍 NuvaRing", "Flexible ring inserted monthly. Contains estrogen and progestin."))
                if not bmi_over_30:
                    recs.append(("🩹 Xulane Patch", "Weekly patch containing estrogen and progestin. Not recommended for BMI > 30."))
            elif "Hormone-free" not in priorities:
                recs.append(("💉 DMPA (Depo-Provera Injection)", "Progestin-only injection given every 3 months."))

        # Short-term users or pregnancy planning soon
        if plans == "Yes" or "Short-term flexibility" in priorities:
            if not avoid_daily_pills and "Hormone-free" not in priorities:
                recs.append(("💊 Micronor (Progestin-Only Pill)", "Daily pill with only progestin."))
            if not estrogen_contraindicated and "Hormone-free" not in priorities:
                recs.append(("💍 NuvaRing", "Flexible ring inserted monthly. Contains estrogen and progestin."))

        # Acne/mood improvement
        if "Improving acne or mood" in priorities and not any("Yaz" in r[0] for r in recs):
            if not estrogen_contraindicated and "Hormone-free" not in priorities and not avoid_daily_pills:
                recs.append(("💊 Yaz (Combined Pill)", "Daily pill containing estrogen and drospirenone. May help with acne and mood."))
            elif not avoid_daily_pills and "Hormone-free" not in priorities:
                recs.append(("💊 Micronor (Progestin-Only Pill)", "Daily pill with only progestin."))

        # Cost-conscious
        if "Cost" in priorities:
            if not estrogen_contraindicated and "Hormone-free" not in priorities and not avoid_daily_pills:
                recs.append(("💊 Aviane (Combined Pill)", "Daily pill containing estrogen and progestin. Helps regulate periods."))
            elif not avoid_daily_pills:
                recs.append(("💊 Micronor (Progestin-Only Pill)", "Daily pill with only progestin."))

        # Add safety note if estrogen is contraindicated
        if estrogen_contraindicated:
            st.warning("Important: Based on your health profile, estrogen-containing birth control may not be safe for you. The recommendations below focus on estrogen-free options.")

        if not recs:
            recs.append(("🤔 Consultation Recommended", "We recommend scheduling a consultation with a Mochi provider to find your best match."))

        # Remove duplicates while preserving order
        seen = set()
        unique_recs = []
        for rec in recs:
            if rec[0] not in seen:
                unique_recs.append(rec)
                seen.add(rec[0])

        for icon, desc in unique_recs:
            display_card("", icon, desc)

        st.write("---")
        
        # Add reference list of all available options
        st.subheader("All Available Birth Control Options")
        st.write("For reference, here are all the birth control methods we offer:")
        
        all_options = [
            ("🧡 Paragard (Copper IUD)", "Non-hormonal IUD that lasts 10-12 years. Copper prevents fertilization."),
            ("💉 DMPA (Depo-Provera Injection)", "Progestin-only injection given every 3 months."),
            ("💊 Yaz (Combined Pill)", "Daily pill containing estrogen and drospirenone. May help with acne and mood."),
            ("💊 Aviane (Combined Pill)", "Daily pill containing estrogen and progestin. Helps regulate periods."),
            ("💊 Micronor (Progestin-Only Pill)", "Daily pill with only progestin."),
            ("💍 NuvaRing", "Flexible ring inserted monthly. Contains estrogen and progestin."),
            ("🩹 Xulane Patch", "Weekly patch containing estrogen and progestin. Not recommended for BMI > 30.")
        ]
        
        for icon, desc in all_options:
            display_card("", icon, desc)

        st.write("---")
        st.info("This quiz is for informational purposes only and does not replace consultation with a licensed healthcare provider.")
        
        # Buttons aligned to the left
        if st.button("📅 Schedule a Consultation", key="schedule_consultation"):
            st.session_state.consultation = True
            st.rerun()
        # Show consultation form inline if consultation button was clicked
        if st.session_state.consultation:
            st.write("---")
            st.header("Ready to Get Started?")            
            st.write("Schedule a consultation with a licensed Mochi provider to discuss your birth control options.")
            
            # Contact form
            with st.form("consultation_form"):
                st.subheader("Contact Information")
                
                name = st.text_input("Full Name *", placeholder="Enter your full name")
                phone = st.text_input("Phone Number *", placeholder="Enter your phone number")
                email = st.text_input("Email Address *", placeholder="Enter your email address")
                notes = st.text_input("Additional Notes", placeholder="Enter any additional notes or questions")

                submitted = st.form_submit_button("Submit Request")
                
                if submitted:
                    if name and phone and email:
                        st.success("Thank you! Your consultation request has been submitted. A Mochi provider will contact you in 1-2 business days.")
                    else:
                        st.error("Please fill in all required fields.")
        
        # Navigation button
        if st.button("🏠 Return to Home", key="return_home"):
            st.session_state.started = False
            st.session_state.consultation = False
            st.session_state.show_recommendations = False
            st.rerun()

