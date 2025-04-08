from pathlib import Path
from seleniumdrivers import get_prompt, get_images, get_article, combine

import streamlit as st
from openai import OpenAI
import json
import os
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--disable-blink-features=AutomationControlled')

DB_FILE = 'db.json'
THIS_DIR = Path(__file__).parent if "__file__" in locals() else Path.cwd()
CSS_FILE = THIS_DIR / "Styles" / "main.css"
trending_prompt = get_prompt()
trending_url = get_article(trending_prompt)
temp = combine(trending_prompt, trending_url)[:4090]


def load_css_file(css_file_path):
    with open(css_file_path) as f:
        return st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


load_css_file(CSS_FILE)


def main():
    client = OpenAI(api_key=st.session_state.openai_api_key)

    # List of models
    models = ["gpt-4o-mini", "gpt-4o", "gpt-4-turbo", "gpt-4", "gpt-3.5-turbo"]

    # Create a select box for the models
    st.session_state["openai_model"] = st.sidebar.selectbox("Select OpenAI model", models, index=0)
    st.session_state["tone"] = st.sidebar.selectbox("Customize my tone!", ('Normal', 'Philosophical', 'OUTRAGEOUSLY FUNNY!', 'Depressed :('))
    st.session_state["lang"] = st.sidebar.selectbox("Language", ('English', 'Chinese (Mandarin)', 'Korean', 'French'))

    # Load chat history from db.json
    with open(DB_FILE, 'r') as file:
        db = json.load(file)
    st.session_state.messages = db.get('chat_history', [])


    # Add a "Clear Chat" button to the sidebar
    if st.sidebar.button('Clear Chat'):
        # Clear chat history in db.json
        db['chat_history'] = []
        with open(DB_FILE, 'w') as file:
            json.dump(db, file)
        # Clear chat messages in session state
        st.session_state.messages = []
        st.rerun()
    
    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])



    st.session_state.messages.append({"role": "user", "content": temp})
    with st.chat_message("user"):
            st.markdown(temp)
    with st.chat_message("assistant"):
        tone=st.session_state["tone"]
        lang=st.session_state["lang"]
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
    db['chat_history'] = st.session_state.messages
    with open(DB_FILE, 'w') as file:
        json.dump(db, file)

    
    spliter = str(response)[2:].split('**')
    response_title = spliter[0]
    response_rest = str(response[2 + len(response_title):]).strip()

    new_temp = "Which of these four categories is this topic closest to: music, tv, tech, or sports? Reply with one word."
    st.session_state.messages.append({"role": "user", "content": new_temp})
    with st.chat_message("user"):
            st.markdown(new_temp)
    with st.chat_message("assistant"):
        tone=st.session_state["tone"]
        lang=st.session_state["lang"]
        stream = client.chat.completions.create(
            model=st.session_state["openai_model"],
            messages=[
                {"role": m["role"], "content": m["content"]}
                for m in st.session_state.messages
            ],
            stream=True,
        )
        response = st.write_stream(stream)
    st.session_state.messages.append({"role": "assistant", "content": response})
    db['chat_history'] = st.session_state.messages
    with open(DB_FILE, 'w') as file:
        json.dump(db, file)
    
    category = str(response).strip().lower()
    if category not in ['tv', 'music', 'tech', 'sports']:
        category = 'tv'

    images = get_images(temp.split(":")[1])
    edited_list = """
            <li1><a href="../index.html">Home</a></li1>
            <li><a href="../Pages/tech.html">Tech</a></li>
            <li><a href="../Pages/sports.html">Sports</a></li>
            <li><a href="../Pages/tv.html">TV</a></li>
            <li><a href="../Pages/music.html">Music</a></li>
            <li><a href="../Pages/forums.html">Forums</a></li>"""
    if category == 'tv':
        edited_list = """
            <li><a href="../index.html">Home</a></li>
            <li><a href="../Pages/tech.html">Tech</a></li>
            <li><a href="../Pages/sports.html">Sports</a></li>
            <li1><a href="../Pages/tv.html">TV</a></li1>
            <li><a href="../Pages/music.html">Music</a></li>
            <li><a href="../Pages/forums.html">Forums</a></li>"""
    elif category == 'tech':
        edited_list = """
            <li><a href="../index.html">Home</a></li>
            <li1><a href="../Pages/tech.html">Tech</a></li1>
            <li><a href="../Pages/sports.html">Sports</a></li>
            <li><a href="../Pages/tv.html">TV</a></li>
            <li><a href="../Pages/music.html">Music</a></li>
            <li><a href="../Pages/forums.html">Forums</a></li>"""
    elif category == 'sports':
        edited_list = """
            <li><a href="../index.html">Home</a></li>
            <li><a href="../Pages/tech.html">Tech</a></li>
            <li1><a href="../Pages/sports.html">Sports</a></li1>
            <li><a href="../Pages/tv.html">TV</a></li>
            <li><a href="../Pages/music.html">Music</a></li>
            <li><a href="../Pages/forums.html">Forums</a></li>"""
    elif category == 'music':
        edited_list = """
            <li><a href="../index.html">Home</a></li>
            <li><a href="../Pages/tech.html">Tech</a></li>
            <li><a href="../Pages/sports.html">Sports</a></li>
            <li><a href="../Pages/tv.html">TV</a></li>
            <li1><a href="../Pages/music.html">Music</a></li1>
            <li><a href="../Pages/forums.html">Forums</a></li>"""

    final_html = "Archive/"
    final_html += f"{response_title.strip('%20 ')}.html"
    Func = open(final_html, "w")
    Func.write("""

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>You You News - By You, For You!</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        :root {
            --primary-color: #2c3e50;
            --secondary-color: #3498db;
            --light-bg: #f4f4f8;
            --text-color: #333;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            line-height: 1.6;
            background-color: var(--light-bg);
            color: var(--text-color);
            font-family: 'Times New Roman', serif;
        }
        .container {
            width: 90%;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        .p1 {
            font-size: 1.5em;
        }
        .shrinker {
            margin-right: 120px;
            margin-left: 120px;
        }
        .slider_image {
            max-width: 352px;
            max-height: 198px;
            min-width: 352px;
            min-height: 198px;
            overflow: hidden;
            image-rendering: high-quality;
            image-resolution: 300dpi;
        }
        div.scroll-container {
        background-color: #333;
        overflow: auto;
        white-space: nowrap;
        padding: 1px;
        }
        div.scroll-container img {
            padding: 1px;
        }      
        header {
            background:
                /* top, transparent black, faked with gradient */ 
                linear-gradient(
                    rgba(0, 0, 0, 0.7), 
                    rgba(0, 0, 0, 0.7)
                ),
                /* bottom, image */
                url('https://cdn.tinybuddha.com/wp-content/uploads/2015/05/Couple-on-the-Beach-Painting.jpg');
            background-color: var(--primary-color);
            background-position-y: center;
            background-position-x: center;
            color: white;
            text-align: center;
            padding: 20px 0;
            font-family: 'Times New Roman', serif;
        }
        header h1 {
            font-size: 2.5em;
            letter-spacing: -1px;
        }
        nav {
            background-color: #34495e;
            padding: 10px 0;
        }
        nav ul {
            display: flex;
            justify-content: center;
            list-style: none;
        }
        nav ul li {
            margin: 0 15px;
        }
        nav ul li1 {
            margin: 0 15px;
        }
        nav ul li a {
            color: white;
            text-decoration: none;
            font-weight: 600;
            transition: color 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        nav ul li a:hover {
            color: var(--secondary-color);
        }
        nav ul li1 a {
            color: aquamarine;
            text-decoration: none;
            font-weight: 600;
            transition: color 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        nav ul li1 a:hover {
            color: white;
        }
        .section-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-top: 30px;
        }
        .section-card {
            background-color: white;
            border-radius: 8px;
            overflow: hidden;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            transition: transform 0.3s ease;
        }
        .section-card:hover {
            transform: scale(1.03);
        }
        .section-card img {
            width: 100%;
            height: 250px;
            object-fit: cover;
        }
        .section-content {
            padding: 15px;
        }
        .section-content h2 {
            margin-bottom: 10px;
            font-size: 1.3em;
            color: var(--primary-color);
        }
        .section-content p {
            color: #666;
        }
        .forum-section {
            background-color: white;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        .forum-list {
            list-style-type: none;
        }
        .forum-list li {
            padding: 10px;
            border-bottom: 1px solid #f1f1f1;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .forum-list li:last-child {
            border-bottom: none;
        }
        .forum-list li a {
            color: var(--primary-color);
            text-decoration: none;
            font-weight: 600;
        }
        .forum-list li span {
            color: #666;
            font-size: 0.9em;
        }
        footer {
            background-color: var(--primary-color);
            color: white;
            text-align: center;
            padding: 20px 0;
            margin-top: 30px;
        }
        .cta-button {
            display: inline-block;
            background-color: var(--secondary-color);
            color: white;
            padding: 10px 20px;
            border-radius: 5px;
            text-decoration: none;
            margin-top: 15px;
            transition: background-color 0.3s ease;
        }
        .cta-button:hover {
            background-color: #2980b9;
        }
    </style>
<script type="text/javascript"> //<![CDATA[ 
    var tlJsHost = ((window.location.protocol == "https:") ? "https://secure.trust-provider.com/" : "http://www.trustlogo.com/");
    document.write(unescape("%3Cscript src='" + tlJsHost + "trustlogo/javascript/trustlogo.js' type='text/javascript'%3E%3C/script%3E"));
    //]]>
</script>
</head>
<body>
    <header>
        <div class="container">
            <h1>You You News</h1>
            <p>Your Ultimate Source for Trending Content</p>
        </div>
    </header>
    <nav>
        <ul>""" + edited_list +
        """</ul>
    </nav>
    <div class="container">
        <div class="shrinker">
        <div class="scroll-container">
            <img src='""" + str(images[0]) + """' alt="Cinque Terre" class="slider_image">
            <img src='""" + str(images[1]) + """' alt="Cinque Terre" class="slider_image">
            <img src='""" + str(images[2]) + """' alt="Cinque Terre" class="slider_image">
          </div>
        <br>
        <h2>""" + str(response_title) + """</h2>
        <p class="p1">""" + str(response_rest) + """</p>
        </div>
        <section style="margin-top: 40px;">
            <h2>Community Forums</h2>
            <div class="section-grid">
                <div class="forum-section">
                    <h3>Tech Forum</h3>
                    <ul class="forum-list">
                        <li>
                            <a href="#">Jensen Huang</a>
                            <span>245 discussions</span>
                        </li>
                        <li>
                            <a href="#">deepseek vs openai</a>
                            <span>189 discussions</span>
                        </li>
                        <li>
                            <a href="#">Programming Help</a>
                            <span>376 discussions</span>
                        </li>
                    </ul>
                </div>
                <div class="forum-section">
                    <h3>Sports Forum</h3>
                    <ul class="forum-list">
                        <li>
                            <a href="#">March Madness</a>
                            <span>512 discussions</span>
                        </li>
                        <li>
                            <a href="#">Fantasy Football</a>
                            <span>287 discussions</span>
                        </li>
                        <li>
                            <a href="#">Canucks vs Devils</a>
                            <span>203 discussions</span>
                        </li>
                    </ul>
                </div>
                <div class="forum-section">
                    <h3>TV Forum</h3>
                    <ul class="forum-list">
                        <li>
                            <a href="#">Grant Ellis: The Bachelor</a>
                            <span>421 discussions</span>
                        </li>
                        <li>
                            <a href="#">Streaming Recommendations</a>
                            <span>356 discussions</span>
                        </li>
                        <li>
                            <a href="#">TV Show Theories</a>
                            <span>278 discussions</span>
                        </li>
                    </ul>
                </div>
                <div class="forum-section">
                    <h3>Music Forum</h3>
                    <ul class="forum-list">
                        <li>
                            <a href="#">New Releases</a>
                            <span>332 discussions</span>
                        </li>
                        <li>
                            <a href="#">Genre Discussions</a>
                            <span>245 discussions</span>
                        </li>
                        <li>
                            <a href="#">Concert Experiences</a>
                            <span>167 discussions</span>
                        </li>
                    </ul>
                </div>
            </div>
        </section>
    </div>
    <footer>
        <div class="container">
            <p>&copy; 2025 You You News. All Rights Reserved.</p>
            <p>Connect with us on social media</p>
            <img src="../Assets/sectigo_trust_seal_md_106x42.png" alt="Verified Logo">
        </div>
    </footer>
</body>
</html>
""")
    Func.close()
    print("func written")

    with open("index.html", "w") as f:
        overall_text = f.read()
        img_src_split = overall_text.split("img src=")
        final = """"""
        if category == 'tv':
            for i in range(3):
                final += img_src_split[i]
                final += "img src="
            final += '"'
            final += str(images[0])
            final += """
            " alt="TV Blog">
            <div class="section-content">
                    <h2>""" + str(response_title).strip("%20") + """</h2>
                    <p>""" + str(" ".join(response_rest.split(" ")[:16])) + """</p>
                    <a href=""" + '"' + final_html + '"' + """ class="cta-button">Read More</a>
                </div>
            </article>
            <article class="section-card">
                <
            """
            for i in range(4, len(img_src_split)):
                final += "img src="
                final += img_src_split[i]
        elif category == 'sports':
            for i in range(2):
                final += img_src_split[i]
                final += "img src="
            final += '"'
            final += str(images[0])
            final += """
            " alt="TV Blog">
            <div class="section-content">
                    <h2>""" + str(response_title).strip("%20") + """</h2>
                    <p>""" + str(" ".join(response_rest.split(" ")[:16])) + """</p>
                    <a href=""" + '"' + final_html + '"' + """ class="cta-button">Read More</a>
                </div>
            </article>
            <article class="section-card">
                <
            """
            for i in range(3, len(img_src_split)):
                final += "img src="
                final += img_src_split[i]
        elif category == 'music':
            for i in range(4):
                final += img_src_split[i]
                final += "img src="
            final += '"'
            final += str(images[0])
            final += """
            " alt="TV Blog">
            <div class="section-content">
                    <h2>""" + str(response_title).strip("%20") + """</h2>
                    <p>""" + str(" ".join(response_rest.split(" ")[:16])) + """</p>
                    <a href=""" + '"' + final_html + '"' + """ class="cta-button">Read More</a>
                </div>
            </article>
            </div>
        </section>

        <section style="margin-top: 40px;">
            <h2>Community Forums</h2>
            <div class="section-grid">
                <div class="forum-section">
                    <h3>Tech Forum</h3>
                    <ul class="forum-list">
                        <li>
                            <a href="#">Jensen Huang</a>
                            <span>245 discussions</span>
                        </li>
                        <li>
                            <a href="#">deepseek vs openai</a>
                            <span>189 discussions</span>
                        </li>
                        <li>
                            <a href="#">Programming Help</a>
                            <span>376 discussions</span>
                        </li>
                    </ul>
                </div>
                <div class="forum-section">
                    <h3>Sports Forum</h3>
                    <ul class="forum-list">
                        <li>
                            <a href="#">March Madness</a>
                            <span>512 discussions</span>
                        </li>
                        <li>
                            <a href="#">Fantasy Football</a>
                            <span>287 discussions</span>
                        </li>
                        <li>
                            <a href="#">Canucks vs Devils</a>
                            <span>203 discussions</span>
                        </li>
                    </ul>
                </div>
                <div class="forum-section">
                    <h3>TV Forum</h3>
                    <ul class="forum-list">
                        <li>
                            <a href="#">Grant Ellis: The Bachelor</a>
                            <span>421 discussions</span>
                        </li>
                        <li>
                            <a href="#">Streaming Recommendations</a>
                            <span>356 discussions</span>
                        </li>
                        <li>
                            <a href="#">TV Show Theories</a>
                            <span>278 discussions</span>
                        </li>
                    </ul>
                </div>
                <div class="forum-section">
                    <h3>Music Forum</h3>
                    <ul class="forum-list">
                        <li>
                            <a href="#">New Releases</a>
                            <span>332 discussions</span>
                        </li>
                        <li>
                            <a href="#">Genre Discussions</a>
                            <span>245 discussions</span>
                        </li>
                        <li>
                            <a href="#">Concert Experiences</a>
                            <span>167 discussions</span>
                        </li>
                    </ul>
                </div>
            </div>
        </section>
    </div>

    <footer>
        <div class="container">
            <p>&copy; 2025 You You News. All Rights Reserved.</p>
            <p>Connect with us on social media</p>
            <div id="footerlink">
                <a href="/Terms_and_Conditions/terms_of_service.html">Terms of Service</a>
            </div>
            <br>
            <img src="../Assets/sectigo_trust_seal_md_106x42.png" alt="Verified Logo">
        </div>
    </footer>
</body>
</html>
            """
        else:
            for i in range(1):
                final += img_src_split[i]
                final += "img src="
            final += '"'
            final += str(images[0])
            final += """
            " alt="TV Blog">
            <div class="section-content">
                    <h2>""" + str(response_title).strip("%20") + """</h2>
                    <p>""" + str(" ".join(response_rest.split(" ")[:16])) + """</p>
                    <a href=""" + '"' + final_html + '"' + """ class="cta-button">Read More</a>
                </div>
            </article>
            <article class="section-card">
                <
            """
            for i in range(2, len(img_src_split)):
                final += "img src="
                final += img_src_split[i]
        f.write(final)
    # Find the RELEVANT img src AND href
    # Replace it with the new ones
    # TODO: the home page can teach me how to limit images






    # Accept user input
    # if prompt := st.chat_input("Tell me a fact! (ex. I will eat tacos every day)"):
    #     # Add user message to chat history
    #     print(temp)
    #     st.session_state.messages.append({"role": "user", "content": temp})
    #     # Display user message in chat message container
    #     with st.chat_message("user"):
    #         st.markdown(temp)

    #     # Display assistant response in chat message container
    #     with st.chat_message("assistant"):
    #         tone=st.session_state["tone"]
    #         lang=st.session_state["lang"]
    #         stream = client.chat.completions.create(
    #             model=st.session_state["openai_model"],
    #             messages=[
    #                 {"role": m["role"], "content": m["content"]}
    #                 for m in st.session_state.messages
    #             ],
    #             stream=True,
    #         )
    #         response = st.write_stream(stream)
    #     st.session_state.messages.append({"role": "assistant", "content": response})

    #     # Store chat history to db.json
    #     db['chat_history'] = st.session_state.messages
    #     with open(DB_FILE, 'w') as file:
    #         json.dump(db, file)


