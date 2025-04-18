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
trending_prompt = get_prompt()
trending_url = get_article(trending_prompt)
temp = combine(trending_prompt, trending_url)[:4090]


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

    
    spliter = str(response)[2:].split('+++++')
    response_title = spliter[0]
    response_rest = str(" ".join(spliter[1:])).strip('**').strip()
    temp_repr = """"""
    temp_list = spliter[1:]
    for item in temp_list:
        temp_repr += '<div data-aos="fade-up">'
        temp_repr += '<p class="p1">'
        temp_repr += item.strip('**').strip()
        temp_repr += '</p>'
        temp_repr += '</div>'
        temp_repr += '<br>'
    if temp_repr.endswith('<br>'):
        temp_repr = temp_repr[:len(temp_repr) - 4]
    
    response = input("Which category?")
    category = str(response).strip().lower()
    if category not in ['tv', 'music', 'tech', 'sports']:
        category = 'tv'

    images = get_images(trending_prompt)
    edited_list = """
            <li1><a href="../">Home</a></li1>
            <li><a href="../Pages/tech">Tech</a></li>
            <li><a href="../Pages/sports">Sports</a></li>
            <li><a href="../Pages/tv">TV</a></li>
            <li><a href="../Pages/music">Music</a></li>
            <li><a href="https://reindeer-blessed-adversely.ngrok-free.app/">Forums</a></li>"""
    header_url = '../Assets/header.png'
    b_pos = 'center'
    if category == 'tv':
        b_pos = '850px'
        header_url = '../Assets/tvheader.png'
        edited_list = """
            <li><a href="../">Home</a></li>
            <li><a href="../Pages/tech">Tech</a></li>
            <li><a href="../Pages/sports">Sports</a></li>
            <li1><a href="../Pages/tv">TV</a></li1>
            <li><a href="../Pages/music">Music</a></li>
            <li><a href="https://reindeer-blessed-adversely.ngrok-free.app/">Forums</a></li>"""
    elif category == 'tech':
        header_url = '../Assets/techheader.png'
        edited_list = """
            <li><a href="../">Home</a></li>
            <li1><a href="../Pages/tech">Tech</a></li1>
            <li><a href="../Pages/sports">Sports</a></li>
            <li><a href="../Pages/tv">TV</a></li>
            <li><a href="../Pages/music">Music</a></li>
            <li><a href="https://reindeer-blessed-adversely.ngrok-free.app/">Forums</a></li>"""
    elif category == 'sports':
        b_pos = '670px'
        header_url = '../Assets/sportsheader.png'
        edited_list = """
            <li><a href="../">Home</a></li>
            <li><a href="../Pages/tech">Tech</a></li>
            <li1><a href="../Pages/sports">Sports</a></li1>
            <li><a href="../Pages/tv">TV</a></li>
            <li><a href="../Pages/music">Music</a></li>
            <li><a href="https://reindeer-blessed-adversely.ngrok-free.app/">Forums</a></li>"""
    elif category == 'music':
        header_url = '../Assets/musicheader.png'
        edited_list = """
            <li><a href="../index">Home</a></li>
            <li><a href="../Pages/tech">Tech</a></li>
            <li><a href="../Pages/sports">Sports</a></li>
            <li><a href="../Pages/tv">TV</a></li>
            <li1><a href="../Pages/music">Music</a></li1>
            <li><a href="https://reindeer-blessed-adversely.ngrok-free.app/">Forums</a></li>"""

    final_html = "Articles/"
    final_html += f"{response_title.strip('%20 ')}.html"
    Func = open(final_html, "w")
    Func.write("""

<!DOCTYPE html>
<html lang="en">
<head>
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-B4F7KKQ08M"></script>
    <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());

    gtag('config', 'G-B4F7KKQ08M');
    </script>
    <script type="text/javascript"> //<![CDATA[ 
        var tlJsHost = ((window.location.protocol == "https:") ? "https://secure.trust-provider.com/" : "http://www.trustlogo.com/");
        document.write(unescape("%3Cscript src='" + tlJsHost + "trustlogo/javascript/trustlogo.js' type='text/javascript'%3E%3C/script%3E"));
        //]]>
    </script>
    <script async type="application/javascript"
            src="https://news.google.com/swg/js/v1/swg-basic.js"></script>
    <script>
      (self.SWG_BASIC = self.SWG_BASIC || []).push( basicSubscriptions => {
        basicSubscriptions.init({
          type: "NewsArticle",
          isPartOfType: ["Product"],
          isPartOfProductId: "CAow7-3aCw:openaccess",
          clientOptions: { theme: "light", lang: "en" },
        });
      });
    </script>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="You You News Trending Content">
    <meta name="author" content="Derek (Yue) Yu">
    <meta name="keywords" content="News, You You, Tech, Sports, TV, Music, Forum, Discussion">
    <title>You You News</title>
    <link rel="icon" type="image/x-icon" href="../Assets/youyounewslogo.png">
    <link rel="stylesheet" href="https://unpkg.com/aos@next/dist/aos.css" />
    <link href="https://fonts.googleapis.com/css?family=Baloo+2:400,800&display=swap" rel="stylesheet">
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
            --color-blue: #83af9b;
            --color-green: #c8c8a9;
            --color-brown: #774f38;
            --color-beige: #ece5ce;
            --color-yellow: #f9cdad;
            --color-pink: #fe4365;
        }
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            line-height: 1.6;
            background-color: var(--light-bg);
            color: var(--text-color);
            font-family: 'Times New Roman', serif;
        }
        #footerlink a {
            line-height: 1.6;
            color: var(--light-bg);
            font-family: 'Times New Roman', serif;
        }
        .container {
            width: 90%;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
               .p1 {
            font-size: 1.2em;
        }
        .shrinker {
            text-align: center;
            margin-right: 7vw;
            margin-left: 7vw;
            object-fit: cover;
        }
        .slider_image {
            width: 432px;
            height: 323px;
            object-fit: cover;
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
                url('""" + header_url + """');
            background-color: var(--primary-color);
            background-position-y: """ + b_pos + """;
            background-position-x: center;
            color: white;
            text-align: center;
            padding: 20px 0;
            font-family: 'Times New Roman', serif;
        }
        pre {
            font-family: 'Times New Roman', serif;
            padding: 20px;
            text-align: center;
            margin: auto;
            white-space: pre-wrap;
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
        nav ul li1 a {
            color: aquamarine;
            text-decoration: none;
            font-weight: 600;
            transition: color 0.3s ease;
            text-transform: uppercase;
            letter-spacing: 1px;
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
        .bbb {
            height: 50vh;
            margin: 0;
            display: grid;
            place-items: center;
            font: 2vw system-ui;
            background-color: var(--color-yellow);
        }

        .bbb a {
            transform: translatey(0px);
            animation: float 5s ease-in-out infinite;
            text-align: center;
            text-transform: uppercase;
            font-weight: bold;
            letter-spacing: 3px;
            font-size: 15px;
            color: var(--color-brown);
            background-color: var(--color-beige);
            padding: 50px;
            border-radius: 11px;
            position: relative;
            box-shadow: 20px 20px var(--color-blue);
            font-family: "Baloo 2", cursive;
            border: 1px solid var(--color-green);
        }
        .bbb a:after {
            transform: translatey(0px);
            animation: float2 5s ease-in-out infinite;
            content: ".";
            font-weight: bold;
            -webkit-text-stroke: 0.5px var(--color-green);
            -webkit-text-fill-color: var(--color-beige);
            border: 1px solid var(--color-green);
            text-shadow: 22px 22px var(--color-blue);
            text-align: left;
            font-size: 55px;
            width: 55px;
            height: 11px;
            line-height: 30px;
            border-radius: 11px;
            background-color: var(--color-beige);
            position: absolute;
            display: block;
            bottom: -30px;
            left: 0;
            box-shadow: 22px 22px var(--color-blue);
            z-index: -2;
        }
        @keyframes float {
            0% {
                transform: translatey(0px);
            }
            50% {
                transform: translatey(-20px);
            }
            100% {
                transform: translatey(0px);
            }
        }

        @keyframes float2 {
            0% {
                line-height: 30px;
                transform: translatey(0px);
            }
            55% {
                transform: translatey(-20px);
            }
            60% {
                line-height: 10px;
            }
            100% {
                line-height: 30px;
                transform: translatey(0px);
            }
        }
    </style>
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
        <h2>""" + str(response_title) + """</h2>
        <br>
        <div class="scroll-container">
            <img src='""" + str(images[0]) + """' alt="Cinque Terre" class="slider_image">
            <img src='""" + str(images[1]) + """' alt="Cinque Terre" class="slider_image">
            <img src='""" + str(images[2]) + """' alt="Cinque Terre" class="slider_image">
          </div>
        <pre>
        <p class="p1">""" + str(temp_repr) + """</p>
        </pre>
        </div>
        <div class="bbb"><a href="https://reindeer-blessed-adversely.ngrok-free.app/">Want to Join the Discussion?</a></div>
        <section style="margin-top: 40px;">
            <h2>Community Forums</h2>
            <div class="section-grid">
                <div data-aos="fade-up">
                    <div class="forum-section">
                        <h3>Tech Forum</h3>
                        <ul class="forum-list">
                            <li>
                                <a href="https://reindeer-blessed-adversely.ngrok-free.app/">Jensen Huang</a>
                                <span>245 discussions</span>
                            </li>
                            <li>
                                <a href="https://reindeer-blessed-adversely.ngrok-free.app/">deepseek vs openai</a>
                                <span>189 discussions</span>
                            </li>
                            <li>
                                <a href="https://reindeer-blessed-adversely.ngrok-free.app/">Programming Help</a>
                                <span>376 discussions</span>
                            </li>
                        </ul>
                    </div>
                </div>
                <div data-aos="fade-up">
                    <div class="forum-section">
                        <h3>Sports Forum</h3>
                        <ul class="forum-list">
                            <li>
                                <a href="https://reindeer-blessed-adversely.ngrok-free.app/">March Madness</a>
                                <span>512 discussions</span>
                            </li>
                            <li>
                                <a href="https://reindeer-blessed-adversely.ngrok-free.app/">Fantasy Football</a>
                                <span>287 discussions</span>
                            </li>
                            <li>
                                <a href="https://reindeer-blessed-adversely.ngrok-free.app/">Canucks vs Devils</a>
                                <span>203 discussions</span>
                            </li>
                        </ul>
                    </div>
                </div>
                <div data-aos="fade-up">
                    <div class="forum-section">
                        <h3>TV Forum</h3>
                        <ul class="forum-list">
                            <li>
                                <a href="https://reindeer-blessed-adversely.ngrok-free.app/">Grant Ellis: The Bachelor</a>
                                <span>421 discussions</span>
                            </li>
                            <li>
                                <a href="https://reindeer-blessed-adversely.ngrok-free.app/">Streaming Recommendations</a>
                                <span>356 discussions</span>
                            </li>
                            <li>
                                <a href="https://reindeer-blessed-adversely.ngrok-free.app/">TV Show Theories</a>
                                <span>278 discussions</span>
                            </li>
                        </ul>
                    </div>
                </div>
                <div data-aos="fade-up">
                    <div class="forum-section">
                        <h3>Music Forum</h3>
                        <ul class="forum-list">
                            <li>
                                <a href="https://reindeer-blessed-adversely.ngrok-free.app/">New Releases</a>
                                <span>332 discussions</span>
                            </li>
                            <li>
                                <a href="https://reindeer-blessed-adversely.ngrok-free.app/">Genre Discussions</a>
                                <span>245 discussions</span>
                            </li>
                            <li>
                                <a href="https://reindeer-blessed-adversely.ngrok-free.app/">Concert Experiences</a>
                                <span>167 discussions</span>
                            </li>
                        </ul>
                    </div>
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
    <script src="https://unpkg.com/aos@2.3.1/dist/aos.js"></script>
    <script>
        AOS.init();
        AOS.init({
        // Global settings:
        disable: false, // accepts following values: 'phone', 'tablet', 'mobile', boolean, expression or function
        startEvent: 'DOMContentLoaded', // name of the event dispatched on the document, that AOS should initialize on
        initClassName: 'aos-init', // class applied after initialization
        animatedClassName: 'aos-animate', // class applied on animation
        useClassNames: false, // if true, will add content of `data-aos` as classes on scroll
        disableMutationObserver: false, // disables automatic mutations' detections (advanced)
        debounceDelay: 50, // the delay on debounce used while resizing window (advanced)
        throttleDelay: 99, // the delay on throttle used while scrolling the page (advanced)
        

        // Settings that can be overridden on per-element basis, by `data-aos-*` attributes:
        offset: 120, // offset (in px) from the original trigger point
        delay: 0, // values from 0 to 3000, with step 50ms
        duration: 400, // values from 0 to 3000, with step 50ms
        easing: 'ease', // default easing for AOS animations
        once: false, // whether animation should happen only once - while scrolling down
        mirror: false, // whether elements should animate out while scrolling past them
        anchorPlacement: 'top-bottom', // defines which position of the element regarding to window should trigger the animation

        });
    </script>
</body>
</html>
""")
    Func.close()

    overall_text = """"""
    with open("index.html", "r") as f0:
        overall_text = f0.read()

    with open("index.html", "w") as f:
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
                    <p>""" + str(" ".join(response_rest.split(" ")[:14])) + "..." + """</p>
                    <a href=""" + '"' + final_html + '"' + """ class="cta-button">Read Now!</a>
                </div>
            </article>
        </div>
        <div data-aos="fade-up">
            <article class="section-card">
            <"""
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
            " alt="Sports Blog">
                <div class="section-content">
                    <h2>""" + str(response_title).strip("%20") + """</h2>
                    <p>""" + str(" ".join(response_rest.split(" ")[:14])) + "..." + """</p>
                    <a href=""" + '"' + final_html + '"' + """ class="cta-button">Read Now!</a>
                </div>
            </article>
        </div>
        <div data-aos="fade-up">
            <article class="section-card">
                <"""
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
            " alt="Music Blog">
                <div class="section-content">
                    <h2>""" + str(response_title).strip("%20") + """</h2>
                    <p>""" + str(" ".join(response_rest.split(" ")[:14])) + "..." + """</p>
                    <a href=""" + '"' + final_html + '"' + """ class="cta-button">Read Now!</a>
                </div>
            </article>
        </div>
    </div>
    </section>
        <div class="bbb"><a href="https://reindeer-blessed-adversely.ngrok-free.app/">Want to Join the Discussion?</a></div>
        <section style="margin-top: 40px;">
            <h2>Community Forums</h2>
            <div class="section-grid">
                <div data-aos="fade-up">
                    <div class="forum-section">
                        <h3>Tech Forum</h3>
                        <ul class="forum-list">
                            <li>
                                <a href="https://reindeer-blessed-adversely.ngrok-free.app/">Jensen Huang</a>
                                <span>245 discussions</span>
                            </li>
                            <li>
                                <a href="https://reindeer-blessed-adversely.ngrok-free.app/">deepseek vs openai</a>
                                <span>189 discussions</span>
                            </li>
                            <li>
                                <a href="https://reindeer-blessed-adversely.ngrok-free.app/">Programming Help</a>
                                <span>376 discussions</span>
                            </li>
                        </ul>
                    </div>
                </div>
                <div data-aos="fade-up">
                    <div class="forum-section">
                        <h3>Sports Forum</h3>
                        <ul class="forum-list">
                            <li>
                                <a href="https://reindeer-blessed-adversely.ngrok-free.app/">March Madness</a>
                                <span>512 discussions</span>
                            </li>
                            <li>
                                <a href="https://reindeer-blessed-adversely.ngrok-free.app/">Fantasy Football</a>
                                <span>287 discussions</span>
                            </li>
                            <li>
                                <a href="https://reindeer-blessed-adversely.ngrok-free.app/">Canucks vs Devils</a>
                                <span>203 discussions</span>
                            </li>
                        </ul>
                    </div>
                </div>
                <div data-aos="fade-up">
                    <div class="forum-section">
                        <h3>TV Forum</h3>
                        <ul class="forum-list">
                            <li>
                                <a href="https://reindeer-blessed-adversely.ngrok-free.app/">Grant Ellis: The Bachelor</a>
                                <span>421 discussions</span>
                            </li>
                            <li>
                                <a href="https://reindeer-blessed-adversely.ngrok-free.app/">Streaming Recommendations</a>
                                <span>356 discussions</span>
                            </li>
                            <li>
                                <a href="https://reindeer-blessed-adversely.ngrok-free.app/">TV Show Theories</a>
                                <span>278 discussions</span>
                            </li>
                        </ul>
                    </div>
                </div>
                <div data-aos="fade-up">
                    <div class="forum-section">
                        <h3>Music Forum</h3>
                        <ul class="forum-list">
                            <li>
                                <a href="https://reindeer-blessed-adversely.ngrok-free.app/">New Releases</a>
                                <span>332 discussions</span>
                            </li>
                            <li>
                                <a href="https://reindeer-blessed-adversely.ngrok-free.app/">Genre Discussions</a>
                                <span>245 discussions</span>
                            </li>
                            <li>
                                <a href="https://reindeer-blessed-adversely.ngrok-free.app/">Concert Experiences</a>
                                <span>167 discussions</span>
                            </li>
                        </ul>
                    </div>
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
    <script src="https://unpkg.com/aos@2.3.1/dist/aos.js"></script>
    <script>
        AOS.init();
        AOS.init({
        // Global settings:
        disable: false, // accepts following values: 'phone', 'tablet', 'mobile', boolean, expression or function
        startEvent: 'DOMContentLoaded', // name of the event dispatched on the document, that AOS should initialize on
        initClassName: 'aos-init', // class applied after initialization
        animatedClassName: 'aos-animate', // class applied on animation
        useClassNames: false, // if true, will add content of `data-aos` as classes on scroll
        disableMutationObserver: false, // disables automatic mutations' detections (advanced)
        debounceDelay: 50, // the delay on debounce used while resizing window (advanced)
        throttleDelay: 99, // the delay on throttle used while scrolling the page (advanced)
        

        // Settings that can be overridden on per-element basis, by `data-aos-*` attributes:
        offset: 120, // offset (in px) from the original trigger point
        delay: 0, // values from 0 to 3000, with step 50ms
        duration: 400, // values from 0 to 3000, with step 50ms
        easing: 'ease', // default easing for AOS animations
        once: false, // whether animation should happen only once - while scrolling down
        mirror: false, // whether elements should animate out while scrolling past them
        anchorPlacement: 'top-bottom', // defines which position of the element regarding to window should trigger the animation

        });
    </script>
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
            " alt="Tech Blog">
                <div class="section-content">
                    <h2>""" + str(response_title).strip("%20") + """</h2>
                    <p>""" + str(" ".join(response_rest.split(" ")[:14])) + "..." + """</p>
                    <a href=""" + '"' + final_html + '"' + """ class="cta-button">Read Now!</a>
                </div>
            </article>
        </div>
        <div data-aos="fade-up">
            <article class="section-card">
                <"""
            for i in range(2, len(img_src_split)):
                final += "img src="
                final += img_src_split[i]
        f.write(final)


if __name__ == '__main__':
    st.session_state['openai_api_key'] = ''

    if 'openai_api_key' in st.session_state and st.session_state.openai_api_key:
        main()
