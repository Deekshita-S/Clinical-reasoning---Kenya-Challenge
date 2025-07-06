# 🇰🇪 Kenya Clinical Reasoning Challenge

## 🩺 Overview

In many parts of the world, frontline healthcare workers make life-or-death decisions with limited time, resources, and specialist support. This challenge simulates such high-stakes situations from Kenya’s healthcare system, tasking models with replicating the clinical reasoning of experienced nurses.

You are given **400 real-world clinical prompts**, each representing a nuanced medical vignette with contextual information such as:
- Type of healthcare facility
- Nurse’s experience and competency
- Patient demographics and condition

The goal is to predict how a trained clinician would respond to each case, demonstrating both medical knowledge and practical decision-making in low-resource environments.

> 🔬 Expert clinicians and top models (GPT-4, LLAMA, GEMINI) were used to validate and benchmark the dataset.

---

## 📁 Dataset

- **400** training samples  
- **100** test samples  
- Each entry includes:
  - Facility details
  - Nurse experience level
  - Patient characteristics
  - Case scenario + clinical queries

Medical domains covered: maternal health, pediatrics, emergency care, and critical care.

---

## 🧠 Solution Approach

### ✅ Model

We fine-tuned the [**MedAlpaca model**](https://huggingface.co/chavinlo/medalpaca-7b) using LoRA and integrated it into our pipeline.

**Fine-tuned model is available here**:  
👉 [Clinical Reasoning Model](https://huggingface.co/AIMLFreak/medalpaca_kenya-7b-4bit)

- Trained for **2 epochs** (additional epochs caused overfitting)
- Used a prompt-based instruction format (see example below)

---

### 📊 Evaluation

Originally, ROUGE was the official evaluation metric, but we used **BERTScore** for better semantic evaluation of outputs.

**Validation Metrics:**
```json { "eval_loss": 1.2426, "eval_bertscore_precision": 0.8871, "eval_bertscore_recall": 0.9182, "eval_bertscore_f1": 0.9023 } ```


## ⚠️ Limitations

GPT-based reviews suggested that some treatment recommendations were **clinically inaccurate**.  
While the model mimics reasoning patterns well, **further refinement and clinical oversight** are required before any real-world deployment.

---

## 🔍 Data Preprocessing

### Extracted Metadata

- County  
- Facility level  
- Nursing experience  
- Patient age/gender  
- Clinical panel  
- Case context and clinical queries  

---

### 🧾 Formatting

Prompts were standardized using an instruction format like this:

```text
You are an experienced Clinician. Start with a summary of the case and, based on the case below, answer each clinical query with evidence-based rationale.

Case:
Medical Context - Type of healthcare facility: National Referral Hospitals  
Nursing Competency: Emergency Care - Pediatric  
Clinical Panel: CRITICAL CARE  
Years of experience of Nurse: 17 yrs  

Patient details - Age: 2 years | Gender: Female  

...

Questions:
- What are the priorities of assessment?
- What types of injuries are likely?
- Are external burns the only possible injury?
- What consultations are necessary?
```
---

### Cleaning Special Characters
Replaced corrupted or misencoded characters with proper Unicode equivalents

---

## 🧪 Future Work
- Reduce hallucinations and improve factual accuracy

- Incorporate retrieval-augmented generation (RAG) with clinical documents

- Fine-tune on larger and more diverse datasets

- Explore structured prompt engineering and self-verification mechanisms
