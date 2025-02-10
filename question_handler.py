import json
import random
import os

def load_question_bank():
    """Load questions from question_bank.json"""
    with open('question_bank.json', 'r') as file:
        data = json.load(file)
        return data.get('Words', [])

def has_matching_image(word_data):
    """Check if the word has a matching image filename"""
    if 'Word' not in word_data or 'Image' not in word_data:
        return False

    word = word_data['Word'].lower()
    image = word_data['Image'].lower()

    # Check if image filename (without extension) matches the word
    image_base = os.path.splitext(image)[0]
    return word == image_base and (image.endswith('.png') or image.endswith('.jpg'))

def generate_misspellings(word):
    """Generate plausible misspellings for a word"""
    word = word.lower()
    misspellings = []

    # Common letter swaps
    swaps = {
        'i': 'y', 'y': 'i',
        'a': 'e', 'e': 'a',
        'o': 'ou', 'ou': 'o',
        'able': 'ible', 'ible': 'able',
        'ant': 'ent', 'ent': 'ant'
    }

    # Generate first misspelling by swapping letters
    misspelling1 = list(word)
    if len(word) > 3:
        idx = random.randint(1, len(word)-2)
        misspelling1[idx], misspelling1[idx+1] = misspelling1[idx+1], misspelling1[idx]
    misspellings.append(''.join(misspelling1))

    # Generate second misspelling using common swaps
    misspelling2 = word
    for correct, wrong in swaps.items():
        if correct in word:
            misspelling2 = misspelling2.replace(correct, wrong)
            break
    misspellings.append(misspelling2)

    # Generate third misspelling by doubling/removing doubled letters
    misspelling3 = word
    for letter in set(word):
        if letter+letter in word:
            misspelling3 = misspelling3.replace(letter+letter, letter)
            break
        elif letter in word and letter not in ['a', 'e', 'i', 'o', 'u']:
            misspelling3 = misspelling3.replace(letter, letter+letter)
            break
    misspellings.append(misspelling3)

    # Remove any duplicates and the correct spelling
    misspellings = list(set([m for m in misspellings if m != word]))

    # If we don't have enough unique misspellings, add some basic ones
    while len(misspellings) < 3:
        basic_misspelling = word.replace('e', 'a') if 'e' in word else word + 'e'
        if basic_misspelling not in misspellings and basic_misspelling != word:
            misspellings.append(basic_misspelling)

    return misspellings[:3]

def generate_test_questions():
    """Generate a new set of questions by randomly selecting words"""
    all_words = load_question_bank()

    # Filter words for picture section (must have matching image names)
    picture_words = [word for word in all_words if has_matching_image(word)]
    if len(picture_words) < 5:
        raise ValueError("Not enough words with matching images for picture section")

    # Other words can be any from the bank
    other_words = random.sample([w for w in all_words], 20)  # 5 words for each of the 4 other sections

    questions = {
        'dictation': [],
        'scrambled': [],
        'missing_letters': [],
        'word_identification': [],
        'picture_words': []
    }

    # Distribute words across sections
    for i in range(5):
        # Dictation section
        word_data = other_words[i]
        questions['dictation'].append({
            'word': word_data['Word'],
            'hint': word_data['Hint'],
            'audio': word_data['Audio']
        })

        # Scrambled section
        word_data = other_words[i+5]
        word = word_data['Word']
        scrambled = ''.join(random.sample(word.lower(), len(word)))
        questions['scrambled'].append({
            'word': word,
            'scrambled': scrambled,
            'hint': word_data['Hint']
        })

        # Missing letters section
        word_data = other_words[i+10]
        word = word_data['Word']
        display = ''.join([c if random.random() > 0.3 else '_' for c in word.lower()])
        questions['missing_letters'].append({
            'word': word,
            'display': display,
            'hint': word_data['Hint']
        })

        # Word identification section
        word_data = other_words[i+15]
        correct_word = word_data['Word']
        misspellings = generate_misspellings(correct_word)
        options = misspellings + [correct_word]
        random.shuffle(options)
        questions['word_identification'].append({
            'options': options,
            'correct': correct_word,
            'context': f"Choose the correct spelling:",
            'hint': word_data['Hint']
        })

        # Picture words section (using filtered picture words)
        word_data = random.choice(picture_words)
        picture_words.remove(word_data)  # Avoid duplicate selections
        questions['picture_words'].append({
            'word': word_data['Word'],
            'hint': word_data['Hint'],
            'image': word_data['Image']
        })

    return questions

def play_audio(word):
    """Get the audio file path for a word"""
    audio_folder = 'Audio'
    if not os.path.exists(audio_folder):
        os.makedirs(audio_folder)

    audio_path = os.path.join(audio_folder, word)
    if os.path.exists(audio_path):
        return audio_path
    return None