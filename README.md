<h1>🌐 Smart Veterinary Care System with AI-Based Disease Detection</h1>
<p>A modern Django-based web application designed for scalability, performance, and clean architecture.</p>

<hr>

<h2>🖼️ Project Preview</h2>

<p>
  <img src="https://github.com/FarihaIslam321/CSE299-Project/blob/main/support/overview.jpeg"
       alt="Project Screenshot" width="800">
</p>

<hr>

<h1>🚀 Setup Guide — From Zero to Running Project</h1>

<p style="margin-top: 10px;">
  Assuming your system has no installed software mention below.  <strong>If have so no need to install this just follow further steps</strong>
</p>
<ul style="list-style: none; padding-left: 0; font-size: 16px; line-height: 1.7;">
  <li>❌ <strong>NO Python installed</strong></li>
  <li>❌ <strong>NO VS Code installed</strong></li>
  <li>❌ <strong>NO Django installed</strong></li>
</ul>

<p style="margin-top: 10px;">
  Follow the steps below <strong>one by one</strong> to set up and run the project successfully.
</p>

<hr>

<h2>🧩 1. Install Python (Full Beginner Guide)</h2>

<h3>📌 Download Python</h3>
<p>➡ <a href="https://www.python.org/downloads/">https://www.python.org/downloads/</a></p>

<h3>🎥 Python Installation Video (Windows)</h3>
<p>👉 <a href="https://www.youtube.com/watch?v=ddGTXBhaGWA">Watch Tutorial</a></p>

<p><strong>✔ IMPORTANT: During installation check:</strong></p>
<p>☑ Add Python to PATH</p>

<h3>🔍 Verify Installation</h3>
<p style="margin-top: 10px;">
  open terminal (cmd) then type below code:
</p>
<pre><code>python --version
pip --version
</code></pre>

<hr>

<h2>💻 2. Install VS Code</h2>

<h3>⬇ Download VS Code</h3>
<p>➡ <a href="https://code.visualstudio.com/download">https://code.visualstudio.com/download</a></p>

<h3>🎥 VS Code Installation Video</h3>
<p>👉 <a href="https://www.youtube.com/watch?v=wU7IQLIOwoo">Watch Tutorial</a></p>

<hr>

<h2>🧰 3. Download the Project</h2>
<h3>Using Git Clone in git bash</h3>
<pre><code>git clone https://github.com/FarihaIslam321/CSE299-Project.git
</code></pre>


<h3>Or Manually</h3>
<ul>
  <li>Download ZIP from GitHub</li>
  <li>Extract anywhere</li>
</ul>

<hr>

<h2>📂 4. Open the Project in VS Code</h2>

<h3>Option A — Open via windows Terminal</h3>
<p><strong>In your downloaded project folder open the the project folder then open terminal and type :</strong></p>
<pre><code>cd CSE299-Project
code .
</code></pre>

<h3>Option B — Manually</h3>
<ul>
  <li>Open VS Code</li>
  <li>Go to <strong>File → Open Folder</strong></li>
  <li>Select your project folder</li>
</ul>

<h3>✔ Ensure you're in the base directory where <code>manage.py</code> is located:</h3>
<pre><code>ls
</code></pre>

<p><strong>Expected output includes:</strong></p>
<ul>
  <li>manage.py</li>
  <li>requirements.txt</li>
  <li>app_folder/</li>
</ul>

<hr>

<h2>🌱 5. Create Virtual Environment (Important)</h2>

<p>You can skip this step just if you are not familier with virtual environemnet</p> 

<pre><code>python -m venv venv
</code></pre>

<h3>Activate It:</h3>

<p><strong>Windows:</strong></p>
<pre><code>venv\Scripts\activate
</code></pre>

<p><strong>Linux / Mac:</strong></p>
<pre><code>source venv/bin/activate
</code></pre>

<hr>

<h2>📦 6. Install Project Dependencies</h2>
<p>In your vs code open terminal or type (ctrl + j) to open then in the base directory of project where manage.py and requirements and other folder has then type: </p>

<pre><code>pip install -r requirements.txt
</code></pre>

<hr>

<h2>🛠️ 7. Run Django Commands</h2>

<p><strong>Make migrations:</strong></p>
<pre><code>python manage.py makemigrations
</code></pre>

<p><strong>Apply migrations:</strong></p>
<pre><code>python manage.py migrate
</code></pre>

<p><strong>Create admin user:</strong></p>
<pre><code>python manage.py createsuperuser
</code></pre>

<hr>

<h2>▶️ 8. Run the Development Server</h2>

