import os
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "super-secret-key-ai-platform")

# Initialize Supabase
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

# ---------------------------------------------------------------------------
# MOCK SERVICES
# ---------------------------------------------------------------------------
def send_whatsapp_message(phone, message_type, data):
    """Mock WhatsApp sending function"""
    print(f"[WhatsApp Automation] Sending {message_type} to {phone}")
    print(f"Data: {data}")
    return True

def ai_grade_submission(project_requirements, submission_content):
    """Mock AI Grading function"""
    print(f"[AI Grading Engine] Evaluating submission...")
    return {
        "score": 85,
        "feedback": "Great job! The submission meets most requirements but could use better structure.",
        "improvement_suggestions": "Try breaking down the paragraphs into more readable bullet points."
    }

# ---------------------------------------------------------------------------
# ROUTES
# ---------------------------------------------------------------------------

@app.route("/")
def index():
    projects = [
        {
            "title": "Weather App",
            "description": "A robust web-based inventory management system that enables businesses to track stock levels, manage orders, and generate detailed reports in real time.",
            "technologies": ["Python", "Flask", "SQLite", "Jinja2", "Bootstrap"],
            "github": "https://github.com/spw3bt3ch/ai-weather-app",
            "demo": "https://ai-weather-app-p7qr.onrender.com/",
            "image": "images/weather.png",
        },
        {
            "title": "Finance Tracker",
            "description": "A fully functional finance tracker for organizations, supporting inbox management, compose, reply, and attachment functionalities.",
            "technologies": ["Python", "Flask", "SQLite", "REST API", "JavaScript"],
            "github": "https://github.com/spw3bt3ch/finance-trkr",
            "demo": "https://github.com/spw3bt3ch/finance-trkr",
            "image": "images/finance-trckr.png",
        },
        {
            "title": "Portfolio Platform for Designers",
            "description": "A dynamic portfolio web application built for creative designers to showcase their work, attract clients, and manage project galleries.",
            "technologies": ["Python", "Flask", "Tailwind CSS", "SQLite", "Jinja2"],
            "github": "https://github.com/spw3bt3ch",
            "demo": "https://graphics-designers-portfolio-websit.vercel.app/",
            "image": "images/graphics-design.png",
        },
        {
            "title": "Health Radar",
            "description": "A modern Flask web application for evaluating 14 key health metrics including BMI, cardiovascular health, stroke risk, metabolic health, respiratory health, and more.",
            "technologies": ["Python", "Flask", "SQLite", "Jinja2", "Bootstrap"],
            "github": "https://github.com/spw3bt3ch",
            "demo": "https://health-plus-v1u7.onrender.com/",
            "image": "images/health-radarr.png",
        },
    ]

    skills = {
        "Backend": ["Python", "Flask", "FastAPI", "REST APIs"],
        "Frontend": ["HTML5", "Tailwind CSS", "JavaScript", "Jinja2"],
        "Database": ["SQLite", "PostgreSQL", "MySQL"],
        "Tools": ["Git", "GitHub", "Vercel", "Docker"],
    }

    services = [
        {
            "icon": "🖥️",
            "title": "Backend Development",
            "description": "Scalable, secure, and high-performance backend systems using Python, Flask, and FastAPI tailored to your business needs.",
        },
        {
            "icon": "🌐",
            "title": "Fullstack Web Development",
            "description": "End-to-end web applications with clean frontends and robust backends, from design to deployment.",
        },
        {
            "icon": "🔗",
            "title": "API Development",
            "description": "Custom RESTful APIs that power mobile apps, web clients, and third-party integrations with full documentation.",
        },
        {
            "icon": "⚙️",
            "title": "Custom Software Development",
            "description": "Bespoke software solutions engineered from scratch to solve unique business challenges efficiently.",
        },
        {
            "icon": "🤖",
            "title": "Automation Systems",
            "description": "Intelligent automation tools and scripts that eliminate repetitive tasks and streamline operations at scale.",
        },
        {
            "icon": "🎨",
            "title": "Graphics & Product Design",
            "description": "Creative visual solutions spanning brand identity, UI/UX design, and product graphics — delivering stunning, user-centred designs that communicate and convert.",
        },
    ]

    return render_template("index.html", projects=projects, skills=skills, services=services)


