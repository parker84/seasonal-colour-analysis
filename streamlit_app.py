from groq import Groq
import streamlit as st
from decouple import config
import json
import logging, coloredlogs
logger = logging.getLogger(__name__)
coloredlogs.install(level=config('LOG_LEVEL', 'INFO'), logger=logger)


GROQ_MODEL = 'mixtral-8x7b-32768'
TIMEOUT = 120
groq_client = Groq(
    api_key=config('GROQ_API_KEY'),
)

COLOUR_PALETTES = {
    "Bright Spring": {
        "good_colours": ["#FF0000", "#FF4500", "#FF6347", "#FF7F50", "#FF8C00", "#FFA500", "#FFD700", "#FFA07A", "#FF69B4", "#FF1493", "#FFB6C1", "#FFC0CB", "#FF00FF", "#FF69B4", "#FF1493", "#FF4500", "#FF6347", "#FF7F50", "#FF8C00", "#FFA500", "#FFD700", "#FFA07A", "#FF69B4", "#FF1493"],
        "bad_colours": ["#B0C4DE", "#A0B6CC", "#87CEEB", "#87CEFA", "#00BFFF", "#1E90FF", "#6495ED", "#F0E68C", "#FFFF00", "#FFD700", "#DAA520", "#B8860B", "#F0E68C", "#D3D3D3", "#B0C4DE", "#A0B6CC", "#87CEEB", "#87CEFA", "#00BFFF", "#1E90FF", "#6495ED", "#F0E68C", "#FFFF00", "#FFD700"],
        "colour_explanation": "Good colors for a `Bright Spring` are bold and vibrant hues such as true reds, bright oranges, sunny yellows, and vivid greens, while bad colors are muted or cool tones like soft pastels, cool grays, and deep blues that can dull the overall appearance. However, it's important to note that these are just guidelines, and you should ultimately wear whatever colors make you feel confident and beautiful!"
    },
    "Warm Spring": {
         "good_colours": ["#FFD700", "#FFA500", "#DAA520", "#B8860B", "#F0E68C", "#FFD700", "#DAA520", "#B8860B", "#FFA07A", "#FF7F50", "#FF6347", "#FF4500", "#228B22", "#008000", "#556B2F", "#8B4513", "#A0522D", "#D2691E", "#8B0000", "#B22222", "#CD5C5C", "#FF0000", "#DC143C", "#FF4500"],
        "bad_colours": ["#87CEEB", "#87CEFA", "#00BFFF", "#1E90FF", "#6495ED", "#4682B4", "#5F9EA0", "#191970", "#4169E1", "#00CED1", "#20B2AA", "#008B8B", "#008080", "#00FFFF", "#00FFFF", "#008000", "#32CD32", "#00FF00", "#ADFF2F", "#7FFF00", "#ADFF2F", "#FFFF00", "#FFFF00", "#FFD700"],
        "colour_explanation": "Good colors for a `Warm Spring` are warm and vibrant shades such as golden yellows, warm oranges, rich greens, and earthy browns, while bad colors are cool or muted tones like icy blues, cool grays, and deep purples that can clash with the warm undertones of the skin and hair. However, it's important to note that these are just guidelines, and you should ultimately wear whatever colors make you feel confident and beautiful!"
    },
    "Light Spring": {
        "good_colours": ["#FFFACD", "#FAFAD2", "#FFD700", "#F0E68C", "#FFA07A", "#FF7F50", "#FF6347", "#FF4500", "#FF69B4", "#FF1493", "#FFC0CB", "#FFB6C1", "#FF69B4", "#FF1493", "#FFC0CB", "#FFB6C1", "#FF69B4", "#FF1493", "#FFC0CB", "#FFB6C1", "#FF6347", "#FFDAB9", "#FFE4B5", "#FFDEAD", "#FFE4C4"],
        "bad_colours": ["#87CEEB", "#87CEFA", "#00BFFF", "#1E90FF", "#6495ED", "#4682B4", "#5F9EA0", "#191970", "#4169E1", "#00CED1", "#20B2AA", "#008B8B", "#008080", "#00FFFF", "#00FFFF", "#008000", "#32CD32", "#00FF00", "#ADFF2F", "#7FFF00", "#ADFF2F", "#FFFF00", "#FFFF00", "#FFD700", "#FFA500"],
        "colour_explanation": "Good colors for a `Light Spring` are warm and fresh shades such as soft peach, warm yellows, light corals, and soft greens, while bad colors are overly cool or dark tones like deep blues, harsh blacks, and cool grays that can wash out the warm undertones of the skin and hair. However, it's important to note that these are just guidelines, and you should ultimately wear whatever colors make you feel confident and beautiful!"
    },
    "Light Summer": {
        "good_colours": ["#B0C4DE", "#87CEEB", "#87CEFA", "#00BFFF", "#1E90FF", "#6495ED", "#AFEEEE", "#ADD8E6", "#F0F8FF", "#E0FFFF", "#D3D3D3", "#C0C0C0", "#FFC0CB", "#FFB6C1", "#FF69B4", "#FF1493", "#FFC0CB", "#FFB6C1", "#FF69B4", "#FF1493", "#FFC0CB", "#FFB6C1", "#FF69B4", "#FF1493", "#FFC0CB"],
        "bad_colours": ["#FFA500", "#FF4500", "#FF0000", "#DC143C", "#8B0000", "#FFD700", "#FFA500", "#FF4500", "#FF0000", "#DC143C", "#8B0000", "#FFD700", "#FFA500", "#FF4500", "#FF0000", "#DC143C", "#8B0000", "#FFD700", "#FFA500", "#FF4500", "#FF0000", "#DC143C", "#8B0000", "#FFD700", "#FFA500"],
        "colour_explanation": "Good colors for a `Light Summer` are soft and delicate hues such as soft blues, muted pinks, soft lavenders, and light grays, while bad colors are overly warm or intense tones like bright oranges, deep blacks, and overly saturated hues that can overpower the softness of the skin and hair tones. However, it's important to note that these are just guidelines, and you should ultimately wear whatever colors make you feel confident and beautiful!"
    },
    "Cool Summer": {
        "good_colours": ["#AFEEEE", "#B0E0E6", "#87CEEB", "#6495ED", "#4682B4", "#5F9EA0", "#ADD8E6", "#B0C4DE", "#778899", "#AFEEEE", "#B0E0E6", "#87CEEB", "#6495ED", "#4682B4", "#5F9EA0", "#ADD8E6", "#B0C4DE", "#778899", "#87CEFA", "#00BFFF", "#1E90FF", "#87CEFA", "#00BFFF", "#1E90FF", "#87CEFA"],
        "bad_colours": ["#FF4500", "#FF0000", "#DC143C", "#B22222", "#FF69B4", "#FF1493", "#FFC0CB", "#FFD700", "#FFA500", "#DAA520", "#B8860B", "#FF4500", "#FF0000", "#DC143C", "#B22222", "#FF69B4", "#FF1493", "#FFC0CB", "#FF69B4", "#FF1493", "#FFC0CB", "#FFD700", "#FFA500", "#DAA520", "#B8860B"],
        "colour_explanation": "Good colors for a `Cool Summer` are soft and cool tones such as soft blues, soft pinks, cool grays, and soft purples, while bad colors are warm or overly vibrant hues like warm oranges, bright yellows, and harsh blacks that can clash with the cool undertones of the skin and hair. However, it's important to note that these are just guidelines, and you should ultimately wear whatever colors make you feel confident and beautiful!"
    },
    "Soft Summer": {
        "good_colours": ["#B0C4DE", "#A0B6CC", "#87CEEB", "#778899", "#6C7B8B", "#708090", "#D8BFD8", "#E6E6FA", "#C0C0C0", "#A9A9A9", "#D3D3D3", "#BC8F8F", "#DA70D6", "#9370DB", "#DDA0DD", "#A0522D", "#CD853F", "#BC8F8F", "#F4A460", "#CD853F", "#D2691E", "#8B4513", "#F5DEB3", "#FAEBD7", "#FFE4B5", "#FFDEAD", "#FFDAB9", "#FFE4C4", "#FFA07A", "#FF8C00", "#DAA520", "#B8860B", "#FFF8DC", "#F0E68C"],
        "bad_colours": ["#FFA500", "#FF4500", "#8B0000", "#FF0000", "#DC143C", "#FFD700", "#FFA500", "#FF4500", "#8B0000", "#FF0000", "#DC143C", "#FFD700", "#FFA500", "#FF4500", "#8B0000", "#FF0000", "#DC143C", "#FFD700", "#6B8E23", "#556B2F", "#808000", "#2F4F4F", "#8B4513", "#A52A2A", "#800000", "#CD5C5C", "#FF0000", "#DC143C", "#B22222", "#FF6347", "#FF4500", "#FF8C00", "#FFA500", "#D2691E", "#FFA07A"],
        "colour_explanation": "Good colors for a `Soft Summer` are muted and cool tones such as soft blues, dusty roses, cool grays, and soft lavenders, while bad colors are overly warm or intense hues like bright oranges, warm reds, and harsh blacks that can overpower the softness of the skin and hair tones. However, it's important to note that these are just guidelines, and you should ultimately wear whatever colors make you feel confident and beautiful!"
    },
    "Bright Winter": {
         "good_colours": ["#FF0000", "#0000FF", "#00FFFF", "#008080", "#00FF7F", "#7FFFD4", "#20B2AA", "#00BFFF", "#00CED1", "#4682B4", "#6A5ACD", "#800080", "#8A2BE2", "#BA55D3", "#FF1493", "#FF69B4", "#FF4500", "#FFA500", "#FFD700", "#DAA520", "#F0E68C", "#B8860B", "#D2B48C", "#808000", "#008000"],
        "bad_colours": ["#FFC0CB", "#FFA07A", "#FFDAB9", "#FFE4C4", "#FFDEAD", "#FFFF00", "#FFD700", "#FFA500", "#DAA520", "#B8860B", "#F0E68C", "#EEE8AA", "#F5DEB3", "#FFC0CB", "#FFA07A", "#FFDAB9", "#FFE4C4", "#FFDEAD", "#FFFF00", "#FFD700", "#FFA500", "#DAA520", "#B8860B", "#F0E68C", "#EEE8AA"],
        "colour_explanation": "Good colors for a `Bright Winter` are vibrant and bold hues such as true reds, electric blues, emerald greens, and hot pinks, while bad colors are soft or muted tones like pastels, earthy browns, and warm neutrals that can appear washed out against the strong contrast of the skin and hair. However, it's important to note that these are just guidelines, and you should ultimately wear whatever colors make you feel confident and beautiful!"
    },
    "Cool Winter": {
        "good_colours": ["#0000FF", "#00008B", "#4169E1", "#6A5ACD", "#800080", "#8A2BE2", "#483D8B", "#4B0082", "#9370DB", "#7B68EE", "#4682B4", "#87CEEB", "#00BFFF", "#1E90FF", "#6495ED", "#B0C4DE", "#87CEFA", "#AFEEEE", "#8A2BE2", "#800080"],
        "bad_colours": ["#8B4513", "#A52A2A", "#CD5C5C", "#FF0000", "#DC143C", "#B22222", "#FF6347", "#FF4500", "#FF8C00", "#FFA500", "#D2691E", "#FFA07A", "#FF7F50", "#FF69B4", "#FFC0CB", "#FFDAB9", "#FFE4C4", "#FFDEAD", "#FFD700", "#FFA500"],
        "colour_explanation": "Good colors for a `Cool Winter` are jewel tones and icy shades such as sapphire blues, emerald greens, magenta pinks, and cool grays, while bad colors are warm or muted tones like earthy browns, warm oranges, and soft pastels that can clash with the cool undertones of the skin and hair. However, it's important to note that these are just guidelines, and you should ultimately wear whatever colors make you feel confident and beautiful!"
    },
    "Deep Winter": {
        "good_colours": ["#00008B", "#0000FF", "#1E90FF", "#4169E1", "#000080", "#483D8B", "#8A2BE2", "#800080", "#4B0082", "#8B0000", "#B22222", "#FF0000", "#DC143C", "#008000", "#2E8B57", "#006400", "#008000", "#228B22"],
        "bad_colours": ["#87CEEB", "#87CEFA", "#00BFFF", "#1E90FF", "#6495ED", "#4682B4", "#5F9EA0", "#191970", "#4169E1", "#00CED1", "#20B2AA", "#008B8B", "#008080", "#00FFFF", "#008000", "#32CD32", "#00FF00", "#ADFF2F", "#7FFF00", "#FFFF00", "#FFD700", "#FFA500"],
        "colour_explanation": "Good colors for a `Deep Winter` are bold and rich shades such as deep blues, true reds, emerald greens, and royal purples, while bad colors are soft or muted tones like pastels, warm neutrals, and subdued hues that can appear washed out against the strong contrast of the skin and hair. However, it's important to note that these are just guidelines, and you should ultimately wear whatever colors make you feel confident and beautiful!"
    },
    "Soft Autumn": {
        "good_colours": ["#D2B48C", "#BC8F8F", "#DEB887", "#CD853F", "#D2691E", "#8B4513", "#F4A460", "#FFDAB9", "#FFE4C4", "#FFA07A", "#FF8C00", "#DAA520", "#B8860B", "#F5DEB3", "#FAEBD7"],
        "bad_colours": ["#4169E1", "#0000FF", "#00008B", "#000080", "#696969", "#808080", "#708090", "#A9A9A9", "#2F4F4F", "#D3D3D3", "#778899", "#B0C4DE", "#B0E0E6", "#ADD8E6", "#87CEEB", "#87CEFA", "#00BFFF", "#1E90FF", "#6495ED", "#4682B4", "#5F9EA0", "#191970", "#6A5ACD", "#483D8B", "#7B68EE"],
        "colour_explanation": "Good colors for a `Soft Autumn` are warm and muted shades such as soft olive greens, warm beiges, soft browns, and warm grays, while bad colors are overly cool or bright tones like deep blues, harsh blacks, and neon shades that can clash with the warm undertones of the skin and hair. However, it's important to note that these are just guidelines, and you should ultimately wear whatever colors make you feel confident and beautiful!"
    },
}


