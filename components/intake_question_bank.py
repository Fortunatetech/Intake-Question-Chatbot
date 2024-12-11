def intake_question_generator():
    # Predefined conversation flow
    intake_questions = [
        "Hi there! Let’s get started with your intake process. I’ll ask you some questions to ensure we can provide you with the best care possible. Let’s begin!",
        "What’s your first name?",
        "And your last name?",
        "How did you hear about us?",
        "What’s your date of birth? Please use the format MM/DD/YYYY.",
        "Is this appointment for a minor child? (Yes/No)",
        
        # If appointment is for a minor child
        "Please provide your name.",
        "What is your relationship to the child?",
        "Do you consent to your child receiving care from our provider, including potential prescriptions if necessary?",
        "Thank you. Please type your full name as your signature to confirm your understanding of our minor care policies.",
        
        # Personal and Contact Information
        "What is your sex assigned at birth?",
        "If you’d like, you can share your gender identity (optional).",
        "Please enter your street address.",
        "Is there an additional line for your address (like apartment number)?",
        "What city do you live in?",
        "What state?",
        "And your zip code?",
        "What’s your email address?",
        "Can you share your telephone number?",

        # Visit Expectations
        "What brings you to us at this time? Is there something specific, like an event or situation?",
        "Tell us more about the type of mental health care you are seeking.",
        "Have you seen a mental health professional before? (Yes/No)",
        "Have you been diagnosed or experienced the following conditions?",
        
        # Specialized questions
        "In the last six months, have you had frequent, intrusive thoughts, urges, or images that you don’t want to have? (For example, intrusive thoughts, which are ideas or images that come to mind uninvited and unwanted)",
        "Do you do repetitive behaviors such as handwashing or cleaning, avoiding certain people or things without clear reason, constantly asking people for reassurance, repeatedly doing things in your mind to feel better or to prevent something bad from happening, such as reviewing past events? (Yes/No)",
        "Over the last month, have these thoughts or behaviors significantly impacted your life or taken up more than an hour of your day? (Yes/No)",
        
        # If Yes to 2 or more of the above questions
        "You answered 'yes' to two or more of the last three questions. You may benefit from specialized treatment for OCD. Orenda has a referral partnership with NOCD, a practice specializing in OCD therapy. Would you like to learn more about this treatment? (Yes/No)",
        
        # Optional therapy offer
        "Our psychiatric providers stay up to date with the evolving landscape of the field, incorporating the latest research and innovative treatments. Some of our providers offer at-home ketamine-assisted therapy for patients who suffer from treatment-resistant mental health issues and meet the necessary criteria. Would you like to learn more about ketamine therapy? (Yes/No)",

        # Medical History
        "Can you list any medications or supplements you are currently taking, along with their purposes?",
        "If applicable, who is your prescribing doctor? Please include their type, name, and contact information.",
        "Do you have any medication allergies?",
        "Let’s talk lifestyle. Do you drink alcohol? If yes, how much and how often?",
        "Do you use recreational drugs? If yes, what kind, and how often?",
        "Do you have current thoughts of self-harm or harming others? (Yes/No)",
        
        # If Yes
        "Please provide more details. Remember, if this is an emergency, call 911 or visit your nearest emergency room immediately.",

        # Personal Life
        "What is your living situation like? Do you live alone, with family, or others?",
        "What’s your highest level of education, and what type of degree do you have?",
        "What is your current occupation, and how long have you been doing it?",
        "Do you have any hearing impairments that require accommodations for sessions? (Yes/No)",

        # Final Steps
        "Please click the link below to securely add your insurance and payment information: [Secure Link]",
        "Before we finish, we need your agreement to our Terms of Use and practice policies. Please review them at the link below and click 'I Agree' to proceed: [Link to Terms of Use and Policies]",
        "Thank you! Your intake is now complete. We look forward to supporting you!"
    ]
    return intake_questions