<pre><code>python manage.py runserver
</code></pre>

<p>Now open your browser:</p>
<p><a href="http://127.0.0.1:8000/">http://127.0.0.1:8000/</a></p>

<p>🎉 <strong>Your project is now running!</strong></p>

<hr>

<h2>🔄 9. Pull Latest Updates (If Project Updated)</h2>
<pre><code>git pull
</code></pre>

<hr>

<h1>🤝 Contributing Guide</h1>

<p>We welcome all contributions! 💙</p>

<h3>📝 How to Contribute</h3>

<ol>
  <li><strong>Fork the repository</strong></li>
  <li>Clone your fork:</li>
</ol>
<div style="font-family: Arial, sans-serif; line-height: 1.6;">

  <h1 style="color: #2c3e50;">🔱 How to Fork This Repository</h1>

  <p><strong>Your Repository:</strong></p>
  <p>
    👉 <a href="https://github.com/FarihaIslam321/CSE299-Project" 
          style="color: #007bff; font-weight: bold;">
        https://github.com/FarihaIslam321/CSE299-Project
       </a>
  </p>

  <hr style="border: 0; height: 1px; background: #ddd; margin: 25px 0;">

  <h2 style="color: #34495e;">✅ Step 1 — Open the Repository</h2>
  <p>Go to the link above.</p>

  <h2 style="color: #34495e;">✅ Step 2 — Click the “Fork” Button</h2>
  <p>You will find the <strong>Fork</strong> button on the top-right corner of the GitHub page:</p>

  <div style="
      background: #f8f9fa;
      border-left: 4px solid #3498db;
      padding: 10px 15px;
      font-family: monospace;
      color: #2c3e50;
      margin: 10px 0;
      border-radius: 4px;">
    [ ★ Star ] &nbsp;&nbsp; [ 🍴 Fork ]
  </div>

  <h2 style="color: #34495e;">✅ Step 3 — Choose Your Account</h2>
  <p>GitHub will ask <em>“Where do you want to fork this repository?”</em>  
     Select your GitHub account.</p>

  <h2 style="color: #34495e;">✅ Step 4 — Confirm Fork</h2>
  <p>Click the <strong>Create fork</strong> button.</p>

  <p style="
      background: #e8f8f5;
      color: #117a65;
      padding: 12px;
      border-left: 5px solid #1abc9c;
      border-radius: 4px;
      margin-top: 15px;">
    🎉 <strong>Done! You now have your own forked copy of the repository.</strong>
  </p>

  <p>Your fork will be available at:</p>

  <div style="
      background: #fdf2e9;
      border-left: 4px solid #e67e22;
      padding: 10px 15px;
      border-radius: 4px;
      font-family: monospace;
      color: #d35400;">
    https://github.com/<strong>YOUR-USERNAME</strong>/CSE299-Project
  </div>

  <hr style="border: 0; height: 1px; background: #ddd; margin: 25px 0;">

  <h2 style="color: #34495e;">🧩 Optional: Clone Your Fork</h2>
  <p>If you want to download your fork to your computer:</p>

  <pre style="
      background: #2d2d2d;
      color: #f8f8f2;
      padding: 12px;
      border-radius: 5px;
      overflow-x: auto;
      font-size: 14px;">
git clone https://github.com/YOUR-USERNAME/CSE299-Project
  </pre>

  <p style="color: #7f8c8d;"><em>Replace YOUR-USERNAME with your GitHub username.</em></p>

</div>


<ol start="3">
  <li>Create a new branch:</li>
</ol>

<pre><code>git checkout -b feature-branch-name
</code></pre>

<ol start="4">
  <li>Make your changes</li>
  <li>Commit your changes:</li>
</ol>

<pre><code>git commit -m "Description of changes"
</code></pre>

<ol start="6">
  <li>Push your branch:</li>
</ol>

<pre><code>git push origin feature-branch-name
</code></pre>

<p>Then create a <strong>Pull Request</strong> on GitHub.</p>

<h3>✔ Contribution Rules</h3>
<ul>
  <li>Follow Django best practices</li>
  <li>Use clear commit messages</li>
  <li>Do not push directly to <code>main</code></li>
  <li>Follow project folder structure</li>
  <li>Add comments where necessary</li>
  <li>Test your changes before submitting</li>
</ul>

<hr>


<h2>🛡️ License</h2>

<p>This project is licensed under the <strong>MIT License</strong>.</p>

<hr>

<h2>🎉 Thank You for Using This Project!</h2>
<p>If this project helped you, give the repo a ⭐ on GitHub!</p>
