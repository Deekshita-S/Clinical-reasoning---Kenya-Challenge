def clean_output(response,prompt):
    
    return response.strip().split(prompt)[1]