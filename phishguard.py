import streamlit as st
import pandas as pd
import datetime
import random
import io
import base64
from PIL import Image, ImageDraw, ImageFont
import plotly.express as px
import plotly.graph_objects as go
import time

# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="PhishGuard - Phishing Awareness Training",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================
if 'progress' not in st.session_state:
    st.session_state.progress = 0.0
if 'quiz_score' not in st.session_state:
    st.session_state.quiz_score = 0
if 'quiz_total' not in st.session_state:
    st.session_state.quiz_total = 0
if 'modules_completed' not in st.session_state:
    st.session_state.modules_completed = set()
if 'certificate_issued' not in st.session_state:
    st.session_state.certificate_issued = False
if 'user_name' not in st.session_state:
    st.session_state.user_name = ""
if 'quiz_answers' not in st.session_state:
    st.session_state.quiz_answers = []
if 'quiz_finished' not in st.session_state:
    st.session_state.quiz_finished = False
if 'simulation_answers' not in st.session_state:
    st.session_state.simulation_answers = {}
if 'simulation_finished' not in st.session_state:
    st.session_state.simulation_finished = False
if 'badges' not in st.session_state:
    st.session_state.badges = []
if 'module_history' not in st.session_state:
    st.session_state.module_history = []  # timestamps for completion

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.image("https://img.icons8.com/fluency/96/000000/shield.png", width=70)
    st.title("🔐 PhishGuard")
    st.markdown("### Pro Edition")
    st.markdown("---")
    st.metric("📘 Modules", f"{len(st.session_state.modules_completed)}/6")
    st.metric("🎯 Quiz Score", f"{st.session_state.quiz_score}/{st.session_state.quiz_total}" if st.session_state.quiz_total else "0/0")
    st.metric("📜 Certificate", "✅ Issued" if st.session_state.certificate_issued else "🔒 Locked")
    st.markdown("---")
    st.caption(f"v3.0 Pro • {datetime.datetime.now().strftime('%Y-%m-%d')}")
    st.caption("🔒 Cybersecurity Awareness Training")

# ============================================================
# MAIN TABS – No Resources Tab
# ============================================================
tabs = st.tabs(["🏠 Home", "📚 Training", "🧠 Quiz", "📊 Progress", "📜 Certificate", "🎯 Simulation"])

# ----- HOME -----
with tabs[0]:
    # Animated header with a progress spinner placeholder
    st.markdown("# 🔐 PhishGuard")
    st.markdown("*Advanced Phishing Awareness Training Platform – Pro Edition*")
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("📘 Modules", f"{len(st.session_state.modules_completed)}/6")
    with col2:
        st.metric("✅ Progress", f"{st.session_state.progress:.0f}%")
    with col3:
        st.metric("🎯 Quiz Score", f"{st.session_state.quiz_score}/{st.session_state.quiz_total}" if st.session_state.quiz_total else "0/0")
    with col4:
        cert_status = "✅ Issued" if st.session_state.certificate_issued else "🔒 Locked"
        st.metric("📜 Certificate", cert_status)

    st.markdown("---")
    st.info("""
    **Welcome to PhishGuard Pro!**  
    Phishing attacks are the #1 cyber threat. This platform provides comprehensive training to help you:

    - Recognize all types of phishing (Email, Smishing, Vishing, Social Media, etc.)  
    - Identify red flags in real‑world examples  
    - Test your knowledge with an advanced quiz  
    - Practice with a realistic email simulator  
    - Earn a verified certificate upon completion  

    **Complete all 6 modules and score ≥ 80% on the quiz to get certified.**
    """)

    # Random cybersecurity fact with a spinner animation (simulated)
    facts = [
        "🔹 90% of data breaches start with a phishing email.",
        "🔹 The first phishing attack was carried out in 1995 against AOL users.",
        "🔹 Spear phishing attacks are 10x more effective than generic phishing.",
        "🔹 30% of phishing emails are opened by the recipient.",
        "🔹 Multi‑factor authentication blocks 99.9% of account compromise attacks."
    ]
    fact_placeholder = st.empty()
    with st.spinner("Loading a cybersecurity fact..."):
        time.sleep(0.5)  # just for effect
        fact_placeholder.info(random.choice(facts))

    # A quick tip with a progress bar animation (just for show)
    st.markdown("### 💡 Quick Tip")
    tip_bar = st.progress(0)
    for i in range(100):
        # Simulate loading
        time.sleep(0.001)
        tip_bar.progress(i + 1)
    st.success("Always hover over links to check the true destination before clicking!")

