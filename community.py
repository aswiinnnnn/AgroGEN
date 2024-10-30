import streamlit as st
import sqlite3
from PIL import Image
import io

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect("posts.db")
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            content TEXT NOT NULL,
            image BLOB
        )
    ''')
    conn.commit()
    conn.close()

# Function to add a post to the database
def add_post_to_db(title, content, image):
    conn = sqlite3.connect("posts.db")
    cursor = conn.cursor()
    
    try:
        if image is not None:
            # Convert uploaded file to bytes
            image_bytes = image.getvalue()
        else:
            image_bytes = None
        
        cursor.execute('INSERT INTO posts (title, content, image) VALUES (?, ?, ?)', 
                      (title, content, image_bytes))
        conn.commit()
        return True
    except Exception as e:
        st.error(f"Error saving post: {str(e)}")
        return False
    finally:
        conn.close()

# Function to retrieve posts from the database
def get_posts_from_db():
    conn = sqlite3.connect("posts.db")
    cursor = conn.cursor()
    try:
        cursor.execute('SELECT id, title, content, image FROM posts ORDER BY id DESC')
        posts = cursor.fetchall()
        return [{
            "id": post[0],
            "title": post[1],
            "content": post[2],
            "image": post[3]
        } for post in posts]
    except Exception as e:
        st.error(f"Error retrieving posts: {str(e)}")
        return []
    finally:
        conn.close()

def create_post():
    """Function to create a new post."""
    st.subheader("📝 Create a New Post")
    
    # Form inputs
    with st.form("post_form"):
        title = st.text_input("Title")
        content = st.text_area("Content")
        image = st.file_uploader("Upload an image", type=['jpg', 'jpeg', 'png'])
        
        submit_button = st.form_submit_button("Post")
        
        if submit_button:
            if title and content:
                if add_post_to_db(title, content, image):
                    st.success("Post created successfully!")
                    st.experimental_rerun()
            else:
                st.error("Please enter both title and content.")

def view_posts():
    """Function to display all posts with search functionality."""
    st.subheader("📖 All Posts")
    
    search_query = st.text_input("🔍 Search Posts", "")
    
    posts = get_posts_from_db()
    
    if search_query:
        posts = [
            post for post in posts 
            if search_query.lower() in post['title'].lower() 
            or search_query.lower() in post['content'].lower()
        ]
    
    if posts:
        for post in posts:
            with st.container():
                st.markdown(f"### {post['title']}")
                st.write(post['content'])
                
                # Display image if it exists
                if post['image'] is not None:
                    try:
                        # Create a BytesIO object from the image bytes
                        image_bytes = io.BytesIO(post['image'])
                        # Open the image using PIL
                        image = Image.open(image_bytes)
                        # Display the image
                        st.image(image, caption="Post Image", use_column_width=True)
                    except Exception as e:
                        st.error(f"Error displaying image for post {post['id']}: {str(e)}")
                
                st.markdown("---")
    else:
        st.info("No posts found.")

def faq_section():
    """Function to display frequently asked questions."""
    st.subheader("❓ Frequently Asked Questions (FAQ)")
    faqs = {
        "What is this forum about?": "This forum is a simple platform for sharing posts and discussions.",
        "How do I create a post?": "Select 'Create Post' from the sidebar and fill in the title and content.",
        "Can I edit or delete my posts?": "Currently, this feature is not supported. Please check back for updates.",
        "Who can participate?": "Anyone can create posts and view existing posts. All are welcome!"
    }
    
    for question, answer in faqs.items():
        st.markdown(f"*Q: {question}*")
        st.write(f"A: {answer}")
        st.markdown("---")

def community():
    """Main function to run the community app."""
    init_db()
    
    # Main title with custom style
    st.markdown("<h1 style='color: #4B9CD3;'>🌐 AgriGEN Community Forum</h1>", unsafe_allow_html=True)
    
    # Customized Sidebar
    st.sidebar.markdown(
        "<style>"
        "div[data-testid='stSidebar'] {"
        "    background-color: #f0f2f6;"
        "}"
        ".css-1aumxhk {"
        "    color: #4B9CD3;"
        "}"
        "</style>", unsafe_allow_html=True
    )
    
    # Sidebar header
    st.sidebar.header("Forum Actions")
    
    # Action with icon in sidebar
    action = st.sidebar.radio(
        "Choose an action:",
        ("📝 Create Post", "📖 View Posts", "❓ FAQ")
    )

    if action == "📝 Create Post":
        create_post()
    elif action == "📖 View Posts":
        view_posts()
    else:
        faq_section()

# Call the community function to run the app
community()