st.set_page_config(
    page_title='Seasonal Colour Analysis',
    page_icon='🎨',
    initial_sidebar_state='collapsed'
)

st.title('🎨 Seasonal Colour Analysis')
st.caption('Enter your information and learn about your seasonal colour palette! 🌈')

with st.form(key='my_form'):
    eye_colour = st.selectbox('What is your eye colour? 👀', ['Blue', 'Green', 'Brown', 'Hazel', 'Amber', 'Gray'], index=None)
    hair_colour = st.selectbox('What is your hair colour? 💇‍♀️', ['Blonde', 'Brown', 'Black', 'Red', 'Gray', 'White'], index=None)
    skin_tone = st.selectbox('What is your skin tone? 🎨', ['Fair', 'Light', 'Medium', 'Olive', 'Tan', 'Dark'], index=None)
    vein_colour = st.selectbox('What is the colour of your veins? 🩸', ['Blue', 'Green', 'Purple'], index=None)
    with st.expander('Get more specific (optional)'):
        eye_colour_adv = st.color_picker('Eye Colour', value='#000000')
        hair_colour_adv = st.color_picker('Hair Colour', value='#000000')
        skin_tone_adv = st.color_picker('Skin Tone', value='#000000')
        vein_colour_adv = st.color_picker('Vein Colour', value='#000000')
        if eye_colour_adv != '#000000':
            eye_colour = eye_colour_adv
        if hair_colour_adv != '#000000':
            hair_colour = hair_colour_adv
        if skin_tone_adv != '#000000':
            skin_tone = skin_tone_adv
        if vein_colour_adv != '#000000':
            vein_colour = vein_colour_adv
    submit_button = st.form_submit_button(label='Get My Seasonal Colour Palette!', type='primary')

