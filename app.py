import streamlit as st
from PIL import Image
from pydub import AudioSegment
import io
from io import BytesIO

# Set theme to blue

def set_theme():
    """
    Sets the theme color to dark mode and makes background transparent with centered text.
    """
    # Inject CSS for a dark color scheme and transparent background with centered text
    main_bg = "rgba(0, 0, 0, 0)"  # Transparent background
    main_fg = "#FFFFFF"
    secondary_bg = "#343a40"
    secondary_fg = "#FFFFFF"
    accent_bg = "#6c757d"
    accent_fg = "#FFFFFF"

    st.markdown(
        f"""
        <style>
            .reportview-container .main .block-container{{
                color: {main_fg};
                background-color: {main_bg};
                text-align: center; /* Center-align text */
            }}
            .reportview-container .main {{
                color: {main_fg};
                background-color: {main_bg};
            }}
            .reportview-container .sidebar .block-container {{
                color: {secondary_fg};
                background-color: {secondary_bg};
            }}
            .reportview-container .sidebar {{
                color: {secondary_fg};
                background-color: {secondary_bg};
            }}
            .reportview-container .highlight .highlight {{
                background-color: {accent_bg};
            }}
            .reportview-container .markdown-text-container {{
                color: {main_fg};
                background-color: {main_bg};
                text-align: center; /* Center-align text */
            }}
            .element-container {{
                color: {main_fg};
                background-color: {main_bg};
            }}
            .streamlit-button {{
                color: {accent_fg};
                background-color: {accent_bg};
            }}
            .streamlit-button:hover {{
                background-color: {secondary_bg};
            }}
            .streamlit-button:disabled {{
                color: rgba(255,255,255,0.2);
                background-color: rgba(255,255,255,0.1);
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )


# Function to resize image


def resize_image(image, width, height):
    return image.resize((width, height))

# Function to compress audio


def compress_audio(audio_bytes, bitrate='192k'):
    audio = AudioSegment.from_file(BytesIO(audio_bytes))
    compressed_audio = audio.export(format="mp3", bitrate=bitrate)
    return compressed_audio

# Function to convert audio format


def convert_audio_format(audio_bytes, new_format='mp3'):
    audio = AudioSegment.from_file(BytesIO(audio_bytes))
    converted_audio = audio.export(format=new_format)
    return converted_audio

# Main function


def main():
    set_theme() 

    st.title("Resize Image - Compress Audio")
    st.markdown("""
    Resize Photos and Compress Audio Easily and Quickly
    """)
    st.markdown("Rifky Zaini Faroj")

    st.header("Image Resizer")
    image_file = st.file_uploader("Upload Image", type=['jpg', 'png', 'jpeg'])
    if image_file:
        image = Image.open(image_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        new_width = st.number_input("New Width", min_value=1)
        new_height = st.number_input("New Height", min_value=1)

        if st.button("Resize Image"):
            resized_image = resize_image(image, new_width, new_height)
            st.image(resized_image, caption="Resized Image",
                     use_column_width=True)

# Create a button to download the resized image

            img_bytes = io.BytesIO()
            resized_image.save(img_bytes, format='PNG')
            img_bytes.seek(0)
            st.download_button(label="Download Resized Image", data=img_bytes,
                               file_name="resized_image.png", mime="image/png")

    st.header("Audio Processor")
    uploaded_audio = st.file_uploader("Upload Audio File", type=["mp3", "wav"])
    if uploaded_audio is not None:
        st.write('Uploaded Audio File:', uploaded_audio.name)

        compression_options = ['128k', '192k', '256k', '320k', '384k', '448k']
        selected_compression = st.selectbox(
            "Select Compression Bitrate", compression_options)

        if st.button('Compress Audio'):
            compressed_audio = compress_audio(
                uploaded_audio.getvalue(), bitrate=selected_compression)
            compressed_audio_bytes = compressed_audio.read()

            st.audio(compressed_audio_bytes, format='audio/mp3', start_time=0)

            st.download_button(
                label="Download Compressed Audio",
                data=compressed_audio_bytes,
                file_name=f"compressed_audio_{selected_compression}.mp3",
                mime="audio/mp3"
            )
            st.success("Audio compressed successfully!")

        new_format = st.selectbox("Select New Format", ['mp3', 'wav'])
        if st.button("Convert Audio Format"):
            converted_audio = convert_audio_format(
                uploaded_audio.getvalue(), new_format)
            converted_audio_bytes = converted_audio.read()

            st.audio(converted_audio_bytes,
                     format=f'audio/{new_format}', start_time=0)

            st.download_button(
                label=f"Download Converted Audio ({new_format.upper()})",
                data=converted_audio_bytes,
                file_name=f"converted_audio.{new_format}",
                mime=f"audio/{new_format}"
            )
            st.success(
                f"Audio converted to {new_format.upper()} successfully!")


if __name__ == "__main__":
    main()
