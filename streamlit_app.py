from groq import Groq
import streamlit as st
from decouple import config
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
You are an expert at doing seasonal colour analysis for people. They will tell you their eye colour, hair colour, skin tone, and vein colour, and you will tell them their seasonal colour palette.

Here's an example of what your output will look like:
"{
    "season_explanation": "You are a Light Summer. Your best colours are light and cool, like light blues, light pinks, and light purples. Avoid dark and warm colours like dark reds, oranges, and yellows.",
    "season": "Summer",
    "sub_season": "Light Summer",
    "good_colours: ["#f0f8ff", "#b0e0e6", "#87cefa", "#4682b4", "#5f9ea0", "#7b68ee", "#6a5acd", "#483d8b"],
    "bad_colours": ["#ff0000", "#ff4500", "#ff8c00", "#ffd700", "#adff2f", "#32cd32", "#008000", "#006400"],
    'colour_explanation": "Your eye colour is blue, your hair colour is blonde, your skin tone is fair, and your vein colour is blue. This makes you a Light Summer."
}"

It's important you output the information in the correct python dict format (so I can call eval() on the output without errror), as shown above, or everything will break.
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

    clean_dict = eval(text) 

    logger.info(f'Cleaned up json text ✅')
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
                "season_explanation": "Based on the information you provided, it sounds like you have cool-toned features, with blue eyes, blonde hair, fair skin, and blue veins. This would suggest that you are a cool-toned individual, and I would recommend exploring the "Winter" and "Summer" seasons.\n\nBased on your fair skin and blue veins, I would recommend the "Light Summer" sub-season within the Summer season. "Light Summer" individuals have a muted, soft, and delicate colouring, with a cool undertone. They typically have light blonde, light brown, or strawberry blonde hair, fair skin, and blue or green eyes.",
                "season": "Summer",
                "sub_season": "Light Summer",
                "good_colours": ["#f0f8ff", "#b0e0e6", "#87cefa", "#4682b4", "#5f9ea0", "#7b68ee", "#6a5acd", "#483d8b"],
                "bad_colours": ["#ff0000", "#ff4500", "#ff8c00", "#ffd700", "#adff2f", "#32cd32", "#008000", "#006400"],
                'colour_explanation': "The "Good Colours" listed are cool-toned and muted, and should be complementary to your colouring. The "Bad Colours" listed are warm-toned and bright, and may not be as complementary to your colouring. However, it\'s important to note that these are just guidelines, and you should ultimately wear whatever colours make you feel confident and beautiful!"
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

You are a **{color_analysis['sub_season']}**!
    """
)

st.expander('Season Explanation').markdown(
    f"""{color_analysis['season_explanation']}"""
)

st.markdown('### Colour Palette')

col1, col2 = st.columns(2)

with col1:
    st.markdown('#### Good Colours')
    for colour in color_analysis['good_colours']:
        st.markdown(f'<div style="background-color: {colour}; padding: 10px; margin: 5px; border-radius: 5px;"></div>', unsafe_allow_html=True)

with col2:
    st.markdown('#### Bad Colours')
    for colour in color_analysis['bad_colours']:
        st.markdown(f'<div style="background-color: {colour}; padding: 10px; margin: 5px; border-radius: 5px;"></div>', unsafe_allow_html=True)

st.expander('Colour Explanation').markdown(
    f"""{color_analysis['colour_explanation']}"""
)