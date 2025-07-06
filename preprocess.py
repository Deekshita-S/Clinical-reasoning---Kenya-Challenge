import numpy as np
import pandas as pd
import re






# Preprocess text
def preprocess_text(text):
    
    replacements = {
        'âœ“': '✔',
        'â€™': "'",
        'â€“': '-',
        'â€”': '-',
        'â€': '"',
        'â€œ': '"',
        'â€¢': '•',
        'â€¦': '...',
        'â‚‚': '2',
        'â†‘': 'increased',
        'â†“': 'decreased',
        'Â°C': '°C',
        'Â': '',
        '_x0001_': ' ',
        '_x0001_â€¢_x0001_': '• ',
        'â  â': ') ',
        '@':' at ',
        '↑': 'increased',
        '↓': 'decreased',
        '₂': '2',
        
    }

    regex_replacements = {
    # Standardize SpO2 variations
    r'\bSpO₂\b': 'SpO2',
    r'\bSPO₂\b': 'SpO2',
    r'\bSPO2\b': 'SpO2',
    
    # Blood Pressure (standardize to "BP")
    r'\b([Bb][Pp]|[Bb]lood\s[Pp]ressure)\b': 'BP',
    r'\bBP\b': 'Blood Pressure',  # Optional: Expand if needed
    
    # Heart Rate/Pulse (standardize to "bpm")
    r'\b(beats?/min(?:ute)?|beats?\sper\smin(?:ute)?)\b': 'bpm',
    r'\b[Bb][Pp][Mm]\b': 'bpm',
    
    # Respiratory Rate (standardize to "RR")
    r'\b[Rr][Rr]?\b': 'RR',
    r'\bresp(?:iration|iratory)?\srate\b': 'RR',
    
    # Standard format for vitals:
    # BP 120/80 mmHg | Pulse 72 bpm | RR 16 | SpO2 98%
    r'\b([Bb][Pp]|[Bb]lood\s[Pp]ressure)[\s:-]*([0-9]{2,3})/([0-9]{2,3})\s*(mmHg)?\b': r'BP \2/\3 mmHg',
    r'\b([Pp](?:ulse)?|[Hh][Rr])\s*[:-]*\s*([0-9]{2,3})\s*bpm\b': r'Pulse \2 bpm',
    r'\b[Rr][Rr]?\s*[:-]*\s*([0-9]{2,3})\s*(?:breaths?/?min)?\b': r'RR \1',
    r'\b[Ss][Pp][Oo2]2?\s*[:-]*\s*([0-9]{2,3})%?\b': r'SpO2 \1%',
        # Handles: "Temp 36.8°C", "Temperature: 37.2C", "T 38.0°C"
    r'\b[Tt](?:emp(?:erature)?)?[\s:-]*([0-9]{2,3}\.[0-9])\s*°?[Cc]\b': r'Temperature \1°C',
    
    # Handles: "Temp 37°C", "T 38C" (whole numbers)
    r'\b[Tt](?:emp(?:erature)?)?[\s:-]*([0-9]{2,3})\s*°?[Cc]\b': r'Temperature \1.0°C',
    r'\b(?:temp(?:erature)?)[\s:-]*([3-4][0-9](?:\.\d{1,2})?)\s*°?[Cc]\b':r'Temperature \1°C',

    
    # Handles: "Temp: 98.6F", "T 99F" (Fahrenheit)
    r'\b[Tt](?:emp(?:erature)?)?[\s:-]*([0-9]{2,3}\.[0-9])\s*°?[Ff]\b': r'Temperature \1°F',
    r'\b[Tt](?:emp(?:erature)?)?[\s:-]*([0-9]{2,3})\s*°?[Ff]\b': r'Temperature \1.0°F',
    r'\b[Tt](?:emp(?:erature)?)?[\s:-]*([0-9]{2,3})\s+([0-9])\s*[Cc]\b': r'Temperature \1.\2°C',
}


        
    if 'Questions'  in text or 'Question'  in text  or 'questions'  in text or 'question'  in text or 'QUESTIONS'  in text or 'QUESTION'  in text:
    
            filtered = [r for r in text if not any(w in r.lower() for w in ["question", "questions"])]
            text=''.join(filtered)
            split = re.split(r'\bquestions?\b\s*[:\-]?\s*', text, flags=re.IGNORECASE)
            case_text,questions_text =split[0],split[1]
            text = f"{case_text}\nQuestions:\n{questions_text}"
        
                
    else:
            # Split text into sentences
            sentences = re.split(r'(?<=[.!?])\s+', text)
            
            questions = []
            remaining_text = []
            found_first_question = False
            
            for sentence in sentences:
                if not found_first_question and sentence.endswith('?'):
                    # This is our first question sentence
                    questions.append(sentence.strip())
                    found_first_question = True
                elif found_first_question:
                    # All sentences after first question
                    questions.append(sentence.strip())
                else:
                    # Sentences before any questions
                    remaining_text.append(sentence.strip())
            
            if not questions:
                pass  # No questions found
            else:
                # Reconstruct the text
                main_text = ' '.join(remaining_text)
                questions_text = "\n".join(questions)
                text = f"{main_text}\nQuestions:\n{questions_text}"
        
    # First handle plain string replacements
    for k, v in replacements.items():
        text = text.replace(k, v)

    # Then handle regex replacements
    for pattern, repl in regex_replacements.items():
        text = re.sub(pattern, repl, text, flags=re.IGNORECASE)
    
    
    return text.strip()
  

# Create enhanced prompts
def create_prompt(user_input,structured_data):
    """Create enhanced prompt with medical context"""
    prompt = user_input.strip()
    prompt = re.sub(r'^[^.!?]*[.!?]\s*', '', prompt) # remove the first sentence that corresponds to nurses details
    

    age_gender=[]
    if structured_data['age']!='unknown':
        age_gender.append(f"Age: {structured_data['age']}")
    if structured_data['gender']!='unknown':
        age_gender.append(f"Gender: {structured_data['gender']}")

        prompt = f"Patient details - { ' | '.join(age_gender) }\n{prompt}"

    # Add context if available
    context_parts = []
    if structured_data['county']!='unknown':
        context_parts.append(f"County: {structured_data['county']}")
    if structured_data['health_level']!='unknown':
        context_parts.append(f"Type of healthcare facility: {structured_data['health_level']}")
    if structured_data['nursing_competency']!='unknown':
        context_parts.append(f"Nursing competency: {structured_data['nursing_competency']}")
    if structured_data['clinical_panel']!='unknown':
        context_parts.append(f"Clinical Panel: {structured_data['clinical_panel']}")
    if structured_data['years_experience']!='unknown':
        context_parts.append(f"Years of experience of Nurse: {structured_data['years_experience']}")
    
    if context_parts:
        prompt = f"Medical Context - {' , '.join(context_parts)}\n{prompt}"


    return f'''You are an experienced Clinician.Start with the summary of the case and based on the case below answer each clinical query with evidence-based rationale.\nCase:\n{prompt}'''




def preprocess_input(user_input, structured_data):
    prompt = create_prompt(user_input,structured_data)

    return preprocess_text(prompt)


