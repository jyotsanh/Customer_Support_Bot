from openai import OpenAI
import os

def list_available_models():
    """
    Lists all available OpenAI models for the given API key
    Returns a dictionary with model categories and their corresponding models
    """
    try:
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        models = client.models.list()
        
        # Categorize models
        model_categories = {
            'GPT-4': [],
            'GPT-3.5': [],
            'Other': []
        }
        
        for model in models:
            model_id = model.id
            if 'gpt-4' in model_id:
                model_categories['GPT-4'].append(model_id)
            elif 'gpt-3.5' in model_id:
                model_categories['GPT-3.5'].append(model_id)
            else:
                model_categories['Other'].append(model_id)
                
        return model_categories
        
    except Exception as e:
        return f"Error accessing OpenAI API: {str(e)}"

# Usage
if __name__ == "__main__":
    available_models = list_available_models()
    
    print("Available OpenAI Models:")
    print("----------------------")
    for category, models in available_models.items():
        print(f"\n{category}:")
        for model in sorted(models):
            print(f"- {model}")