if eye_colour is None or hair_colour is None or skin_tone is None or vein_colour is None:
    st.warning('Please fill out all fields to get your colour analysis.') # TODO: do this better
    st.stop()

colour_analysis_prompt = """
You are an expert at doing seasonal colour analysis for people. They will tell you their eye colour, hair colour, skin tone, and vein colour, 
and you will tell them their seasonal colour palette (see options below) and an explanation as to why you assigned this colour palette.

Here are the palette options: ["Bright Spring", "Warm Spring", "Light Spring", "Light Summer", "Cool Summer", "Soft Summer", "Bright Winter", "Cool Winter", "Deep Winter", "Soft Autumn"]

Here's an example of what your output will look like:
"{
    "season_explanation": "Based on the information provided (blue eyes, blonde hair, blue veins, and fair skin), you fall into the `Cool Summer` category for your seasonal color analysis.",
    "season": "Cool Summer"
}"

It's important you output the information in the correct python dict format (so I can call eval() on the output without errror), as shown above, or everything will break.
Ensure your output has these exact keys ("season_explanation", "season") in the dictionary - otherwise the application will break.
Do not return any text before or after the python dict.
"""

def get_user_input_messages(eye_colour, hair_colour, skin_tone, vein_colour):
    user_input = f"""

    Heres is my information:
        Eye Colour: {eye_colour}
        Hair Colour: {hair_colour}
        Skin Tone: {skin_tone}
        Vein Colour: {vein_colour}

    Now, tell me my seasonal colour palette (and output it in the proper python dict format).
    """
    return user_input

