import streamlit as st
from datetime import datetime
import google.generativeai as genai
import os
import json
from PIL import Image
import base64
import re

# Configure Gemini API with the newer model
genai.configure(api_key="AIzaSyDmp5-XbF4AfLbyBm1xOEjVwkg98LqCrUg")  # Replace with your actual API key
model = genai.GenerativeModel('gemini-1.5-flash')

# Create images directory if it doesn't exist
if not os.path.exists("images"):
    os.makedirs("images")

# Custom CSS for ultra high-end styling
def load_css():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800&family=Montserrat:wght@300;400;500;600;700&display=swap');
        
        :root {
            --primary: #5d417a;
            --primary-dark: #3e2a56;
            --primary-light: #7d5b9e;
            --secondary: #9e6b4e;
            --secondary-dark: #7a4f38;
            --secondary-light: #c38b6a;
            --accent: #f8b400;
            --accent-dark: #d89a00;
            --accent-light: #ffd166;
            --light: #f9f9f9;
            --light-gray: #f0f0f0;
            --dark: #222222;
            --dark-gray: #444444;
            --success: #28a745;
            --info: #17a2b8;
            --warning: #ffc107;
            --danger: #dc3545;
            --luxury: #8a6dae;
        }
        
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }
        
        body {
            font-family: 'Montserrat', sans-serif;
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            color: var(--dark);
            line-height: 1.6;
            overflow-x: hidden;
        }
        
        .main {
            background-color: rgba(255, 255, 255, 0.95);
            border-radius: 25px;
            box-shadow: 0 15px 40px rgba(0, 0, 0, 0.12);
            padding: 3rem;
            margin: 2rem auto;
            max-width: 1000px;
            border: 1px solid rgba(255, 255, 255, 0.4);
            backdrop-filter: blur(12px);
            transform-style: preserve-3d;
            perspective: 1000px;
            position: relative;
            overflow: hidden;
            transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.1);
        }
        
        .main::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(93, 65, 122, 0.05) 0%, transparent 70%);
            z-index: -1;
            animation: rotate 30s linear infinite;
        }
        
        @keyframes rotate {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
        
        h1, h2, h3, h4, h5, h6 {
            font-family: 'Playfair Display', serif;
            color: var(--primary-dark);
            font-weight: 700;
            letter-spacing: 0.5px;
            margin-bottom: 1rem;
        }
        
        h1 {
            font-size: 2.8rem;
            line-height: 1.2;
            text-shadow: 1px 1px 3px rgba(0, 0, 0, 0.1);
            position: relative;
            display: inline-block;
        }
        
        h1::after {
            content: '';
            position: absolute;
            bottom: -10px;
            left: 0;
            width: 70px;
            height: 4px;
            background: linear-gradient(90deg, var(--primary), var(--accent));
            border-radius: 2px;
        }
        
        h2 {
            font-size: 2.2rem;
            margin-top: 2.5rem;
            position: relative;
            padding-bottom: 10px;
        }
        
        h2::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 0;
            width: 50px;
            height: 3px;
            background: linear-gradient(90deg, var(--primary), var(--accent));
            border-radius: 2px;
        }
        
        h3 {
            font-size: 1.8rem;
            color: var(--primary);
        }
        
        h4 {
            font-size: 1.4rem;
            color: var(--primary-light);
        }
        
        p {
            margin-bottom: 1rem;
            color: var(--dark-gray);
            font-weight: 400;
        }
        
        .stButton>button {
            background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
            color: white;
            border: none;
            padding: 14px 28px;
            border-radius: 50px;
            font-weight: 600;
            font-size: 1rem;
            letter-spacing: 0.5px;
            box-shadow: 0 6px 20px rgba(93, 65, 122, 0.3);
            transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
            transform: translateY(0);
            position: relative;
            overflow: hidden;
            z-index: 1;
        }
        
        .stButton>button:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 25px rgba(93, 65, 122, 0.4);
        }
        
        .stButton>button::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: linear-gradient(135deg, var(--primary-dark) 0%, var(--primary) 100%);
            opacity: 0;
            transition: opacity 0.3s ease;
            z-index: -1;
        }
        
        .stButton>button:hover::before {
            opacity: 1;
        }
        
        .stTextInput>div>div>input, 
        .stNumberInput>div>div>input,
        .stDateInput>div>div>input,
        .stSelectbox>div>div>select,
        .stMultiSelect>div>div>div {
            border-radius: 12px !important;
            padding: 14px 18px !important;
            border: 1px solid rgba(0, 0, 0, 0.08) !important;
            box-shadow: 0 3px 8px rgba(0, 0, 0, 0.04) !important;
            transition: all 0.3s ease !important;
            font-size: 0.95rem !important;
            background-color: var(--light) !important;
        }
        
        .stTextInput>div>div>input:focus, 
        .stNumberInput>div>div>input:focus,
        .stDateInput>div>div>input:focus,
        .stSelectbox>div>div>select:focus,
        .stMultiSelect>div>div>div:focus {
            border-color: var(--primary-light) !important;
            box-shadow: 0 0 0 2px rgba(93, 65, 122, 0.2) !important;
        }
        
        .card {
            background: white;
            border-radius: 18px;
            padding: 25px;
            margin: 20px 0;
            box-shadow: 0 8px 25px rgba(0, 0, 0, 0.06);
            border: 1px solid rgba(0, 0, 0, 0.03);
            transition: all 0.4s cubic-bezier(0.165, 0.84, 0.44, 1);
            position: relative;
            overflow: hidden;
        }
        
        .card::before {
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            width: 4px;
            height: 100%;
            background: linear-gradient(to bottom, var(--primary), var(--accent));
        }
        
        .card:hover {
            transform: translateY(-8px);
            box-shadow: 0 12px 30px rgba(0, 0, 0, 0.12);
        }
        
        .food-image {
            border-radius: 15px;
            overflow: hidden;
            box-shadow: 0 8px 20px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
            height: 220px;
            object-fit: cover;
            width: 100%;
            transition: all 0.4s ease;
        }
        
        .food-image:hover {
            transform: scale(1.02);
            box-shadow: 0 12px 25px rgba(0, 0, 0, 0.15);
        }
        
        .sidebar .sidebar-content {
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            border-radius: 0 25px 25px 0;
            box-shadow: 8px 0 25px rgba(0, 0, 0, 0.06);
            padding: 2rem 1.5rem;
            border-left: 1px solid rgba(0, 0, 0, 0.05);
        }
        
        .divider {
            height: 1px;
            background: linear-gradient(to right, transparent, rgba(0,0,0,0.08), transparent);
            margin: 30px 0;
            border: none;
        }
        
        .tag {
            display: inline-block;
            background: rgba(93, 65, 122, 0.12);
            color: var(--primary-dark);
            padding: 6px 14px;
            border-radius: 50px;
            font-size: 0.85rem;
            margin-right: 10px;
            margin-bottom: 10px;
            font-weight: 500;
            transition: all 0.3s ease;
        }
        
        .tag:hover {
            background: rgba(93, 65, 122, 0.2);
            transform: translateY(-2px);
        }
        
        .price-level {
            display: inline-block;
            padding: 6px 16px;
            border-radius: 50px;
            font-size: 0.85rem;
            margin-right: 10px;
            margin-bottom: 10px;
            font-weight: 600;
            letter-spacing: 0.5px;
            text-transform: uppercase;
        }
        
        .low-price {
            background: rgba(40, 167, 69, 0.12);
            color: var(--success);
        }
        
        .medium-price {
            background: rgba(255, 193, 7, 0.12);
            color: var(--warning);
        }
        
        .high-price {
            background: rgba(220, 53, 69, 0.12);
            color: var(--danger);
        }
        
        .luxury-price {
            background: rgba(138, 109, 174, 0.15);
            color: var(--luxury);
            box-shadow: 0 0 0 1px rgba(138, 109, 174, 0.3);
        }
        
        .metric-container {
            background: white;
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 5px 15px rgba(0, 0, 0, 0.05);
            border: 1px solid rgba(0, 0, 0, 0.03);
            transition: all 0.3s ease;
        }
        
        .metric-container:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0, 0, 0, 0.08);
        }
        
        .metric-title {
            font-size: 0.9rem;
            color: var(--dark-gray);
            font-weight: 500;
            margin-bottom: 5px;
        }
        
        .metric-value {
            font-size: 1.8rem;
            font-weight: 700;
            color: var(--primary-dark);
            font-family: 'Playfair Display', serif;
        }
        
        .success-message {
            background: rgba(40, 167, 69, 0.1);
            border-left: 4px solid var(--success);
            padding: 20px;
            border-radius: 0 8px 8px 0;
            margin: 20px 0;
        }
        
        .spinner-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            padding: 40px;
        }
        
        .spinner {
            width: 50px;
            height: 50px;
            border: 5px solid rgba(93, 65, 122, 0.1);
            border-radius: 50%;
            border-top-color: var(--primary);
            animation: spin 1s ease-in-out infinite;
            margin-bottom: 20px;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        
        .floating-shape {
            position: absolute;
            opacity: 0.05;
            z-index: -1;
        }
        
        .shape-1 {
            top: -50px;
            right: -50px;
            width: 200px;
            height: 200px;
            background: radial-gradient(circle, var(--primary) 0%, transparent 70%);
            border-radius: 50%;
        }
        
        .shape-2 {
            bottom: -100px;
            left: -100px;
            width: 300px;
            height: 300px;
            background: radial-gradient(circle, var(--accent) 0%, transparent 70%);
            border-radius: 50%;
        }
        
        .shape-3 {
            top: 50%;
            right: -100px;
            width: 150px;
            height: 150px;
            background: radial-gradient(circle, var(--secondary) 0%, transparent 70%);
            border-radius: 50%;
        }
        
        /* Responsive adjustments */
        @media (max-width: 768px) {
            .main {
                padding: 2rem;
                border-radius: 20px;
            }
            
            h1 {
                font-size: 2.2rem;
            }
            
            h2 {
                font-size: 1.8rem;
            }
            
            .stButton>button {
                padding: 12px 24px;
            }
        }
    </style>
    """, unsafe_allow_html=True)

# Function to generate food recommendations using Gemini 1.5 Flash
def generate_recommendations(event_data):
    prompt = f"""
    Act as an expert party food planner. Recommend a complete menu for the following event:
    
    Event Name: {event_data['event_name']}
    Date: {event_data['date'].strftime('%B %d, %Y')}
    Number of Guests: {event_data['guests']}
    Dietary Preferences: {', '.join(event_data['dietary_preferences'])}
    Event Type: {event_data['event_type']}
    Cuisine: {event_data['cuisine']}
    Expense Level: {event_data['expense_level']}
    
    Provide recommendations in the following JSON format:
    {{
        "menu_name": "Creative name for this menu",
        "description": "Brief description of why this menu fits the event",
        "appetizers": [
            {{
                "name": "Appetizer name",
                "description": "Brief description",
                "serving_size": "Serving size for {event_data['guests']} guests",
                "image_prompt": "Detailed prompt for generating an image of this dish"
            }}
        ],
        "main_courses": [
            {{
                "name": "Main course name",
                "description": "Brief description",
                "serving_size": "Serving size for {event_data['guests']} guests",
                "image_prompt": "Detailed prompt for generating an image of this dish"
            }}
        ],
        "desserts": [
            {{
                "name": "Dessert name",
                "description": "Brief description",
                "serving_size": "Serving size for {event_data['guests']} guests",
                "image_prompt": "Detailed prompt for generating an image of this dish"
            }}
        ],
        "beverages": [
            {{
                "name": "Beverage name",
                "description": "Brief description",
                "serving_size": "Serving size for {event_data['guests']} guests",
                "image_prompt": "Detailed prompt for generating an image of this drink"
            }}
        ],
        "grocery_list": [
            {{
                "ingredient": "Ingredient name",
                "quantity": "Estimated quantity for {event_data['guests']} guests",
                "category": "Category (produce, dairy, etc.)"
            }}
        ],
        "budget_estimate": {{
            "low_range": "Estimated low budget range",
            "high_range": "Estimated high budget range",
            "currency": "USD"
        }},
        "leftover_tips": [
            "Tip 1 for handling leftovers",
            "Tip 2 for handling leftovers"
        ]
    }}
    
    Make sure the menu:
    1. Perfectly matches the dietary preferences
    2. Is appropriate for the event type
    3. Fits the specified cuisine
    4. Matches the expense level
    5. Includes authentic Indian options if "other" dietary preference is selected
    6. Provides accurate serving sizes for the number of guests
    Ensure the response is a valid JSON string without any markdown or extra text.
    """
    
    try:
        response = model.generate_content(prompt)
        response_text = response.text.strip()

        # Remove any markdown code block markers (e.g., ```json or ```)
        response_text = re.sub(r'^```json\s*|\s*```$', '', response_text, flags=re.MULTILINE)
        response_text = response_text.strip()

        # Use regex to find the JSON content between curly braces
        json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
        if not json_match:
            st.error("No valid JSON found in the response. Using a mock response instead.")
            return {
                "menu_name": "Sample Menu",
                "description": "A sample menu for demonstration purposes.",
                "appetizers": [
                    {
                        "name": "Sample Appetizer",
                        "description": "A delicious starter.",
                        "serving_size": f"Serves {event_data['guests']}",
                        "image_prompt": "A plate of appetizers on a wooden table"
                    }
                ],
                "main_courses": [
                    {
                        "name": "Sample Main Course",
                        "description": "A hearty main dish.",
                        "serving_size": f"Serves {event_data['guests']}",
                        "image_prompt": "A plate of main course with garnish"
                    }
                ],
                "desserts": [
                    {
                        "name": "Sample Dessert",
                        "description": "A sweet treat.",
                        "serving_size": f"Serves {event_data['guests']}",
                        "image_prompt": "A dessert on a plate with a fork"
                    }
                ],
                "beverages": [
                    {
                        "name": "Sample Beverage",
                        "description": "A refreshing drink.",
                        "serving_size": f"Serves {event_data['guests']}",
                        "image_prompt": "A glass of beverage with ice"
                    }
                ],
                "grocery_list": [
                    {
                        "ingredient": "Sample Ingredient",
                        "quantity": "1 unit",
                        "category": "produce"
                    }
                ],
                "budget_estimate": {
                    "low_range": "$50",
                    "high_range": "$100",
                    "currency": "USD"
                },
                "leftover_tips": [
                    "Store in airtight containers.",
                    "Refrigerate promptly."
                ]
            }

        json_str = json_match.group(0)
        # Attempt to parse the JSON
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            st.error(f"Invalid JSON format: {str(e)}. Using a mock response instead.")
            return {
                "menu_name": "Sample Menu",
                "description": "A sample menu for demonstration purposes.",
                "appetizers": [
                    {
                        "name": "Sample Appetizer",
                        "description": "A delicious starter.",
                        "serving_size": f"Serves {event_data['guests']}",
                        "image_prompt": "A plate of appetizers on a wooden table"
                    }
                ],
                "main_courses": [
                    {
                        "name": "Sample Main Course",
                        "description": "A hearty main dish.",
                        "serving_size": f"Serves {event_data['guests']}",
                        "image_prompt": "A plate of main course with garnish"
                    }
                ],
                "desserts": [
                    {
                        "name": "Sample Dessert",
                        "description": "A sweet treat.",
                        "serving_size": f"Serves {event_data['guests']}",
                        "image_prompt": "A dessert on a plate with a fork"
                    }
                ],
                "beverages": [
                    {
                        "name": "Sample Beverage",
                        "description": "A refreshing drink.",
                        "serving_size": f"Serves {event_data['guests']}",
                        "image_prompt": "A glass of beverage with ice"
                    }
                ],
                "grocery_list": [
                    {
                        "ingredient": "Sample Ingredient",
                        "quantity": "1 unit",
                        "category": "produce"
                    }
                ],
                "budget_estimate": {
                    "low_range": "$50",
                    "high_range": "$100",
                    "currency": "USD"
                },
                "leftover_tips": [
                    "Store in airtight containers.",
                    "Refrigerate promptly."
                ]
            }
    except Exception as e:
        st.error(f"Error generating recommendations: {str(e)}. Using a mock response instead.")
        return {
            "menu_name": "Sample Menu",
            "description": "A sample menu for demonstration purposes.",
            "appetizers": [
                {
                    "name": "Sample Appetizer",
                    "description": "A delicious starter.",
                    "serving_size": f"Serves {event_data['guests']}",
                    "image_prompt": "A plate of appetizers on a wooden table"
                }
            ],
            "main_courses": [
                {
                    "name": "Sample Main Course",
                    "description": "A hearty main dish.",
                    "serving_size": f"Serves {event_data['guests']}",
                    "image_prompt": "A plate of main course with garnish"
                }
            ],
            "desserts": [
                {
                    "name": "Sample Dessert",
                    "description": "A sweet treat.",
                    "serving_size": f"Serves {event_data['guests']}",
                    "image_prompt": "A dessert on a plate with a fork"
                }
            ],
            "beverages": [
                {
                    "name": "Sample Beverage",
                    "description": "A refreshing drink.",
                    "serving_size": f"Serves {event_data['guests']}",
                    "image_prompt": "A glass of beverage with ice"
                }
            ],
            "grocery_list": [
                {
                    "ingredient": "Sample Ingredient",
                    "quantity": "1 unit",
                    "category": "produce"
                }
            ],
            "budget_estimate": {
                "low_range": "$50",
                "high_range": "$100",
                "currency": "USD"
            },
            "leftover_tips": [
                "Store in airtight containers.",
                "Refrigerate promptly."
            ]
        }

# Function to get local image based on cuisine type
def get_local_image(cuisine_type, dish_name):
    # Map cuisine types to local image paths
    image_map = {
        "Indian": "images/indian.jpg",
        "Italian": "images/italian.jpg",
        "Mexican": "images/mexican.jpg",
        "Chinese": "images/chinese.webp",
        "American": "images/american.jpg",
        "Mediterranean": "images/mediterranean.jpg"
    }
    
    # Default image if specific cuisine image not found
    default_image = "images/default.jpg"
    
    # Try to get the cuisine-specific image, fallback to default
    image_path = image_map.get(cuisine_type, default_image)
    
    # Check if file exists, if not use default
    if not os.path.exists(image_path):
        image_path = default_image
    
    return image_path

# Function to display a dish section
def display_dish_section(title, dishes, cuisine):
    st.markdown(f"### {title}")
    cols = st.columns(2)
    for i, dish in enumerate(dishes):
        with cols[i % 2]:
            with st.container():
                st.markdown(f"#### {dish['name']}")
                
                # Get local image path
                image_path = get_local_image(cuisine, dish['name'])
                
                # Display image with error handling
                try:
                    st.image(image_path, use_column_width=True, caption=dish['name'])
                except Exception as e:
                    st.error(f"Error loading image: {e}")
                    st.image("images/default.jpg", use_column_width=True, caption="Default dish image")
                
                st.markdown(f"<p style='margin-bottom: 10px;'><strong>Description:</strong> {dish['description']}</p>", unsafe_allow_html=True)
                st.markdown(f"<p style='margin-bottom: 15px;'><strong>Serving Size:</strong> {dish['serving_size']}</p>", unsafe_allow_html=True)
                st.markdown("---")

# Main app function
def main():
    load_css()
    
    # Sidebar with logo and info
    with st.sidebar:
        st.markdown("<h1 style='text-align: center; color: var(--primary); margin-bottom: 0;'>PLANORA</h1>", unsafe_allow_html=True)
        st.markdown("<p style='text-align: center; margin-top: 0; color: var(--secondary); font-weight: 500;'>PARTY FOOD PLANNER</p>", unsafe_allow_html=True)
        
        # Display local logo image
        try:
            logo_path = "images/logo.png"
            if os.path.exists(logo_path):
                st.image(logo_path, use_column_width=True)
            else:
                st.warning("Logo image not found at images/logo.jpg")
        except Exception as e:
            st.error(f"Error loading logo: {e}")
        
        st.markdown("""
        <div class='card' style='margin-top: 20px;'>
            <h4>Problem Solved</h4>
            <p>Event organizers often struggle with disconnected tools for menu planning, leading to inefficiencies like:</p>
            <ul style='margin-left: 20px; color: var(--dark-gray);'>
                <li>Forgotten ingredients</li>
                <li>Last-minute store runs</li>
                <li>Food wastage</li>
                <li>Lack of preparation</li>
            </ul>
            <p>PLANORA solves all these with AI-powered comprehensive planning.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Main content
    st.markdown("<div class='floating-shape shape-1'></div>", unsafe_allow_html=True)
    st.markdown("<div class='floating-shape shape-2'></div>", unsafe_allow_html=True)
    st.markdown("<div class='floating-shape shape-3'></div>", unsafe_allow_html=True)
    
    st.markdown("<h1 style='text-align: center; position: relative;'>PLANORA <span style='font-size: 1.8rem; vertical-align: middle; color: var(--secondary);'>- PARTY FOOD PLANNER</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; margin-top: -10px; color: var(--dark-gray); font-size: 1.1rem;'>Create the perfect menu for your event with AI-powered recommendations</p>", unsafe_allow_html=True)
    
    with st.form("event_form"):
        st.markdown("### Event Details")
        
        col1, col2 = st.columns(2)
        with col1:
            event_name = st.text_input("Event Name*", placeholder="e.g., Priya's Birthday Party")
            date = st.date_input("Date*", min_value=datetime.today())
            guests = st.number_input("Number of Guests*", min_value=1, max_value=500, value=20)
            
        with col2:
            event_type = st.selectbox("Type of Event*", 
                                    ["Birthday", "Wedding", "Corporate", "Casual Gathering", "Anniversary", "Other"])
            cuisine = st.selectbox("Cuisine*", 
                                 ["Indian", "Italian", "Mexican", "Chinese", "American", "Mediterranean", "Other"])
            expense_level = st.selectbox("Expense Level*", 
                                       ["Budget", "Moderate", "Premium", "Luxury"])
        
        dietary_preferences = st.multiselect("Dietary Preferences*",
                                           ["Vegetarian", "Vegan", "Nut-Free", "Non-Vegetarian", 
                                            "Dairy-Free", "Gluten-Free", "Other (Authentic Indian)"])
        
        submitted = st.form_submit_button("✨ Generate Menu Plan", type="primary")
    
    if submitted:
        if not event_name or not date or not guests or not event_type or not cuisine or not expense_level or not dietary_preferences:
            st.error("Please fill all required fields (marked with *)")
        else:
            event_data = {
                "event_name": event_name,
                "date": date,
                "guests": guests,
                "dietary_preferences": dietary_preferences,
                "event_type": event_type,
                "cuisine": cuisine,
                "expense_level": expense_level
            }
            
            with st.spinner("""
                <div class='spinner-container'>
                    <div class='spinner'></div>
                    <p style='color: var(--primary); font-weight: 500;'>Creating your perfect menu plan...</p>
                </div>
            """):
                recommendations = generate_recommendations(event_data)
                
                if recommendations:
                    st.markdown("""
                    <div class='success-message'>
                        <h3 style='color: var(--success); margin-bottom: 10px;'>Your custom menu plan is ready!</h3>
                        <p style='color: var(--dark-gray);'>Scroll down to view your personalized recommendations.</p>
                    </div>
                    """, unsafe_allow_html=True)
                    st.balloons()
                    
                    # Display the menu
                    st.markdown(f"## {recommendations['menu_name']}")
                    st.markdown(f"<p style='font-size: 1.1rem; color: var(--dark-gray);'>{recommendations['description']}</p>", unsafe_allow_html=True)
                    
                    # Display price level tag
                    price_class = "low-price" if expense_level == "Budget" else \
                                 "medium-price" if expense_level == "Moderate" else \
                                 "high-price" if expense_level == "Premium" else "luxury-price"
                    st.markdown(f"<span class='price-level {price_class}'>{expense_level}</span>", unsafe_allow_html=True)
                    
                    # Display dietary tags
                    tags_html = "".join([f"<span class='tag'>{pref}</span>" for pref in dietary_preferences])
                    st.markdown(tags_html, unsafe_allow_html=True)
                    
                    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
                    
                    # Display menu sections
                    st.markdown("## 🍽️ Menu Recommendations")
                    
                    if recommendations.get('appetizers'):
                        display_dish_section("🥟 Appetizers", recommendations['appetizers'], cuisine)
                    
                    if recommendations.get('main_courses'):
                        display_dish_section("🍛 Main Courses", recommendations['main_courses'], cuisine)
                    
                    if recommendations.get('desserts'):
                        display_dish_section("🍰 Desserts", recommendations['desserts'], cuisine)
                    
                    if recommendations.get('beverages'):
                        display_dish_section("🍹 Beverages", recommendations['beverages'], cuisine)
                    
                    # Grocery List
                    st.markdown("## 🛒 Grocery List")
                    grocery_cols = st.columns(3)
                    categories = {}
                    for item in recommendations['grocery_list']:
                        if item['category'] not in categories:
                            categories[item['category']] = []
                        categories[item['category']].append(f"{item['ingredient']} ({item['quantity']})")
                    
                    for i, (category, items) in enumerate(categories.items()):
                        with grocery_cols[i % 3]:
                            with st.expander(f"**{category.capitalize()}**", expanded=True):
                                for item in items:
                                    st.markdown(f"- {item}")
                    
                    # Budget Estimate
                    st.markdown("## 💰 Budget Estimate")
                    col1, col2 = st.columns(2)
                    with col1:
                        st.markdown(f"""
                        <div class='metric-container'>
                            <div class='metric-title'>Low Range Estimate</div>
                            <div class='metric-value'>{recommendations['budget_estimate']['low_range']}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    with col2:
                        st.markdown(f"""
                        <div class='metric-container'>
                            <div class='metric-title'>High Range Estimate</div>
                            <div class='metric-value'>{recommendations['budget_estimate']['high_range']}</div>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # Leftover Tips
                    st.markdown("## ♻️ Leftover Management Tips")
                    for tip in recommendations['leftover_tips']:
                        st.markdown(f"- {tip}")

if __name__ == "__main__":
    main()
