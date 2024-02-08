import urllib.request
from openai import OpenAI
import re

def parse_recipe(response_text):
    # Pattern to match the recipe sections
    dish_pattern = re.compile(r'(\d\..*?):')
    ingredients_pattern = re.compile(r'- Ingredients:(.*?)- Instructions:', re.DOTALL)
    instructions_pattern = re.compile(r'- Instructions:(.*)', re.DOTALL)

    # Find all dishes
    dishes = dish_pattern.findall(response_text)
    
    # Split the response by dishes to handle them separately
    dish_splits = dish_pattern.split(response_text)[1:]
    
    recipes = []
    for i in range(0, len(dish_splits), 2):
        dish_name = dishes[i//2].strip()
        dish_info = dish_splits[i] + dish_splits[i + 1]
        
        # Extract ingredients and instructions
        ingredients = ingredients_pattern.search(dish_info).group(1).strip()
        instructions = instructions_pattern.search(dish_info).group(1).strip()

        recipes.append({
            'name': dish_name,
            'ingredients': ingredients,
            'instructions': instructions
        })

    return recipes


# Convert the joke to spoken audio and save it as an MP3 file
# response = openai.audio.speech.create(model="tts-1", voice="alloy", input=ingredients)
# response.stream_to_file("joke.mp3")


def main():
    openai = OpenAI(
        api_key="sbhf8eshdtbz",
        base_url="https://openai.sd42.nl/api/providers/openai/v1"
    )

    user_prompt = 'chicken, eggs, cheese, tortilla' # fetched from flask form
    baseline_prompt = 'I want you to give me 2 meal options and the dish names that I can cook with the following ingredients: ' + user_prompt

    # print(baseline_prompt)
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": f"{baseline_prompt}"}
        ],
    )
    response_text = response.choices[0].message.content
    print(response_text)

    image_prompt = ''
    # parse text and separate different parts
    recipes = parse_recipe(response_text)
    for recipe in recipes:
        print("Dish Name:", recipe['name'])
        print("Ingredients:", recipe['ingredients'])
        print("Instructions:", recipe['instructions'])
        print("\n---\n")
        # do it with a list and append recipe instead?
        image_prompt = f"I want you to generate one image for each of these two meals: {recipe['name']}, {recipe}" # dish suggestions = str

    print(f'IMAGE PROMPT!!!! - {image_prompt}')

    # Create a DALL-E image for the joke

    # response = openai.images.generate(model="dall-e-2", prompt=image_prompt, quality="standard", n=2, size="1024x1024")
    # urllib.request.urlretrieve(response.data[0].url, 'joke.png')

    # credit usage check
    print(openai.models.with_raw_response.list().headers['OpenAiProxy'])

if __name__ == "main":
    main()