def clean_dict(text):
    logger.info(f'Cleaning up json text...')
    
    json_cleaning_prompt = """
You take text and clean it up so that the output is a proper python dictionary. When you return the results (clean_dict) I can call eval(clean_dict) (in python) in our output and it runs without error.
Do not return anything except the cleaned json (not text before or after the json).
"""
    messages = [
        {
            "role": "system",
            "content": json_cleaning_prompt
        },
        {
            "role": "user",
            "content": text
        }
    ]

    text = groq_client.chat.completions.create(
        messages=messages,
        model=GROQ_MODEL,
        temperature=0,
        timeout=TIMEOUT
    ).choices[0].message.content

    clean_dict = eval(text.replace('\\', '')) 

    logger.info(f'Cleaned up json text ✅')
    logger.info(json.dumps(clean_dict, indent=4))
    return clean_dict

@st.cache_data()
def get_seasonal_colour_pallette(eye_colour, hair_colour, skin_tone, vein_colour):
    logger.info(f'Getting seasonal colour palette for eye_colour={eye_colour}, hair_colour={hair_colour}, skin_tone={skin_tone}, vein_colour={vein_colour}...')
    messages = [
        {
            "role": "system",
            "content": colour_analysis_prompt
        },
        {
            "role": "user",
            "content": get_user_input_messages('Blue', 'Blonde', 'Fair', 'Blue')
        },
        {
            "role": "assistant",
            "content": """{
                "season_explanation": "Based on the information you provided, it sounds like you have cool-toned features, with blue eyes, blonde hair, fair skin, and blue veins. This would suggest that you are a cool-toned individual, and I would recommend exploring the `Winter` and `Summer` seasons. Based on your fair skin and blue veins, I would recommend the `Light Summer` sub-season within the Summer season. `Light Summer` individuals have a muted, soft, and delicate colouring, with a cool undertone. They typically have light blonde, light brown, or strawberry blonde hair, fair skin, and blue or green eyes.",
                "season": "Light Summer"
            }"""
        },
        {
            "role": "user",
            "content": get_user_input_messages('Brown', 'Blonde', 'Fair', 'Blue')
        },
        {
            "role": "assistant",
            "content": """{
                "season_explanation": "Based on the information you provided, it sounds like you have cool-toned features, with brown eyes, blonde hair, fair skin, and blue veins. This would suggest that you are a cool-toned individual, and I would recommend exploring the `Winter` and `Summer` seasons. Based on your fair skin and blue veins, I would recommend the `Light Spring` sub-season within the Spring season. `Light Spring` individuals have a warm undertone, and typically have light blonde, light brown, or strawberry blonde hair, fair skin, and brown or green eyes.",
                "season": "Light Spring"
            }"""
        },
        {
            "role": "user",
            "content": get_user_input_messages(eye_colour, hair_colour, skin_tone, vein_colour)
        }
    ]

    chat_completion = groq_client.chat.completions.create(
        messages=messages,
        model=GROQ_MODEL,
        temperature=0,
        timeout=TIMEOUT
    ).choices[0].message

    logger.info(f'Got seasonal colour palette for eye_colour={eye_colour}, hair_colour={hair_colour}, skin_tone={skin_tone}, vein_colour={vein_colour} ✅')

    colour_analysis = clean_dict(chat_completion.content)

    return colour_analysis