@app.route("/ai-training")
def ai_training():
    return render_template("genai_training.html")


# Legacy redirect — keep old URL working
@app.route("/women-ai-training")
def women_ai_training():
    from flask import redirect
    return redirect("/ai-training")


from datetime import datetime

# ---------------------------------------------------------------------------
# PLATFORM ROUTES
# ---------------------------------------------------------------------------

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        full_name = request.form.get("full_name")
        email = request.form.get("email")
        password = request.form.get("password")
        mobile = request.form.get("mobile_number")
        whatsapp = request.form.get("whatsapp_number") or mobile
        location = request.form.get("location")
        referral = request.form.get("referral_source")
        goal = request.form.get("learning_goal")

        # Basic validation handled by HTML form, but insert to Supabase here
        try:
            response = supabase.table("users").insert({
                "full_name": full_name,
                "email": email,
                "password": password,
                "mobile_number": mobile,
                "whatsapp_number": whatsapp,
                "location": location,
                "referral_source": referral,
                "learning_goal": goal,
                "role": "student",
                "created_by_admin": False,
                "is_verified": True
            }).execute()
            
            user_data = response.data[0]
            session['user_id'] = user_data['id']
            session['role'] = user_data['role']

            # WhatsApp Automation
            send_whatsapp_message(whatsapp, "WELCOME_AND_CREDS", {
                "name": full_name,
                "email": email
            })

            return redirect("https://chat.whatsapp.com/Dd42VhSNicJDGGBhFYKvhR")
        except Exception as e:
            print("Error registering:", e)
            return "Registration Error", 500

    return render_template("register.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        
        # Demo Admin Login
        if email == "admin@demo.com" and password == "demo123":
            session['user_id'] = "demo_admin_123"
            session['role'] = "admin"
            return redirect(url_for('admin_dashboard'))
            
        # Demo Student Login
        if email == "student@demo.com" and password == "demo123":
            session['user_id'] = "demo_student_123"
            session['role'] = "student"
            return redirect(url_for('student_dashboard'))
            
        # Demo Graduated Student Login
        if email == "graduated@demo.com" and password == "demo123":
            session['user_id'] = "demo_graduated_123"
            session['role'] = "student"
            return redirect(url_for('student_dashboard'))
            
        try:
            response = supabase.table("users").select("*").eq("email", email).eq("password", password).execute()
            if response.data:
                user = response.data[0]
                session['user_id'] = user['id']
                session['role'] = user['role']
                if user['role'] == 'admin':
                    return redirect(url_for('admin_dashboard'))
                return redirect(url_for('student_dashboard'))
        except Exception as e:
            print("Error logging in:", e)
            
        return "Invalid credentials", 401
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('index'))

@app.route("/student/dashboard")
def student_dashboard():
    if not session.get('user_id') or session.get('role') != 'student':
        return redirect(url_for('login'))
    
    # Fetch student name and progress
    student_name = "Student"
    progress_percent = 50 # Mock progress
    is_graduated = False
    
    projects = []
    if session.get('user_id') == 'demo_student_123':
        student_name = "Demo Student"
        progress_percent = 20
        # Mock project for demo
        projects = [{
            "id": 1,
            "title": "Module 1: Advanced Prompt Engineering",
            "description": "Design a multi-step prompt chain to automatically generate a complete marketing campaign from a single product description.",
            "instructions": "Your submission should include the exact prompts and the output generated by the AI.",
            "output_format": "Text/Links"
        }]
    elif session.get('user_id') == 'demo_graduated_123':
        student_name = "Graduated Scholar"
        progress_percent = 100
        is_graduated = True
        projects = [] # No pending projects
    else:
        try:
            response = supabase.table("users").select("full_name").eq("id", session.get('user_id')).execute()
            if response.data:
                student_name = response.data[0].get("full_name", "Student").split(" ")[0] # Use first name
            
            # Fetch dynamic projects
            proj_response = supabase.table("projects").select("*").execute()
            if proj_response.data:
                projects = proj_response.data
        except Exception as e:
            print("Error fetching user or projects:", e)
    
    return render_template("student_dashboard.html", student_name=student_name, progress_percent=progress_percent, projects=projects, is_graduated=is_graduated)

