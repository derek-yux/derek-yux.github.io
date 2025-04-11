<?php
require_once('pdo.php');
require_once('util.php');
session_start();

?>
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
   <title>You You News - By You, For You!</title>
   <link rel="icon" type="image/x-icon" href="../Assets/youyounewslogo.png">
  <style>
    :root {
      --primary: #3b82f6;
      --primary-hover: #2563eb;
      --dark: #1e293b;
      --light: #f8fafc;
      --danger: #ef4444;
      --success: #22c55e;
      --gray: #64748b;
      --light-gray: #e2e8f0;
      --primary-color: #2c3e50;
      --secondary-color: #3498db;
      --light-bg: #f4f4f8;
      --text-color: #333;
    }
    
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
      font-family: 'Times New Roman', serif;
    }
    
    body {
      background-color: var(--light-bg);
      color: var(--text-color);
      line-height: 1.6;
      font-family: 'Times New Roman', serif;
    }
    #footerlink a {
        line-height: 1.6;
        color: var(--light-bg);
        font-family: 'Times New Roman', serif;
    }
    footer {
        background-color: var(--primary-color);
        color: white;
        text-align: center;
        padding: 20px 0;
        margin-top: 30px;
    }
    .container {
            width: 90%;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
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
        position: sticky;
        z-index: 10;
        display: flex;
        justify-content: space-between;
        align-items: center;
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
    
    .container {
      max-width: 1200px;
      margin: 0 auto;
      padding: 1rem;
    }
    
    .hidden {
      display: none !important;
    }
    
    button, .btn {
      background-color: var(--primary);
      color: white;
      border: none;
      padding: 0.5rem 1rem;
      border-radius: 0.25rem;
      cursor: pointer;
      font-size: 1rem;
      transition: background-color 0.2s;
      margin-right:10vw;
    }
    
    button:hover, .btn:hover {
      background-color: var(--primary-hover);
    }
    
    .btn-outline {
      background-color: var(--success);
      color: var(--);
      border: 1px solid var(--light);
    }
    
    .btn-outline:hover {
      background-color: var(--primary);
      color: white;
    }
    
    .btn-danger {
      background-color: var(--danger);
    }
    
    input, textarea {
      width: 100%;
      padding: 0.5rem;
      border: 1px solid var(--light-gray);
      border-radius: 0.25rem;
      font-size: 1rem;
      margin-bottom: 1rem;
    }
    
    .auth-container {
      max-width: 400px;
      margin: 2rem auto;
      background-color: white;
      padding: 2rem;
      border-radius: 0.5rem;
      box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .auth-toggle {
      text-align: center;
      margin-top: 1rem;
    }
    
    .auth-toggle a {
      color: var(--primary);
      cursor: pointer;
    }
    
    .forum-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 2rem;
    }
    
    .discussion-list {
      display: flex;
      flex-direction: column;
      gap: 1rem;
    }
    
    .discussion-card {
      background-color: white;
      border-radius: 0.5rem;
      padding: 1rem;
      box-shadow: 0 2px 4px rgba(0,0,0,0.05);
      transition: transform 0.2s;
    }
    
    .discussion-card:hover {
      transform: translateY(-2px);
      box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    .discussion-header {
      display: flex;
      justify-content: space-between;
      margin-bottom: 0.5rem;
    }
    
    .discussion-title {
      font-size: 1.25rem;
      font-weight: bold;
      color: var(--dark);
    }
    
    .discussion-meta {
      display: flex;
      gap: 1rem;
      color: var(--gray);
      font-size: 0.875rem;
      margin-bottom: 0.5rem;
    }
    
    .user-info {
      display: flex;
      align-items: center;
      gap: 0.5rem;
    }
    
    .avatar {
      width: 32px;
      height: 32px;
      border-radius: 50%;
      background-color: var(--primary);
      display: flex;
      align-items: center;
      justify-content: center;
      color: white;
      font-weight: bold;
    }
    
    .rank {
      background-color: var(--light-gray);
      color: var(--dark);
      padding: 0.25rem 0.5rem;
      border-radius: 1rem;
      font-size: 0.75rem;
      margin-left: 0.5rem;
    }
    
    .rank-novice { background-color: #dbeafe; color: #1e40af; }
    .rank-regular { background-color: #dcfce7; color: #166534; }
    .rank-expert { background-color: #ffedd5; color: #9a3412; }
    .rank-master { background-color: #fef3c7; color: #854d0e; }
    .rank-legendary { background-color: #fae8ff; color: #6b21a8; }
    
    .modal {
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background-color: rgba(0,0,0,0.5);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 100;
    }
    
    .modal-content {
      background-color: white;
      padding: 2rem;
      border-radius: 0.5rem;
      width: 100%;
      max-width: 600px;
    }
    
    .comment-section {
      margin-top: 1rem;
    }
    
    .comments-list {
      display: flex;
      flex-direction: column;
      gap: 1rem;
      margin-top: 1rem;
    }
    
    .comment-card {
      background-color: var(--light);
      padding: 1rem;
      border-radius: 0.25rem;
    }
    
    .comment-actions {
      display: flex;
      gap: 0.5rem;
      margin-top: 0.5rem;
    }
    
    .vote-btn {
      background-color: transparent;
      color: var(--gray);
      padding: 0.25rem 0.5rem;
      display: flex;
      align-items: center;
      gap: 0.25rem;
    }
    
    .vote-btn:hover {
      background-color: var(--light-gray);
    }
    
    .profile-container {
      max-width: 800px;
      margin: 2rem auto;
      background-color: white;
      padding: 2rem;
      border-radius: 0.5rem;
      box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    
    .profile-header {
      display: flex;
      align-items: center;
      gap: 1rem;
      margin-bottom: 2rem;
    }
    
    .profile-avatar {
      width: 80px;
      height: 80px;
      border-radius: 50%;
      background-color: var(--primary);
      display: flex;
      align-items: center;
      justify-content: center;
      color: white;
      font-size: 2rem;
      font-weight: bold;
    }
    
    .badge-list {
      display: flex;
      gap: 0.5rem;
      margin-top: 0.5rem;
    }
    
    .badge {
      background-color: var(--light-gray);
      color: var(--dark);
      padding: 0.25rem 0.5rem;
      border-radius: 0.25rem;
      font-size: 0.75rem;
    }
    
    .tabs {
      display: flex;
      border-bottom: 1px solid var(--light-gray);
      margin-bottom: 1rem;
    }
    
    .tab {
      padding: 0.5rem 1rem;
      cursor: pointer;
    }
    
    .tab.active {
      border-bottom: 2px solid var(--primary);
      color: var(--primary);
      font-weight: bold;
    }
    
    .tab-content {
      display: none;
    }
    
    .tab-content.active {
      display: block;
    }
    
    .stats-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
      gap: 1rem;
    }
    
    .stat-card {
      background-color: var(--light);
      padding: 1rem;
      border-radius: 0.25rem;
      text-align: center;
    }
    
    .stat-value {
      font-size: 1.5rem;
      font-weight: bold;
      color: var(--primary);
    }
    
    .stat-label {
      color: var(--gray);
      font-size: 0.875rem;
    }

    #login-btn {
      position: absolute;
      top: 4rem;
      right: 2rem;
      background-color: var(--primary);
      color: white;
      border: none;
      padding: 0.5rem 1rem;
      border-radius: 0.25rem;
      cursor: pointer;
      font-size: 1rem;
      transition: background-color 0.2s;
      margin-right:10vw;
    }
    #login-btn:hover {
      background-color: var(--primary-hover);
    }
    #profile-btn {
      position: absolute;
      top: 4rem;
      right: 5rem;
      background-color: var(--primary);
      color: white;
      border: none;
      padding: 0.5rem 1rem;
      border-radius: 0.25rem;
      cursor: pointer;
      font-size: 1rem;
      transition: background-color 0.2s;
      margin-right:10vw;
    }
    #profile-btn:hover {
      background-color: var(--primary-hover);
    }
    #logout-btn {
      position: absolute;
      top: 4rem;
      right: 0rem;
      background-color: var(--primary);
      color: white;
      border: none;
      padding: 0.5rem 1rem;
      border-radius: 0.25rem;
      cursor: pointer;
      font-size: 1rem;
      transition: background-color 0.2s;
      margin-right:10vw;
    }
    #logout-btn:hover {
      background-color: var(--primary-hover);
    }
    #new-post-btn {
      position: fixed;
      bottom: 2rem;
      right: 2rem;
      width: 60px;
      height: 60px;
      border-radius: 50%;
      background-color: var(--primary);
      color: white;
      font-size: 1.5rem;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 4px 6px rgba(0,0,0,0.1);
      cursor: pointer;
      transition: background-color 0.2s, transform 0.2s;
    }
    
    #new-post-btn:hover {
      background-color: var(--primary-hover);
      transform: scale(1.05);
    }
  </style>