color_analysis = get_seasonal_colour_pallette(eye_colour, hair_colour, skin_tone, vein_colour)
color_palette = COLOUR_PALETTES[color_analysis['season']]

def add_emoji_to_season(season):
    if 'Winter' in season:
        return season + ' ❄️'
    if 'Spring' in season:
        return season + ' 💐'
    if 'Summer' in season:
        return season + ' ☀️'
    if 'Autumn' in season:
        return season + ' 🍂'

st.markdown(
    f"""
## Your Seasonal Colour Palette 🌈

You are a **{add_emoji_to_season(color_analysis['season'])}**!
    """
)

st.expander('Season Explanation').markdown(
    f"""{color_analysis['season_explanation']}"""
)

st.markdown('### Colour Palette')

with st.expander('Palette Explanation', expanded=True):
    st.markdown(
        f"""{color_palette['colour_explanation']}"""
    )

col1, col2 = st.columns(2)

with col1:
    st.markdown('#### Good Colours')
    for colour in set(color_palette['good_colours']):
        st.markdown(f'<div style="background-color: {colour}; padding: 10px; margin: 5px; border-radius: 5px;"></div>', unsafe_allow_html=True)

with col2:
    st.markdown('#### Bad Colours')
    for colour in set(color_palette['bad_colours']):
        st.markdown(f'<div style="background-color: {colour}; padding: 10px; margin: 5px; border-radius: 5px;"></div>', unsafe_allow_html=True)

st.caption("Want to say thanks? \n[Buy me a coffee ☕](https://www.buymeacoffee.com/brydon)")