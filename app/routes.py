from flask import Blueprint, render_template, request, jsonify
import requests
import os
from dotenv import find_dotenv, load_dotenv

# Load environment variables
load_dotenv(find_dotenv())
NEMOTRONS_API_KEY = os.getenv("NEMOTRONS_API_KEY")

main = Blueprint('main', __name__)

CATEGORIES = {
    "Kids": "Write a fun and engaging story suitable for kids inspired ancient indian stroybook called 'Panchtantra' with moral of the story in the end ",
    "Teen": "Create an intriguing meaningful story for teenagers with twist.",
    "Senior": "Generate a story for senior citizen with wose meaning and thoughtful."
}

LANGUAGES = {
    "English": "en",
    "Hindi": "hi",
    "Marathi": "mr",
    "Spanish": "es",
    "French": "fr",
    "German": "de",
    "Japanese": "ja"
}

GENRES = ["Comedy","Romance","Drama","Horror","Science Fiction", "Mystery", "Adventure","Fictional", ]

def story_generator(scenario, category, language, genre):
    context = CATEGORIES.get(category, "")
    full_scenario = f"Instructions: {context}\nGenre: {genre}\nScenario: {scenario}\nLanguage: {language}"

    API_URL = "https://integrate.api.nvidia.com/v1/chat/completions"
    headers = {"Authorization": f"Bearer {NEMOTRONS_API_KEY}"}
    payload = {
        "model": "nvidia/llama-3.1-nemotron-70b-instruct",
        "messages": [{"role": "user", "content": full_scenario}],
        "temperature": 0.5,
        "top_p": 1,
        "max_tokens": 900,
        "stream": False
    }

    response = requests.post(API_URL, headers=headers, json=payload, verify=False)
    response.raise_for_status()
    data = response.json()
    
    story = ''.join([choice['message']['content'] for choice in data['choices']])
    

    formatted_story = story.replace('**The Moral of the Story**', '<h3>The Moral of the Story</h3>').replace('**', '<b>').replace('**', '</b>')
    return formatted_story

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/story_generator')
def story_generator_page():
    return render_template('main.html', categories=CATEGORIES, languages=LANGUAGES, genres=GENRES)

@main.route('/generate_story', methods=['POST'])
def generate_story():
    data = request.json
    category = data.get('category')
    genre = data.get('genre')
    language = data.get('language')
    scenario = data.get('scenario', 'Once upon a time...')

    story = story_generator(scenario, category, language, genre)
    return jsonify({"story": story})