</head>
<body>
    
  <!-- Header -->
  <header>
    <div class="container">
        <h1>You You News</h1>
        <p>Your Ultimate Source for Trending Content</p>
    </div>
    <button id="login-btn" class="head-outline">Login</button>
    <button id="profile-btn" class="hidden">Profile</button>
    <button id="logout-btn" class="hidden">Logout</button> 
  </header>
  
  <nav>
    <ul>
        <li><a href="../">Home</a></li>
        <li><a href="tech">Tech</a></li>
        <li><a href="sports">Sports</a></li>
        <li><a href="tv">TV</a></li>
        <li><a href="music">Music</a></li>
        <li1><a href="forums.php">Forums</a></li1>
    </ul>
  </nav>
  

  <!-- Main Content -->
  <div class="container">
    <!-- Auth Container -->
    <div id="auth-container" class="auth-container hidden">
      <h2 id="auth-title">Login</h2>
      <form id="auth-form">
        <div id="name-field" class="hidden">
          <label for="name">Name</label>
          <input type="text" id="name" placeholder="Your name">
        </div>
        <div>
          <label for="email">Email</label>
          <input type="email" id="email" placeholder="Your email">
        </div>
        <div>
          <label for="password">Password</label>
          <input type="password" id="password" placeholder="Your password">
        </div>
        <button type="submit" id="auth-submit">Login</button>
      </form>
      <div class="auth-toggle">
        <p id="auth-toggle-text">Don't have an account? <a id="auth-toggle-link">Sign up</a></p>
      </div>
    </div>

    <!-- Forum Container -->
    <div id="forum-container">
      <div class="forum-header">
        <h1>Recent Discussions</h1>
        <div>
          <select id="sort-select">
            <option value="recent">Most Recent</option>
            <option value="popular">Most Popular</option>
            <option value="active">Most Active</option>
          </select>
        </div>
      </div>

      <div id="discussion-list" class="discussion-list">
        <!-- Discussion cards will be added here -->
        <div class="discussion-card">
          <div class="discussion-header">
            <div class="discussion-title">Welcome to the Community Forum!</div>
            <div>42 likes</div>
          </div>
          <div class="discussion-meta">
            <div class="user-info">
              <div class="avatar">A</div>
              <span>Admin</span>
              <span class="rank rank-legendary">Legendary</span>
            </div>
            <div>15 comments</div>
            <div>2 days ago</div>
          </div>
          <p>Welcome to our new community forum! This is a place to discuss ideas, share knowledge, and connect with other members. Feel free to start a new discussion or join existing ones.</p>
        </div>
        
        <div class="discussion-card">
          <div class="discussion-header">
            <div class="discussion-title">Tips for New Members</div>
            <div>28 likes</div>
          </div>
          <div class="discussion-meta">
            <div class="user-info">
              <div class="avatar">M</div>
              <span>Moderator</span>
              <span class="rank rank-master">Master</span>
            </div>
            <div>8 comments</div>
            <div>1 day ago</div>
          </div>
          <p>Here are some tips for new members to get the most out of our community forum. Make sure to complete your profile, be respectful to others, and contribute regularly to earn ranks and badges!</p>
        </div>
      </div>
    </div>

    <!-- New Post Button -->
    <div id="new-post-btn" class="hidden">+</div>

    <!-- New Post Modal -->
    <div id="new-post-modal" class="modal hidden">
      <div class="modal-content">
        <h2>Create New Discussion</h2>
        <form id="new-post-form">
          <div>
            <label for="post-title">Title</label>
            <input type="text" id="post-title" placeholder="Discussion title">
          </div>
          <div>
            <label for="post-content">Content</label>
            <textarea id="post-content" rows="5" placeholder="Share your thoughts..."></textarea>
          </div>
          <div>
            <label for="post-tags">Tags (comma separated)</label>
            <input type="text" id="post-tags" placeholder="e.g. help, question, idea">
          </div>
          <div style="display: flex; gap: 1rem; justify-content: flex-end;">
            <button type="button" id="cancel-post-btn" class="btn-outline">Cancel</button>
            <button type="submit">Create Discussion</button>
          </div>
        </form>
      </div>
    </div>

    <!-- Discussion Modal -->
    <div id="discussion-modal" class="modal hidden">
      <div class="modal-content">
        <h2 id="discussion-modal-title"></h2>
        <div class="user-info">
          <div class="avatar" id="discussion-modal-avatar"></div>
          <span id="discussion-modal-author"></span>
          <span id="discussion-modal-rank" class="rank"></span>
        </div>
        <p id="discussion-modal-content"></p>
        
        <div class="comment-section">
          <h3>Comments</h3>
          <form id="comment-form">
            <textarea id="comment-content" rows="3" placeholder="Add a comment..."></textarea>
            <button type="submit">Comment</button>
          </form>
          <div id="comments-list" class="comments-list">
            <!-- Comments will be added here -->
          </div>
        </div>
      </div>
    </div>

    <!-- Profile Container -->
    <div id="profile-container" class="profile-container hidden">
      <div class="profile-header">
        <div class="profile-avatar" id="profile-avatar"></div>
        <div>
          <h2 id="profile-name"></h2>
          <div id="profile-rank" class="rank"></div>
          <div class="badge-list" id="profile-badges">
            <!-- Badges will be added here -->
          </div>
        </div>
      </div>

      <div class="tabs">
        <div class="tab active" data-tab="profile-info">Profile Info</div>
        <div class="tab" data-tab="activity">Activity</div>
        <div class="tab" data-tab="stats">Stats</div>
      </div>

      <div id="profile-info" class="tab-content active">
        <h3>Profile Information</h3>
        <form id="profile-form">
          <div>
            <label for="profile-display-name">Display Name</label>
            <input type="text" id="profile-display-name">
          </div>
          <div>
            <label for="profile-bio">Bio</label>
            <textarea id="profile-bio" rows="3"></textarea>
          </div>
          <button type="submit">Save Profile</button>
        </form>
      </div>

      <div id="activity" class="tab-content">
        <h3>Recent Activity</h3>
        <div id="activity-list">
          <!-- Activity items will be added here -->
        </div>
      </div>

      <div id="stats" class="tab-content">
        <h3>User Statistics</h3>
        <div class="stats-grid">
          <div class="stat-card">
            <div class="stat-value" id="posts-count">0</div>
            <div class="stat-label">Posts</div>
          </div>
          <div class="stat-card">
            <div class="stat-value" id="comments-count">0</div>
            <div class="stat-label">Comments</div>
          </div>
          <div class="stat-card">
            <div class="stat-value" id="contribution-points">0</div>
            <div class="stat-label">Contribution Points</div>
          </div>
          <div class="stat-card">
            <div class="stat-value" id="days-active">0</div>
            <div class="stat-label">Days Active</div>
          </div>
        </div>
      </div>
    </div>
  </div>
  <footer>
    <div class="container">
        <p>&copy; 2025 You You News. All Rights Reserved.</p>
        <p>Connect with us on social media</p>
        <div id="footerlink">
            <a href="/Terms_and_Conditions/terms_of_service.html">Terms of Service</a>
        </div>
        <br>
        <img src="/Assets/sectigo_trust_seal_md_106x42.png" alt="Verified Logo">
    </div>
