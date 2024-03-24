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


st.set_page_config(
    page_title='Seasonal Colour Analysis',
    page_icon='🎨',
    # layout='wide',
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
You are an expert at doing seasonal colour analysis for people. They will tell you their eye colour, hair colour, skin tone, and vein colour, and you will tell them their seasonal colour palette and show 25 diverse examples (don't have them be too similar) of good and bad colours for that palette.

Here's an example of what your output will look like:
"{
    "season_explanation": "Based on the information provided (blue eyes, blonde hair, blue veins, and fair skin), you fall into the `Cool Summer` category for your seasonal color analysis.",
    "season": "Cool Summer ☀️",
    "good_colours: ["#AFD5D1", "#A7C7C3", "#A6C9D4", "#B9D1C8", "#AFC8D7", "#AFB6BB", "#C4C9CD", "#CED0CD", "#B8C5C8", "#A7BCC4", "#ABC4C4", "#B5C7C8", "#BACAC7", "#B7C4C8", "#AEBDBE", "#A9C6C5", "#BBC6C8", "#A3B9BF", "#A5BBBF", "#ADC2C2", "#ABC0BF", "#9FAEB3", "#B8C2C4", "#B3B9BB", "#B3BDBE"],
    "bad_colours":  ["#FF0000", "#FFA500", "#FFFF00", "#008000", "#0000FF", "#800080", "#000000", "#FFFFFF", "#FFC0CB", "#FF69B4", "#FFD700", "#4B0082", "#800000", "#808080", "#C0C0C0", "#800080", "#00FFFF", "#00FF00", "#FFFF99", "#FFB6C1", "#FF6347", "#6A5ACD", "#8A2BE2", "#FF4500", "#FF00FF"],
    'colour_explanation": "Good colors for Cool Summer include cool-toned hues like soft blues, muted pinks, lavender, and cool greens, characterized by soft, muted, and slightly dusty qualities, while bad colors encompass warm-toned hues such as yellows, oranges, and warm browns, along with bright, highly saturated colors and vibrant neon shades, which clash with cool undertones and may create an unbalanced look. However, it's important to note that these are just guidelines, and you should ultimately wear whatever colors make you feel confident and beautiful!"
}"

Format your explanations nicely in markdown and feel free to use emojis to make it more fun! 🎨
It's important you output the information in the correct python dict format (so I can call eval() on the output without errror), as shown above, or everything will break.
Ensure your output has these exact keys ("season_explanation", "season", "good_colours", "bad_colours", "colour_explanation") in the dictionary - otherwise the application will break.
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
                "season": "Light Summer ☀️",
                "good_colours": ["#B8D9C8", "#AACDBE", "#C9E5E2", "#C1D5E0", "#D5E3E9", "#E1D7DB", "#F1E3E4", "#F4F2F3", "#DDD0C7", "#D6CEB1", "#B0BFBF", "#A8B2B2", "#DFD1CA", "#B7C9A3", "#B4C3C2", "#A6A6A6", "#F0E7D8", "#F7EFE2", "#E0DDD6", "#BEB3A9", "#D6E0CD", "#E5E1E0", "#E7E2D9", "#E2E1D8"],
                "bad_colours": ["#FF0000", "#FFA500", "#FFFF00", "#008000", "#0000FF", "#800080", "#000000", "#FFFFFF", "#FFC0CB", "#FF69B4", "#FFD700", "#4B0082", "#800000", "#808080", "#C0C0C0", "#800080", "#00FFFF", "#00FF00", "#FFFF99", "#FFB6C1", "#FF6347", "#6A5ACD", "#8A2BE2", "#FF4500", "#FF00FF"],
                'colour_explanation': "The Good Colours listed are cool-toned and muted, and should be complementary to your colouring. The Bad Colours listed are warm-toned and bright, and may not be as complementary to your colouring. However, it\'s important to note that these are just guidelines, and you should ultimately wear whatever colours make you feel confident and beautiful!"
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
                "season": "Light Sprint 💐",
                "good_colours": ["#F5F5D9", "#F5E8D9", "#F5E1D5", "#F5D5D5", "#F5D5E1", "#F5D5E6", "#F5D5E0", "#F5D5D0", "#F5D5CF", "#F5D5C3", "#F5D5B8", "#F5D5AD", "#F5D5A3", "#F5D599", "#F5D58F", "#F5D585", "#F5D57B", "#F5D571", "#F5D566", "#F5D55B", "#F5D551", "#F5D53B", "#F5D531"],
                "bad_colours": ["#FF0000", "#FFA500", "#FFFF00", "#008000", "#0000FF", "#800080", "#000000", "#FFFFFF", "#FFC0CB", "#FF69B4", "#FFD700", "#4B0082", "#800000", "#808080", "#C0C0C0", "#800080", "#00FFFF", "#00FF00", "#FFFF99", "#FFB6C1", "#FF6347", "#6A5ACD", "#8A2BE2", "#FF4500", "#FF00FF"],
                'colour_explanation': "The Good Colours listed are warm-toned and muted, and should be complementary to your colouring. The Bad Colours listed are cool-toned and bright, and may not be as complementary to your colouring. However, it's important to note that these are just guidelines, and you should ultimately wear whatever colours make you feel confident and beautiful!"
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

st.markdown(
    f"""
## Your Seasonal Colour Palette 🌈

You are a **{color_analysis['season']}**!
    """
)

st.expander('Season Explanation').markdown(
    f"""{color_analysis['season_explanation']}"""
)

st.markdown('### Colour Palette')

st.expander('Palette Explanation').markdown(
    f"""{color_analysis['colour_explanation']}"""
)

col1, col2 = st.columns(2)

with col1:
    st.markdown('#### Good Colours')
    for colour in color_analysis['good_colours']:
        st.markdown(f'<div style="background-color: {colour}; padding: 10px; margin: 5px; border-radius: 5px;"></div>', unsafe_allow_html=True)

with col2:
    st.markdown('#### Bad Colours')
    for colour in color_analysis['bad_colours']:
        st.markdown(f'<div style="background-color: {colour}; padding: 10px; margin: 5px; border-radius: 5px;"></div>', unsafe_allow_html=True)

st.caption("Want to say thanks? \n[Buy me a coffee ☕](https://www.buymeacoffee.com/brydon)")