# ----- TRAINING (6 Modules) -----
with tabs[1]:
    st.markdown("# 📚 Training Modules")
    st.markdown("Complete all 6 modules to unlock the certificate.")

    modules = {
        "Introduction to Phishing": {
            "content": """
            **Phishing** is a cyber attack where attackers impersonate legitimate entities to steal sensitive data.
            - **Goal**: Trick victims into clicking malicious links, downloading attachments, or revealing credentials.
            - **Impact**: Financial loss, identity theft, data breaches.
            - **Statistics**: Over 80% of organisations have experienced a phishing attack.
            """,
            "red_flags": [
                "Urgent or threatening language",
                "Suspicious sender email address",
                "Generic greetings (e.g., 'Dear Customer')",
                "Unexpected attachments or links"
            ]
        },
        "Email Phishing": {
            "content": """
            The most common form – fraudulent emails appearing to come from reputable sources.
            **Example**: An email from 'bank-security@secure.com' asking you to verify your account by clicking a link.
            **How to spot**:
            - Check the sender's domain (e.g., 'secure.com' vs 'bank.com')
            - Look for spelling and grammar errors
            - Be wary of requests for personal information
            """,
            "red_flags": [
                "Spoofed email address",
                "Suspicious links (hover to check URL)",
                "Attachments with macros",
                "Mismatched domains"
            ]
        },
        "Smishing & Vishing": {
            "content": """
            **Smishing** – Phishing via SMS text messages.
            **Vishing** – Phishing via voice calls (phone).
            **Example Smishing**: Text from 'your bank' with a link to 'verify' your account.
            **Example Vishing**: Caller pretending to be tech support asking for remote access.
            **Protection**: Never share OTPs or passwords over the phone or via SMS.
            """,
            "red_flags": [
                "Unsolicited texts/calls",
                "Pressure to act immediately",
                "Requests for passwords or OTPs",
                "Suspicious phone numbers"
            ]
        },
        "Social Media Phishing": {
            "content": """
            Attackers use social media platforms (Facebook, LinkedIn, Twitter) to gather personal information and send malicious links.
            - **Fake profiles**: Impersonating friends or colleagues.
            - **Fake giveaways** or surveys.
            - **Malicious ads** that lead to credential harvesting pages.
            **Best practice**: Verify requests through a secondary channel.
            """,
            "red_flags": [
                "Unsolicited messages from unknown profiles",
                "Too‑good‑to‑be‑true offers",
                "Links to unfamiliar websites",
                "Requests for login credentials"
            ]
        },
        "Advanced Threats (Spear Phishing, Whaling)": {
            "content": """
            **Spear Phishing** – Targeted at specific individuals or companies.
            **Whaling** – Spear phishing aimed at high‑profile targets (CEOs, CFOs, etc.).
            These use personal information to appear convincing.
            **Defense**: Implement strict verification procedures for wire transfers and sensitive data requests.
            """,
            "red_flags": [
                "Highly personalised content",
                "Requests for wire transfers or sensitive data",
                "Sender appears to be from within your organisation",
                "Unusual timing or urgency"
            ]
        },
        "Protection Best Practices": {
            "content": """
            **Key strategies to protect against phishing:**
            - **Think before you click**: Hover over links to see the URL.
            - **Enable Multi‑Factor Authentication (MFA)** – adds an extra layer.
            - **Keep software updated** – includes security patches.
            - **Use email filtering** and anti‑spam tools.
            - **Report suspicious emails** to your IT team or the relevant authority.
            - **Regular training** and awareness – like this course!
            """,
            "red_flags": [
                "Lack of MFA",
                "Outdated software",
                "Ignoring security warnings",
                "Using the same password for multiple accounts"
            ]
        }
    }

    for title, data in modules.items():
        with st.expander(f"📘 {title}"):
            st.markdown(data["content"])
            st.markdown("**🚩 Red Flags to Watch:**")
            for flag in data["red_flags"]:
                st.markdown(f"- {flag}")
            if title not in st.session_state.modules_completed:
                if st.button(f"✅ Mark as Completed", key=f"complete_{title}"):
                    st.session_state.modules_completed.add(title)
                    st.session_state.module_history.append({"module": title, "timestamp": datetime.datetime.now().isoformat()})
                    total_modules = len(modules)
                    completed = len(st.session_state.modules_completed)
                    st.session_state.progress = (completed / total_modules) * 100
                    st.success(f"Module '{title}' completed!")
                    st.balloons()  # fun animation
                    st.rerun()
            else:
                st.success("✅ Completed")
    st.progress(st.session_state.progress / 100)
    st.caption(f"Progress: {st.session_state.progress:.0f}%")