@app.route("/admin/dashboard")
def admin_dashboard():
    if not session.get('user_id') or session.get('role') != 'admin':
        return redirect(url_for('login'))
        
    return render_template("admin_dashboard.html")

@app.route("/admin/project/create", methods=["POST"])
def admin_project_create():
    if not session.get('user_id') or session.get('role') != 'admin':
        return redirect(url_for('login'))
        
    title = request.form.get("title")
    description = request.form.get("description")
    instructions = request.form.get("instructions")
    output_format = request.form.get("output_format")
    
    try:
        supabase.table("projects").insert({
            "title": title,
            "description": description,
            "instructions": instructions,
            "output_format": output_format
        }).execute()
    except Exception as e:
        print("Error creating project:", e)
        
    return redirect(url_for('admin_dashboard'))

@app.route("/student/submit", methods=["POST"])
def student_submit():
    if not session.get('user_id') or session.get('role') != 'student':
        return redirect(url_for('login'))
        
    project_id = request.form.get("project_id")
    content = request.form.get("content")
    
    # Handle File Upload
    file_url = None
    if 'submission_file' in request.files:
        file = request.files['submission_file']
        if file.filename != '':
            # Ensure static/uploads exists
            os.makedirs(os.path.join(app.root_path, 'static/uploads'), exist_ok=True)
            file_path = os.path.join(app.root_path, 'static/uploads', file.filename)
            file.save(file_path)
            file_url = f"/static/uploads/{file.filename}"
    
    # AI Grading placeholder
    grading_result = ai_grade_submission("Project Requirements", content)
    
    # Save to Supabase (submissions table)
    # Mock save for now
    print(f"Submitted to Project ID: {project_id}")
    print(f"File attached: {file_url}")
    
    return redirect(url_for('student_dashboard'))

@app.route("/certificate/<user_id>")
def certificate(user_id):
    # Fetch certificate data from Supabase
    return render_template("certificate.html")

