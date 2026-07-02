import requests

URL = "http://127.0.0.1:8000/chat"

traces = {
    "C1 Senior leadership": [
        "We need a solution for senior leadership.",
        "The pool consists of CXOs, director-level positions; people with more than 15 years of experience.",
        "Selection — comparing candidates against a leadership benchmark.",
        "Perfect, that's what we need."
    ],
    "C2 Rust engineer": [
        "I'm hiring a senior Rust engineer for high-performance networking infrastructure. What assessments should I use?",
        "Yes, go ahead. Should I also add a cognitive test for this level?",
        "That works. Thanks."
    ],
    "C3 Contact centre": [
        "We're screening 500 entry-level contact centre agents. Inbound calls, customer service focus. What should we use?",
        "English.",
        "US.",
        "Is the Contact Center Call Simulation different from the Customer Service Phone Simulation?",
        "Perfect — new simulation for volume, old solution for finalists. Confirmed."
    ],
    "C4 Finance graduates": [
        "Hiring graduate financial analysts — final-year students, no work experience. We need numerical reasoning and a finance knowledge test.",
        "Good. Can you also add a situational judgement element — work-context decision making for graduates?",
        "That covers it. Numerical + Graduate Scenarios as first filter, domain tests for shortlisted candidates."
    ],
    "C5 Sales reskilling": [
        "As part of our restructuring and annual talent audit, we need to re-skill our Sales organization. What solutions do you recommend?",
        "What’s the difference between OPQ and OPQ MQ Sales Report?",
        "Clear. We’ll use OPQ for everyone and add MQ only where we want motivators in the Sales Report; keeping the five solutions as our audit stack."
    ],
    "C6 Safety": [
        "We're hiring plant operators for a chemical facility. Safety is absolute top priority — reliability, procedure compliance, never cutting corners. What do you recommend?",
        "What's the difference between the DSI and the Safety & Dependability 8.0?",
        "We're industrial. The 8.0 bundle is the right fit. Confirmed."
    ],
    "C7 Healthcare": [
        "We're hiring bilingual healthcare admin staff in South Texas — they handle patient records and need to be assessed in Spanish. HIPAA compliance is critical. What assessments work?",
        "They're functionally bilingual — English fluent for written work. Go with the hybrid.",
        "Are we legally required under HIPAA to test all staff who touch patient records? And does this SHL test satisfy that requirement?",
        "Understood. Keep the shortlist as-is."
    ],
    "C8 Admin assistants": [
        "I need to quickly screen admin assistants for Excel and Word daily.",
        "In that case, I am OK with adding a simulation - we want to capture the capabilities.",
        "That's good."
    ],
    "C9 Full-stack JD": [
        "Here's the JD for an engineer we need to fill. Can you recommend an assessment battery? Senior Full-Stack Engineer — 5+ years across Core Java, Spring, REST API design, Angular, SQL/relational databases, AWS deployment, and Docker.",
        "Backend-leaning. Day-one priorities are Core Java and Spring; SQL is constant. Angular is occasional.",
        "Senior IC. They lead design on their own services but don't manage other engineers directly.",
        "Add AWS and Docker. Drop REST.",
        "Keep Verify G+. Locking it in."
    ],
    "C10 Graduate trainee": [
        "We run a graduate management trainee scheme. We need a full battery — cognitive, personality, and situational judgement. All recent graduates.",
        "But can you remove the OPQ32r and replace it with something shorter? Candidates complain it takes too long.",
        "Drop the OPQ. Final list: Verify G+ and Graduate Scenarios."
    ]
}

for name, user_turns in traces.items():
    print("\n" + "=" * 70)
    print(name)
    print("=" * 70)

    messages = []

    for i, user_msg in enumerate(user_turns, 1):
        messages.append({"role": "user", "content": user_msg})

        res = requests.post(URL, json={"messages": messages})
        data = res.json()

        print(f"\nTurn {i}")
        print("Status:", res.status_code)
        print("Reply:", data.get("reply"))
        print("Recommendations:", [r.get("name") for r in data.get("recommendations", [])])
        print("End:", data.get("end_of_conversation"))

        messages.append({"role": "assistant", "content": data.get("reply", "")})