# ----- QUIZ (8 Questions) -----
with tabs[2]:
    st.markdown("# 🧠 Phishing Awareness Quiz")
    st.markdown("Answer 8 questions. You need at least 7 correct to pass.")

    # Expanded question bank
    question_bank = [
        {
            "question": "Which of the following is a sign of a phishing email?",
            "options": ["Professional design", "Urgent action required", "Personalised greeting", "No attachments"],
            "answer": 1
        },
        {
            "question": "What is 'Smishing'?",
            "options": ["Email phishing", "Phishing via SMS", "Phishing via phone calls", "Phishing via social media"],
            "answer": 1
        },
        {
            "question": "What should you do if you receive a suspicious email from your bank?",
            "options": ["Click the link to check", "Reply for more info", "Contact the bank directly using official channels", "Ignore it"],
            "answer": 2
        },
        {
            "question": "Which of the following is a 'red flag' in a phishing attempt?",
            "options": ["Familiar sender name", "Correct grammar", "Unexpected attachment", "Official logo"],
            "answer": 2
        },
        {
            "question": "What is 'whaling'?",
            "options": ["Phishing targeting children", "Phishing targeting executives", "Phishing via social media", "Phishing via QR codes"],
            "answer": 1
        },
        {
            "question": "What is the best defence against phishing?",
            "options": ["Strong passwords only", "Multi‑factor authentication (MFA)", "Antivirus software", "Using the same password everywhere"],
            "answer": 1
        },
        {
            "question": "What should you do if you suspect a phishing attempt?",
            "options": ["Reply and ask for more info", "Forward it to your IT team or report it", "Delete it without reporting", "Click the link to see what happens"],
            "answer": 1
        },
        {
            "question": "Which type of phishing involves a fake SMS message?",
            "options": ["Vishing", "Smishing", "Spear Phishing", "Whaling"],
            "answer": 1
        }
    ]

    # Shuffle questions each session
    if 'shuffled_questions' not in st.session_state:
        st.session_state.shuffled_questions = random.sample(question_bank, len(question_bank))
        st.session_state.quiz_answers = [None] * len(st.session_state.shuffled_questions)
        st.session_state.quiz_finished = False
        st.session_state.quiz_score = 0
        st.session_state.quiz_total = 0

    total_q = len(st.session_state.shuffled_questions)
    if not st.session_state.quiz_finished:
        # Show each question with radio
        for i, q in enumerate(st.session_state.shuffled_questions):
            st.markdown(f"**Question {i+1} of {total_q}**")
            st.markdown(q["question"])
            selected = st.radio(
                "Choose your answer:",
                q["options"],
                key=f"q_{i}",
                index=None
            )
            if selected is not None:
                st.session_state.quiz_answers[i] = selected
            st.markdown("---")

        if st.button("Submit Quiz"):
            # Score
            correct = 0
            for i, q in enumerate(st.session_state.shuffled_questions):
                if st.session_state.quiz_answers[i] == q["options"][q["answer"]]:
                    correct += 1
            st.session_state.quiz_score = correct
            st.session_state.quiz_total = total_q
            st.session_state.quiz_finished = True
            st.rerun()
    else:
        st.success(f"🎉 Quiz completed! Your score: {st.session_state.quiz_score}/{total_q}")
        if st.session_state.quiz_score >= 7:
            st.balloons()
            st.success("🏆 Congratulations! You passed the quiz! You are eligible for the certificate.")
        else:
            st.warning("You need at least 7/10 to pass. Review the training and try again.")
        if st.button("🔄 Restart Quiz"):
            st.session_state.shuffled_questions = random.sample(question_bank, len(question_bank))
            st.session_state.quiz_answers = [None] * len(st.session_state.shuffled_questions)
            st.session_state.quiz_finished = False
            st.session_state.quiz_score = 0
            st.session_state.quiz_total = 0
            st.rerun()

