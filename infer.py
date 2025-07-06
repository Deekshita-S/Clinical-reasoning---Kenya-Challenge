from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import torch
import os
token = os.getenv("HF_TOKEN")



# Load the model with disk offloading
bnb_config = BitsAndBytesConfig(load_in_4bit=True)  # Required again when loading

model = AutoModelForCausalLM.from_pretrained(
    "AIMLFreak/medalpaca_kenya-7b-4bit",
    # quantization_config=bnb_config,  # Re-enable 8-bit
    device_map="auto",
    torch_dtype=torch.float16,
    token=token
)

tokenizer = AutoTokenizer.from_pretrained(
    "AIMLFreak/medalpaca_kenya-7b-4bit",
    token=token
)


def generate_response(prompt, max_new_tokens=400):
    inputs = tokenizer(prompt, return_tensors="pt").to(model.device)
    with torch.no_grad():
        output_ids = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            repetition_penalty=1.1,
            pad_token_id=tokenizer.eos_token_id
        )
    decoded = tokenizer.decode(output_ids[0], skip_special_tokens=True)
    return decoded