</footer>

  <script>
    // DOM Elements
    const loginBtn = document.getElementById('login-btn');
    const profileBtn = document.getElementById('profile-btn');
    const logoutBtn = document.getElementById('logout-btn');
    const authContainer = document.getElementById('auth-container');
    const authTitle = document.getElementById('auth-title');
    const authForm = document.getElementById('auth-form');
    const nameField = document.getElementById('name-field');
    const authSubmit = document.getElementById('auth-submit');
    const authToggleText = document.getElementById('auth-toggle-text');
    const authToggleLink = document.getElementById('auth-toggle-link');
    const forumContainer = document.getElementById('forum-container');
    const discussionList = document.getElementById('discussion-list');
    const sortSelect = document.getElementById('sort-select');
    const newPostBtn = document.getElementById('new-post-btn');
    const newPostModal = document.getElementById('new-post-modal');
    const newPostForm = document.getElementById('new-post-form');
    const cancelPostBtn = document.getElementById('cancel-post-btn');
    const discussionModal = document.getElementById('discussion-modal');
    const discussionModalTitle = document.getElementById('discussion-modal-title');
    const discussionModalAvatar = document.getElementById('discussion-modal-avatar');
    const discussionModalAuthor = document.getElementById('discussion-modal-author');
    const discussionModalRank = document.getElementById('discussion-modal-rank');
    const discussionModalContent = document.getElementById('discussion-modal-content');
    const commentForm = document.getElementById('comment-form');
    const commentsList = document.getElementById('comments-list');
    const profileContainer = document.getElementById('profile-container');
    const profileAvatar = document.getElementById('profile-avatar');
    const profileName = document.getElementById('profile-name');
    const profileRank = document.getElementById('profile-rank');
    const profileBadges = document.getElementById('profile-badges');
    const profileForm = document.getElementById('profile-form');
    const tabs = document.querySelectorAll('.tab');
    const tabContents = document.querySelectorAll('.tab-content');
    const activityList = document.getElementById('activity-list');
    const postsCount = document.getElementById('posts-count');
    const commentsCount = document.getElementById('comments-count');
    const contributionPoints = document.getElementById('contribution-points');
    const daysActive = document.getElementById('days-active');

    // Mock data for demo purposes
    let currentUser = null;
    
    // Rank system
    const ranks = {
      0: { name: 'Novice', class: 'rank-novice' },
      25: { name: 'Regular', class: 'rank-regular' },
      100: { name: 'Expert', class: 'rank-expert' },
      250: { name: 'Master', class: 'rank-master' },
      500: { name: 'Legendary', class: 'rank-legendary' }
    };

    // Get user rank based on points
    function getUserRank(points) {
      let rankLevel = 0;
      for (const threshold in ranks) {
        if (points >= threshold) {
          rankLevel = threshold;
        } else {
          break;
        }
      }
      return ranks[rankLevel];
    }

    // Initialize event listeners
    function initApp() {
      // Login button
      loginBtn.addEventListener('click', () => {
        authContainer.classList.remove('hidden');
        forumContainer.classList.add('hidden');
      });
      
      authToggleLink.addEventListener('click', () => {
      const isLogin = authTitle.textContent === 'Login';
      
      // Toggle the form mode
      authTitle.textContent = isLogin ? 'Sign Up' : 'Login';
      authSubmit.textContent = isLogin ? 'Sign Up' : 'Login';
      authToggleText.textContent = isLogin ? 'Already have an account? ' : 'Don\'t have an account? ';
      authToggleLink.textContent = isLogin ? 'Login' : 'Sign up';
      
      // Toggle the name field visibility
      nameField.classList.toggle('hidden', !isLogin);
      
      // Clear any error messages
      const errorElement = document.getElementById('auth-error');
      if (errorElement) {
        errorElement.remove();
      }
      
      // Reset form fields
      authForm.reset();
    });
      
      // Logout button
      logoutBtn.addEventListener('click', () => {
        currentUser = null;
        loginBtn.classList.remove('hidden');
        profileBtn.classList.add('hidden');
        logoutBtn.classList.add('hidden');
        newPostBtn.classList.add('hidden');
        forumContainer.classList.remove('hidden');
        profileContainer.classList.add('hidden');
      });
      
      // Profile button
      profileBtn.addEventListener('click', () => {
        showProfile();
      });
      
      // New post button
      newPostBtn.addEventListener('click', () => {
        newPostModal.classList.remove('hidden');
      });
      
      // Cancel post button
      cancelPostBtn.addEventListener('click', () => {
        newPostModal.classList.add('hidden');
        newPostForm.reset();
      });
      
      // New post form
      newPostForm.addEventListener('submit', (e) => {
        e.preventDefault();
        
        // Get form data
        const title = document.getElementById('post-title').value;
        const content = document.getElementById('post-content').value;
        const tags = document.getElementById('post-tags').value.split(',').map(tag => tag.trim());
        
        // Create mock discussion card
        const card = createDiscussionCard({
          id: 'new' + Date.now(),
          title: title,
          content: content,
          tags: tags,
          author: currentUser.displayName,
          authorRank: 'Novice',
          createdAt: new Date(),
          likes: 0,
          commentsCount: 0
        });
        
        // Add to list
        discussionList.prepend(card);
        
        // Close modal
        newPostModal.classList.add('hidden');
        newPostForm.reset();
      });
      
      // Comment form
      commentForm.addEventListener('submit', (e) => {
        e.preventDefault();
        
        if (!currentUser) {
          alert('Please login to comment');
          return;
        }
        
        const content = document.getElementById('comment-content').value;
        
        // Add mock comment
        const comment = document.createElement('div');
        comment.className = 'comment-card';
        comment.innerHTML = `
          <div class="user-info">
            <div class="avatar">${currentUser.displayName.charAt(0)}</div>
            <span>${currentUser.displayName}</span>
            <span class="rank rank-novice">Novice</span>
            <span style="margin-left: auto;">Just now</span>
          </div>
          <p>${content}</p>
          <div class="comment-actions">
            <button class="vote-btn" data-action="like">
              <span>👍</span>
              <span>0</span>
            </button>
          </div>
        `;
        
        commentsList.prepend(comment);
        commentForm.reset();
      });
      
      // Initialize tabs
      tabs.forEach(tab => {
        tab.addEventListener('click', () => {
          // Remove active class from all tabs
          tabs.forEach(t => t.classList.remove('active'));
          tabContents.forEach(t => t.classList.remove('active'));
          
          // Add active class to current tab
          tab.classList.add('active');
          document.getElementById(tab.dataset.tab).classList.add('active');
        });
      });
      
      // Sort select
      sortSelect.addEventListener('change', () => {
        const value = sortSelect.value;
        // In a real app, this would reload discussions with the new sort
        console.log('Sort changed to:', value);
      });
      
      // Populate discussion cards with event listeners
      const discussionCards = document.querySelectorAll('.discussion-card');
      discussionCards.forEach(card => {
        card.addEventListener('click', () => {
          openDiscussion(card);
        });
      });
      
      // Close modals when clicking outside
      window.addEventListener('click', (e) => {
        if (e.target === newPostModal) {
          newPostModal.classList.add('hidden');
        }
        if (e.target === discussionModal) {
          discussionModal.classList.add('hidden');
        }
      });
      
      // Profile form
      profileForm.addEventListener('submit', (e) => {
        e.preventDefault();
        alert('Profile updated successfully!');
      });
    }

    // Create discussion card
    function createDiscussionCard(data) {
      const card = document.createElement('div');
      card.className = 'discussion-card';
      card.dataset.id = data.id;
      
      card.innerHTML = `
        <div class="discussion-header">
          <div class="discussion-title">${data.title}</div>
          <div>${data.likes} likes</div>
        </div>
        <div class="discussion-meta">
          <div class="user-info">
            <div class="avatar">${data.author.charAt(0)}</div>
            <span>${data.author}</span>
            <span class="rank rank-${data.authorRank.toLowerCase()}">${data.authorRank}</span>
          </div>
          <div>${data.commentsCount} comments</div>
          <div>Just now</div>
        </div>
        <p>${data.content.substring(0, 150)}${data.content.length > 150 ? '...' : ''}</p>
      `;
      
      card.addEventListener('click', () => {
        openDiscussion(card);
      });
      
      return card;
    }

    // Open discussion
    function openDiscussion(card) {
      // Get data from card
      const title = card.querySelector('.discussion-title').textContent;
      const avatar = card.querySelector('.avatar').textContent;
      const author = card.querySelector('.user-info span').textContent;
      const rank = card.querySelector('.rank').textContent;
      const rankClass = card.querySelector('.rank').className.split(' ')[1];
      const content = card.querySelector('p').textContent;
      
      // Populate modal
      discussionModalTitle.textContent = title;
      discussionModalAvatar.textContent = avatar;
      discussionModalAuthor.textContent = author;
      discussionModalRank.textContent = rank;
      discussionModalRank.className = `rank ${rankClass}`;
      discussionModalContent.textContent = content;
      
      // Show comments if exists
      if (commentsList.children.length === 0) {
        commentsList.innerHTML = '<p>No comments yet. Be the first to comment!</p>';
      }
      
      // Show modal
      discussionModal.classList.remove('hidden');
    }

    // Show profile
    function showProfile() {
      if (!currentUser) {
        alert('Please login to view profile');
        return;
      }
      
      // Populate profile data
      profileAvatar.textContent = currentUser.displayName.charAt(0);
      profileName.textContent = currentUser.displayName;
      
      // Rank (for demo purposes)
      const rank = getUserRank(10);
      profileRank.textContent = rank.name;
      profileRank.className = `rank ${rank.class}`;
      
      // Badges (for demo purposes)
      profileBadges.innerHTML = `
        <div class="badge">Early Adopter</div>
        <div class="badge">Contributor</div>
      `;
      
      // Profile form
      document.getElementById('profile-display-name').value = currentUser.displayName;

      // Profile form (continued)
      document.getElementById('profile-bio').value = currentUser.bio || '';
      
      // Stats (for demo purposes)
      postsCount.textContent = '5';
      commentsCount.textContent = '12';
      contributionPoints.textContent = '37';
      daysActive.textContent = '7';
      
      // Activity (for demo purposes)
      activityList.innerHTML = `
        <div class="discussion-card">
          <div class="discussion-meta">
            <div>Posted a discussion</div>
            <div>2 days ago</div>
          </div>
          <p>How to earn badges in the community?</p>
        </div>
        <div class="discussion-card">
          <div class="discussion-meta">
            <div>Commented on a discussion</div>
            <div>3 days ago</div>
          </div>
          <p>Great tip! This helped me a lot.</p>
        </div>
      `;
      
      // Show profile container
      forumContainer.classList.add('hidden');
      profileContainer.classList.remove('hidden');
    }

    // Mock database functions
    const db = {
      users: [
        {
          uid: 'admin123',
          email: 'admin@example.com',
          displayName: 'Admin',
          bio: 'Forum administrator',
          createdAt: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000),
          contributionPoints: 520,
          posts: 24,
          comments: 95,
          badges: ['Admin', 'Founder', 'Top Contributor']
        },
        {
          uid: 'mod123',
          email: 'moderator@example.com',
          displayName: 'Moderator',
          bio: 'Forum moderator',
          createdAt: new Date(Date.now() - 20 * 24 * 60 * 60 * 1000),
          contributionPoints: 320,
          posts: 18,
          comments: 64,
          badges: ['Moderator', 'Expert', 'Helpful']
        }
      ],
      discussions: [
        {
          id: 'disc1',
          title: 'Welcome to the Community Forum!',
          content: 'Welcome to our new community forum! This is a place to discuss ideas, share knowledge, and connect with other members. Feel free to start a new discussion or join existing ones.',
          author: 'Admin',
          authorId: 'admin123',
          createdAt: new Date(Date.now() - 2 * 24 * 60 * 60 * 1000),
          likes: 42,
          commentsCount: 15,
          tags: ['welcome', 'announcement']
        },
        {
          id: 'disc2',
          title: 'Tips for New Members',
          content: 'Here are some tips for new members to get the most out of our community forum. Make sure to complete your profile, be respectful to others, and contribute regularly to earn ranks and badges!',
          author: 'Moderator',
          authorId: 'mod123',
          createdAt: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000),
          likes: 28,
          commentsCount: 8,
          tags: ['tips', 'help']
        }
      ],
      comments: [
        {
          id: 'comment1',
          discussionId: 'disc1',
          content: 'This is great! Looking forward to engaging with the community.',
          author: 'Moderator',
          authorId: 'mod123',
          createdAt: new Date(Date.now() - 1.5 * 24 * 60 * 60 * 1000),
          likes: 12
        },
        {
          id: 'comment2',
          discussionId: 'disc1',
          content: 'Thank you for creating this space!',
          author: 'Regular User',
          authorId: 'user456',
          createdAt: new Date(Date.now() - 1 * 24 * 60 * 60 * 1000),
          likes: 5
        }
      ],
      
      // Get user by ID
      getUser(uid) {
        return this.users.find(user => user.uid === uid);
      },
      
      // Get user rank
      getUserRank(uid) {
        const user = this.getUser(uid);
        return user ? getUserRank(user.contributionPoints) : ranks[0];
      },
      
      // Get discussions
      getDiscussions(sort = 'recent') {
        let discussions = [...this.discussions];
        
        switch(sort) {
          case 'popular':
            discussions.sort((a, b) => b.likes - a.likes);
            break;
          case 'active':
            discussions.sort((a, b) => b.commentsCount - a.commentsCount);
            break;
          case 'recent':
          default:
            discussions.sort((a, b) => b.createdAt - a.createdAt);
            break;
        }
        
        return discussions;
      },
      
      // Get comments for discussion
      getComments(discussionId) {
        return this.comments
          .filter(comment => comment.discussionId === discussionId)
          .sort((a, b) => b.createdAt - a.createdAt);
      },
      
      // Add user
      addUser(user) {
        this.users.push({
          ...user,
          createdAt: new Date(),
          contributionPoints: 0,
          posts: 0,
          comments: 0,
          badges: []
        });
        return user;
      },
      
      // Add discussion
      addDiscussion(discussion) {
        const newDiscussion = {
          ...discussion,
          id: 'disc' + Date.now(),
          createdAt: new Date(),
          likes: 0,
          commentsCount: 0
        };
        
        this.discussions.unshift(newDiscussion);
        
        // Update user stats
        const user = this.getUser(discussion.authorId);
        if (user) {
          user.posts += 1;
          user.contributionPoints += 5;  // 5 points for new discussion
        }
        
        return newDiscussion;
      },
      
      // Add comment
      addComment(comment) {
        const newComment = {
          ...comment,
          id: 'comment' + Date.now(),
          createdAt: new Date(),
          likes: 0
        };
        
        this.comments.unshift(newComment);
        
        // Update discussion
        const discussion = this.discussions.find(d => d.id === comment.discussionId);
        if (discussion) {
          discussion.commentsCount += 1;
        }
        
        // Update user stats
        const user = this.getUser(comment.authorId);
        if (user) {
          user.comments += 1;
          user.contributionPoints += 2;  // 2 points for new comment
        }
        
        return newComment;
      },
      
      // Like discussion
      likeDiscussion(discussionId, userId) {
        const discussion = this.discussions.find(d => d.id === discussionId);
        if (discussion) {
          discussion.likes += 1;
          
          // Update author stats
          const author = this.getUser(discussion.authorId);
          if (author) {
            author.contributionPoints += 1;  // 1 point for receiving a like
          }
        }
      },
      
      // Like comment
      likeComment(commentId, userId) {
        const comment = this.comments.find(c => c.id === commentId);
        if (comment) {
          comment.likes += 1;
          
          // Update author stats
          const author = this.getUser(comment.authorId);
          if (author) {
            author.contributionPoints += 1;  // 1 point for receiving a like
          }
        }
      }
    };

    // Format date
    function formatDate(date) {
      const now = new Date();
      const diff = now - date;
      
      const seconds = Math.floor(diff / 1000);
      const minutes = Math.floor(seconds / 60);
      const hours = Math.floor(minutes / 60);
      const days = Math.floor(hours / 24);
      
      if (days > 7) {
        return date.toLocaleDateString();
      } else if (days > 0) {
        return `${days} day${days > 1 ? 's' : ''} ago`;
      } else if (hours > 0) {
        return `${hours} hour${hours > 1 ? 's' : ''} ago`;
      } else if (minutes > 0) {
        return `${minutes} minute${minutes > 1 ? 's' : ''} ago`;
      } else {
        return 'Just now';
      }
    }

    // Initialize real-time updates with WebSockets (mock)
    function initRealTimeUpdates() {
      console.log('Initializing real-time updates...');
      
      // Mock WebSocket connection
      const mockSocket = {
        onmessage: null,
        send: function(data) {
          console.log('Sending data:', data);
        }
      };
      
      // Set message handler
      mockSocket.onmessage = function(event) {
        const data = JSON.parse(event.data);
        
        switch(data.type) {
          case 'new_discussion':
            // Add new discussion to the list
            const card = createDiscussionCard(data.discussion);
            discussionList.prepend(card);
            break;
            
          case 'new_comment':
            // If the discussion is open, add the comment
            if (!discussionModal.classList.contains('hidden') && 
                discussionModalTitle.textContent === data.comment.discussionTitle) {
              addCommentToList(data.comment);
            }
            break;
            
          case 'like_update':
            // Update like count
            const discussions = document.querySelectorAll('.discussion-card');
            discussions.forEach(disc => {
              if (disc.dataset.id === data.id) {
                const likeElement = disc.querySelector('.discussion-header > div:last-child');
                likeElement.textContent = `${data.likes} likes`;
              }
            });
            break;
        }
      };
      
      // Simulate sending status
      setInterval(() => {
        mockSocket.send(JSON.stringify({ type: 'heartbeat', userId: currentUser?.uid }));
      }, 5000);
      
      return mockSocket;
    }

    // Add comment to list
    function addCommentToList(comment) {
      const commentElement = document.createElement('div');
      commentElement.className = 'comment-card';
      commentElement.innerHTML = `
        <div class="user-info">
          <div class="avatar">${comment.author.charAt(0)}</div>
          <span>${comment.author}</span>
          <span class="rank rank-${comment.authorRank.toLowerCase()}">${comment.authorRank}</span>
          <span style="margin-left: auto;">${formatDate(comment.createdAt)}</span>
        </div>
        <p>${comment.content}</p>
        <div class="comment-actions">
          <button class="vote-btn" data-action="like" data-id="${comment.id}">
            <span>👍</span>
            <span>${comment.likes}</span>
          </button>
        </div>
      `;
      
      // Add like functionality
      const likeBtn = commentElement.querySelector('.vote-btn');
      likeBtn.addEventListener('click', (e) => {
        e.stopPropagation();
        
        if (!currentUser) {
          alert('Please login to like comments');
          return;
        }
        
        const likeCount = likeBtn.querySelector('span:last-child');
        likeCount.textContent = parseInt(likeCount.textContent) + 1;
        
        // Update in mock database
        db.likeComment(comment.id, currentUser.uid);
      });
      
      // Prepend to comments list
      const noCommentsMsg = commentsList.querySelector('p');
      if (noCommentsMsg) {
        commentsList.innerHTML = '';
      }
      
      commentsList.prepend(commentElement);
    }

    // Load discussions from database
    function loadDiscussions(sort = 'recent') {
      const discussions = db.getDiscussions(sort);
      
      // Clear current discussions
      discussionList.innerHTML = '';
      
      // Add discussion cards
      discussions.forEach(discussion => {
        const authorData = db.getUser(discussion.authorId);
        const rank = getUserRank(authorData?.contributionPoints || 0);
        
        const card = createDiscussionCard({
          id: discussion.id,
          title: discussion.title,
          content: discussion.content,
          author: discussion.author,
          authorRank: rank.name,
          createdAt: discussion.createdAt,
          likes: discussion.likes,
          commentsCount: discussion.commentsCount
        });
        
        discussionList.appendChild(card);
      });
    }

    // Enhanced open discussion function
    function openDiscussion(card) {
      const discussionId = card.dataset.id;
      const discussion = db.discussions.find(d => d.id === discussionId);
      
      if (!discussion) {
        // Get data from card if not in database
        const title = card.querySelector('.discussion-title').textContent;
        const avatar = card.querySelector('.avatar').textContent;
        const author = card.querySelector('.user-info span').textContent;
        const rank = card.querySelector('.rank').textContent;
        const rankClass = card.querySelector('.rank').className.split(' ')[1];
        const content = card.querySelector('p').textContent;
        
        // Populate modal
        discussionModalTitle.textContent = title;
        discussionModalAvatar.textContent = avatar;
        discussionModalAuthor.textContent = author;
        discussionModalRank.textContent = rank;
        discussionModalRank.className = `rank ${rankClass}`;
        discussionModalContent.textContent = content;
        
        // Show default message for comments
        commentsList.innerHTML = '<p>No comments yet. Be the first to comment!</p>';
      } else {
        // Get data from database
        const authorData = db.getUser(discussion.authorId);
        const rank = getUserRank(authorData?.contributionPoints || 0);
        
        // Populate modal
        discussionModalTitle.textContent = discussion.title;
        discussionModalAvatar.textContent = discussion.author.charAt(0);
        discussionModalAuthor.textContent = discussion.author;
        discussionModalRank.textContent = rank.name;
        discussionModalRank.className = `rank ${rank.class}`;
        discussionModalContent.textContent = discussion.content;
        
        // Load comments
        commentsList.innerHTML = '';
        const comments = db.getComments(discussionId);
        
        if (comments.length === 0) {
          commentsList.innerHTML = '<p>No comments yet. Be the first to comment!</p>';
        } else {
          comments.forEach(comment => {
            const commentAuthor = db.getUser(comment.authorId);
            const commentAuthorRank = getUserRank(commentAuthor?.contributionPoints || 0);
            
            addCommentToList({
              ...comment,
              authorRank: commentAuthorRank.name
            });
          });
        }
      }
      
      // Show modal
      discussionModal.classList.remove('hidden');
      
      // Enhanced comment form functionality
      commentForm.onsubmit = (e) => {
        e.preventDefault();
        
        if (!currentUser) {
          alert('Please login to comment');
          return;
        }
        
        const content = document.getElementById('comment-content').value;
        
        // Add to database
        if (discussion) {
          const newComment = db.addComment({
            discussionId: discussionId,
            content: content,
            author: currentUser.displayName,
            authorId: currentUser.uid
          });
          
          // Update comment count on card
          const commentCountElement = card.querySelector('.discussion-meta > div:nth-child(2)');
          commentCountElement.textContent = `${discussion.commentsCount} comments`;
          
          // Get rank
          const userRank = db.getUserRank(currentUser.uid);
          
          // Add to UI
          addCommentToList({
            ...newComment,
            authorRank: userRank.name
          });
        } else {
          // Just add UI element for demo purposes
          const comment = document.createElement('div');
          comment.className = 'comment-card';
          comment.innerHTML = `
            <div class="user-info">
              <div class="avatar">${currentUser.displayName.charAt(0)}</div>
              <span>${currentUser.displayName}</span>
              <span class="rank rank-novice">Novice</span>
              <span style="margin-left: auto;">Just now</span>
            </div>
            <p>${content}</p>
            <div class="comment-actions">
              <button class="vote-btn" data-action="like">
                <span>👍</span>
                <span>0</span>
              </button>
            </div>
          `;
          
          // Update comment count on card
          const commentCountElement = card.querySelector('.discussion-meta > div:nth-child(2)');
          const currentCount = parseInt(commentCountElement.textContent);
          commentCountElement.textContent = `${currentCount + 1} comments`;
          
          const noCommentsMsg = commentsList.querySelector('p');
          if (noCommentsMsg) {
            commentsList.innerHTML = '';
          }
          
          commentsList.prepend(comment);
        }
        
        commentForm.reset();
      };
    }
    // Email validation helper
    function validateEmail(email) {
    const re = /^(([^<>()\[\]\\.,;:\s@"]+(\.[^<>()\[\]\\.,;:\s@"]+)*)|(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/;
    return re.test(String(email).toLowerCase());
    }

    // Show error message
    function showError(message) {
        // Check if error element already exists
        let errorElement = document.getElementById('auth-error');
    
        if (!errorElement) {
            // Create error element if it doesn't exist
            errorElement = document.createElement('div');
            errorElement.id = 'auth-error';
            errorElement.style.color = 'var(--danger)';
            errorElement.style.marginBottom = '1rem';
            errorElement.style.fontSize = '0.875rem';
            
            // Insert before the submit button
            const submitButton = document.getElementById('auth-submit');
            submitButton.parentNode.insertBefore(errorElement, submitButton);
        }
        
        // Set error message
        errorElement.textContent = message;
        
        // Shake the form
        authForm.classList.add('shake');
        setTimeout(() => {
            authForm.classList.remove('shake');
        }, 500);
    }
    function showSuccess(message) {
        // Remove error message if exists
        const errorElement = document.getElementById('auth-error');
        if (errorElement) {
            errorElement.remove();
        }
        
        // Create toast notification
        const toast = document.createElement('div');
        toast.className = 'toast';
        toast.textContent = message;
        toast.style.position = 'fixed';
        toast.style.bottom = '1rem';
        toast.style.right = '1rem';
        toast.style.backgroundColor = 'var(--success)';
        toast.style.color = 'white';
        toast.style.padding = '0.75rem 1.5rem';
        toast.style.borderRadius = '0.25rem';
        toast.style.boxShadow = '0 4px 6px rgba(0,0,0,0.1)';
        toast.style.zIndex = '1000';
        toast.style.opacity = '0';
        toast.style.transform = 'translateY(1rem)';
        toast.style.transition = 'opacity 0.3s, transform 0.3s';
        
        document.body.appendChild(toast);
        
        // Show toast
        setTimeout(() => {
            toast.style.opacity = '1';
            toast.style.transform = 'translateY(0)';
        }, 10);
        
        // Hide toast after 3 seconds
        setTimeout(() => {
            toast.style.opacity = '0';
            toast.style.transform = 'translateY(1rem)';
            
            // Remove toast from DOM after animation
            setTimeout(() => {
            toast.remove();
            }, 300);
        }, 3000);
    }
    // Add a small animation for the shake effect
    const styleElement = document.createElement('style');
    styleElement.textContent = `
    @keyframes shake {
        0%, 100% { transform: translateX(0); }
        10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
        20%, 40%, 60%, 80% { transform: translateX(5px); }
    }
    
    .shake {
        animation: shake 0.5s cubic-bezier(.36,.07,.19,.97) both;
    }
    
    .toast {
        animation: fadein 0.3s;
    }
    
    @keyframes fadein {
        from { opacity: 0; transform: translateY(1rem); }
        to { opacity: 1; transform: translateY(0); }
    }
    `;
    document.head.appendChild(styleElement);

    // Update the db object's users array to include passwords for the example users
    db.users = [
    {
        uid: 'admin123',
        email: 'admin@example.com',
        password: 'admin123', // In a real app, this would be hashed
        displayName: 'Admin',
        bio: 'Forum administrator',
        createdAt: new Date(Date.now() - 30 * 24 * 60 * 60 * 1000),
        contributionPoints: 520,
        posts: 24,
        comments: 95,
        badges: ['Admin', 'Founder', 'Top Contributor']
    },
    {
        uid: 'mod123',
        email: 'moderator@example.com',
        password: 'mod123', // In a real app, this would be hashed
        displayName: 'Moderator',
        bio: 'Forum moderator',
        createdAt: new Date(Date.now() - 20 * 24 * 60 * 60 * 1000),
        contributionPoints: 320,
        posts: 18,
        comments: 64,
        badges: ['Moderator', 'Expert', 'Helpful']
    }
    ];

    // Initialize app with enhanced features
    function initEnhancedApp() {
      // Initialize basic app
      initApp();
      
      // Set up real-time updates
      const socket = initRealTimeUpdates();
      
      // Enhanced login/signup
      authForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const email = document.getElementById('email').value.trim();
        const password = document.getElementById('password').value;
        const name = document.getElementById('name').value.trim() || email.split('@')[0];
        
        // Form validation
        if (!email) {
            showError('Please enter your email address');
            return;
        }
        
        if (!validateEmail(email)) {
            showError('Please enter a valid email address');
            return;
        }
        
        if (!password) {
            showError('Please enter your password');
            return;
        }
        
        const isLogin = authTitle.textContent === 'Login';
        
        if (isLogin) {
            // Mock login with password check
            const user = db.users.find(u => u.email === email);
            
            if (!user) {
            showError('User not found. Please check your email or sign up');
            return;
            }
            
            // In a real app, you'd use proper password hashing
            // This is just a simple check for demonstration purposes
            if (user.password !== password) {
            showError('Incorrect password. Please try again');
            return;
            }
            
            currentUser = {
            uid: user.uid,
            email: user.email,
            displayName: user.displayName,
            bio: user.bio
            };
            
            showSuccess('Login successful!');
        } else {
            // Signup validation
            if (name.length < 2) {
            showError('Name must be at least 2 characters long');
            return;
            }
            
            if (password.length < 6) {
            showError('Password must be at least 6 characters long');
            return;
            }
            
            // Check if user already exists
            const existingUser = db.users.find(u => u.email === email);
            if (existingUser) {
            showError('An account with this email already exists');
            return;
            }
            
            // Create new user
            currentUser = {
            uid: 'user' + Date.now(),
            email: email,
            displayName: name,
            bio: ''
            };
            
            // Add to database with password
            db.addUser({
            ...currentUser,
            password: password // In a real app, this would be hashed
            });
            
            showSuccess('Account created successfully!');
        }
        
        // Update UI
        loginBtn.classList.add('hidden');
        profileBtn.classList.remove('hidden');
        logoutBtn.classList.remove('hidden');
        newPostBtn.classList.remove('hidden');
        authContainer.classList.add('hidden');
        forumContainer.classList.remove('hidden');
        
        // Reset form
        authForm.reset();
        
        // Send to socket
        socket.send(JSON.stringify({ type: 'user_login', userId: currentUser.uid }));
      });
      
      // Enhanced sort select
      sortSelect.addEventListener('change', () => {
        const value = sortSelect.value;
        loadDiscussions(value);
      });
      
      // Enhanced profile form
      profileForm.addEventListener('submit', (e) => {
        e.preventDefault();
        
        // Update user info
        currentUser.displayName = document.getElementById('profile-display-name').value;
        currentUser.bio = document.getElementById('profile-bio').value;
        
        // Update in database
        const user = db.getUser(currentUser.uid);
        if (user) {
          user.displayName = currentUser.displayName;
          user.bio = currentUser.bio;
        }
        
        // Update UI
        profileName.textContent = currentUser.displayName;
        profileAvatar.textContent = currentUser.displayName.charAt(0);
        
        alert('Profile updated successfully!');
      });
      
      // Load discussions on startup
      loadDiscussions();
    }

    // Initialize enhanced app when the DOM is loaded
    document.addEventListener('DOMContentLoaded', initEnhancedApp);
  </script>
</body>
</html>