BLOG_POSTS = {
    1: {
        "title": "Mastering Zero-Shot Prompting in GPT-4",
        "category": "Guide",
        "category_color": "blue-600",
        "date": "April 12, 2026",
        "read_time": "5 min read",
        "image": "https://images.unsplash.com/photo-1677442136019-21780ecad995?w=1200&q=80",
        "excerpt": "Learn the exact structure needed to consistently extract high-quality outputs from LLMs without providing examples, saving tokens and time.",
        "content": "<p class='mb-6'>Zero-shot prompting is a critical skill for any AI practitioner. Unlike few-shot prompting where you provide examples, zero-shot relies entirely on the model's pre-trained knowledge combined with the clarity of your instructions.</p><p class='mb-6'>To master zero-shot prompting, you must structure your prompts with explicit intent. Always define a <strong>Persona</strong>, outline the <strong>Task</strong>, set strict <strong>Constraints</strong>, and specify the exact <strong>Output Format</strong>. By removing ambiguity, the LLM stops guessing and starts executing exactly what you envisioned.</p>"
    },
    2: {
        "title": "Building Autonomous Agents for Customer Support",
        "category": "Automation",
        "category_color": "purple-600",
        "date": "April 5, 2026",
        "read_time": "8 min read",
        "image": "https://images.unsplash.com/photo-1620712943543-bcc4688e7485?w=1200&q=80",
        "excerpt": "A deep dive into connecting language models with your internal databases to create self-sufficient support agents that actually resolve tickets.",
        "content": "<p class='mb-6'>Customer support is undergoing a massive transformation. We are moving away from rigid decision-tree chatbots towards dynamic, autonomous agents powered by Large Language Models.</p><p class='mb-6'>By using frameworks like LangChain, you can give your AI agents 'tools'—the ability to query your SQL database, fetch order statuses via API, and trigger refunds. The agent dynamically decides which tool to use based on the customer's natural language request, completely automating up to 80% of tier-1 support tickets.</p>"
    },
    3: {
        "title": "Why 90% of Businesses Will Adopt AI by 2027",
        "category": "News",
        "category_color": "cyan-600",
        "date": "March 28, 2026",
        "read_time": "4 min read",
        "image": "https://images.unsplash.com/photo-1485827404703-89b55fcc595e?w=1200&q=80",
        "excerpt": "Recent industry reports show a massive shift in corporate spending towards AI integration. Here's what it means for your career trajectory.",
        "content": "<p class='mb-6'>Enterprise adoption of AI has accelerated beyond initial projections. According to recent tech industry surveys, corporate spending on AI infrastructure and software integration has tripled year-over-year.</p><p class='mb-6'>For professionals, this means AI literacy is no longer just a 'bonus skill'—it is the baseline. Those who understand how to implement LLMs into their daily workflows are seeing rapid career progression, acting as force multipliers within their organizations.</p>"
    },
    4: {
        "title": "Data Privacy in the Era of LLMs",
        "category": "Security",
        "category_color": "emerald-600",
        "date": "March 15, 2026",
        "read_time": "6 min read",
        "image": "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=1200&q=80",
        "excerpt": "How to ensure your company's proprietary data remains secure when building custom internal AI tools and API endpoints.",
        "content": "<p class='mb-6'>As companies rush to build custom AI tools using their internal data, security often takes a back seat. When passing proprietary data to external APIs like OpenAI or Anthropic, it is vital to understand their data retention and training policies.</p><p class='mb-6'>Using enterprise API tiers ensures your data is not used for model training. Additionally, techniques like PII masking and deploying open-source models (like Llama 3) locally on private servers provide maximum security for sensitive operations.</p>"
    },
    5: {
        "title": "AI-Assisted Pair Programming",
        "category": "Coding",
        "category_color": "rose-600",
        "date": "March 02, 2026",
        "read_time": "10 min read",
        "image": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?w=1200&q=80",
        "excerpt": "Our instructor breaks down exactly how to use Copilot and Claude to 10x your development speed without introducing subtle bugs.",
        "content": "<p class='mb-6'>Coding with an AI assistant requires a paradigm shift. You transition from being a syntax writer to an architectural director. AI models excel at writing boilerplate, generating tests, and refactoring blocks of code.</p><p class='mb-6'>However, blind acceptance of AI code leads to technical debt. The key is to provide the AI with extreme context—feeding it your schema, your styling guidelines, and your architectural decisions before asking it to generate a single line of code.</p>"
    },
    6: {
        "title": "The 4-Hour Workday with AI",
        "category": "Lifestyle",
        "category_color": "amber-600",
        "date": "February 20, 2026",
        "read_time": "4 min read",
        "image": "https://images.unsplash.com/photo-1593642532973-d31b6557fa68?w=1200&q=80",
        "excerpt": "A case study on a student who completely automated their administrative tasks, freeing up 20 hours a week to focus on deep work.",
        "content": "<p class='mb-6'>Sarah, a project manager and recent graduate of our AI program, successfully automated her most tedious weekly tasks. By chaining Zapier with the OpenAI API, she created a system that automatically summarizes client emails, drafts responses, and updates Jira boards.</p><p class='mb-6'>This simple automation pipeline saves her roughly 20 hours a week, allowing her to focus entirely on high-level strategy and team management. It proves that AI isn't about replacing jobs; it's about reclaiming your time.</p>"
    }
}

@app.route("/blog")
def blog():
    # Only logged in students (or admins) should access this according to the request
    if not session.get('user_id'):
        return redirect(url_for('login'))
        
    return render_template("blog.html", posts=BLOG_POSTS)

@app.route("/blog/<int:post_id>")
def blog_post(post_id):
    if not session.get('user_id'):
        return redirect(url_for('login'))
        
    post = BLOG_POSTS.get(post_id)
    if not post:
        return "Post not found", 404
        
    return render_template("blog_post.html", post=post)

if __name__ == "__main__":
    app.run(debug=True)