# ----- PROGRESS (with charts) -----
with tabs[3]:
    st.markdown("# 📊 Your Progress")
    st.markdown("Track your learning journey and achievements.")

    col1, col2 = st.columns(2)
    with col1:
        st.metric("📘 Modules Completed", f"{len(st.session_state.modules_completed)}/6")
    with col2:
        st.metric("🧠 Quiz Score", f"{st.session_state.quiz_score}/{st.session_state.quiz_total}" if st.session_state.quiz_total else "0/0")

    st.progress(st.session_state.progress / 100)
    st.caption(f"Overall Progress: {st.session_state.progress:.0f}%")

    # Chart: Module completion over time (if history available)
    if st.session_state.module_history:
        df = pd.DataFrame(st.session_state.module_history)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df['count'] = 1
        df = df.sort_values('timestamp')
        df['cumulative'] = df['count'].cumsum()
        fig = px.line(df, x='timestamp', y='cumulative', title='Modules Completed Over Time',
                      labels={'timestamp': 'Date', 'cumulative': 'Modules Completed'})
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)',
                          font_color='#cccccc', xaxis=dict(gridcolor='#333333'),
                          yaxis=dict(gridcolor='#333333'))
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Start completing modules to see your progress chart.")

    # Badges
    st.markdown("### 🏅 Achievements")
    badges = []
    if len(st.session_state.modules_completed) >= 6:
        badges.append("📘 Master of Phishing")
    if len(st.session_state.modules_completed) >= 3:
        badges.append("📘 Phishing Novice")
    if st.session_state.quiz_score >= 7 and st.session_state.quiz_total == 8:
        badges.append("🧠 Quiz Champion")
    if st.session_state.certificate_issued:
        badges.append("📜 Certified Expert")

    st.session_state.badges = list(set(badges))
    if not st.session_state.badges:
        st.info("Complete modules and pass the quiz to earn badges!")
    else:
        for b in st.session_state.badges:
            st.markdown(f"- {b}")

    # Eligibility
    if len(st.session_state.modules_completed) >= 6 and st.session_state.quiz_score >= 7:
        st.success("🎉 You are eligible for the certificate! Go to the Certificate tab.")
    else:
        st.info("Complete all 6 modules and score at least 7/8 on the quiz to unlock the certificate.")

# ----- CERTIFICATE -----
with tabs[4]:
    st.markdown("# 📜 Certificate of Completion")

    if len(st.session_state.modules_completed) < 6:
        st.warning("⚠️ You must complete all 6 training modules before generating a certificate.")
    elif st.session_state.quiz_score < 7:
        st.warning("⚠️ You need a quiz score of at least 7/8 to earn the certificate.")
    else:
        st.success("🏆 Congratulations! You are eligible for a certificate.")
        user_name = st.text_input("Enter your full name for the certificate:", value=st.session_state.user_name)
        if st.button("💾 Generate Certificate"):
            if user_name.strip() == "":
                st.error("Please enter your name.")
            else:
                st.session_state.user_name = user_name
                st.session_state.certificate_issued = True
                if "📜 Certified Expert" not in st.session_state.badges:
                    st.session_state.badges.append("📜 Certified Expert")
                with st.spinner("Generating your certificate..."):
                    time.sleep(1)  # simulate work
                try:
                    img = Image.new('RGB', (1200, 800), color=(0, 0, 0))
                    draw = ImageDraw.Draw(img)
                    draw.rectangle([20, 20, 1180, 780], outline=(0, 212, 255), width=8)
                    try:
                        font_title = ImageFont.truetype("arial.ttf", 70)
                        font_sub = ImageFont.truetype("arial.ttf", 40)
                        font_name = ImageFont.truetype("arial.ttf", 60)
                    except:
                        font_title = ImageFont.load_default()
                        font_sub = ImageFont.load_default()
                        font_name = ImageFont.load_default()
                    draw.text((600, 200), "PHISHGUARD", fill=(0, 212, 255), anchor="mt", font=font_title)
                    draw.text((600, 280), "Certificate of Completion", fill=(255,255,255), anchor="mt", font=font_sub)
                    draw.text((600, 380), f"This certifies that", fill=(200,200,200), anchor="mt", font=font_sub)
                    draw.text((600, 450), user_name.upper(), fill=(0, 212, 255), anchor="mt", font=font_name)
                    draw.text((600, 540), "has successfully completed the Phishing Awareness Training (Pro)", fill=(200,200,200), anchor="mt", font=font_sub)
                    draw.text((600, 610), f"Issued on {datetime.datetime.now().strftime('%B %d, %Y')}", fill=(150,150,150), anchor="mt", font=font_sub)
                    buf = io.BytesIO()
                    img.save(buf, format="PNG")
                    byte_im = buf.getvalue()
                    st.image(byte_im, caption="Your Certificate", use_container_width=True)
                    b64 = base64.b64encode(byte_im).decode()
                    href = f'<a href="data:image/png;base64,{b64}" download="PhishGuard_Certificate_{user_name}.png">📥 Download Certificate</a>'
                    st.markdown(href, unsafe_allow_html=True)
                    st.balloons()
                except Exception as e:
                    st.error(f"Error generating certificate: {e}")