if __name__ == '__main__':
    st.session_state['openai_api_key'] = ''

    if 'openai_api_key' in st.session_state and st.session_state.openai_api_key:
        main()
    
    else:

        # if the DB_FILE not exists, create it
        if not os.path.exists(DB_FILE):
            with open(DB_FILE, 'w') as file:
                db = {
                    'openai_api_keys': [],
                    'chat_history': []
                }
                json.dump(db, file)
        # load the database
        else:
            with open(DB_FILE, 'r') as file:
                db = json.load(file)

        # display the selectbox from db['openai_api_keys']
        selected_key = st.selectbox(
            label = "Existing OpenAI API Keys", 
            options = db['openai_api_keys']
        )

        # a text input box for entering a new key
        new_key = st.text_input(
            label="New OpenAI API Key", 
            type="password"
        )

        login = st.button("Login")

        # if new_key is given, add it to db['openai_api_keys']
        # if new_key is not given, use the selected_key
        if login:
            if new_key:
                db['openai_api_keys'].append(new_key)
                with open(DB_FILE, 'w') as file:
                    json.dump(db, file)
                st.success("Key saved successfully.")
                st.session_state['openai_api_key'] = new_key
                st.rerun()
            else:
                if selected_key:
                    st.success(f"Logged in with key '{selected_key}'")
                    st.session_state['openai_api_key'] = selected_key
                    st.rerun()
                else:
                    st.error("API Key is required to login")
