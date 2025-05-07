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
temp = combine(trending_prompt, trending_url)[:4080]


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
    response_title = spliter[0].strip('*').strip('*').strip()
    while response_title.startswith('<') or response_title.startswith('>') or response_title.startswith('/'):
        response_title = response_title[1:]
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
            <li><a href="/Pages/working">Forums</a></li>"""
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
            <li><a href="/Pages/working">Forums</a></li>"""
    elif category == 'tech':
        header_url = '../Assets/techheader.png'
        edited_list = """
            <li><a href="../">Home</a></li>
            <li1><a href="../Pages/tech">Tech</a></li1>
            <li><a href="../Pages/sports">Sports</a></li>
            <li><a href="../Pages/tv">TV</a></li>
            <li><a href="../Pages/music">Music</a></li>
            <li><a href="/Pages/working">Forums</a></li>"""
    elif category == 'sports':
        b_pos = '670px'
        header_url = '../Assets/sportsheader.png'
        edited_list = """
            <li><a href="../">Home</a></li>
            <li><a href="../Pages/tech">Tech</a></li>
            <li1><a href="../Pages/sports">Sports</a></li1>
            <li><a href="../Pages/tv">TV</a></li>
            <li><a href="../Pages/music">Music</a></li>
            <li><a href="/Pages/working">Forums</a></li>"""
    elif category == 'music':
        header_url = '../Assets/musicheader.png'
        edited_list = """
            <li><a href="../index">Home</a></li>
            <li><a href="../Pages/tech">Tech</a></li>
            <li><a href="../Pages/sports">Sports</a></li>
            <li><a href="../Pages/tv">TV</a></li>
            <li1><a href="../Pages/music">Music</a></li1>
            <li><a href="/Pages/working">Forums</a></li>"""

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
    <title>""" + str(response_title) + """ - You You News</title>
    <link rel="icon" type="image/x-icon" href="../Assets/youyounewslogo.png">
    <link rel="stylesheet" href="https://unpkg.com/aos@next/dist/aos.css" />
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
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
            margin: 0 min(15px, 1.4vw);
            font-size: min(16px, 3vw);
        }
        nav ul li1 {
            margin: 0 min(15px, 1.4vw);
            font-size: min(16px, 3vw);
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
        .fa {
        font-size: 30px;
        width: 60px;
        text-align: center;
        text-decoration: none;
        color: var(--color-pink);
        background-position: center;
        background-color: var(--color-blue);
        border-radius: 50%;
        }

        /* Add a hover effect if you want */
        .fa:hover {
        opacity: 0.7;
        width: 80px;
        background-color:#A6FFB9
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
        /* Glowing animation */
@keyframes glow {
  0% {
    box-shadow: 0 0 10px #ffcb6b, 0 0 20px #ffc107, 0 0 30px #ff9800;
    transform: scale(1);
  }
  50% {
    box-shadow: 0 0 30px #ffcb6b, 0 0 50px #ffc107, 0 0 80px #ff5722;
    transform: scale(1.05);
  }
  100% {
    box-shadow: 0 0 10px #ffcb6b, 0 0 20px #ffc107, 0 0 30px #ff9800;
    transform: scale(1);
  }
}

.glow-reward {
  animation: glow 1.2s ease-in-out infinite;
  border: 2px solid #ffc107 !important;
  background-color: #fff3cd !important;
  color: #d35400 !important;
  text-shadow: 0 0 3px #fff;
}
#closePopupButton:hover {
  background-color: #ff9800;
  color: white;
  transform: scale(1.05);
}
@keyframes subtlePulse {
  0% {
    transform: scale(1);
    opacity: 1;
  }
  50% {
    transform: scale(1.03);
    opacity: 0.85;
  }
  100% {
    transform: scale(1);
    opacity: 1;
  }
}

.pulse-soft {
  animation: subtlePulse 2.5s ease-in-out infinite;
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
            <p>Making News Fun 4 U!</p>
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
        <section style="margin-top: 40px;">
        <h2 style="color: var(--color-brown); font-family: 'Baloo 2', cursive, sans-serif; letter-spacing: 1px;">Yesterday's Top Google Trends</h2>
        <div class="slideshow-container" style="background-color: var(--color-beige); border-radius: 11px; padding: 20px; box-shadow: 10px 10px var(--color-blue); position: relative; height: 400px; overflow: hidden; border: 1px solid var(--color-green);">
            <!-- Slides -->
            <div class="trend-slide" style="position: absolute; width: 100%; height: 100%; opacity: 1; transition: opacity 1s ease-in-out;">
                <h3 style="color: var(--color-brown); margin-bottom: 15px; font-family: 'Baloo 2', cursive, sans-serif;">1. Coachella Livestream</h3>
                <div class="trend-content" style="display: flex; flex-direction: column; align-items: center;">
                    <div class="trend-graph" style="width: 90%; height: 250px; margin-bottom: 15px; position: relative;">
                        <div style="position: absolute; bottom: 0; left: 0; width: 100%; height: 1px; background-color: var(--color-green); opacity: 0.3;"></div>
                        <div style="position: absolute; left: 0; bottom: 0; width: 1px; height: 100%; background-color: var(--color-green); opacity: 0.3;"></div>
                        <!-- Graph line -->
                        <svg width="100%" height="100%" viewBox="0 0 1000 250" preserveAspectRatio="none">
                            <path d="M0,250 L100,200 L200,220 L300,150 L400,180 L500,100 L600,50 L700,20 L800,10 L900,5 L1000,0" stroke="var(--color-blue)" stroke-width="3" fill="none" />
                            <path d="M0,250 L100,200 L200,220 L300,150 L400,180 L500,100 L600,50 L700,20 L800,10 L900,5 L1000,0 L1000,250 L0,250" fill="var(--color-blue)" fill-opacity="0.1" />
                        </svg>
                    </div>
                    <p style="text-align: center; color: var(--color-brown); font-family: 'Baloo 2', cursive, sans-serif;">Interest spiked yesterday as fans searched for ways to watch performances live online</p>
                </div>
            </div>
    
            <div class="trend-slide" style="position: absolute; width: 100%; height: 100%; opacity: 0; transition: opacity 1s ease-in-out;">
                <h3 style="color: var(--color-brown); margin-bottom: 15px; font-family: 'Baloo 2', cursive, sans-serif;">2. NBA Playoffs</h3>
                <div class="trend-content" style="display: flex; flex-direction: column; align-items: center;">
                    <div class="trend-graph" style="width: 90%; height: 250px; margin-bottom: 15px; position: relative;">
                        <div style="position: absolute; bottom: 0; left: 0; width: 100%; height: 1px; background-color: var(--color-green); opacity: 0.3;"></div>
                        <div style="position: absolute; left: 0; bottom: 0; width: 1px; height: 100%; background-color: var(--color-green); opacity: 0.3;"></div>
                        <!-- Graph line -->
                        <svg width="100%" height="100%" viewBox="0 0 1000 250" preserveAspectRatio="none">
                            <path d="M0,100 L100,120 L200,110 L300,130 L400,150 L500,140 L600,150 L700,120 L800,50 L900,20 L1000,0" stroke="var(--color-green)" stroke-width="3" fill="none" />
                            <path d="M0,100 L100,120 L200,110 L300,130 L400,150 L500,140 L600,150 L700,120 L800,50 L900,20 L1000,0 L1000,250 L0,250" fill="var(--color-green)" fill-opacity="0.1" />
                        </svg>
                    </div>
                    <p style="text-align: center; color: var(--color-brown); font-family: 'Baloo 2', cursive, sans-serif;">Search interest surged after yesterday's key matchups and upsets</p>
                </div>
            </div>
    
            <div class="trend-slide" style="position: absolute; width: 100%; height: 100%; opacity: 0; transition: opacity 1s ease-in-out;">
                <h3 style="color: var(--color-brown); margin-bottom: 15px; font-family: 'Baloo 2', cursive, sans-serif;">3. Spotify New Features</h3>
                <div class="trend-content" style="display: flex; flex-direction: column; align-items: center;">
                    <div class="trend-graph" style="width: 90%; height: 250px; margin-bottom: 15px; position: relative;">
                        <div style="position: absolute; bottom: 0; left: 0; width: 100%; height: 1px; background-color: var(--color-green); opacity: 0.3;"></div>
                        <div style="position: absolute; left: 0; bottom: 0; width: 1px; height: 100%; background-color: var(--color-green); opacity: 0.3;"></div>
                        <!-- Graph line -->
                        <svg width="100%" height="100%" viewBox="0 0 1000 250" preserveAspectRatio="none">
                            <path d="M0,220 L100,230 L200,220 L300,210 L400,200 L500,180 L600,150 L700,100 L800,50 L900,30 L1000,20" stroke="var(--color-yellow)" stroke-width="3" fill="none" />
                            <path d="M0,220 L100,230 L200,220 L300,210 L400,200 L500,180 L600,150 L700,100 L800,50 L900,30 L1000,20 L1000,250 L0,250" fill="var(--color-yellow)" fill-opacity="0.1" />
                        </svg>
                    </div>
                    <p style="text-align: center; color: var(--color-brown); font-family: 'Baloo 2', cursive, sans-serif;">Users searching for information about Spotify's latest language options announcement</p>
                </div>
            </div>
    
            <div class="trend-slide" style="position: absolute; width: 100%; height: 100%; opacity: 0; transition: opacity 1s ease-in-out;">
                <h3 style="color: var(--color-brown); margin-bottom: 15px; font-family: 'Baloo 2', cursive, sans-serif;">4. Ryan Gosling Star Wars</h3>
                <div class="trend-content" style="display: flex; flex-direction: column; align-items: center;">
                    <div class="trend-graph" style="width: 90%; height: 250px; margin-bottom: 15px; position: relative;">
                        <div style="position: absolute; bottom: 0; left: 0; width: 100%; height: 1px; background-color: var(--color-green); opacity: 0.3;"></div>
                        <div style="position: absolute; left: 0; bottom: 0; width: 1px; height: 100%; background-color: var(--color-green); opacity: 0.3;"></div>
                        <!-- Graph line -->
                        <svg width="100%" height="100%" viewBox="0 0 1000 250" preserveAspectRatio="none">
                            <path d="M0,200 L100,190 L200,195 L300,170 L400,150 L500,100 L600,80 L700,40 L800,20 L900,30 L1000,10" stroke="var(--color-green)" stroke-width="3" fill="none" />
                            <path d="M0,200 L100,190 L200,195 L300,170 L400,150 L500,100 L600,80 L700,40 L800,20 L900,30 L1000,10 L1000,250 L0,250" fill="var(--color-green)" fill-opacity="0.1" />
                        </svg>
                    </div>
                    <p style="text-align: center; color: var(--color-brown); font-family: 'Baloo 2', cursive, sans-serif;">Fans searching for details about Ryan Gosling joining the Star Wars franchise</p>
                </div>
            </div>
    
            <div class="trend-slide" style="position: absolute; width: 100%; height: 100%; opacity: 0; transition: opacity 1s ease-in-out;">
                <h3 style="color: var(--color-brown); margin-bottom: 15px; font-family: 'Baloo 2', cursive, sans-serif;">5. Climate Change Reports</h3>
                <div class="trend-content" style="display: flex; flex-direction: column; align-items: center;">
                    <div class="trend-graph" style="width: 90%; height: 250px; margin-bottom: 15px; position: relative;">
                        <div style="position: absolute; bottom: 0; left: 0; width: 100%; height: 1px; background-color: var(--color-green); opacity: 0.3;"></div>
                        <div style="position: absolute; left: 0; bottom: 0; width: 1px; height: 100%; background-color: var(--color-green); opacity: 0.3;"></div>
                        <!-- Graph line -->
                        <svg width="100%" height="100%" viewBox="0 0 1000 250" preserveAspectRatio="none">
                            <path d="M0,150 L100,160 L200,170 L300,180 L400,200 L500,190 L600,180 L700,140 L800,100 L900,40 L1000,20" stroke="var(--color-yellow)" stroke-width="3" fill="none" />
                            <path d="M0,150 L100,160 L200,170 L300,180 L400,200 L500,190 L600,180 L700,140 L800,100 L900,40 L1000,20 L1000,250 L0,250" fill="var(--color-yellow)" fill-opacity="0.1" />
                        </svg>
                    </div>
                    <p style="text-align: center; color: var(--color-brown); font-family: 'Baloo 2', cursive, sans-serif;">Recent environmental reports triggered increased searches about climate change</p>
                </div>
            </div>
    
            <!-- Navigation dots -->
            <div style="text-align: center; position: absolute; bottom: 15px; width: 100%;">
                <span class="dot" style="height: 12px; width: 12px; margin: 0 4px; background-color: var(--color-brown); opacity: 0.4; border-radius: 50%; display: inline-block; transition: background-color 0.3s ease; cursor: pointer; border: 1px solid var(--color-green);"></span>
                <span class="dot" style="height: 12px; width: 12px; margin: 0 4px; background-color: var(--color-brown); opacity: 0.4; border-radius: 50%; display: inline-block; transition: background-color 0.3s ease; cursor: pointer; border: 1px solid var(--color-green);"></span>
                <span class="dot" style="height: 12px; width: 12px; margin: 0 4px; background-color: var(--color-brown); opacity: 0.4; border-radius: 50%; display: inline-block; transition: background-color 0.3s ease; cursor: pointer; border: 1px solid var(--color-green);"></span>
                <span class="dot" style="height: 12px; width: 12px; margin: 0 4px; background-color: var(--color-brown); opacity: 0.4; border-radius: 50%; display: inline-block; transition: background-color 0.3s ease; cursor: pointer; border: 1px solid var(--color-green);"></span>
                <span class="dot" style="height: 12px; width: 12px; margin: 0 4px; background-color: var(--color-brown); opacity: 0.4; border-radius: 50%; display: inline-block; transition: background-color 0.3s ease; cursor: pointer; border: 1px solid var(--color-green);"></span>
            </div>
        </div>
    </section>
         <section>
            <div class="section-grid">
                <div data-aos="fade-up">
                <article class="section-card" style="background: linear-gradient(90deg,rgba(91, 0, 227, 1) 0%, rgba(9, 9, 121, 1) 35%, rgba(106, 189, 212, 1) 100%);">
                    <div class="section-content" style="text-align: center;">
                    <h2 style="color: white;">Why Choose <u>You You</u>? (and not just because you're <b style="font-style:italic">awesome</b>)</h2>
                    <p ><u>Traditional News Sources</u>: Not relevant to you, always about some sad crimes/wars and full of ads</p>
                    <p style="color: #A6FFB9;"><u>You You News</u>: Free access to the trendiest, coolest, and most "in-the-loop" events in the world!</p>
                    <p style="color: #A6FFB9;">[+ we have a happy lemon (help us name the lemon!) at the top of a page--can you find it?]</p>
                    <br>
                    <br>
                    <h2 style="color: white;">Want to Create <u>YOUR</u> Articles the <u>WORLD</u> Will Admire?</h2>
                    <p style="color: #A6FFB9;">Our AI-powered <u>ARTICLE-U</u> service is coming soon! With 2-3 words, you create a trendy article that we feature for the world to admire! Don't just be "in the loop"; lead the loop!</p>
                    <p>=== Beta Release Coming 06/06/25 ===</p>
                </div>
                </article>
            </div>
            </div>
        </section>
        <br>
        <div class="bbb"><a href="/Pages/working">Want to Join the Discussion?</a></div>
        <section style="margin-top: 40px;">
            <h2>Community Forums</h2>
            <div class="section-grid">
                <div data-aos="fade-up">
                    <div class="forum-section">
                        <h3>Tech Forum</h3>
                        <ul class="forum-list">
                            <li>
                                <a href="/Pages/working.html">Jensen Huang</a>
                                <span>245 discussions</span>
                            </li>
                            <li>
                                <a href="/Pages/working.html">deepseek vs openai</a>
                                <span>189 discussions</span>
                            </li>
                            <li>
                                <a href="/Pages/working.html">Programming Help</a>
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
                                <a href="/Pages/working.html">March Madness</a>
                                <span>512 discussions</span>
                            </li>
                            <li>
                                <a href="/Pages/working.html">Fantasy Football</a>
                                <span>287 discussions</span>
                            </li>
                            <li>
                                <a href="/Pages/working.html">Canucks vs Devils</a>
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
                                <a href="/Pages/working.html">Grant Ellis: The Bachelor</a>
                                <span>421 discussions</span>
                            </li>
                            <li>
                                <a href=/Pages/working.html">Streaming Recommendations</a>
                                <span>356 discussions</span>
                            </li>
                            <li>
                                <a href="/Pages/working.html">TV Show Theories</a>
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
                                <a href="/Pages/working.html">New Releases</a>
                                <span>332 discussions</span>
                            </li>
                            <li>
                                <a href="/Pages/working.html">Genre Discussions</a>
                                <span>245 discussions</span>
                            </li>
                            <li>
                                <a href="/Pages/working.html">Concert Experiences</a>
                                <span>167 discussions</span>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
        </section>
    </div>
    <!-- Login Rewards Modal -->
    <div id="loginRewardsModal" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background-color: rgba(0,0,0,0.7); z-index: 1000; justify-content: center; align-items: center;">
        <div style="background-color: white; border-radius: 12px; padding: 30px; max-width: 500px; width: 90%; text-align: center; position: relative; box-shadow: 0 10px 25px rgba(0,0,0,0.2); animation: popIn 0.5s ease-out;">
            <span id="closeModal" style="position: absolute; top: 15px; right: 20px; font-size: 24px; cursor: pointer; color: #666;">&times;</span>
            <h2 style="color: #2c3e50; margin-bottom: 15px;">Welcome Back!</h2>
            <div id="streakCounter" style="font-size: 18px; color: #3498db; margin-bottom: 20px;">
                <span>Your login streak: <strong id="currentStreak">0</strong> days</span>
            </div>
            
            <div id="weeklyRewards" style="display: flex; justify-content: space-between; margin-bottom: 30px; flex-wrap: wrap;">
                <!-- Days will be generated by JavaScript -->
            </div>
            
            <div id="rewardMessage" style="margin: 20px 0; padding: 15px; border-radius: 8px; background-color: #f4f4f8; font-weight: bold;"></div>
            
            <button id="claimReward" style="background-color: #3498db; color: white; border: none; padding: 12px 25px; border-radius: 5px; font-size: 16px; cursor: pointer; transition: background-color 0.3s;">
                Claim Daily Reward
            </button>
        </div>
    </div>

    <footer>
        <div class="container">
            <p>&copy; 2025 You You News. All Rights Reserved.</p>
            <p>Connect with us on social media</p>
            <a href="https://www.instagram.com/youyou_news/" class="fa fa-instagram"></a>
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
    <script>
        // Create an array of funny whale responses
        const whaleResponses = [
        "That tickles!",
        "*Whale noise*",
        "Oo...I like that :)",
        "Wheee!",
        "Hello human!",
        "Need a ride?",
        "vroom goes the roomba",
        "What language do gnomes speak?",
        "wtf is the uscmind challenge",
        "Love LePookie",
        "Gojo should have beat Sukuna",
        "Which ninja turtle is Mbappé?",
        "Moo",
        "Why do dogs say 'bark?' that does not sound like 'bark' to me",
        "I JUST WANT TO BE PART OF YOUR SYMPHONYYYYY",
        "lalala :o",
        "emotional damage",
        "popular mmos' intro was so fire",
        "shinra tensei",
        "wheeeeeeeeeeeeeeeeeee",
        "Shrek or Kung Fu Panda?",
        "It's that me espresso >:)",
        "Thanks for logging in!",
        "Wow, thanks for using our website!",
        "you're a champ! <3",
        "*happy whale noises",
        "i bet SGA is at the free throw line rn",
        "Have a great day!!!",
        "Manifesting good things for u",
        "You're my super idol",
        "**talk no jutsu",
        "look at curry, so inspirational",
        "biden on the epstein list??",
        "You're the real MVP!",
        "you are enough :)",
        "this whale is here for u :>",
        "alexa, how do i slide in dms?",
        "...uh, fein, fein fein?",
        "So 2 penguins walked into a bar...BANG",
        "Could u beat Olaf in a fight?",
        "LET IT GOOOO, LET IT GOOOOO",
        "'how much do u bench bro' is crazy",
        "yap yap yap",
        "Toronto wind is CRAZY",
        "Imagine ur in Cancun..ahhhh :>",
        "Stay home, cook rice - Ryan Higa",
        "I'm a fish (whatttttt)",
        "Happy bday to uuuu",
        "Hiii",
        "netflix n chill?",
        "You're awesome!",
        "You're the best human i've met today",
        "Does Trump have fanfic?!?",
        "Jensen Huang is my goat",
        "How is it like being human?",
        "Read and read are different",
        "You're getting into Harvard",
        "BE CONFIDENT! If Benny Blanco can pull Selena Gomez, u can do anything",
        "You warm my heart :>",
        "By referring friends, you can change my avatar (top-right)!"
        ];

        // Create a function to add the whale to the page
        function createSwimmingWhale() {
        // Create the whale element
        const whale = document.createElement('div');
        whale.className = 'swimming-whale';
        
        // Use an img element with the exact whale image
        whale.innerHTML = `
            <img src="/Assets/whale.png" alt="Watercolor whale swimming" />
        `;
        
        // Randomize starting position (top position)
        const startingPosition = Math.random() * (window.innerHeight - 150);
        
        // Set styles for the whale
        Object.assign(whale.style, {
            position: 'fixed',
            top: `${startingPosition}px`,
            left: '-300px', // Start off-screen 
            zIndex: '9999',
            filter: 'drop-shadow(3px 5px 8px rgba(0,0,0,0.3))',
            cursor: 'pointer' // Change cursor to indicate clickability
        });
        
        // Randomly select one of five movement patterns
        const patternNumber = Math.floor(Math.random() * 5) + 1;
        whale.style.animation = `swim-pattern-${patternNumber} ${patternNumber <= 3 ? '8s' : '25s'} forwards`;
        
        // Store active speech bubble
        let activeBubble = null;
        let bubbleRemovalTimeout = null;
        
        // Add click event listener for funny responses
        whale.addEventListener('click', function(e) {
            e.stopPropagation();
            
            // Remove existing bubble if there is one
            if (activeBubble && document.body.contains(activeBubble)) {
                document.body.removeChild(activeBubble);
                clearTimeout(bubbleRemovalTimeout);
            }
            
            // Create speech bubble container div with bbb class
            const bubbleContainer = document.createElement('div');
            bubbleContainer.className = 'bbb';
            
            // Create the actual bubble as an a element per your CSS
            const bubble = document.createElement('a');
            
            // Select random response
            const randomResponse = whaleResponses[Math.floor(Math.random() * whaleResponses.length)];
            bubble.textContent = randomResponse;
            
            // Add bubble to container
            bubbleContainer.appendChild(bubble);
            
            // Calculate responsive bubble size based on viewport width
            const viewportWidth = window.innerWidth;
            const bubbleWidth = Math.min(Math.max(viewportWidth * 0.15, 120), 200); // Between 120px and 200px
            
            // Position the bubble container near the whale
            const whaleRect = whale.getBoundingClientRect();
            
            // Position directly above the whale with minimal gap
            Object.assign(bubbleContainer.style, {
                position: 'fixed',
                left: `${whaleRect.left + (whaleRect.width / 2) - (bubbleWidth / 2)}px`,
                top: `${whaleRect.top - 10}px`, // Positioned much closer to whale
                height: 'auto',
                width: `${bubbleWidth}px`,
                margin: '0',
                display: 'grid',
                placeItems: 'center',
                zIndex: '10000',
                opacity: '1',
                transition: 'opacity 0.3s ease',
                pointerEvents: 'none'
            });
            
            // Add to body
            document.body.appendChild(bubbleContainer);
            activeBubble = bubbleContainer;
            
            // Remove after animation - shortened to 3 seconds
            bubbleRemovalTimeout = setTimeout(() => {
                bubbleContainer.style.opacity = '0';
                setTimeout(() => {
                    if (document.body.contains(bubbleContainer)) {
                    document.body.removeChild(bubbleContainer);
                    activeBubble = null;
                    }
                }, 300); // Faster fade out
            }, 3000); // Display time
        });
        
        // Set up animation tracking to move the speech bubble with the whale
        function updateBubblePosition() {
            if (activeBubble && document.body.contains(activeBubble) && document.body.contains(whale)) {
                const whaleRect = whale.getBoundingClientRect();
                const bubbleWidth = parseFloat(activeBubble.style.width);
                
                Object.assign(activeBubble.style, {
                    left: `${whaleRect.left + (whaleRect.width / 2) - (bubbleWidth / 2)}px`,
                    top: `${whaleRect.top - 20}px` // Keep bubble close during animation
                });
                
                requestAnimationFrame(updateBubblePosition);
            }
        }
        
        // Start tracking if needed
        whale.addEventListener('click', function() {
            if (activeBubble) {
                requestAnimationFrame(updateBubblePosition);
            }
        });
        
        // Add whale to the body
        document.body.appendChild(whale);
        
        // Remove the whale after animation completes
        const animationDuration = patternNumber <= 3 ? 8000 : 25000;
        setTimeout(() => {
            if (document.body.contains(whale)) {
                if (activeBubble && document.body.contains(activeBubble)) {
                    document.body.removeChild(activeBubble);
                }
                document.body.removeChild(whale);
            }
        }, animationDuration + 500);
        }

        // Create CSS for the whale animation with multiple patterns
        const style = document.createElement('style');
        style.textContent = `
        /* Pattern 1: Standard swim across - FAST */
        @keyframes swim-pattern-1 {
            0% {
                left: -300px;
                transform: scaleX(1) translateY(0px);
            }
            100% {
                left: calc(100vw + 300px);
                transform: scaleX(1) translateY(0px);
            }
        }
        
        /* Pattern 2: Swim with flip in the middle - FAST */
        @keyframes swim-pattern-2 {
            0% {
                left: -300px;
                transform: scaleX(1) translateY(0px) rotate(0deg);
            }
            20% {
                left: calc(30vw);
                transform: scaleX(1) translateY(0px) rotate(0deg);
            }
            30% {
                left: calc(40vw);
                transform: scaleX(1) translateY(0px) rotate(180deg);
            }
            40% {
                left: calc(50vw);
                transform: scaleX(1) translateY(0px) rotate(360deg);
            }
            100% {
                left: calc(100vw + 300px);
                transform: scaleX(1) translateY(0px) rotate(360deg);
            }
        }
        
        /* Pattern 3: Zigzag fast path - FAST */
        @keyframes swim-pattern-3 {
            0% {
                left: -300px;
                top: 50%;
            }
            20% {
                left: calc(20vw);
                top: 30%;
            }
            40% {
                left: calc(40vw);
                top: 70%;
            }
            60% {
                left: calc(60vw);
                top: 20%;
            }
            80% {
                left: calc(80vw);
                top: 60%;
            }
            100% {
                left: calc(100vw + 300px);
                top: 40%;
            }
        }
        
        /* Pattern 4: Lingering in the middle - SLOW */
        @keyframes swim-pattern-4 {
            0% {
                left: -300px;
                transform: scaleX(1) translateY(0px);
            }
            20% {
                left: calc(40vw);
                transform: scaleX(1) translateY(0px);
            }
            /* Linger in the center section */
            25% {
                left: calc(45vw);
                transform: scaleX(1) translateY(20px);
            }
            30% {
                left: calc(43vw);
                transform: scaleX(1) translateY(-10px);
            }
            35% {
                left: calc(47vw);
                transform: scaleX(1) translateY(15px);
            }
            40% {
                left: calc(42vw);
                transform: scaleX(1) translateY(-5px);
            }
            45% {
                left: calc(46vw);
                transform: scaleX(1) translateY(10px);
            }
            50% {
                left: calc(44vw);
                transform: scaleX(1) translateY(0px);
            }
            /* Continue swimming */
            55% {
                left: calc(50vw);
                transform: scaleX(1) translateY(0px);
            }
            90% {
                left: calc(100vw + 100px);
                transform: scaleX(1) translateY(10px);
            }
            100% {
                left: calc(100vw + 300px);
                transform: scaleX(1) translateY(0px);
            }
        }
        
        /* Pattern 5: Enter from top, exit from bottom - SLOW */
        @keyframes swim-pattern-5 {
            0% {
                left: -300px;
                top: 20%;
                transform: scaleX(1) rotate(15deg);
            }
            10% {
                left: calc(20vw);
                top: 10%;
                transform: scaleX(1) rotate(15deg);
            }
            50% {
                left: calc(50vw);
                top: 50%;
                transform: scaleX(1) rotate(30deg);
            }
            90% {
                left: calc(80vw);
                top: 90%;
                transform: scaleX(1) rotate(45deg);
            }
            100% {
                left: calc(90vw);
                top: 110%;
                transform: scaleX(1) rotate(45deg);
            }
        }
        
        .swimming-whale {
            will-change: transform;
            pointer-events: auto;
        }
        
        .swimming-whale img {
            height: 150px;
            width: auto;
        }
        
        /* Updated bubble styles with responsive sizing and closer positioning */
        .bbb {
            height: auto;
            margin: 0;
            display: grid;
            place-items: center;
            font: 1vw system-ui;
            background-color: var(--color-yellow, transparent);
        }

        .bbb a {
            transform: translatey(0px);
            animation: float 5s ease-in-out infinite;
            text-align: center;
            text-transform: uppercase;
            font-weight: bold;
            letter-spacing: 1px;
            font-size: clamp(10px, 1.2vw, 14px);
            color: var(--color-brown, #5d4037);
            background-color: var(--color-beige, #f5f5dc);
            padding: clamp(6px, 1.5vw, 15px);
            border-radius: 8px;
            position: relative;
            box-shadow: 6px 6px var(--color-blue, #2196f3);
            font-family: "Baloo 2", cursive;
            border: 1px solid var(--color-green, #4caf50);
            width: 100%;
            box-sizing: border-box;
            word-wrap: break-word;
            line-height: 1.3;
        }
        
        .bbb a:after {
            transform: translatey(0px);
            animation: float2 5s ease-in-out infinite;
            content: ".";
            font-weight: bold;
            -webkit-text-stroke: 0.5px var(--color-green, #4caf50);
            -webkit-text-fill-color: var(--color-beige, #f5f5dc);
            border: 1px solid var(--color-green, #4caf50);
            text-shadow: 6px 6px var(--color-blue, #2196f3);
            text-align: left;
            font-size: clamp(18px, 2vw, 25px);
            width: clamp(18px, 2vw, 25px);
            height: 6px;
            line-height: 15px;
            border-radius: 6px;
            background-color: var(--color-beige, #f5f5dc);
            position: absolute;
            display: block;
            bottom: -15px;
            left: 10%;
            box-shadow: 6px 6px var(--color-blue, #2196f3);
            z-index: -2;
        }
        
        /* Adding the float animations that were referenced but missing */
        @keyframes float {
            0% {
                transform: translatey(0px);
            }
            50% {
                transform: translatey(-4px);
            }
            100% {
                transform: translatey(0px);
            }
        }
        
        @keyframes float2 {
            0% {
                transform: translatey(0px);
            }
            50% {
                transform: translatey(-2px);
            }
            100% {
                transform: translatey(0px);
            }
        }
        `;
        document.head.appendChild(style);

        // Function to trigger whale randomly
        function scheduleWhaleAppearance() {
        // Random time between 20 and 60 seconds
        const nextAppearance = 20000 + Math.random() * 15000;
        
        setTimeout(() => {
            createSwimmingWhale();
            scheduleWhaleAppearance(); // Schedule next appearance
        }, nextAppearance);
        }

        // Start the random whale appearances when the page loads
        window.addEventListener('load', () => {
        // Show one whale shortly after page load
        setTimeout(createSwimmingWhale, 3000);
        
        // Schedule random appearances
        scheduleWhaleAppearance();
        });

        // Add window resize handler to adjust bubble size if active
        window.addEventListener('resize', () => {
        const activeBubble = document.querySelector('.bbb');
        if (activeBubble) {
            const viewportWidth = window.innerWidth;
            const bubbleWidth = Math.min(Math.max(viewportWidth * 0.15, 120), 200);
            activeBubble.style.width = `${bubbleWidth}px`;
            
            // Adjust position if whale is still visible
            const whale = document.querySelector('.swimming-whale');
            if (whale) {
            const whaleRect = whale.getBoundingClientRect();
            activeBubble.style.left = `${whaleRect.left + (whaleRect.width / 2) - (bubbleWidth / 2)}px`;
            }
        }
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
    <section style="margin-top: 40px;">
        <h2 style="color: var(--color-brown); font-family: 'Baloo 2', cursive, sans-serif; letter-spacing: 1px;">Yesterday's Top Google Trends</h2>
        <div class="slideshow-container" style="background-color: var(--color-beige); border-radius: 11px; padding: 20px; box-shadow: 10px 10px var(--color-blue); position: relative; height: 400px; overflow: hidden; border: 1px solid var(--color-green);">
            <!-- Slides -->
            <div class="trend-slide" style="position: absolute; width: 100%; height: 100%; opacity: 1; transition: opacity 1s ease-in-out;">
                <h3 style="color: var(--color-brown); margin-bottom: 15px; font-family: 'Baloo 2', cursive, sans-serif;">1. Coachella Livestream</h3>
                <div class="trend-content" style="display: flex; flex-direction: column; align-items: center;">
                    <div class="trend-graph" style="width: 90%; height: 250px; margin-bottom: 15px; position: relative;">
                        <div style="position: absolute; bottom: 0; left: 0; width: 100%; height: 1px; background-color: var(--color-green); opacity: 0.3;"></div>
                        <div style="position: absolute; left: 0; bottom: 0; width: 1px; height: 100%; background-color: var(--color-green); opacity: 0.3;"></div>
                        <!-- Graph line -->
                        <svg width="100%" height="100%" viewBox="0 0 1000 250" preserveAspectRatio="none">
                            <path d="M0,250 L100,200 L200,220 L300,150 L400,180 L500,100 L600,50 L700,20 L800,10 L900,5 L1000,0" stroke="var(--color-blue)" stroke-width="3" fill="none" />
                            <path d="M0,250 L100,200 L200,220 L300,150 L400,180 L500,100 L600,50 L700,20 L800,10 L900,5 L1000,0 L1000,250 L0,250" fill="var(--color-blue)" fill-opacity="0.1" />
                        </svg>
                    </div>
                    <p style="text-align: center; color: var(--color-brown); font-family: 'Baloo 2', cursive, sans-serif;">Interest spiked yesterday as fans searched for ways to watch performances live online</p>
                </div>
            </div>
    
            <div class="trend-slide" style="position: absolute; width: 100%; height: 100%; opacity: 0; transition: opacity 1s ease-in-out;">
                <h3 style="color: var(--color-brown); margin-bottom: 15px; font-family: 'Baloo 2', cursive, sans-serif;">2. NBA Playoffs</h3>
                <div class="trend-content" style="display: flex; flex-direction: column; align-items: center;">
                    <div class="trend-graph" style="width: 90%; height: 250px; margin-bottom: 15px; position: relative;">
                        <div style="position: absolute; bottom: 0; left: 0; width: 100%; height: 1px; background-color: var(--color-green); opacity: 0.3;"></div>
                        <div style="position: absolute; left: 0; bottom: 0; width: 1px; height: 100%; background-color: var(--color-green); opacity: 0.3;"></div>
                        <!-- Graph line -->
                        <svg width="100%" height="100%" viewBox="0 0 1000 250" preserveAspectRatio="none">
                            <path d="M0,100 L100,120 L200,110 L300,130 L400,150 L500,140 L600,150 L700,120 L800,50 L900,20 L1000,0" stroke="var(--color-green)" stroke-width="3" fill="none" />
                            <path d="M0,100 L100,120 L200,110 L300,130 L400,150 L500,140 L600,150 L700,120 L800,50 L900,20 L1000,0 L1000,250 L0,250" fill="var(--color-green)" fill-opacity="0.1" />
                        </svg>
                    </div>
                    <p style="text-align: center; color: var(--color-brown); font-family: 'Baloo 2', cursive, sans-serif;">Search interest surged after yesterday's key matchups and upsets</p>
                </div>
            </div>
    
            <div class="trend-slide" style="position: absolute; width: 100%; height: 100%; opacity: 0; transition: opacity 1s ease-in-out;">
                <h3 style="color: var(--color-brown); margin-bottom: 15px; font-family: 'Baloo 2', cursive, sans-serif;">3. Spotify New Features</h3>
                <div class="trend-content" style="display: flex; flex-direction: column; align-items: center;">
                    <div class="trend-graph" style="width: 90%; height: 250px; margin-bottom: 15px; position: relative;">
                        <div style="position: absolute; bottom: 0; left: 0; width: 100%; height: 1px; background-color: var(--color-green); opacity: 0.3;"></div>
                        <div style="position: absolute; left: 0; bottom: 0; width: 1px; height: 100%; background-color: var(--color-green); opacity: 0.3;"></div>
                        <!-- Graph line -->
                        <svg width="100%" height="100%" viewBox="0 0 1000 250" preserveAspectRatio="none">
                            <path d="M0,220 L100,230 L200,220 L300,210 L400,200 L500,180 L600,150 L700,100 L800,50 L900,30 L1000,20" stroke="var(--color-yellow)" stroke-width="3" fill="none" />
                            <path d="M0,220 L100,230 L200,220 L300,210 L400,200 L500,180 L600,150 L700,100 L800,50 L900,30 L1000,20 L1000,250 L0,250" fill="var(--color-yellow)" fill-opacity="0.1" />
                        </svg>
                    </div>
                    <p style="text-align: center; color: var(--color-brown); font-family: 'Baloo 2', cursive, sans-serif;">Users searching for information about Spotify's latest language options announcement</p>
                </div>
            </div>
    
            <div class="trend-slide" style="position: absolute; width: 100%; height: 100%; opacity: 0; transition: opacity 1s ease-in-out;">
                <h3 style="color: var(--color-brown); margin-bottom: 15px; font-family: 'Baloo 2', cursive, sans-serif;">4. Ryan Gosling Star Wars</h3>
                <div class="trend-content" style="display: flex; flex-direction: column; align-items: center;">
                    <div class="trend-graph" style="width: 90%; height: 250px; margin-bottom: 15px; position: relative;">
                        <div style="position: absolute; bottom: 0; left: 0; width: 100%; height: 1px; background-color: var(--color-green); opacity: 0.3;"></div>
                        <div style="position: absolute; left: 0; bottom: 0; width: 1px; height: 100%; background-color: var(--color-green); opacity: 0.3;"></div>
                        <!-- Graph line -->
                        <svg width="100%" height="100%" viewBox="0 0 1000 250" preserveAspectRatio="none">
                            <path d="M0,200 L100,190 L200,195 L300,170 L400,150 L500,100 L600,80 L700,40 L800,20 L900,30 L1000,10" stroke="var(--color-green)" stroke-width="3" fill="none" />
                            <path d="M0,200 L100,190 L200,195 L300,170 L400,150 L500,100 L600,80 L700,40 L800,20 L900,30 L1000,10 L1000,250 L0,250" fill="var(--color-green)" fill-opacity="0.1" />
                        </svg>
                    </div>
                    <p style="text-align: center; color: var(--color-brown); font-family: 'Baloo 2', cursive, sans-serif;">Fans searching for details about Ryan Gosling joining the Star Wars franchise</p>
                </div>
            </div>
    
            <div class="trend-slide" style="position: absolute; width: 100%; height: 100%; opacity: 0; transition: opacity 1s ease-in-out;">
                <h3 style="color: var(--color-brown); margin-bottom: 15px; font-family: 'Baloo 2', cursive, sans-serif;">5. Climate Change Reports</h3>
                <div class="trend-content" style="display: flex; flex-direction: column; align-items: center;">
                    <div class="trend-graph" style="width: 90%; height: 250px; margin-bottom: 15px; position: relative;">
                        <div style="position: absolute; bottom: 0; left: 0; width: 100%; height: 1px; background-color: var(--color-green); opacity: 0.3;"></div>
                        <div style="position: absolute; left: 0; bottom: 0; width: 1px; height: 100%; background-color: var(--color-green); opacity: 0.3;"></div>
                        <!-- Graph line -->
                        <svg width="100%" height="100%" viewBox="0 0 1000 250" preserveAspectRatio="none">
                            <path d="M0,150 L100,160 L200,170 L300,180 L400,200 L500,190 L600,180 L700,140 L800,100 L900,40 L1000,20" stroke="var(--color-yellow)" stroke-width="3" fill="none" />
                            <path d="M0,150 L100,160 L200,170 L300,180 L400,200 L500,190 L600,180 L700,140 L800,100 L900,40 L1000,20 L1000,250 L0,250" fill="var(--color-yellow)" fill-opacity="0.1" />
                        </svg>
                    </div>
                    <p style="text-align: center; color: var(--color-brown); font-family: 'Baloo 2', cursive, sans-serif;">Recent environmental reports triggered increased searches about climate change</p>
                </div>
            </div>
    
            <!-- Navigation dots -->
            <div style="text-align: center; position: absolute; bottom: 15px; width: 100%;">
                <span class="dot" style="height: 12px; width: 12px; margin: 0 4px; background-color: var(--color-brown); opacity: 0.4; border-radius: 50%; display: inline-block; transition: background-color 0.3s ease; cursor: pointer; border: 1px solid var(--color-green);"></span>
                <span class="dot" style="height: 12px; width: 12px; margin: 0 4px; background-color: var(--color-brown); opacity: 0.4; border-radius: 50%; display: inline-block; transition: background-color 0.3s ease; cursor: pointer; border: 1px solid var(--color-green);"></span>
                <span class="dot" style="height: 12px; width: 12px; margin: 0 4px; background-color: var(--color-brown); opacity: 0.4; border-radius: 50%; display: inline-block; transition: background-color 0.3s ease; cursor: pointer; border: 1px solid var(--color-green);"></span>
                <span class="dot" style="height: 12px; width: 12px; margin: 0 4px; background-color: var(--color-brown); opacity: 0.4; border-radius: 50%; display: inline-block; transition: background-color 0.3s ease; cursor: pointer; border: 1px solid var(--color-green);"></span>
                <span class="dot" style="height: 12px; width: 12px; margin: 0 4px; background-color: var(--color-brown); opacity: 0.4; border-radius: 50%; display: inline-block; transition: background-color 0.3s ease; cursor: pointer; border: 1px solid var(--color-green);"></span>
            </div>
        </div>
    </section>
    <section>
        <div class="section-grid">
            <div data-aos="fade-up">
            <article class="section-card" style="background: linear-gradient(90deg,rgba(91, 0, 227, 1) 0%, rgba(9, 9, 121, 1) 35%, rgba(106, 189, 212, 1) 100%);">
                <div class="section-content" style="text-align: center;">
                <h2 style="color: white;">Why Choose <u>You You</u>? (and not just because you're <b style="font-style:italic">awesome</b>)</h2>
                <p ><u>Traditional News Sources</u>: Not relevant to you, always about some sad crimes/wars and full of ads</p>
                <p style="color: #A6FFB9;"><u>You You News</u>: Free access to the trendiest, coolest, and most "in-the-loop" events in the world!</p>
                <p style="color: #A6FFB9;">[+ we have a happy whale (beluga?) at the top of this page]</p>
                <br>
                <br>
                <h2 style="color: white;">Want to Create <u>YOUR</u> Articles the <u>WORLD</u> Will Admire?</h2>
                <p style="color: #A6FFB9;">Our AI-powered <u>ARTICLE-U</u> service is coming soon! With 2-3 words, you create a trendy article that we feature for the world to admire! Don't just be "in the loop"; lead the loop!</p>
                <p>=== Beta Release Coming 06/06/25 ===</p>
            </div>
            </article>
        </div>
        </div>
    </section>
    <br>
        <div class="bbb"><a href="/Pages/working">Want to Join the Discussion?</a></div>
        <section style="margin-top: 40px;">
            <h2>Community Forums</h2>
            <div class="section-grid">
                <div data-aos="fade-up">
                    <div class="forum-section">
                        <h3>Tech Forum</h3>
                        <ul class="forum-list">
                            <li>
                                <a href="/Pages/working.html">Jensen Huang</a>
                                <span>245 discussions</span>
                            </li>
                            <li>
                                <a href="/Pages/working.html">deepseek vs openai</a>
                                <span>189 discussions</span>
                            </li>
                            <li>
                                <a href="/Pages/working.html">Programming Help</a>
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
                                <a href="/Pages/working.html">March Madness</a>
                                <span>512 discussions</span>
                            </li>
                            <li>
                                <a href="/Pages/working.html">Fantasy Football</a>
                                <span>287 discussions</span>
                            </li>
                            <li>
                                <a href="/Pages/working.html">Canucks vs Devils</a>
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
                                <a href="/Pages/working.html">Grant Ellis: The Bachelor</a>
                                <span>421 discussions</span>
                            </li>
                            <li>
                                <a href="/Pages/working.html">Streaming Recommendations</a>
                                <span>356 discussions</span>
                            </li>
                            <li>
                                <a href="/Pages/working.html">TV Show Theories</a>
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
                                <a href="/Pages/working.html">New Releases</a>
                                <span>332 discussions</span>
                            </li>
                            <li>
                                <a href="/Pages/working.html">Genre Discussions</a>
                                <span>245 discussions</span>
                            </li>
                            <li>
                                <a href="/Pages/working.html">Concert Experiences</a>
                                <span>167 discussions</span>
                            </li>
                        </ul>
                    </div>
                </div>
            </div>
        </section>
    </div>
    <!-- Login Rewards Modal -->
    <div id="loginRewardsModal" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background-color: rgba(0,0,0,0.7); z-index: 1000; justify-content: center; align-items: center;">
        <div style="background-color: white; border-radius: 12px; padding: 30px; max-width: 500px; width: 90%; text-align: center; position: relative; box-shadow: 0 10px 25px rgba(0,0,0,0.2); animation: popIn 0.5s ease-out;">
            <span id="closeModal" style="position: absolute; top: 15px; right: 20px; font-size: 24px; cursor: pointer; color: #666;">&times;</span>
            <h2 style="color: #2c3e50; margin-bottom: 15px;">Welcome Back!</h2>
            <div id="streakCounter" style="font-size: 18px; color: #3498db; margin-bottom: 20px;">
                <span>Your login streak: <strong id="currentStreak">0</strong> days</span>
            </div>
            
            <div id="weeklyRewards" style="display: flex; justify-content: space-between; margin-bottom: 30px; flex-wrap: wrap;">
                <!-- Days will be generated by JavaScript -->
            </div>
            
            <div id="rewardMessage" style="margin: 20px 0; padding: 15px; border-radius: 8px; background-color: #f4f4f8; font-weight: bold;"></div>
            
            <button id="claimReward" style="background-color: #3498db; color: white; border: none; padding: 12px 25px; border-radius: 5px; font-size: 16px; cursor: pointer; transition: background-color 0.3s;">
                Claim Daily Reward
            </button>
        </div>
    </div>
    <!-- Add this to your existing HTML before the closing </body> tag -->

<!-- Login Rewards Modal -->
    <div id="loginRewardsModal" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background-color: rgba(0,0,0,0.7); z-index: 1000; justify-content: center; align-items: center;">
        <div style="background-color: white; border-radius: 12px; padding: 30px; max-width: 500px; width: 90%; text-align: center; position: relative; box-shadow: 0 10px 25px rgba(0,0,0,0.2); animation: popIn 0.5s ease-out;">
            <span id="closeModal" style="position: absolute; top: 15px; right: 20px; font-size: 24px; cursor: pointer; color: #666;">&times;</span>
            <h2 style="color: #2c3e50; margin-bottom: 15px;">Welcome Back!</h2>
            <div id="streakCounter" style="font-size: 18px; color: #3498db; margin-bottom: 20px;">
                <span>Your login streak: <strong id="currentStreak">0</strong> days</span>
            </div>
            
            <div id="weeklyRewards" style="display: flex; justify-content: space-between; margin-bottom: 30px; flex-wrap: wrap;">
                <!-- Days will be generated by JavaScript -->
            </div>
            
            <div id="rewardMessage" style="margin: 20px 0; padding: 15px; border-radius: 8px; background-color: #f4f4f8; font-weight: bold;"></div>
            
            <button id="claimReward" style="background-color: #3498db; color: white; border: none; padding: 12px 25px; border-radius: 5px; font-size: 16px; cursor: pointer; transition: background-color 0.3s;">
                Claim Daily Reward
            </button>
        </div>
    </div>

    <footer>
        <div class="container">
            <p>&copy; 2025 You You News. All Rights Reserved.</p>
            <p>Connect with us on social media</p>
            <a href="https://www.instagram.com/youyou_news/" class="fa fa-instagram"></a>
            <div id="footerlink">
                <a href="/Terms_and_Conditions/terms_of_service.html">Terms of Service</a>
            </div>
            <br>
            <img src="../Assets/sectigo_trust_seal_md_106x42.png" alt="Verified Logo">
        </div>
    </footer>
    <!-- Add this to your existing HTML before the closing </body> tag -->

<!-- Login Rewards Modal -->
<div id="loginRewardsModal" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background-color: rgba(0,0,0,0.7); z-index: 1000; justify-content: center; align-items: center;">
    <div style="background-color: white; border-radius: 12px; padding: 30px; max-width: 500px; width: 90%; text-align: center; position: relative; box-shadow: 0 10px 25px rgba(0,0,0,0.2); animation: popIn 0.5s ease-out;">
        <span id="closeModal" style="position: absolute; top: 15px; right: 20px; font-size: 24px; cursor: pointer; color: #666;">&times;</span>
        <h2 style="color: #2c3e50; margin-bottom: 15px;">Welcome Back!</h2>
        <div id="streakCounter" style="font-size: 18px; color: #3498db; margin-bottom: 20px;">
            <span>Your login streak: <strong id="currentStreak">0</strong> days</span>
        </div>
        
        <div id="weeklyRewards" style="display: flex; justify-content: space-between; margin-bottom: 30px; flex-wrap: wrap;">
            <!-- Days will be generated by JavaScript -->
        </div>
        
        <div id="rewardMessage" style="margin: 20px 0; padding: 15px; border-radius: 8px; background-color: #f4f4f8; font-weight: bold;"></div>
        
        <button id="claimReward" style="background-color: #3498db; color: white; border: none; padding: 12px 25px; border-radius: 5px; font-size: 16px; cursor: pointer; transition: background-color 0.3s;">
            Claim Daily Reward
        </button>
    </div>
</div>

<!-- Theme Selector Modal -->
<div id="themeModal" style="display: none; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background-color: rgba(0,0,0,0.7); z-index: 1000; justify-content: center; align-items: center;">
    <div style="background-color: white; border-radius: 12px; padding: 30px; max-width: 600px; width: 90%; text-align: center; position: relative; box-shadow: 0 10px 25px rgba(0,0,0,0.2); animation: popIn 0.5s ease-out;">
        <span id="closeThemeModal" style="position: absolute; top: 15px; right: 20px; font-size: 24px; cursor: pointer; color: #666;">&times;</span>
        <h2 style="color: #2c3e50; margin-bottom: 25px;">Select Your Theme</h2>
        
        <div id="themeGrid" style="display: grid; grid-template-columns: repeat(auto-fill, minmax(120px, 1fr)); gap: 20px; margin-bottom: 30px; max-height: 300px; overflow-y: auto; padding-right: 5px;">
            <!-- Themes will be generated by JavaScript -->
        </div>
        
        <div style="margin-top: 20px;">
            <button id="applyTheme" style="background-color: #3498db; color: white; border: none; padding: 12px 25px; border-radius: 5px; font-size: 16px; margin-right: 15px; cursor: pointer;">
                Apply Theme
            </button>
            <button id="cancelTheme" style="background-color: #e74c3c; color: white; border: none; padding: 12px 25px; border-radius: 5px; font-size: 16px; cursor: pointer;">
                Cancel
            </button>
        </div>
    </div>
</div>
<!-- ✨ Fun News Popup (with click-to-copy referral link) -->
<div id="funNewsPopup" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background-color:rgba(0,0,0,0.7); z-index:9999; justify-content:center; align-items:center; overflow-y: auto; padding: 20px;">
    <div style="background-color:white; border-radius:15px; padding:30px; max-width:500px; width:90%; box-shadow:0 10px 25px rgba(0,0,0,0.3); text-align:center; font-family:'Baloo 2', cursive; max-height: 90vh; overflow-y: auto;">
      <h2 style="color:#774f38;">📣 NEWS SHOULD BE FUN!</h2>
      <p style="color:#333; margin-bottom:20px; font-size:16px;">
        We believe news should be like <b>playing a video game</b> or <b>watching your favourite K-drama</b> — not dull and boring like other sources!
      </p>
      <p style="color:#333; font-size:16px;">
        If <b>you</b> think news should be fun too, share <b>YOUR SPECIAL LINK</b> (for you only!):
      </p>
      <div style="margin:15px 0;">
        <input type="text" id="specialLinkInput" readonly value="" style="width:100%; padding:10px; font-size:14px; border:1px solid #ccc; border-radius:5px; text-align:center; cursor:pointer;">
        <div id="copyConfirm" style="display:none; color:#4caf50; font-size:13px; margin-top:5px;">✅ Copied!</div>
      </div>
      <p style="color:#5d4037; font-size:15px;">
        The more visits from your link, the more chances you have at our <b>$25 Gift Card Draw</b> 🎁 and an <b>Instagram feature</b>! 🌟
      </p>
      <p style="font-size:14px; color:#888;">You've shared this link <span id="shareCount">0</span> times!</p>
      <div style="margin-top: 20px;">
        <label style="display: flex; align-items: center; gap: 10px; font-size: 14px; color: #555;">
          <input type="checkbox" id="dontShowAgainCheckbox"> Don't Show This Again!
        </label>
        <button id="closePopupButton" style="margin-top:10px; background-color:#f9cdad; color:#5d4037; padding:10px 20px; border:none; border-radius:8px; font-weight:bold; font-family:'Baloo 2', cursive;">Got it!</button>
      </div>      
    </div>
  </div>
  
  <script>
    function getReferralCode() {
      const urlParams = new URLSearchParams(window.location.search);
      return urlParams.get('ref') || null;
    }
  
    function incrementShareCount(refCode) {
  const key = `referral_share_count_${refCode}`;
  const visitedKey = 'referral_visited_codes';

  // Skip incrementing if user is the one who owns this code
  const selfRefCode = localStorage.getItem('user_ref_code');
  if (refCode === selfRefCode) {
    return parseInt(localStorage.getItem(key)) || 0;
  }

  // Check if already visited this referral code
  let visited = JSON.parse(localStorage.getItem(visitedKey) || '[]');
  if (visited.includes(refCode)) {
    return parseInt(localStorage.getItem(key)) || 0;
  }

  // Mark as visited
  visited.push(refCode);
  localStorage.setItem(visitedKey, JSON.stringify(visited));

  // Increment and store
  let count = parseInt(localStorage.getItem(key)) || 0;
  count += 1;
  localStorage.setItem(key, count);
  return count;
}

  
    window.addEventListener('load', () => {
      const referral = getReferralCode();
      const popup = document.getElementById('funNewsPopup');
      const input = document.getElementById('specialLinkInput');
      const shareCountDisplay = document.getElementById('shareCount');
      const copyConfirm = document.getElementById('copyConfirm');
      const closeBtn = document.getElementById('closePopupButton');
      const dontShowAgain = localStorage.getItem('hideFunNewsPopup');
      if (dontShowAgain === 'true') return;
      let refCode = referral;
      if (!refCode) {
        refCode = localStorage.getItem('user_ref_code');
        if (!refCode) {
          refCode = Math.random().toString(36).substr(2, 6);
          localStorage.setItem('user_ref_code', refCode);
        }
      }
  
      const shareLink = `https://youyounews.live/?ref=${refCode}`;
      input.value = shareLink;
  
      const count = incrementShareCount(refCode);
      shareCountDisplay.textContent = count;
  
      // Show popup after delay
      setTimeout(() => {
        popup.style.display = 'flex';
      }, 3000);
  
      // Copy-to-clipboard interaction
      input.addEventListener('click', () => {
        navigator.clipboard.writeText(input.value).then(() => {
          copyConfirm.style.display = 'block';
          setTimeout(() => {
            copyConfirm.style.display = 'none';
          }, 2000);
        });
      });
  
      closeBtn.addEventListener('click', () => {
    if (document.getElementById('dontShowAgainCheckbox').checked) {
      localStorage.setItem('hideFunNewsPopup', 'true');
    }
    popup.style.display = 'none';
  });
    });
  </script>
  
<!-- Add this to your existing JavaScript section or create a new <script> block -->
<script>
    document.addEventListener('DOMContentLoaded', function() {
        // Theme definitions
        const themes = [
            { 
                id: 'default', 
                name: 'Default',
                description: 'The classic You You News theme',
                background: 'var(--light-bg)',
                unlocked: true 
            },
            { 
                id: 'dark', 
                name: 'Dark Mode',
                description: 'Easy on the eyes',
                background: '#121212',
                textColor: '#ffffff',
                headerBackground: 'linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), url("/Assets/header.png")',
                unlocked: false 
            },
            { 
                id: 'ocean', 
                name: 'Ocean Waves',
                description: 'Dive into the deep blue',
                background: 'linear-gradient(to right, #41b3a3, #85cdca)',
                navBackground: '#2e8b9e',
                unlocked: false 
            },
            { 
                id: 'sunset', 
                name: 'Sunset Vibes',
                description: 'Warm orange glow',
                background: 'linear-gradient(to bottom right, #ff7e5f, #feb47b)',
                headerBackground: 'linear-gradient(rgba(0, 0, 0, 0.5), rgba(0, 0, 0, 0.5)), url("/Assets/header.png")',
                unlocked: false 
            },
            { 
                id: 'cyberpunk', 
                name: 'Cyberpunk',
                description: 'Futuristic neon style',
                background: '#0f0f2d',
                textColor: '#ffffff',
                accentColor: '#f638dc',
                headerBackground: 'linear-gradient(rgba(10, 10, 45, 0.8), rgba(10, 10, 45, 0.8)), url("/Assets/header.png")',
                unlocked: false 
            },
            { 
                id: 'forest', 
                name: 'Forest',
                description: 'Natural green paradise',
                background: 'linear-gradient(to bottom, #dcedc8, #aed581)',
                headerBackground: 'linear-gradient(rgba(0, 0, 0, 0.6), rgba(0, 0, 0, 0.6)), url("/Assets/header.png")',
                unlocked: false 
            },
            { 
                id: 'cosmic', 
                name: 'Cosmic',
                description: 'Space explorer theme',
                background: 'linear-gradient(to bottom, #141e30, #243b55)',
                textColor: '#ffffff',
                headerBackground: 'linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), url("/Assets/header.png")',
                unlocked: false 
            }
        ];
        const styleElement = document.createElement('style');
        styleElement.textContent = `
            :root {
                --color-yellow: #FFC107;
                --color-brown: #5D4037;
                --color-beige: #FFF8E1;
                --color-blue: #81D4FA;
                --color-green: #81C784;
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
            
            @keyframes fadeIn {
                from { opacity: 0; }
                to { opacity: 1; }
            }
            
            @keyframes fadeOut {
                from { opacity: 1; }
                to { opacity: 0; }
            }
            
            #reward-notification-overlay {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0, 0, 0, 0.6);
                display: flex;
                justify-content: center;
                align-items: center;
                z-index: 9999;
                opacity: 0;
                visibility: hidden;
                transition: opacity 0.3s, visibility 0.3s;
            }
            
            .notification-bubble {
                transform: translatey(0px);
                animation: float 5s ease-in-out infinite;
                text-align: center;
                text-transform: uppercase;
                font-weight: bold;
                letter-spacing: 3px;
                font-size: 15px;
                color: var(--color-brown);
                background-color: var(--color-beige);
                padding: 40px;
                border-radius: 11px;
                position: relative;
                box-shadow: 20px 20px var(--color-blue);
                font-family: "Baloo 2", cursive, sans-serif;
                border: 1px solid var(--color-green);
                max-width: 90%;
                z-index: 10000;
            }
            
            .notification-bubble:after {
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
            
            .notification-bubble .reward-icon {
                font-size: 48px;
                margin: 10px 0;
                display: block;
            }
            
            .notification-bubble h3 {
                margin: 10px 0;
                color: var(--color-brown);
            }
            
            .notification-bubble p {
                margin: 10px 0;
                font-size: 16px;
                letter-spacing: 1px;
            }
            
            .close-notification {
                background: var(--color-beige);
                border: 1px solid var(--color-green);
                color: var(--color-brown);
                padding: 8px 20px;
                margin-top: 15px;
                border-radius: 5px;
                cursor: pointer;
                font-family: inherit;
                font-weight: bold;
                transition: all 0.2s;
            }
            
            .close-notification:hover {
                background: var(--color-green);
                color: var(--color-beige);
            }
        `;
        document.head.appendChild(styleElement);
        
        // Create overlay div for notification if it doesn't exist
        if (!document.getElementById('reward-notification-overlay')) {
            const overlay = document.createElement('div');
            overlay.id = 'reward-notification-overlay';
            document.body.appendChild(overlay);
        }
        // Function to show styled notification
        window.showStyledNotification = function(title, message, iconEmoji) {
            const overlay = document.getElementById('reward-notification-overlay');
            
            // Clear any existing notifications
            overlay.innerHTML = '';
            
            // Create notification element
            const notification = document.createElement('div');
            notification.className = 'notification-bubble';
            
            // Add content
            notification.innerHTML = `
                <span class="reward-icon">${iconEmoji}</span>
                <h3>${title}</h3>
                <p>${message}</p>
                <button class="close-notification">OK, GOT IT!</button>
            `;
            
            // Add notification to overlay
            overlay.appendChild(notification);
            
            // Show overlay with animation
            overlay.style.visibility = 'visible';
            overlay.style.opacity = '1';
            
            // Setup close button
            const closeButton = notification.querySelector('.close-notification');
            closeButton.addEventListener('click', function() {
                overlay.style.opacity = '0';
                setTimeout(() => {
                    overlay.style.visibility = 'hidden';
                }, 300);
            });
        };
        // Function to check if it's a new day since last login
        function isNewDay() {
            const lastLogin = localStorage.getItem('lastLoginDate');
            const today = new Date().toDateString();
            
            // Return true if there's no last login or if it's different from today
            return (lastLogin !== today);
        }
        
        // Function to update and get current streak
        function updateStreak() {
            let streak = parseInt(localStorage.getItem('loginStreak') || '0');
            let lastLoginDate = localStorage.getItem('lastLoginDateForStreak');
            const today = new Date();
            const yesterday = new Date(today);
            yesterday.setDate(yesterday.getDate() - 1);
            
            if (!lastLoginDate) {
                // First time login
                streak = 1;
            } else {
                const lastLogin = new Date(lastLoginDate);
                
                // If last login was yesterday, increment streak
                if (yesterday.toDateString() === lastLogin.toDateString()) {
                    streak += 1;
                } 
                // If last login was before yesterday, reset streak
                else if (lastLogin < yesterday) {
                    streak = 1;
                }
                // If last login was today, maintain streak (don't increment)
            }
            
            localStorage.setItem('loginStreak', streak.toString());
            localStorage.setItem('lastLoginDateForStreak', today.toDateString());
            
            return streak;
        }
        
        // Get rewards based on the day of the week
        function getDailyReward(dayNumber) {
            const rewards = [
                { day: 1, name: "10 Forum Points", icon: "🎁", type: "points" },
                { day: 2, name: "Dark Mode Theme", icon: "🌙", type: "theme", themeId: "dark" },
                { day: 3, name: "15 Forum Points", icon: "🎁", type: "points" },
                { day: 4, name: "Ocean Theme", icon: "🌊", type: "theme", themeId: "ocean" },
                { day: 5, name: "20 Forum Points", icon: "🎁", type: "points" },
                { day: 6, name: "Sunset Theme", icon: "🌅", type: "theme", themeId: "sunset" },
                { day: 7, name: "Cosmic Theme", icon: "✨", type: "theme", themeId: "cosmic" }
            ];
            
            return rewards[dayNumber - 1];
        }
        
        // Create the forum points display element
        const pointsDisplay = document.createElement('div');
        pointsDisplay.id = 'forumPointsDisplay';
        pointsDisplay.className = 'forum-points-display';
        
        // Get current points or default to 0
        const currentPoints = parseInt(localStorage.getItem('forumPoints') || '0');
        
        // Set initial HTML content
        pointsDisplay.innerHTML = `
            <div class="points-bubble">
                <span class="points-icon">🏆</span>
                <span class="points-value">${currentPoints}</span>
                <span class="points-label">Points</span>
            </div>
        `;
        
        // Add styles
        const pointsStyles = document.createElement('style');
        pointsStyles.textContent = `
            /* Points counter adjustments for mobile */
            .forum-points-display {
                position: fixed;
                top: 10px;
                left: 10px;
                z-index: 1000;
            }

            .points-bubble {
                transform: translatey(0px);
                animation: float 5s ease-in-out infinite;
                text-align: center;
                text-transform: uppercase;
                font-weight: bold;
                letter-spacing: 2px;
                font-size: 13px;
                color: var(--color-brown);
                background-color: var(--color-beige);
                padding: 8px 12px;
                border-radius: 8px;
                position: relative;
                box-shadow: 6px 6px var(--color-blue);
                font-family: "Baloo 2", cursive, sans-serif;
                border: 1px solid var(--color-green);
                display: flex;
                align-items: center;
                gap: 6px;
                cursor: pointer;
            }

            .points-bubble:after {
                transform: translatey(0px);
                animation: float2 5s ease-in-out infinite;
                content: ".";
                font-weight: bold;
                -webkit-text-stroke: 0.5px var(--color-green);
                -webkit-text-fill-color: var(--color-beige);
                border: 1px solid var(--color-green);
                text-shadow: 6px 6px var(--color-blue);
                text-align: left;
                font-size: 18px;
                width: 20px;
                height: 4px;
                line-height: 20px;
                border-radius: 8px;
                background-color: var(--color-beige);
                position: absolute;
                display: block;
                bottom: -10px;
                left: 0;
                box-shadow: 6px 6px var(--color-blue);
                z-index: -2;
            }

            .points-icon {
                font-size: 14px;
                margin-right: 2px;
            }

            .points-value {
                font-size: 14px;
                margin-right: 2px;
            }

            .points-label {
                font-size: 10px;
            }

            /* Modal/popup container styles */
            .modal-container {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background-color: rgba(0, 0, 0, 0.5);
                display: flex;
                justify-content: center;
                align-items: center;
                z-index: 2000;
                overflow-y: auto; /* Enable vertical scrolling */
                padding: 20px 0;
            }

            /* Modal content styles */
            .modal-content {
                background-color: var(--color-beige);
                border-radius: 12px;
                border: 1px solid var(--color-green);
                box-shadow: 10px 10px var(--color-blue);
                padding: 20px;
                width: 90%;
                max-width: 400px;
                max-height: 80vh; /* Limit height on mobile */
                overflow-y: auto; /* Make content scrollable */
                position: relative;
                margin: auto; /* Center in scrollable container */
            }

            /* Close button styles */
            .close-btn {
                position: sticky; /* Make the close button sticky */
                top: 0;
                right: 0;
                float: right;
                font-size: 20px;
                font-weight: bold;
                color: var(--color-brown);
                cursor: pointer;
                background: var(--color-beige);
                padding: 5px 10px;
                border-radius: 5px;
                z-index: 10;
            }

            /* Email form adjustments */
            .email-form {
                margin-top: 15px;
                display: flex;
                flex-direction: column;
                gap: 10px;
                width: 100%;
                box-sizing: border-box;
            }

            .email-input {
                padding: 8px 12px;
                border-radius: 6px;
                border: 1px solid var(--color-green);
                font-family: inherit;
                font-size: 13px;
                width: 100%;
                box-sizing: border-box;
            }

            .submit-btn {
                background-color: var(--color-yellow);
                color: var(--color-brown);
                border: 1px solid var(--color-green);
                border-radius: 6px;
                padding: 10px 15px;
                font-family: inherit;
                font-weight: bold;
                text-transform: uppercase;
                cursor: pointer;
                transition: all 0.2s;
                letter-spacing: 1px;
                font-size: 13px;
                margin-bottom: 15px; /* Add space above success message */
            }

            .success-message {
                background-color: rgba(129, 199, 132, 0.2);
                border: 1px solid var(--color-green);
                color: var(--color-brown);
                padding: 12px;
                border-radius: 6px;
                margin-top: 12px;
                text-align: center;
                display: none;
                font-size: 13px;
            }

            /* Media queries for responsive design */
            @media screen and (max-width: 480px) {
                .forum-points-display {
                    top: 5px;
                    left: 5px;
                }
                
                .points-bubble {
                    padding: 6px 10px;
                    font-size: 11px;
                    letter-spacing: 1px;
                    box-shadow: 4px 4px var(--color-blue);
                }
                
                .points-bubble:after {
                    font-size: 16px;
                    width: 16px;
                    height: 3px;
                    box-shadow: 4px 4px var(--color-blue);
                    text-shadow: 4px 4px var(--color-blue);
                    bottom: -8px;
                }
                
                .points-icon, .points-value {
                    font-size: 12px;
                }
                
                .points-label {
                    font-size: 9px;
                }
                
                .modal-content {
                    padding: 15px;
                    width: 85%;
                    max-height: 75vh;
                }
                
                .close-btn {
                    padding: 3px 8px;
                    font-size: 18px;
                }
                
                .email-form {
                    margin-top: 10px;
                    gap: 8px;
                }
                
                .email-input, .submit-btn {
                    padding: 8px 10px;
                    font-size: 12px;
                }
            }
        `;
        
        // Add the elements to the document
        document.head.appendChild(pointsStyles);
        document.body.appendChild(pointsDisplay);
        
        // Function to update points display
        window.updatePointsDisplay = function(newPoints) {
            const pointsValueElement = document.querySelector('.points-value');
            const oldPoints = parseInt(pointsValueElement.textContent);
            
            // Update the points display
            pointsValueElement.textContent = newPoints;
            
            // Add animation class if points increased
            if (newPoints > oldPoints) {
                pointsValueElement.classList.add('points-increment');
                setTimeout(() => {
                    pointsValueElement.classList.remove('points-increment');
                }, 800);
            }
        };
        // ✅ Self-Updating Daily Streak Banner Logic
function updateStreakBannerDisplay() {
  const streakBanner = document.getElementById('streakBanner');
  const today = new Date().toDateString();
  const lastLoginDate = localStorage.getItem('lastLoginDateForStreak');
  const lastShownDate = localStorage.getItem('lastBannerShownDate');
  let currentStreak = parseInt(localStorage.getItem('loginStreak') || '0');

  // If already shown today, don't repeat
  if (lastShownDate === today) return;

  if (!lastLoginDate) {
    currentStreak = 1;
  } else {
    const yesterday = new Date(Date.now() - 86400000).toDateString();
    if (lastLoginDate === yesterday) {
      currentStreak += 1;
    } else if (lastLoginDate !== today) {
      currentStreak = 1;
    }
  }

  // Save new streak and last login
  localStorage.setItem('loginStreak', currentStreak);
  localStorage.setItem('lastLoginDateForStreak', today);
  localStorage.setItem('lastBannerShownDate', today);

  if (streakBanner) {
    streakBanner.textContent = `🔥 You're on a ${currentStreak}-day streak! Keep it up! Come back tomorrow for more rewards!`;
    streakBanner.style.display = 'block';

    // Optional: glow effect on streaks 3+
    if (currentStreak >= 3) {
      streakBanner.classList.add('glow-reward');
    } else {
      streakBanner.classList.remove('glow-reward');
    }
  }
}

window.addEventListener('DOMContentLoaded', () => {
  updateStreakBannerDisplay();
});

        // Listen for points changes in local storage
        window.addEventListener('storage', function(e) {
            if (e.key === 'forumPoints') {
                updatePointsDisplay(parseInt(e.newValue || '0'));
            }
        });

        // Make points display clickable to show points info and email collection
        pointsDisplay.addEventListener('click', function() {
            showPointsEmailCollector();
        });
        
        // Function to show points info and email collection modal
    function showPointsEmailCollector() {
        // Create modal if it doesn't exist
        let pointsModal = document.getElementById('pointsDetailModal');
        
        if (!pointsModal) {
            pointsModal = document.createElement('div');
            pointsModal.id = 'pointsDetailModal';
            pointsModal.className = 'modal';
            pointsModal.style.cssText = `
                display: none;
                position: fixed;
                z-index: 9999;
                left: 0;
                top: 0;
                width: 100%;
                height: 100%;
                background-color: rgba(0,0,0,0.7);
                justify-content: center;
                align-items: center;
            `;
            
            const modalContent = document.createElement('div');
            modalContent.className = 'modal-content notification-bubble';
            modalContent.style.cssText = `
                background-color: var(--color-beige);
                border-radius: 11px;
                padding: 25px;
                width: 80%;
                max-width: 500px;
                border: 1px solid var(--color-green);
                box-shadow: 20px 20px var(--color-blue);
                position: relative;
                animation: popIn 0.3s ease-out;
            `;
            
            modalContent.innerHTML = `
                <span class="reward-icon">✨</span>
                <h2 style="color: var(--color-brown); margin-top: 5px; text-transform: uppercase; letter-spacing: 2px;">Coming Soon!</h2>
                <div style="margin: 20px 0; text-align: center;">
                    <p style="font-size: 16px; margin-bottom: 15px;">Forum Points will be part of an upcoming update! They'll allow you to:</p>
                    <ul style="text-align: left; padding-left: 20px; margin-bottom: 20px;">
                        <li>Upvote/downvote posts and comments</li>
                        <li>Create custom profile badges</li>
                        <li>Access exclusive forum sections</li>
                        <li>Unlock special themes</li>
                    </ul>
                    <p style="font-size: 16px; margin-bottom: 10px;">Want to stay in the loop? Enter your email below for updates!</p>
                </div>
                
                <form id="emailSignupForm" class="email-form">
                    <input type="email" class="email-input" id="emailInput" placeholder="Your email address" required>
                    <button type="submit" class="submit-btn">Stay Updated</button>
                </form>
                
                <div id="successMessage" class="success-message">
                    <p>Thank you! We'll keep you updated on all Forum Points news!</p>
                </div>
                
                <button id="closePointsModal" class="close-notification" style="margin-top: 15px;">Close</button>
            `;
            
            pointsModal.appendChild(modalContent);
            document.body.appendChild(pointsModal);
            
            // Add close button functionality
            document.getElementById('closePointsModal').addEventListener('click', function() {
                pointsModal.style.display = 'none';
            });
            
            // Add form submission handler
            document.getElementById('emailSignupForm').addEventListener('submit', function(e) {
                e.preventDefault();
                
                const email = document.getElementById('emailInput').value;
                if (email && validateEmail(email)) {
                    // Store that this user has signed up
                    localStorage.setItem('emailSignedUp', 'true');
                    
                    // Send email to site owner with the user's email
                    sendEmailToSiteOwner(email);
                    
                    // Show success message
                    document.getElementById('emailSignupForm').style.display = 'none';
                    document.getElementById('successMessage').style.display = 'block';
                }
            });
        }
        
        // Check if user already signed up
        const alreadySignedUp = localStorage.getItem('emailSignedUp') === 'true';
        if (alreadySignedUp) {
            document.getElementById('emailSignupForm').style.display = 'none';
            document.getElementById('successMessage').style.display = 'block';
        } else {
            document.getElementById('emailSignupForm').style.display = 'flex';
            document.getElementById('successMessage').style.display = 'none';
        }
        
        // Show the modal
        pointsModal.style.display = 'flex';
    }
    
    // Email validation function
    function validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(String(email).toLowerCase());
    }
    
    // Function to send email to site owner
    function sendEmailToSiteOwner(userEmail) {
        // Create a hidden form for submission
        const form = document.createElement('form');
        form.method = 'POST';
        form.action = '/submit-email'; // Update this to your server endpoint
        form.style.display = 'none';
        
        // Create an input for the email address
        const emailInput = document.createElement('input');
        emailInput.type = 'email';
        emailInput.name = 'userEmail';
        emailInput.value = userEmail;
        
        // Create hidden input for destination email
        const destinationInput = document.createElement('input');
        destinationInput.type = 'hidden';
        destinationInput.name = 'destination';
        destinationInput.value = 'youyounews.live@gmail.com';
        
        // Create hidden input for subject
        const subjectInput = document.createElement('input');
        subjectInput.type = 'hidden';
        subjectInput.name = 'subject';
        subjectInput.value = 'New Forum Points Update Subscriber';
        
        // Add all inputs to form
        form.appendChild(emailInput);
        form.appendChild(destinationInput);
        form.appendChild(subjectInput);
        
        // Add form to document and submit
        document.body.appendChild(form);
        
        // Submit using fetch API instead of form submission
        fetch('/submit-email', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                userEmail: userEmail,
                destination: 'youyounews.live@gmail.com',
                subject: 'New Forum Points Update Subscriber'
            })
        })
        .catch(error => {
            console.error('Error sending email signup:', error);
        });
        
        // Remove form
        document.body.removeChild(form);
    }
        // Create weekly rewards display
        function createWeeklyRewardsDisplay() {
            const weeklyRewardsContainer = document.getElementById('weeklyRewards');
            weeklyRewardsContainer.innerHTML = '';
            
            // Use a new variable for claimed days instead of login days
            const loginDays = parseInt(localStorage.getItem('loginDays') || '0');
            const claimedDays = parseInt(localStorage.getItem('claimedDays') || '0');
            
            for (let i = 1; i <= 7; i++) {
                const reward = getDailyReward(i);
                const dayElement = document.createElement('div');
                // Use claimedDays for determining if checkmark should be shown
                dayElement.style.cssText = 'width: 60px; height: 90px; margin: 5px; display: flex; flex-direction: column; align-items: center; justify-content: space-between; border-radius: 8px; background-color: ' + (i <= loginDays ? '#f4f4f8' : '#f4f4f8') + '; position: relative; padding: 5px 2px;';
                
                // Highlight current day
                if (i === loginDays) {
                    dayElement.style.border = '2px solid #3498db';
                }
                
                const dayNumber = document.createElement('div');
                dayNumber.style.cssText = 'width: 100%; text-align: left; font-size: 12px; font-weight: bold; margin-bottom: 5px;';
                dayNumber.textContent = 'Day ' + i;
                
                const icon = document.createElement('div');
                icon.style.cssText = 'font-size: 24px; margin: 4px 0;';
                icon.textContent = reward.icon;
                
                const rewardName = document.createElement('div');
                rewardName.style.cssText = 'width: 100%; font-size: 10px; text-align: center; padding: 0 2px; margin-top: 4px;';
                rewardName.textContent = reward.name;
                
                // Only show checkmark for claimed days
                if (i <= claimedDays) {
                    const checkmark = document.createElement('div');
                    checkmark.style.cssText = 'position: absolute; top: -5px; right: -5px; background-color: #4caf50; color: white; border-radius: 50%; width: 20px; height: 20px; display: flex; align-items: center; justify-content: center; font-size: 12px;';
                    checkmark.innerHTML = '✓';
                    dayElement.appendChild(checkmark);
                    
                    // Also change background to indicate claimed
                    dayElement.style.backgroundColor = '#c8e6c9';
                }
                
                dayElement.appendChild(dayNumber);
                dayElement.appendChild(icon);
                dayElement.appendChild(rewardName);
                weeklyRewardsContainer.appendChild(dayElement);
            }
        }
        
        // Display login reward modal
        function showLoginRewards() {
            const modal = document.getElementById('loginRewardsModal');
            modal.style.display = 'flex';
            
            // Update streak counter
            const streak = updateStreak();
            document.getElementById('currentStreak').textContent = streak;
            
            // Manage weekly login days
            let loginDays = parseInt(localStorage.getItem('loginDays') || '0');
            const claimedDays = parseInt(localStorage.getItem('claimedDays') || '0');
            const lastResetWeek = localStorage.getItem('lastResetWeek');
            const currentWeek = getWeekNumber(new Date());
            
            // Reset counters if it's a new week
            if (lastResetWeek !== currentWeek) {
                loginDays = 0;
                localStorage.setItem('loginDays', '0');
                localStorage.setItem('claimedDays', '0');
                localStorage.setItem('lastResetWeek', currentWeek);
            }
            
            // Check if it's a new day for reward purposes
            const newDay = isNewDay();
            
            // Increment login days if it's a new day and we haven't hit 7 yet
            if (newDay && loginDays < 7) {
                loginDays = Math.max(loginDays, claimedDays + 1);
                localStorage.setItem('loginDays', loginDays.toString());
            }
            
            // Create weekly rewards display
            createWeeklyRewardsDisplay();
            
            // Display today's reward - show the next unclaimed reward
            const nextDay = claimedDays + 1;
            const todayReward = getDailyReward(nextDay);
            
            document.getElementById('rewardMessage').textContent = newDay ? 
                `Today's reward: ${todayReward.icon} ${todayReward.name}` : 
                "You already claimed today\'s reward. Come back tomorrow!";
            
            // Enable or disable claim button
            const claimButton = document.getElementById('claimReward');
            claimButton.disabled = !newDay;
            claimButton.style.backgroundColor = newDay ? '#3498db' : '#cccccc';
        }
        
        // Get week number of the year
        function getWeekNumber(date) {
            const firstDayOfYear = new Date(date.getFullYear(), 0, 1);
            const pastDaysOfYear = (date - firstDayOfYear) / 86400000;
            return Math.ceil((pastDaysOfYear + firstDayOfYear.getDay() + 1) / 7).toString();
        }
        
        // Function to unlock a theme
        function unlockTheme(themeId) {
            // Get currently unlocked themes
            let unlockedThemes = JSON.parse(localStorage.getItem('unlockedThemes') || '["default"]');
            
            // Add the new theme if it's not already unlocked
            if (!unlockedThemes.includes(themeId)) {
                unlockedThemes.push(themeId);
                localStorage.setItem('unlockedThemes', JSON.stringify(unlockedThemes));
            }
        }
        
        // Function to check if a theme is unlocked
        function isThemeUnlocked(themeId) {
            const unlockedThemes = JSON.parse(localStorage.getItem('unlockedThemes') || '["default"]');
            return unlockedThemes.includes(themeId);
        }
        
        // Function to apply a theme
        function applyTheme(themeId) {
            // Find the theme
            const theme = themes.find(t => t.id === themeId);
            if (!theme) return;
            
            // Create or update theme style element
            let themeStyle = document.getElementById('custom-theme-style');
            if (!themeStyle) {
                themeStyle = document.createElement('style');
                themeStyle.id = 'custom-theme-style';
                document.head.appendChild(themeStyle);
            }
            
            // Build CSS based on theme properties
            let css = '';
            
            if (theme.background) {
                css += `body { background: ${theme.background}; }\n`;
            }
            
            if (theme.textColor) {
                css += `body { color: ${theme.textColor}; }\n`;
                css += `.section-content p { color: ${theme.textColor}; }\n`;
            }
            
            if (theme.headerBackground) {
                css += `header { background: ${theme.headerBackground}; }\n`;
            }
            
            if (theme.navBackground) {
                css += `nav { background-color: ${theme.navBackground}; }\n`;
            }
            
            if (theme.accentColor) {
                css += `.cta-button { background-color: ${theme.accentColor}; }\n`;
                css += `.cta-button:hover { background-color: ${theme.accentColor}cc; }\n`;
            }
            
            // Apply styles
            themeStyle.textContent = css;
            
            // Save current theme
            localStorage.setItem('currentTheme', themeId);
        }
        
        // Function to show theme selection modal
        function showThemeSelector() {
            const themeModal = document.getElementById('themeModal');
            const themeGrid = document.getElementById('themeGrid');
            
            // Clear previous themes
            themeGrid.innerHTML = '';
            
            // Get currently selected theme
            const currentTheme = localStorage.getItem('currentTheme') || 'default';
            
            // Get unlocked themes
            const unlockedThemes = JSON.parse(localStorage.getItem('unlockedThemes') || '["default"]');
            
            // Add each theme to the grid
            themes.forEach(theme => {
                const isUnlocked = unlockedThemes.includes(theme.id);
                const isSelected = theme.id === currentTheme;
                
                const themeCard = document.createElement('div');
                themeCard.className = 'theme-card';
                themeCard.dataset.themeId = theme.id;
                
                // Style for theme card
                let cardStyle = `
                    border-radius: 8px;
                    padding: 10px;
                    height: 120px;
                    display: flex;
                    flex-direction: column;
                    justify-content: space-between;
                    align-items: center;
                    cursor: ${isUnlocked ? 'pointer' : 'not-allowed'};
                    position: relative;
                    background: ${theme.background || 'var(--light-bg)'};
                    color: ${theme.textColor || '#333'};
                    border: ${isSelected ? '3px solid #3498db' : '1px solid #ddd'};
                    opacity: ${isUnlocked ? '1' : '0.7'};
                    transition: transform 0.2s, box-shadow 0.2s;
                `;
                
                if (isUnlocked) {
                    cardStyle += `
                        &:hover {
                            transform: translateY(-5px);
                            box-shadow: 0 5px 15px rgba(0,0,0,0.2);
                        }
                    `;
                }
                
                themeCard.style.cssText = cardStyle;
                
                // Theme name
                const themeName = document.createElement('h3');
                themeName.textContent = theme.name;
                themeName.style.cssText = `
                    margin: 0;
                    font-size: 14px;
                    text-align: center;
                    font-weight: bold;
                `;
                
                // Theme description
                const themeDesc = document.createElement('p');
                themeDesc.textContent = theme.description;
                themeDesc.style.cssText = `
                    margin: 0;
                    font-size: 12px;
                    text-align: center;
                `;
                
                // Lock icon for locked themes
                if (!isUnlocked) {
                    const lockIcon = document.createElement('div');
                    lockIcon.textContent = '🔒';
                    lockIcon.style.cssText = `
                        position: absolute;
                        top: 5px;
                        right: 5px;
                        font-size: 16px;
                    `;
                    themeCard.appendChild(lockIcon);
                }
                
                // Selected indicator
                if (isSelected) {
                    const selectedIndicator = document.createElement('div');
                    selectedIndicator.textContent = '✓';
                    selectedIndicator.style.cssText = `
                        position: absolute;
                        bottom: 5px;
                        right: 5px;
                        background-color: #3498db;
                        color: white;
                        border-radius: 50%;
                        width: 20px;
                        height: 20px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        font-size: 12px;
                    `;
                    themeCard.appendChild(selectedIndicator);
                }
                
                // Add elements to card
                themeCard.appendChild(themeName);
                themeCard.appendChild(themeDesc);
                
                // Add click handler
                if (isUnlocked) {
                    themeCard.addEventListener('click', function() {
                        // Deselect all themes
                        document.querySelectorAll('.theme-card').forEach(card => {
                            card.style.border = '1px solid #ddd';
                            
                            // Remove check mark if it exists
                            const check = card.querySelector('div[style*="background-color: #3498db"]');
                            if (check) card.removeChild(check);
                        });
                        
                        // Select this theme
                        this.style.border = '3px solid #3498db';
                        
                        // Add selected indicator
                        const selectedIndicator = document.createElement('div');
                        selectedIndicator.textContent = '✓';
                        selectedIndicator.style.cssText = `
                            position: absolute;
                            bottom: 5px;
                            right: 5px;
                            background-color: #3498db;
                            color: white;
                            border-radius: 50%;
                            width: 20px;
                            height: 20px;
                            display: flex;
                            align-items: center;
                            justify-content: center;
                            font-size: 12px;
                        `;
                        this.appendChild(selectedIndicator);
                        document.querySelectorAll('.theme-card').forEach(card => {
  card.classList.remove('selected-theme');
});
                        this.style.border = '3px solid #3498db';
                        this.classList.add('selected-theme');
                        // Live preview the clicked theme
applyTheme(this.dataset.themeId);

                    });
                }
                
                themeGrid.appendChild(themeCard);
            });
            
            themeModal.style.display = 'flex';
        }
        document.getElementById('rewardsButton').addEventListener('click', function(e) {
            e.preventDefault();
            showLoginRewards();
        });
        
        document.getElementById('themesButton').addEventListener('click', function(e) {
            e.preventDefault();
            showThemeSelector();
        });
        
        // Close modals
        document.getElementById('closeModal').addEventListener('click', function() {
            document.getElementById('loginRewardsModal').style.display = 'none';
        });
        
        document.getElementById('closeThemeModal').addEventListener('click', function() {
            document.getElementById('themeModal').style.display = 'none';
        });
        
        document.getElementById('cancelTheme').addEventListener('click', function() {
            document.getElementById('themeModal').style.display = 'none';
        });
        
        // Apply selected theme
        document.getElementById('applyTheme').addEventListener('click', function() {
            const selectedTheme = document.querySelector('.theme-card.selected-theme');
            if (selectedTheme) {
                const themeId = selectedTheme.dataset.themeId;
                applyTheme(themeId);
                document.getElementById('themeModal').style.display = 'none';
            }
        });
        const originalClaimReward = document.getElementById('claimReward').onclick;
    if (document.getElementById('claimReward')) {
        document.getElementById('claimReward').onclick = null; // Remove existing handler if any
        
        document.getElementById('claimReward').addEventListener('click', function() {
            if (isNewDay()) {
                // Get current claimed days and increment
                let claimedDays = parseInt(localStorage.getItem('claimedDays') || '0');
                claimedDays++;
                
                // Get the reward for the next unclaimed day
                const reward = getDailyReward(claimedDays);
                
                // Handle different reward types
                if (reward.type === 'theme' && reward.themeId) {
                    unlockTheme(reward.themeId);
                    
                    showStyledNotification(
                        "Theme Unlocked!",
                        `You've unlocked the ${reward.name} -- come back in 24 hours for your next gift!! 🎁`,
                        reward.icon
                    );
                } else if (reward.type === 'points') {
                    // Add points to user account
                    let currentPoints = parseInt(localStorage.getItem('forumPoints') || '0');
                    const pointsToAdd = parseInt(reward.name.match(/\d+/)[0]); // Extract number from reward name
                    currentPoints += pointsToAdd;
                    localStorage.setItem('forumPoints', currentPoints.toString());
                    
                    // Update points display
                    updatePointsDisplay(currentPoints);
                    
                    showStyledNotification(
                        "Points Earned!",
                        `Come back in 24 hours for your next gift!! 🎁`,
                        reward.icon
                    );
                }
                
                // Save claimed days
                localStorage.setItem('claimedDays', claimedDays.toString());
                
                // Mark as claimed for today
                localStorage.setItem('lastLoginDate', new Date().toDateString());
                
                // Update UI
                document.getElementById('rewardMessage').textContent = "You already claimed today\'s reward. Come back tomorrow!";
                this.disabled = true;
                this.style.backgroundColor = '#cccccc';
                
                // Update the weekly rewards display to show the checkmark
                if (typeof createWeeklyRewardsDisplay === 'function') {
                    createWeeklyRewardsDisplay();
                }
            }
        });
    }
        
        // Make points display clickable to show points history/details
        pointsDisplay.addEventListener('click', function() {
            showPointsDetails();
        });
        
        // Apply saved theme if any
        const savedTheme = localStorage.getItem('currentTheme');
        if (savedTheme) {
            applyTheme(savedTheme);
        }
        
        // Add animations
        const style = document.createElement('style');
        style.textContent = `
            @keyframes popIn {
                0% { transform: scale(0.8); opacity: 0; }
                100% { transform: scale(1); opacity: 1; }
            }
            
            /* Fix for reward boxes to prevent text overflow */
            #weeklyRewards > div {
                display: flex;
                flex-direction: column;
                justify-content: space-between;
            }
            
            .theme-card:hover {
                transform: translateY(-5px);
                box-shadow: 0 5px 15px rgba(0,0,0,0.2);
            }
        `;
        document.head.appendChild(style);
    });
</script>
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
    <script>
        // Create an array of funny whale responses
        const whaleResponses = [
        "That tickles!",
        "*Whale noise*",
        "Oo...I like that :)",
        "Wheee!",
        "Hello human!",
        "Need a ride?",
        "vroom goes the roomba",
        "What language do gnomes speak?",
        "wtf is the uscmind challenge",
        "Love LePookie",
        "Gojo should have beat Sukuna",
        "Which ninja turtle is Mbappé?",
        "Moo",
        "Why do dogs say 'bark?' that does not sound like 'bark' to me",
        "I JUST WANT TO BE PART OF YOUR SYMPHONYYYYY",
        "lalala :o",
        "emotional damage",
        "popular mmos' intro was so fire",
        "shinra tensei",
        "wheeeeeeeeeeeeeeeeeee",
        "Shrek or Kung Fu Panda?",
        "It's that me espresso >:)",
        "Thanks for logging in!",
        "Wow, thanks for using our website!",
        "you're a champ! <3",
        "*happy whale noises",
        "i bet SGA is at the free throw line rn",
        "Have a great day!!!",
        "Manifesting good things for u",
        "You're my super idol",
        "**talk no jutsu",
        "look at curry, so inspirational",
        "biden on the epstein list??",
        "You're the real MVP!",
        "you are enough :)",
        "this whale is here for u :>",
        "alexa, how do i slide in dms?",
        "...uh, fein, fein fein?",
        "So 2 penguins walked into a bar...BANG",
        "Could u beat Olaf in a fight?",
        "LET IT GOOOO, LET IT GOOOOO",
        "'how much do u bench bro' is crazy",
        "yap yap yap",
        "Toronto wind is CRAZY",
        "Imagine ur in Cancun..ahhhh :>",
        "Stay home, cook rice - Ryan Higa",
        "I'm a fish (whatttttt)",
        "Happy bday to uuuu",
        "Hiii",
        "netflix n chill?",
        "You're awesome!",
        "You're the best human i've met today",
        "Does Trump have fanfic?!?",
        "Jensen Huang is my goat",
        "How is it like being human?",
        "Read and read are different",
        "You're getting into Harvard",
        "BE CONFIDENT! If Benny Blanco can pull Selena Gomez, u can do anything",
        "You warm my heart :>"
        ];

        // Create a function to add the whale to the page
        function createSwimmingWhale() {
        // Create the whale element
        const whale = document.createElement('div');
        whale.className = 'swimming-whale';
        
        // Use an img element with the exact whale image
        whale.innerHTML = `
            <img src="/Assets/${localStorage.getItem('swimmingAnimal') || 'whale.png'}" alt="Swimming creature" />
        `;
        
        // Randomize starting position (top position)
        const startingPosition = Math.random() * (window.innerHeight - 150);
        
        // Set styles for the whale
        Object.assign(whale.style, {
            position: 'fixed',
            top: `${startingPosition}px`,
            left: '-300px', // Start off-screen 
            zIndex: '9999',
            filter: 'drop-shadow(3px 5px 8px rgba(0,0,0,0.3))',
            cursor: 'pointer' // Change cursor to indicate clickability
        });
        
        // Randomly select one of five movement patterns
        const patternNumber = Math.floor(Math.random() * 5) + 1;
        whale.style.animation = `swim-pattern-${patternNumber} ${patternNumber <= 3 ? '8s' : '25s'} forwards`;
        
        // Store active speech bubble
        let activeBubble = null;
        let bubbleRemovalTimeout = null;
        
        // Add click event listener for funny responses
        whale.addEventListener('click', function(e) {
            e.stopPropagation();
            
            // Remove existing bubble if there is one
            if (activeBubble && document.body.contains(activeBubble)) {
                document.body.removeChild(activeBubble);
                clearTimeout(bubbleRemovalTimeout);
            }
            
            // Create speech bubble container div with bbb class
            const bubbleContainer = document.createElement('div');
            bubbleContainer.className = 'bbb';
            
            // Create the actual bubble as an a element per your CSS
            const bubble = document.createElement('a');
            
            // Select random response
            const randomResponse = whaleResponses[Math.floor(Math.random() * whaleResponses.length)];
            bubble.textContent = randomResponse;
            
            // Add bubble to container
            bubbleContainer.appendChild(bubble);
            
            // Calculate responsive bubble size based on viewport width
            const viewportWidth = window.innerWidth;
            const bubbleWidth = Math.min(Math.max(viewportWidth * 0.15, 120), 200); // Between 120px and 200px
            
            // Position the bubble container near the whale
            const whaleRect = whale.getBoundingClientRect();
            
            // Position directly above the whale with minimal gap
            Object.assign(bubbleContainer.style, {
                position: 'fixed',
                left: `${whaleRect.left + (whaleRect.width / 2) - (bubbleWidth / 2)}px`,
                top: `${whaleRect.top - 10}px`, // Positioned much closer to whale
                height: 'auto',
                width: `${bubbleWidth}px`,
                margin: '0',
                display: 'grid',
                placeItems: 'center',
                zIndex: '10000',
                opacity: '1',
                transition: 'opacity 0.3s ease',
                pointerEvents: 'none'
            });
            
            // Add to body
            document.body.appendChild(bubbleContainer);
            activeBubble = bubbleContainer;
            
            // Remove after animation - shortened to 3 seconds
            bubbleRemovalTimeout = setTimeout(() => {
                bubbleContainer.style.opacity = '0';
                setTimeout(() => {
                    if (document.body.contains(bubbleContainer)) {
                    document.body.removeChild(bubbleContainer);
                    activeBubble = null;
                    }
                }, 300); // Faster fade out
            }, 3000); // Display time
        });
        
        // Set up animation tracking to move the speech bubble with the whale
        function updateBubblePosition() {
            if (activeBubble && document.body.contains(activeBubble) && document.body.contains(whale)) {
                const whaleRect = whale.getBoundingClientRect();
                const bubbleWidth = parseFloat(activeBubble.style.width);
                
                Object.assign(activeBubble.style, {
                    left: `${whaleRect.left + (whaleRect.width / 2) - (bubbleWidth / 2)}px`,
                    top: `${whaleRect.top - 20}px` // Keep bubble close during animation
                });
                
                requestAnimationFrame(updateBubblePosition);
            }
        }
        
        // Start tracking if needed
        whale.addEventListener('click', function() {
            if (activeBubble) {
                requestAnimationFrame(updateBubblePosition);
            }
        });
        
        // Add whale to the body
        document.body.appendChild(whale);
        
        // Remove the whale after animation completes
        const animationDuration = patternNumber <= 3 ? 8000 : 25000;
        setTimeout(() => {
            if (document.body.contains(whale)) {
                if (activeBubble && document.body.contains(activeBubble)) {
                    document.body.removeChild(activeBubble);
                }
                document.body.removeChild(whale);
            }
        }, animationDuration + 500);
        }

        // Create CSS for the whale animation with multiple patterns
        const style = document.createElement('style');
        style.textContent = `
        /* Pattern 1: Standard swim across - FAST */
        @keyframes swim-pattern-1 {
            0% {
                left: -300px;
                transform: scaleX(1) translateY(0px);
            }
            100% {
                left: calc(100vw + 300px);
                transform: scaleX(1) translateY(0px);
            }
        }
        
        /* Pattern 2: Swim with flip in the middle - FAST */
        @keyframes swim-pattern-2 {
            0% {
                left: -300px;
                transform: scaleX(1) translateY(0px) rotate(0deg);
            }
            20% {
                left: calc(30vw);
                transform: scaleX(1) translateY(0px) rotate(0deg);
            }
            30% {
                left: calc(40vw);
                transform: scaleX(1) translateY(0px) rotate(180deg);
            }
            40% {
                left: calc(50vw);
                transform: scaleX(1) translateY(0px) rotate(360deg);
            }
            100% {
                left: calc(100vw + 300px);
                transform: scaleX(1) translateY(0px) rotate(360deg);
            }
        }
        
        /* Pattern 3: Zigzag fast path - FAST */
        @keyframes swim-pattern-3 {
            0% {
                left: -300px;
                top: 50%;
            }
            20% {
                left: calc(20vw);
                top: 30%;
            }
            40% {
                left: calc(40vw);
                top: 70%;
            }
            60% {
                left: calc(60vw);
                top: 20%;
            }
            80% {
                left: calc(80vw);
                top: 60%;
            }
            100% {
                left: calc(100vw + 300px);
                top: 40%;
            }
        }
        
        /* Pattern 4: Lingering in the middle - SLOW */
        @keyframes swim-pattern-4 {
            0% {
                left: -300px;
                transform: scaleX(1) translateY(0px);
            }
            20% {
                left: calc(40vw);
                transform: scaleX(1) translateY(0px);
            }
            /* Linger in the center section */
            25% {
                left: calc(45vw);
                transform: scaleX(1) translateY(20px);
            }
            30% {
                left: calc(43vw);
                transform: scaleX(1) translateY(-10px);
            }
            35% {
                left: calc(47vw);
                transform: scaleX(1) translateY(15px);
            }
            40% {
                left: calc(42vw);
                transform: scaleX(1) translateY(-5px);
            }
            45% {
                left: calc(46vw);
                transform: scaleX(1) translateY(10px);
            }
            50% {
                left: calc(44vw);
                transform: scaleX(1) translateY(0px);
            }
            /* Continue swimming */
            55% {
                left: calc(50vw);
                transform: scaleX(1) translateY(0px);
            }
            90% {
                left: calc(100vw + 100px);
                transform: scaleX(1) translateY(10px);
            }
            100% {
                left: calc(100vw + 300px);
                transform: scaleX(1) translateY(0px);
            }
        }
        
        /* Pattern 5: Enter from top, exit from bottom - SLOW */
        @keyframes swim-pattern-5 {
            0% {
                left: -300px;
                top: 20%;
                transform: scaleX(1) rotate(15deg);
            }
            10% {
                left: calc(20vw);
                top: 10%;
                transform: scaleX(1) rotate(15deg);
            }
            50% {
                left: calc(50vw);
                top: 50%;
                transform: scaleX(1) rotate(30deg);
            }
            90% {
                left: calc(80vw);
                top: 90%;
                transform: scaleX(1) rotate(45deg);
            }
            100% {
                left: calc(90vw);
                top: 110%;
                transform: scaleX(1) rotate(45deg);
            }
        }
        
        .swimming-whale {
            will-change: transform;
            pointer-events: auto;
        }
        
        .swimming-whale img {
            height: 150px;
            width: auto;
        }
        
        /* Updated bubble styles with responsive sizing and closer positioning */
        .bbb {
            height: auto;
            margin: 0;
            display: grid;
            place-items: center;
            font: 1vw system-ui;
            background-color: var(--color-yellow, transparent);
        }

        .bbb a {
            transform: translatey(0px);
            animation: float 5s ease-in-out infinite;
            text-align: center;
            text-transform: uppercase;
            font-weight: bold;
            letter-spacing: 1px;
            font-size: clamp(10px, 1.2vw, 14px);
            color: var(--color-brown, #5d4037);
            background-color: var(--color-beige, #f5f5dc);
            padding: clamp(6px, 1.5vw, 15px);
            border-radius: 8px;
            position: relative;
            box-shadow: 6px 6px var(--color-blue, #2196f3);
            font-family: "Baloo 2", cursive;
            border: 1px solid var(--color-green, #4caf50);
            width: 100%;
            box-sizing: border-box;
            word-wrap: break-word;
            line-height: 1.3;
        }
        
        .bbb a:after {
            transform: translatey(0px);
            animation: float2 5s ease-in-out infinite;
            content: ".";
            font-weight: bold;
            -webkit-text-stroke: 0.5px var(--color-green, #4caf50);
            -webkit-text-fill-color: var(--color-beige, #f5f5dc);
            border: 1px solid var(--color-green, #4caf50);
            text-shadow: 6px 6px var(--color-blue, #2196f3);
            text-align: left;
            font-size: clamp(18px, 2vw, 25px);
            width: clamp(18px, 2vw, 25px);
            height: 6px;
            line-height: 15px;
            border-radius: 6px;
            background-color: var(--color-beige, #f5f5dc);
            position: absolute;
            display: block;
            bottom: -15px;
            left: 10%;
            box-shadow: 6px 6px var(--color-blue, #2196f3);
            z-index: -2;
        }
        
        /* Adding the float animations that were referenced but missing */
        @keyframes float {
            0% {
                transform: translatey(0px);
            }
            50% {
                transform: translatey(-4px);
            }
            100% {
                transform: translatey(0px);
            }
        }
        
        @keyframes float2 {
            0% {
                transform: translatey(0px);
            }
            50% {
                transform: translatey(-2px);
            }
            100% {
                transform: translatey(0px);
            }
        }
        `;
        document.head.appendChild(style);

        // Function to trigger whale randomly
        function scheduleWhaleAppearance() {
        // Random time between 20 and 60 seconds
        const nextAppearance = 20000 + Math.random() * 15000;
        
        setTimeout(() => {
            createSwimmingWhale();
            scheduleWhaleAppearance(); // Schedule next appearance
        }, nextAppearance);
        }

        // Start the random whale appearances when the page loads
        window.addEventListener('load', () => {
        // Show one whale shortly after page load
        setTimeout(createSwimmingWhale, 3000);
        
        // Schedule random appearances
        scheduleWhaleAppearance();
        });

        // Add window resize handler to adjust bubble size if active
        window.addEventListener('resize', () => {
        const activeBubble = document.querySelector('.bbb');
        if (activeBubble) {
            const viewportWidth = window.innerWidth;
            const bubbleWidth = Math.min(Math.max(viewportWidth * 0.15, 120), 200);
            activeBubble.style.width = `${bubbleWidth}px`;
            
            // Adjust position if whale is still visible
            const whale = document.querySelector('.swimming-whale');
            if (whale) {
            const whaleRect = whale.getBoundingClientRect();
            activeBubble.style.left = `${whaleRect.left + (whaleRect.width / 2) - (bubbleWidth / 2)}px`;
            }
        }
        });
    </script>
    <script>
        document.addEventListener("DOMContentLoaded", function () {
            const rewardBtn = document.getElementById("rewardsButton");
            const claimBtn = document.getElementById("claimReward");
            const today = new Date().toDateString();
        
            function updateGlowState() {
                const claimed = localStorage.getItem("dailyRewardClaimed");
                if (claimed === today) {
                    rewardBtn.classList.remove("glow-reward");
                } else {
                    rewardBtn.classList.add("glow-reward");
                }
            }
        
            // Always update on page load
            updateGlowState();
        
            // Attach glow removal after claim
            if (claimBtn) {
                claimBtn.addEventListener("click", function () {
                    localStorage.setItem("dailyRewardClaimed", today);
                    updateGlowState();
                });
            }
        });
        </script>        
        <script>
// ================================
// PHASE 1: Engagement Boosters
// ================================

// 🔥 Daily Streak Logic
function updateStreak() {
  const today = new Date().toDateString();
  const lastClaimed = localStorage.getItem('lastRewardClaim') || '';
  let currentStreak = parseInt(localStorage.getItem('rewardStreak') || '0');

  if (today !== lastClaimed) {
    const yesterday = new Date(Date.now() - 86400000).toDateString();
    currentStreak = (lastClaimed === yesterday) ? currentStreak + 1 : 1;
    localStorage.setItem('rewardStreak', currentStreak);
    localStorage.setItem('lastRewardClaim', today);
    localStorage.setItem('streakClaimedToday', 'true');
    grantStreakReward(currentStreak);
  }
}

function displayStreakBanner() {
  const streak = parseInt(localStorage.getItem('rewardStreak') || '0');
  const banner = document.getElementById('streakBanner');
  if (banner) {
    banner.textContent = `🔥 You're on a ${streak}-day streak! Keep it up!`;
    banner.style.display = 'block';
  }
  updateStreakProgressBar(streak);
}

function grantStreakReward(streak) {
  let reward = '';
  if (streak === 7) {
    reward = '🎉 Bonus Theme Unlocked!';
    unlockTheme('midnight_whale');
  } else {
    reward = `+${10 * streak} stars added!`;
  }

  const rewardMessage = document.createElement('div');
  rewardMessage.textContent = `✅ Daily Reward: ${reward}`;
  rewardMessage.style.cssText = `
    position: fixed;
    bottom: 20px;
    right: 20px;
    background-color: #f9cdad;
    color: #5d4037;
    font-weight: bold;
    padding: 12px 18px;
    border-radius: 10px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.3);
    z-index: 10000;
    font-family: 'Baloo 2', cursive;
  `;
  document.body.appendChild(rewardMessage);

  setTimeout(() => {
    rewardMessage.remove();
  }, 5000);

  // Optional: increment points if you have a system
  let stars = parseInt(localStorage.getItem('userStars') || '0');
  stars += 10 * streak;
  localStorage.setItem('userStars', stars);
}

function unlockTheme(themeId) {
  const unlockedThemes = JSON.parse(localStorage.getItem('unlockedThemes') || '[]');
  if (!unlockedThemes.includes(themeId)) {
    unlockedThemes.push(themeId);
    localStorage.setItem('unlockedThemes', JSON.stringify(unlockedThemes));
  }
}

// 🌟 Streak Progress Bar Visual Update
function updateStreakProgressBar(streak) {
  const progressContainer = document.getElementById('streakProgressContainer');
  if (!progressContainer) return;

  progressContainer.innerHTML = '';
  for (let i = 1; i <= 7; i++) {
    const day = document.createElement('div');
    day.className = 'streak-day';
    day.textContent = `Day ${i}`;
    day.style.cssText = `
      width: 40px;
      height: 40px;
      margin: 5px;
      border-radius: 8px;
      display: flex;
      align-items: center;
      justify-content: center;
      background-color: ${i <= streak ? '#4caf50' : '#ccc'};
      color: white;
      font-weight: bold;
      font-size: 12px;
      font-family: 'Baloo 2', cursive;
    `;
    progressContainer.appendChild(day);
  }
}

// 🐳 Whale Easter Egg Click Tracker
function setupWhaleClicks() {
  const whale = document.querySelector('.swimming-whale img');
  if (!whale) return;

  let clicks = parseInt(localStorage.getItem('whaleClicks') || '0');

  whale.addEventListener('click', () => {
    clicks++;
    localStorage.setItem('whaleClicks', clicks);

    if (clicks === 10) {
      alert("🎉 You've unlocked the 'Talking Roomba' Easter Egg!");
      localStorage.setItem('unlockedBadge', 'Talking Roomba');
      // you can add more visual effects or badge unlock logic here
    }
  });
}

// 🚀 Referral Progress Tracker
function updateReferralProgress(refCode) {
  const milestones = [1, 5, 10, 20];
  const key = `referral_share_count_${refCode}`;
  const progressBar = document.getElementById('refProgressBar');
  const count = parseInt(localStorage.getItem(key) || '0');

  const nextMilestone = milestones.find(m => m > count);
  const currentMilestone = milestones.filter(m => m <= count).slice(-1)[0] || 0;

  if (progressBar) {
    const percent = nextMilestone ? ((count - currentMilestone) / (nextMilestone - currentMilestone)) * 100 : 100;
    progressBar.style.width = `${percent}%`;
  }
}
// ✅ Self-Updating Referral Progress Bar
function updateReferralProgressBar() {
  const refCode = localStorage.getItem('user_ref_code');
  if (!refCode) return;

  const key = `referral_share_count_${refCode}`;
  const progressBar = document.getElementById('refProgressBar');
  const count = parseInt(localStorage.getItem(key) || '0');

  // Define milestone targets
  const milestones = [1, 3, 5, 10, 20];
  const rewards = {
    1: '/Assets/whale.png',
    3: '/Assets/capybara.png',
    5: '/Assets/penguin.png',
    10: '/Assets/panda.png',
    20: '/Assets/axolotl.png'
  };
  const nextMilestone = milestones.find(m => m > count) || milestones[milestones.length - 1];
  const prevMilestone = milestones.slice().reverse().find(m => m <= count) || 0;

  const percent = nextMilestone === prevMilestone ? 100 : ((count - prevMilestone) / (nextMilestone - prevMilestone)) * 100;

  if (progressBar) {
    progressBar.style.width = `${Math.min(percent, 100)}%`;
  }
  // Change whale image if reward milestone reached
  const avatarImg = document.querySelector('.swimming-whale img');
  const available = milestones.slice().reverse().find(m => count >= m);
  if (avatarImg && rewards[available]) {
    avatarImg.src = rewards[available];
  }
}
        </script>
        <script>
            // ================================
// PHASE 2: User Identity & Competition
// ================================

// 🎭 Avatar and Badge Selection
function loadUserProfile() {
  const avatar = localStorage.getItem('userAvatar') || 'default_avatar.png';
  const badge = localStorage.getItem('userBadge') || '';

  const avatarImg = document.getElementById('userAvatar');
  const badgeSpan = document.getElementById('userBadge');

  if (avatarImg) avatarImg.src = `/Assets/${avatar}`;
  if (badgeSpan) badgeSpan.textContent = badge ? `🏅 ${badge}` : '';
}

function setAvatar(avatarFile) {
  localStorage.setItem('userAvatar', avatarFile);
  loadUserProfile();

  // Update swimming animal image for future whales
  localStorage.setItem('swimmingAnimal', avatarFile);
}


function setBadge(badgeName) {
  localStorage.setItem('userBadge', badgeName);
  loadUserProfile();
}
const allAvatars = [
  { id: 'whale.png', name: 'Whale', requiredReferrals: 0 },
  { id: 'capybara.png', name: 'Capybara', requiredReferrals: 3 },
  { id: 'penguin.png', name: 'Penguin', requiredReferrals: 5 },
  { id: 'panda.png', name: 'Panda', requiredReferrals: 10 },
  { id: 'axolotl.png', name: 'Axolotl', requiredReferrals: 20 }
];

document.getElementById('userAvatar').addEventListener('click', showAvatarSelector);

function showAvatarSelector() {
  const referralCount = parseInt(localStorage.getItem('referral_share_count_' + (localStorage.getItem('user_ref_code') || '')) || '0');
  const currentAvatar = localStorage.getItem('userAvatar') || 'whale.png';
  const grid = document.getElementById('avatarGrid');
  grid.innerHTML = '';

  allAvatars.forEach(avatar => {
    const isUnlocked = referralCount >= avatar.requiredReferrals;

    const card = document.createElement('div');
    card.style = `
      text-align: center;
      padding: 10px;
      border-radius: 8px;
      background: ${isUnlocked ? '#e0f7fa' : '#f8f8f8'};
      border: 2px solid ${currentAvatar === avatar.id ? '#3498db' : '#ccc'};
      opacity: ${isUnlocked ? '1' : '0.4'};
      cursor: ${isUnlocked ? 'pointer' : 'not-allowed'};
    `;

    const img = document.createElement('img');
    img.src = '/Assets/' + avatar.id;
    img.style = 'width: 60px; height: 60px; border-radius: 50%; object-fit: cover;';

    const name = document.createElement('div');
    name.textContent = avatar.name;
    name.style = 'margin-top: 6px; font-weight: bold; font-size: 14px;';

    if (!isUnlocked) {
      const lock = document.createElement('div');
      lock.textContent = `🔒 ${avatar.requiredReferrals} referrals`;
      lock.style = 'font-size: 12px; color: #888;';
      card.appendChild(lock);
    }

    if (isUnlocked) {
        card.addEventListener('click', () => {
  setAvatar(avatar.id);
  document.getElementById('avatarSelectModal').style.display = 'none';

  // Remove all currently active whales
  document.querySelectorAll('.swimming-whale').forEach(w => w.remove());

  // Immediately spawn a new one with the selected avatar
  createSwimmingWhale();
});

    }

    card.appendChild(img);
    card.appendChild(name);
    grid.appendChild(card);
  });

  document.getElementById('avatarSelectModal').style.display = 'flex';
}

// 🏆 Leaderboard Generation
function generateLeaderboard(type = 'referrals') {
  const leaderboardData = JSON.parse(localStorage.getItem('leaderboardData') || '{}');
  const board = leaderboardData[type] || [];

  const container = document.getElementById('leaderboard');
  if (!container) return;

  container.innerHTML = `<h3>🏆 Top ${type.charAt(0).toUpperCase() + type.slice(1)}</h3>`;

  const list = document.createElement('ol');
  board.slice(0, 10).forEach(entry => {
    const item = document.createElement('li');
    item.textContent = `${entry.name} - ${entry.count}`;
    list.appendChild(item);
  });

  container.appendChild(list);
}

// 🧠 Store Fake Data for Testing
function mockLeaderboardData() {
  const data = {
    referrals: [
      { name: 'NewsNinja', count: 22 },
      { name: 'WhaleWhisperer', count: 18 },
      { name: 'CivicSleuth', count: 12 }
    ],
    comments: [
      { name: 'SharpCommenter', count: 55 },
      { name: 'BanterBoss', count: 48 },
      { name: 'AnalysisAce', count: 37 }
    ],
    reads: [
      { name: 'ArticleHunter', count: 90 },
      { name: 'FastReader', count: 75 },
      { name: 'HeadlineHero', count: 64 }
    ]
  };
  localStorage.setItem('leaderboardData', JSON.stringify(data));
}
document.getElementById('userIdentityBox').addEventListener('click', () => {
  const board = document.getElementById('leaderboard');
  if (board.style.display === 'none' || board.style.display === '') {
    board.style.display = 'block';
  } else {
    board.style.display = 'none';
  }
});
</script>
<script>
    document.addEventListener("DOMContentLoaded", function () {
      // Avatar click to open avatar selection modal
      const avatarEl = document.getElementById("userAvatar");
      if (avatarEl) {
        avatarEl.addEventListener("click", showAvatarSelector);
      }
    
      // Rewards glow logic
      const rewardBtn = document.getElementById("rewardsButton");
      const claimBtn = document.getElementById("claimReward");
      const today = new Date().toDateString();
    
      function updateGlowState() {
        const claimed = localStorage.getItem("dailyRewardClaimed");
        if (claimed === today) {
          rewardBtn?.classList.remove("glow-reward");
        } else {
          rewardBtn?.classList.add("glow-reward");
        }
      }
    
      updateGlowState();
    
      if (claimBtn) {
        claimBtn.addEventListener("click", function () {
          localStorage.setItem("dailyRewardClaimed", today);
          updateGlowState();
        });
      }
    
      // Slideshow init
      let slideIndex = 0;
      const slides = document.getElementsByClassName("trend-slide");
      const dots = document.getElementsByClassName("dot");
    
      if (slides.length > 0 && dots.length > 0) {
        slides[0].style.opacity = "1";
        dots[0].style.backgroundColor = "var(--color-blue)";
        dots[0].style.opacity = "1";
    
        for (let i = 0; i < dots.length; i++) {
          dots[i].addEventListener("click", function () {
            showSlide(i);
          });
        }
    
        function startSlideshow() {
          setInterval(function () {
            slideIndex++;
            if (slideIndex >= slides.length) {
              slideIndex = 0;
            }
            showSlide(slideIndex);
          }, 5000);
        }
    
        function showSlide(n) {
          for (let i = 0; i < slides.length; i++) {
            slides[i].style.opacity = "0";
            dots[i].style.backgroundColor = "var(--color-brown)";
            dots[i].style.opacity = "0.4";
          }
          slides[n].style.opacity = "1";
          dots[n].style.backgroundColor = "var(--color-blue)";
          dots[n].style.opacity = "1";
          slideIndex = n;
        }
    
        startSlideshow();
      }
    
      // Referral update on query param
      const ref = new URLSearchParams(window.location.search).get("ref");
      if (ref) {
        updateReferralProgress(ref);
      }
    
      // Theme, points, whale, leaderboard, streak, avatars
      loadUserProfile();
      mockLeaderboardData();
      generateLeaderboard("referrals");
      updateReferralProgressBar();
      updateStreak();
      displayStreakBanner();
    
      const pointsDisplay = document.getElementById("forumPointsDisplay");
      pointsDisplay?.addEventListener("click", showPointsDetails);
    
      const savedTheme = localStorage.getItem("currentTheme");
      if (savedTheme) {
        applyTheme(savedTheme);
      }
    
      // Resize bubble if whale is active
      window.addEventListener("resize", () => {
        const activeBubble = document.querySelector(".bbb");
        if (activeBubble) {
          const viewportWidth = window.innerWidth;
          const bubbleWidth = Math.min(Math.max(viewportWidth * 0.15, 120), 200);
          activeBubble.style.width = `${bubbleWidth}px`;
    
          const whale = document.querySelector(".swimming-whale");
          if (whale) {
            const whaleRect = whale.getBoundingClientRect();
            activeBubble.style.left = `${whaleRect.left + whaleRect.width / 2 - bubbleWidth / 2}px`;
          }
        }
      });
    
      // Whale spawn
      setTimeout(createSwimmingWhale, 3000);
      scheduleWhaleAppearance();
    });
    </script>
    <script>
  document.addEventListener("DOMContentLoaded", () => {
    const cards = document.querySelectorAll(".section-grid > div > article.section-card");
    let direction = 1;
    let index = 0;

    function cycleGlow() {
      // Remove glow from all with fade-out effect
      cards.forEach((card, i) => {
        if (card.classList.contains("glow-reward")) {
          card.classList.remove("glow-reward");
        }
      });

      // Add glow with a slight delay to let removal settle
      setTimeout(() => {
        cards[index].classList.add("glow-reward");
      }, 100); // small delay to allow transition smoothing

      // Move index
      index += direction;
      if (index >= cards.length) {
        direction = -1;
        index = cards.length - 2;
      } else if (index < 0) {
        direction = 1;
        index = 1;
      }
    }

    setInterval(cycleGlow, 1800); // slightly slower for smoothness
  });
</script>
    

<div id="userIdentityBox" style="
position: fixed;
top: 12px;
right: 12px;
display: flex;
align-items: center;
gap: 10px;
background-color: rgba(255, 255, 255, 0.9);
padding: 6px 12px;
border-radius: 30px;
box-shadow: 0 2px 8px rgba(0,0,0,0.1);
font-family: 'Baloo 2', cursive;
z-index: 9999;
max-width: 45vw;
">

<img id="userAvatar" class="glow-reward" src="/Assets/default_avatar.png" style="
  width: 36px;
  height: 36px;
  border-radius: 50%;
  object-fit: cover;
  cursor: pointer;
">

<span id="userBadge" style="
  font-weight: bold;
  font-size: clamp(12px, 2vw, 16px);
  color: #5d4037;
  white-space: nowrap;
"></span>

</div>
<!-- 🏆 Leaderboard Container -->
<div id="leaderboard" style="
  position: fixed;
  top: 60px;
  right: 12px;
  background-color: white;
  border-radius: 12px;
  padding: 12px 18px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.2);
  max-width: 90vw;
  width: 260px;
  font-family: 'Baloo 2', cursive;
  display: none;
  z-index: 9998;
  font-size: clamp(12px, 1.8vw, 15px);
">
  <h3>🏆 Top Referrals</h3>
  <ol id="leaderboardList">
    <li>Loading leaderboard...</li>
  </ol>
</div>

<!-- 🎨 Avatar Selection Modal -->
<div id="avatarSelectModal" style="display:none; position:fixed; top:0; left:0; width:100%; height:100%; background:rgba(0,0,0,0.5); z-index:9999; justify-content:center; align-items:center;">
    <div style="background:white; max-width:500px; width:90%; padding:20px; border-radius:12px; max-height:80vh; overflow-y:auto;">
      <h2 style="margin-top:0; font-family:'Baloo 2', cursive;">Choose Your Avatar</h2>
      <div id="avatarGrid" style="display:grid; grid-template-columns:repeat(auto-fit, minmax(80px, 1fr)); gap:12px; margin-top:20px;"></div>
      <button onclick="document.getElementById('avatarSelectModal').style.display='none'" style="margin-top:15px; padding:8px 16px; border:none; border-radius:8px; background:#f2c94c; font-weight:bold;">Close</button>
    </div>
  </div>
  
</body>
</html>"""
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
