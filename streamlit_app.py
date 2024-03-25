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
        "good_colours": ['#fdfdfd', '#625a51', '#e78590', '#dbdcd4', '#8f9e97', '#30352d', '#5e9ed1', '#cf9863', '#325f6c', '#a04739', '#f0d176', '#f1d3c5', '#695997', '#3470b4', '#c8c4c7', '#609445', '#997dc2', '#eaa7b9', '#c36090', '#2b3867', '#c4d982', '#793255', '#abaaaa', '#78ced1', '#aeded8', '#41837b', '#c04f5c', '#efeeee', '#9a8372', '#836959'],
        "bad_colours": ["#B0C4DE", "#A0B6CC", "#87CEEB", "#87CEFA", "#00BFFF", "#1E90FF", "#6495ED", "#F0E68C", "#FFFF00", "#FFD700", "#DAA520", "#B8860B", "#F0E68C", "#D3D3D3", "#B0C4DE", "#A0B6CC", "#87CEEB", "#87CEFA", "#00BFFF", "#1E90FF", "#6495ED", "#F0E68C", "#FFFF00", "#FFD700"],
        "colour_explanation": "Good colors for a `Bright Spring` are bold and vibrant hues such as true reds, bright oranges, sunny yellows, and vivid greens, while bad colors are muted or cool tones like soft pastels, cool grays, and deep blues that can dull the overall appearance. However, it's important to note that these are just guidelines, and you should ultimately wear whatever colors make you feel confident and beautiful!"
    },
    "Warm Spring": {
         "good_colours": ['#bf99cb', '#f4f1ea', '#7d7a6d', '#aeac9a', '#6b503e', '#e0a592', '#2c659f', '#366e56', '#e07b61', '#e1d2b8', '#4b342c', '#60c4b6', '#fdfdfd', '#604381', '#4d9d7b', '#6180bf', '#c4464b', '#ad966b', '#c9da7f', '#92c9bd', '#8f9d46', '#efe1c8', '#dfc59d', '#a5bbe0', '#d09875', '#edce83', '#c4c3ba', '#d5dfe5', '#e6af64', '#7f9595'],
        "bad_colours": ["#87CEEB", "#87CEFA", "#00BFFF", "#1E90FF", "#6495ED", "#4682B4", "#5F9EA0", "#191970", "#4169E1", "#00CED1", "#20B2AA", "#008B8B", "#008080", "#00FFFF", "#00FFFF", "#008000", "#32CD32", "#00FF00", "#ADFF2F", "#7FFF00", "#ADFF2F", "#FFFF00", "#FFFF00", "#FFD700"],
        "colour_explanation": "Good colors for a `Warm Spring` are warm and vibrant shades such as golden yellows, warm oranges, rich greens, and earthy browns, while bad colors are cool or muted tones like icy blues, cool grays, and deep purples that can clash with the warm undertones of the skin and hair. However, it's important to note that these are just guidelines, and you should ultimately wear whatever colors make you feel confident and beautiful!"
    },
    "Light Spring": {
        "good_colours": ['#aeaca4', '#ede1dc', '#5c5183', '#edc578', '#9b8370', '#63b89f', '#fdfdfc', '#8fafd6', '#635649', '#e8bd9d', '#d35f62', '#db889c', '#4ca070', '#d0bd9e', '#9489b6', '#c7c5bc', '#e79f7e', '#a5cd90', '#3c6b96', '#eeb9c3', '#a4a48d', '#6a6961', '#395180', '#4d8678', '#ecdcc2', '#f3d990', '#909698', '#f5f1eb', '#cce2e3', '#96cccb'],
        "bad_colours": ["#87CEEB", "#87CEFA", "#00BFFF", "#1E90FF", "#6495ED", "#4682B4", "#5F9EA0", "#191970", "#4169E1", "#00CED1", "#20B2AA", "#008B8B", "#008080", "#00FFFF", "#00FFFF", "#008000", "#32CD32", "#00FF00", "#ADFF2F", "#7FFF00", "#ADFF2F", "#FFFF00", "#FFFF00", "#FFD700", "#FFA500"],
        "colour_explanation": "Good colors for a `Light Spring` are warm and fresh shades such as soft peach, warm yellows, light corals, and soft greens, while bad colors are overly cool or dark tones like deep blues, harsh blacks, and cool grays that can wash out the warm undertones of the skin and hair. However, it's important to note that these are just guidelines, and you should ultimately wear whatever colors make you feel confident and beautiful!"
    },
    "Light Summer": {
        "good_colours": ['#e0a3aa', '#4e889a', '#fdfdfd', '#9d4b77', '#93c3da', '#5e5859', '#d4dde2', '#7a6da1', '#d45d7f', '#8cbea6', '#c0c6c9', '#563e42', '#3c4855', '#eac3ce', '#5f5796', '#62aca8', '#f4f3f2', '#8b8b92', '#dc7784', '#3f7055', '#b2afd2', '#3573a1', '#b25c83', '#89486b', '#6e7474', '#a8a4af', '#eae3e1', '#a7cce1', '#8cb992', '#c98a9e'],
        "bad_colours": ["#FFA500", "#FF4500", "#FF0000", "#DC143C", "#8B0000", "#FFD700", "#FFA500", "#FF4500", "#FF0000", "#DC143C", "#8B0000", "#FFD700", "#FFA500", "#FF4500", "#FF0000", "#DC143C", "#8B0000", "#FFD700", "#FFA500", "#FF4500", "#FF0000", "#DC143C", "#8B0000", "#FFD700", "#FFA500"],
        "colour_explanation": "Good colors for a `Light Summer` are soft and delicate hues such as soft blues, muted pinks, soft lavenders, and light grays, while bad colors are overly warm or intense tones like bright oranges, deep blacks, and overly saturated hues that can overpower the softness of the skin and hair tones. However, it's important to note that these are just guidelines, and you should ultimately wear whatever colors make you feel confident and beautiful!"
    },
    "Cool Summer": {
        "good_colours": ['#fdfdfd', '#336d78', '#b0bbd2', '#ae5a73', '#488a8a', '#eac3d4', '#5c4e4f', '#6eb2c1', '#d56f88', '#655d8c', '#f0e8e5', '#ddd4ce', '#9694bb', '#85b7d4', '#7e6c72', '#4e80a9', '#38604f', '#418a6c', '#8dbbad', '#b37e95', '#6f959c', '#f4f5c7', '#d98eab', '#e2dba8', '#c7dbe2', '#bcaeae', '#864d5c', '#37735b', '#675f63', '#e3f4f8'],
        "bad_colours": ["#FF4500", "#FF0000", "#DC143C", "#B22222", "#FF69B4", "#FF1493", "#FFC0CB", "#FFD700", "#FFA500", "#DAA520", "#B8860B", "#FF4500", "#FF0000", "#DC143C", "#B22222", "#FF69B4", "#FF1493", "#FFC0CB", "#FF69B4", "#FF1493", "#FFC0CB", "#FFD700", "#FFA500", "#DAA520", "#B8860B"],
        "colour_explanation": "Good colors for a `Cool Summer` are soft and cool tones such as soft blues, soft pinks, cool grays, and soft purples, while bad colors are warm or overly vibrant hues like warm oranges, bright yellows, and harsh blacks that can clash with the cool undertones of the skin and hair. However, it's important to note that these are just guidelines, and you should ultimately wear whatever colors make you feel confident and beautiful!"
    },
    "Soft Summer": {
        "good_colours": ['#fefefe', '#726863', '#c2bcbb', '#808d97', '#5c5250', '#e9e5e3', '#dca5a8', '#9a8d86', '#a59d9b', '#9e4e57', '#598497', '#cbced1', '#49635f', '#b5747f', '#e9c3c2', '#9196b2', '#423b3a', '#ccc5c0', '#a8bec7', '#908379', '#d98691', '#495063', '#676a82', '#f4f2f0', '#739d8d', '#7c7d79', '#b7aeae', '#627e98', '#d8dbdd', '#97b8ad'],
        "bad_colours": ["#FFA500", "#FF4500", "#8B0000", "#FF0000", "#DC143C", "#FFD700", "#FFA500", "#FF4500", "#8B0000", "#FF0000", "#DC143C", "#FFD700", "#FFA500", "#FF4500", "#8B0000", "#FF0000", "#DC143C", "#FFD700", "#6B8E23", "#556B2F", "#808000", "#2F4F4F", "#8B4513", "#A52A2A", "#800000", "#CD5C5C", "#FF0000", "#DC143C", "#B22222", "#FF6347", "#FF4500", "#FF8C00", "#FFA500", "#D2691E", "#FFA07A"],
        "colour_explanation": "Good colors for a `Soft Summer` are muted and cool tones such as soft blues, dusty roses, cool grays, and soft lavenders, while bad colors are overly warm or intense hues like bright oranges, warm reds, and harsh blacks that can overpower the softness of the skin and hair tones. However, it's important to note that these are just guidelines, and you should ultimately wear whatever colors make you feel confident and beautiful!"
    },
    "Bright Winter": {
         "good_colours": ['#272d5e', '#e3e5e1', '#8c5586', '#b1b4c2', '#3b3d41', '#617dbe', '#f9fafb', '#999c9a', '#d67db3', '#bc3b4e', '#626060', '#83b3d9', '#d1cfd9', '#1c1843', '#51a490', '#7a2b36', '#5e5594', '#ece6b2', '#de828b', '#c95770', '#8682b7', '#dcb1c1', '#465262', '#285148', '#bbe0dd', '#f3d5e6', '#582b48', '#304e96', '#151515', '#743664'],
        "bad_colours": ["#FFC0CB", "#FFA07A", "#FFDAB9", "#FFE4C4", "#FFDEAD", "#FFFF00", "#FFD700", "#FFA500", "#DAA520", "#B8860B", "#F0E68C", "#EEE8AA", "#F5DEB3", "#FFC0CB", "#FFA07A", "#FFDAB9", "#FFE4C4", "#FFDEAD", "#FFFF00", "#FFD700", "#FFA500", "#DAA520", "#B8860B", "#F0E68C", "#EEE8AA"],
        "colour_explanation": "Good colors for a `Bright Winter` are vibrant and bold hues such as true reds, electric blues, emerald greens, and hot pinks, while bad colors are soft or muted tones like pastels, earthy browns, and warm neutrals that can appear washed out against the strong contrast of the skin and hair. However, it's important to note that these are just guidelines, and you should ultimately wear whatever colors make you feel confident and beautiful!"
    },
    "Cool Winter": {
        "good_colours": ['#29335b', '#c2e7d2', '#8a5fa4', '#68c392', '#2c4891', '#d485a6', '#f1d8e3', '#3d835e', '#020202', '#7f7978', '#56a9c1', '#89aac6', '#a04172', '#633d7d', '#c0b2c6', '#f8f2ac', '#2b2425', '#e5e6e3', '#31678a', '#d6d6d3', '#faf9f9', '#eea5c7', '#5ab978', '#2f68b1', '#a3a09a', '#9bd3c9', '#493361', '#507d9d', '#a16ba9', '#e37197'],
        "bad_colours": ["#8B4513", "#A52A2A", "#CD5C5C", "#FF0000", "#DC143C", "#B22222", "#FF6347", "#FF4500", "#FF8C00", "#FFA500", "#D2691E", "#FFA07A", "#FF7F50", "#FF69B4", "#FFC0CB", "#FFDAB9", "#FFE4C4", "#FFDEAD", "#FFD700", "#FFA500"],
        "colour_explanation": "Good colors for a `Cool Winter` are jewel tones and icy shades such as sapphire blues, emerald greens, magenta pinks, and cool grays, while bad colors are warm or muted tones like earthy browns, warm oranges, and soft pastels that can clash with the cool undertones of the skin and hair. However, it's important to note that these are just guidelines, and you should ultimately wear whatever colors make you feel confident and beautiful!"
    },
    "Deep Winter": {
        "good_colours": ['#3d4c6c', '#debdc9', '#a69e96', '#361e47', '#89454d', '#fbfbfb', '#4e92a9', '#697949', '#161618', '#d05e81', '#f5eaa6', '#3c788c', '#544c51', '#93aa59', '#bacce0', '#8ea4b6', '#7597c6', '#3b609f', '#d1809a', '#706268', '#443136', '#ebece8', '#320b0f', '#887c7b', '#bcb2ad', '#bed5c6', '#d7d6d0', '#563842', '#2f505b', '#59693d'] ,
        "bad_colours": ["#87CEEB", "#87CEFA", "#00BFFF", "#1E90FF", "#6495ED", "#4682B4", "#5F9EA0", "#191970", "#4169E1", "#00CED1", "#20B2AA", "#008B8B", "#008080", "#00FFFF", "#008000", "#32CD32", "#00FF00", "#ADFF2F", "#7FFF00", "#FFFF00", "#FFD700", "#FFA500"],
        "colour_explanation": "Good colors for a `Deep Winter` are bold and rich shades such as deep blues, true reds, emerald greens, and royal purples, while bad colors are soft or muted tones like pastels, warm neutrals, and subdued hues that can appear washed out against the strong contrast of the skin and hair. However, it's important to note that these are just guidelines, and you should ultimately wear whatever colors make you feel confident and beautiful!"
    },
    "Soft Autumn": {
        "good_colours": ['#cca9a1', '#61554a', '#fdfdfc', '#b75e6b', '#24150f', '#6f7396', '#374d63', '#94b69f', '#f0d4a9', '#f1e5da', '#82919d', '#5c8c84', '#945050', '#d5dde1', '#43627f', '#4f3c33', '#d48883', '#9e7d6d', '#6e685a', '#b9c7c7', '#9fa6b8', '#9a9a82', '#4c5269', '#e4d1ca', '#36261e', '#eff0f0', '#a66763', '#ecd39a', '#415d56', '#d4bfb4'],
        "bad_colours": ["#4169E1", "#0000FF", "#00008B", "#000080", "#696969", "#808080", "#708090", "#A9A9A9", "#2F4F4F", "#D3D3D3", "#778899", "#B0C4DE", "#B0E0E6", "#ADD8E6", "#87CEEB", "#87CEFA", "#00BFFF", "#1E90FF", "#6495ED", "#4682B4", "#5F9EA0", "#191970", "#6A5ACD", "#483D8B", "#7B68EE"],
        "colour_explanation": "Good colors for a `Soft Autumn` are warm and muted shades such as soft olive greens, warm beiges, soft browns, and warm grays, while bad colors are overly cool or bright tones like deep blues, harsh blacks, and neon shades that can clash with the warm undertones of the skin and hair. However, it's important to note that these are just guidelines, and you should ultimately wear whatever colors make you feel confident and beautiful!"
    },
    "Deep Autumn": {
        "good_colours": ['#557065', '#f0e2d0', '#66411e', '#7a8783', '#091b32', '#8b351a', '#3e7897', '#91acb7', '#5e4c4e', '#243957', '#835569', '#95663d', '#f7f6f5', '#641e0c', '#311c0e', '#9e6482', '#b56024', '#aeb470', '#31566d', '#b09d9b', '#e6d2b7', '#d0c0ad', '#5597b3', '#b5cbd2', '#9c2835', '#214a38', '#dbdbdf', '#7c7b55', '#b38468', '#625e38'],
        "bad_colours": ["#87CEEB", "#87CEFA", "#00BFFF", "#1E90FF", "#6495ED", "#4682B4", "#5F9EA0", "#191970", "#4169E1", "#00CED1", "#20B2AA", "#008B8B", "#008080", "#00FFFF", "#00FFFF", "#008000", "#32CD32", "#00FF00", "#ADFF2F", "#7FFF00", "#ADFF2F", "#FFFF00", "#FFFF00", "#FFD700", "#FFA500"],
        "colour_explanation": "Good colors for a `Deep Autumn` include rich, warm tones like deep oranges, burgundies, olive greens, and mustard yellows, while bad colors are cool or pastel shades that may wash out the warm undertones. However, it's important to note that these are just guidelines, and you should ultimately wear whatever colors make you feel confident and beautiful!"
    },
    "Warm Autumn": {
        "good_colours": ['#e2dad3', '#614d3d', '#a58285', '#313e3f', '#eeece8', '#63768d', '#bab4a6', '#994a3f', '#466a69', '#9aa9b2', '#b76d70', '#485f3e', '#d9c4ba', '#adaa88', '#c9a88f', '#2c2b24', '#5e566e', '#c87b75', '#b66a59', '#6b9ead', '#d4c7a0', '#633531', '#7f6c62', '#7b3f47', '#fcfcfa', '#b99182', '#353e58', '#c3966f', '#d4d1c6', '#8c8f8d'],
        "bad_colours": ["#00FFFF", "#00FFFF", "#00CED1", "#20B2AA", "#008080", "#40E0D0", "#7FFFD4", "#AFEEEE", "#E0FFFF", "#B0E0E6", "#ADD8E6", "#B0C4DE", "#4682B4", "#87CEEB", "#87CEFA", "#6495ED", "#1E90FF", "#ADD8E6", "#B0C4DE", "#5F9EA0", "#00BFFF", "#87CEEB", "#4682B4", "#6495ED", "#4169E1"],
        "colour_explanation": "Good colors for a `Warm Autumn` include earthy tones like warm browns, rich oranges, deep reds, and olive greens, while bad colors are cool or pastel shades that may wash out the warm undertones. However, it's important to note that these are just guidelines, and you should ultimately wear whatever colors make you feel confident and beautiful!"
    }
}

# TODO: deal with white better except for deep / cool winter

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