
import streamlit as st
import requests

st.set_page_config(
    page_title="AI Language Translator",
    page_icon="🌐"
)

st.title("🌐 AI Language Translation Tool")
st.write("Translate text between different languages.")

languages = {
    "English": "en",
    "Hindi": "hi",
    "Telugu": "te",
    "Tamil": "ta",
    "French": "fr",
    "Spanish": "es",
    "German": "de"
}

col1, col2 = st.columns(2)

with col1:
    source = st.selectbox(
        "Source Language",
        list(languages.keys())
    )

with col2:
    target = st.selectbox(
        "Target Language",
        list(languages.keys()),
        index=1
    )

input_text = st.text_area(
    "Enter your text",
    placeholder="Type something to translate..."
)

if st.button("Translate", type="primary"):

    if not input_text.strip():
        st.warning("Please enter some text.")

    elif source == target:
        st.warning("Choose two different languages.")

    else:
        try:
            url = "https://api.mymemory.translated.net/get"

            params = {
                "q": input_text,
                "langpair": (
                    f"{languages[source]}|{languages[target]}"
                )
            }

            with st.spinner("Translating..."):
                response = requests.get(
                    url,
                    params=params,
                    timeout=20
                )

                response.raise_for_status()
                data = response.json()

            translated = data.get(
                "responseData", {}
            ).get("translatedText", "")

            if (
                data.get("responseStatus") == 200
                and translated
            ):
                st.subheader("Translation Result")

                st.text_area(
                    "Translated Text",
                    value=translated,
                    height=150
                )

            else:
                st.error("Translation failed. Try again.")

        except requests.RequestException:
            st.error(
                "Connection error. Check your internet connection."
            )

        except (ValueError, TypeError):
            st.error("Invalid response from translation service.")