# ----- SIMULATION (Phishing Email Simulator) -----
with tabs[5]:
    st.markdown("# 🎯 Phishing Email Simulator")
    st.markdown("Analyze real‑world phishing emails and decide if they are legitimate or fraudulent.")

    # Simulated emails
    simulations = [
        {
            "id": 1,
            "subject": "URGENT: Verify your account now",
            "from": "security@banking-secure.com",
            "body": "Dear Customer,\n\nWe have detected suspicious activity on your account. Please verify your identity immediately by clicking the link below to avoid account suspension.\n\n[Verify Now]\n\nFailure to do so within 24 hours will result in account closure.\n\nRegards,\nSecurity Team",
            "is_phishing": True,
            "explanation": "Urgent language, generic greeting, suspicious sender domain, and a link to an unknown site are classic phishing signs."
        },
        {
            "id": 2,
            "subject": "Your invoice #10239 is ready",
            "from": "invoices@company.com",
            "body": "Dear John,\n\nPlease find attached the invoice for the recent services. The total amount is $450.00, due by March 15th.\n\nIf you have any questions, reply to this email.\n\nBest regards,\nAccounting Department",
            "is_phishing": False,
            "explanation": "This email uses the recipient's name, has a legitimate sender domain, and does not ask for sensitive information. It's safe."
        },
        {
            "id": 3,
            "subject": "You've won a free iPhone!",
            "from": "giveaway@prizes.net",
            "body": "Congratulations! You have been selected as the winner of our monthly giveaway. To claim your prize, please click the link below and enter your credit card details for shipping verification.\n\n[Claim Prize]\n\nHurry, this offer expires in 2 hours!",
            "is_phishing": True,
            "explanation": "Too‑good‑to‑be‑true offers, urgency, and requests for credit card details are clear phishing indicators."
        }
    ]

    # Initialize simulation answers for all IDs
    for sim in simulations:
        if sim['id'] not in st.session_state.simulation_answers:
            st.session_state.simulation_answers[sim['id']] = None

    for sim in simulations:
        st.markdown(f"### 📧 Email {sim['id']}")
        st.markdown(f"**Subject:** {sim['subject']}")
        st.markdown(f"**From:** {sim['from']}")
        st.code(sim['body'], language='text')
        current_ans = st.session_state.simulation_answers[sim['id']]
        idx = 0 if current_ans == "Yes" else (1 if current_ans == "No" else None)
        answer = st.radio(
            f"Is this email a phishing attempt? (Email {sim['id']})",
            ["Yes", "No"],
            key=f"sim_{sim['id']}",
            index=idx,
            horizontal=True
        )
        if answer:
            st.session_state.simulation_answers[sim['id']] = answer
        st.markdown("---")

    if st.button("Check My Answers"):
        correct = 0
        for sim in simulations:
            user_ans = st.session_state.simulation_answers.get(sim['id'])
            expected = "Yes" if sim['is_phishing'] else "No"
            if user_ans == expected:
                correct += 1
        st.success(f"You got {correct}/{len(simulations)} correct!")
        # Show explanations
        for sim in simulations:
            with st.expander(f"Explanation for Email {sim['id']}"):
                st.write(sim['explanation'])
        st.session_state.simulation_finished = True
        if correct == len(simulations):
            st.balloons()

    if st.session_state.simulation_finished:
        if st.button("Reset Simulation"):
            for sim in simulations:
                st.session_state.simulation_answers[sim['id']] = None
            st.session_state.simulation_finished = False
            st.rerun()