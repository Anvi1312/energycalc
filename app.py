import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

def calculate_base_energy(flat_tenement, bhk):
    """
    Calculate base energy consumption based on housing type and BHK configuration
    Uses realistic kWh values based on Indian residential consumption patterns
    
    Args:
        flat_tenement (str): Housing type - 'flat' or 'tenement'
        bhk (str): BHK configuration - '1BHK', '2BHK', or '3BHK'
    
    Returns:
        dict: Base energy consumption breakdown
    """
    # Base consumption in kWh per day for different appliances
    base_consumption = {
        'flat': {
            '1BHK': {
                'lighting': 1.5,
                'fan_ac': 4.0,
                'appliances': 3.5,
                'water_heater': 2.0,
                'refrigerator': 1.8
            },
            '2BHK': {
                'lighting': 2.2,
                'fan_ac': 6.0,
                'appliances': 4.5,
                'water_heater': 2.5,
                'refrigerator': 2.0
            },
            '3BHK': {
                'lighting': 3.0,
                'fan_ac': 8.0,
                'appliances': 6.0,
                'water_heater': 3.0,
                'refrigerator': 2.2
            }
        },
        'tenement': {
            '1BHK': {
                'lighting': 1.8,
                'fan_ac': 5.0,
                'appliances': 3.0,
                'water_heater': 1.5,
                'refrigerator': 1.6
            },
            '2BHK': {
                'lighting': 2.5,
                'fan_ac': 7.0,
                'appliances': 4.0,
                'water_heater': 2.0,
                'refrigerator': 1.8
            },
            '3BHK': {
                'lighting': 3.5,
                'fan_ac': 9.0,
                'appliances': 5.5,
                'water_heater': 2.5,
                'refrigerator': 2.0
            }
        }
    }
    
    return base_consumption.get(flat_tenement, {}).get(bhk, {})

def calculate_weather_adjustment(temperature, base_fan_ac):
    """
    Adjust fan/AC consumption based on temperature
    
    Args:
        temperature (float): Temperature in Celsius
        base_fan_ac (float): Base fan/AC consumption
    
    Returns:
        float: Adjusted fan/AC consumption
    """
    if temperature < 18:
        # Very cold - minimal fan usage
        return base_fan_ac * 0.1
    elif temperature < 22:
        # Cool - reduced fan usage
        return base_fan_ac * 0.3
    elif temperature < 26:
        # Comfortable - normal fan usage
        return base_fan_ac * 0.6
    elif temperature < 30:
        # Warm - increased fan usage
        return base_fan_ac * 0.8
    elif temperature < 35:
        # Hot - maximum fan usage
        return base_fan_ac * 1.0
    else:
        # Very hot - AC usage increases
        return base_fan_ac * 1.3

def calculate_daily_energy(flat_tenement, bhk, temperature):
    """
    Calculate daily energy consumption with weather adjustment
    
    Args:
        flat_tenement (str): Housing type
        bhk (str): BHK configuration
        temperature (float): Daily temperature
    
    Returns:
        dict: Daily energy consumption breakdown
    """
    base_energy = calculate_base_energy(flat_tenement, bhk)
    if not base_energy:
        return None
    
    # Apply weather adjustment to fan/AC consumption
    adjusted_fan_ac = calculate_weather_adjustment(temperature, base_energy['fan_ac'])
    
    daily_consumption = {
        'lighting': base_energy['lighting'],
        'fan_ac': adjusted_fan_ac,
        'appliances': base_energy['appliances'],
        'water_heater': base_energy['water_heater'],
        'refrigerator': base_energy['refrigerator']
    }
    
    daily_consumption['total'] = sum(daily_consumption.values())
    
    return daily_consumption

def main():
    # Custom CSS for bright, glowing UI
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    .stApp {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 25%, #f093fb 50%, #f5576c 75%, #4facfe 100%);
        background-size: 400% 400%;
        animation: gradientShift 10s ease infinite;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .main-header {
        text-align: center;
        background: linear-gradient(135deg, #ff6b6b, #feca57, #48dbfb, #ff9ff3);
        background-size: 400% 400%;
        animation: gradientShift 6s ease infinite;
        color: white;
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        border: 2px solid rgba(255,255,255,0.2);
        backdrop-filter: blur(10px);
    }
    
    .main-header h1 {
        font-family: 'Poppins', sans-serif;
        font-weight: 700;
        font-size: 2.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        margin: 0;
    }
    
    .main-header p {
        font-family: 'Poppins', sans-serif;
        font-weight: 300;
        font-size: 1.2rem;
        margin: 0;
        opacity: 0.9;
    }
    
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        background: rgba(255,255,255,0.1);
        padding: 10px;
        border-radius: 15px;
        backdrop-filter: blur(10px);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        border-radius: 15px;
        padding: 10px 20px;
        font-weight: 600;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
        border: none;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #ff6b6b, #feca57) !important;
        animation: glow 2s ease-in-out infinite alternate;
    }
    
    @keyframes glow {
        from { box-shadow: 0 5px 15px rgba(255,107,107,0.5); }
        to { box-shadow: 0 8px 25px rgba(255,107,107,0.8); }
    }
    
    .stSidebar {
        background: linear-gradient(180deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05));
        backdrop-filter: blur(10px);
        border-right: 2px solid rgba(255,255,255,0.2);
    }
    
    .stMetric {
        background: linear-gradient(135deg, rgba(255,255,255,0.2), rgba(255,255,255,0.1));
        padding: 1rem;
        border-radius: 15px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.3);
        box-shadow: 0 8px 25px rgba(0,0,0,0.2);
    }
    
    .stMetric label {
        color: white !important;
        font-weight: 600;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }
    
    .stMetric [data-testid="metric-value"] {
        color: #fff !important;
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.4);
    }
    
    .weather-card {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 1.5rem;
        border-radius: 20px;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        border: 2px solid rgba(255,255,255,0.2);
        backdrop-filter: blur(10px);
        animation: float 3s ease-in-out infinite;
    }
    
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-5px); }
    }
    
    .stButton > button {
        background: linear-gradient(135deg, #ff6b6b, #feca57);
        color: white;
        border: none;
        border-radius: 15px;
        padding: 0.7rem 2rem;
        font-weight: 600;
        font-size: 1.1rem;
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(255,107,107,0.4);
    }
    
    .stDataFrame {
        background: rgba(255,255,255,0.9);
        border-radius: 15px;
        padding: 1rem;
        backdrop-filter: blur(10px);
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    .stExpander {
        background: rgba(255,255,255,0.1);
        border-radius: 15px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.3);
    }
    
    .stTextInput > div > div > input {
        background: rgba(255,255,255,0.9);
        border: 2px solid rgba(255,255,255,0.3);
        border-radius: 10px;
        color: #333;
        font-weight: 500;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 10px rgba(102,126,234,0.5);
    }
    
    .stNumberInput > div > div > input {
        background: rgba(255,255,255,0.9);
        border: 2px solid rgba(255,255,255,0.3);
        border-radius: 10px;
        color: #333;
        font-weight: 500;
    }
    
    .stSlider {
        background: rgba(255,255,255,0.1);
        padding: 1rem;
        border-radius: 15px;
        backdrop-filter: blur(10px);
    }
    
    .stAlert {
        background: rgba(255,255,255,0.9);
        border-radius: 15px;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.3);
    }
    
    h1, h2, h3 {
        font-family: 'Poppins', sans-serif;
        color: white;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .stMarkdown {
        color: white;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.3);
    }
    
    .bright-card {
        background: linear-gradient(135deg, #667eea, #764ba2);
        color: white;
        padding: 1.5rem;
        border-radius: 20px;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
        border: 2px solid rgba(255,255,255,0.2);
        backdrop-filter: blur(10px);
    }
    
    .glow-text {
        text-shadow: 0 0 10px rgba(255,255,255,0.8);
        font-weight: 700;
    }
    </style>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="main-header">
        <h1>⚡ Smart Energy Consumption Calculator 🏠</h1>
        <p>Track your daily energy usage with weather-smart calculations</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Personal Information Section in Main Area
    st.markdown("""
    <div class="bright-card" style="background: linear-gradient(135deg, #667eea, #764ba2); text-align: center; margin: 2rem 0;">
        <h2 class="glow-text" style="margin: 0; font-size: 2rem;">👤 Personal Information</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Create columns for personal info
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Enter Your Name:", placeholder="e.g., John Doe")
        city = st.text_input("Enter Your City:", placeholder="e.g., Mumbai")
    
    with col2:
        age = st.number_input("Enter Your Age:", min_value=1, max_value=120, value=25)
        area = st.text_input("Enter Your Area:", placeholder="e.g., Bandra")
    
    # Housing Information Section
    st.markdown("""
    <div class="bright-card" style="background: linear-gradient(135deg, #ff6b6b, #feca57); text-align: center; margin: 2rem 0;">
        <h2 class="glow-text" style="margin: 0; font-size: 2rem;">🏠 Housing Information</h2>
    </div>
    """, unsafe_allow_html=True)
    
    # Create columns for housing info
    col1, col2 = st.columns(2)
    
    with col1:
        flat_tenement = st.selectbox(
            "Housing Type:",
            options=["flat", "tenement"],
            help="Flats are typically in apartment buildings, tenements are independent houses"
        )
    
    with col2:
        bhk = st.selectbox(
            "BHK Configuration:",
            options=["1BHK", "2BHK", "3BHK"],
            help="Select your BHK configuration"
        )
    
    # Main content area
    st.header("📅 Weekly Energy Tracking")
    
    # Days of the week tabs
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    day_emojis = ["🌅", "🌤️", "⛅", "🌞", "🌆", "🌙", "🌟"]
    
    # Create tabs for each day
    tabs = st.tabs([f"{emoji} {day}" for emoji, day in zip(day_emojis, days)])
    
    weekly_data = []
    
    for i, (tab, day) in enumerate(zip(tabs, days)):
        with tab:
            col1, col2 = st.columns([1, 1])
            
            with col1:
                st.subheader(f"🌡️ Weather for {day}")
                temperature = st.slider(
                    f"Temperature (°C) - {day}",
                    min_value=10,
                    max_value=45,
                    value=25,
                    key=f"temp_{i}"
                )
                
                # Weather description based on temperature
                if temperature < 18:
                    weather_desc = "❄️ Very Cold"
                    weather_gradient = "linear-gradient(135deg, #74b9ff, #0984e3)"
                elif temperature < 22:
                    weather_desc = "🌤️ Cool"
                    weather_gradient = "linear-gradient(135deg, #00cec9, #00b894)"
                elif temperature < 26:
                    weather_desc = "😊 Comfortable"
                    weather_gradient = "linear-gradient(135deg, #00b894, #55a3ff)"
                elif temperature < 30:
                    weather_desc = "🌞 Warm"
                    weather_gradient = "linear-gradient(135deg, #fdcb6e, #f39c12)"
                elif temperature < 35:
                    weather_desc = "🔥 Hot"
                    weather_gradient = "linear-gradient(135deg, #fd79a8, #e84393)"
                else:
                    weather_desc = "🌋 Very Hot"
                    weather_gradient = "linear-gradient(135deg, #ff6b6b, #ee5253)"
                
                st.markdown(f"""
                <div class="bright-card" style="background: {weather_gradient}; text-align: center; animation: float 3s ease-in-out infinite;">
                    <h3 class="glow-text" style="margin: 0; font-size: 1.5rem;">{weather_desc}</h3>
                    <h2 class="glow-text" style="margin: 0.5rem 0; font-size: 2.5rem;">{temperature}°C</h2>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.subheader("⚡ Energy Calculation")
                
                if name.strip() and city.strip() and area.strip():
                    daily_energy = calculate_daily_energy(flat_tenement, bhk, temperature)
                    
                    if daily_energy:
                        # Store data for weekly summary
                        weekly_data.append({
                            'Day': day,
                            'Temperature': temperature,
                            'Total Energy': daily_energy['total'],
                            'Lighting': daily_energy['lighting'],
                            'Fan/AC': daily_energy['fan_ac'],
                            'Appliances': daily_energy['appliances'],
                            'Water Heater': daily_energy['water_heater'],
                            'Refrigerator': daily_energy['refrigerator']
                        })
                        
                        # Display daily breakdown
                        st.metric(
                            label="Total Daily Consumption",
                            value=f"{daily_energy['total']:.2f} kWh",
                            delta=f"₹{daily_energy['total'] * 6:.2f}"
                        )
                        
                        # Energy breakdown chart
                        breakdown_data = {
                            'Category': ['💡 Lighting', '🌀 Fan/AC', '📱 Appliances', '🚿 Water Heater', '❄️ Refrigerator'],
                            'Energy': [daily_energy['lighting'], daily_energy['fan_ac'], daily_energy['appliances'], 
                                     daily_energy['water_heater'], daily_energy['refrigerator']]
                        }
                        
                        fig = px.pie(
                            values=breakdown_data['Energy'],
                            names=breakdown_data['Category'],
                            title=f"Energy Breakdown - {day}",
                            color_discrete_sequence=['#ff6b6b', '#feca57', '#48dbfb', '#ff9ff3', '#54a0ff']
                        )
                        fig.update_layout(
                            height=400,
                            plot_bgcolor='rgba(0,0,0,0)',
                            paper_bgcolor='rgba(0,0,0,0)',
                            title_font_color='white',
                            title_font_size=18,
                            font_color='white',
                            title_x=0.5
                        )
                        st.plotly_chart(fig, use_container_width=True)
                        
                        # Energy saving tips based on weather
                        if temperature > 30:
                            st.markdown("""
                            <div class="bright-card" style="background: linear-gradient(135deg, #fd79a8, #e84393);">
                                <h4 style="margin: 0; color: white;">🔥 Hot Day Tips</h4>
                                <p style="margin: 0.5rem 0; color: white;">Use AC efficiently, close curtains during day, use fans with AC</p>
                            </div>
                            """, unsafe_allow_html=True)
                        elif temperature < 20:
                            st.markdown("""
                            <div class="bright-card" style="background: linear-gradient(135deg, #74b9ff, #0984e3);">
                                <h4 style="margin: 0; color: white;">❄️ Cold Day Tips</h4>
                                <p style="margin: 0.5rem 0; color: white;">Reduced fan usage, use natural light, water heater usage may increase</p>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown("""
                            <div class="bright-card" style="background: linear-gradient(135deg, #00b894, #55a3ff);">
                                <h4 style="margin: 0; color: white;">😊 Comfortable Day Tips</h4>
                                <p style="margin: 0.5rem 0; color: white;">Perfect weather for natural ventilation, minimal AC usage needed</p>
                            </div>
                            """, unsafe_allow_html=True)
                        
                else:
                    st.markdown("""
                    <div class="bright-card" style="background: linear-gradient(135deg, #ff9ff3, #feca57); text-align: center;">
                        <h4 style="margin: 0; color: white;">⚠️ Getting Started</h4>
                        <p style="margin: 0.5rem 0; color: white;">Please fill in your personal information above first! ⬆️</p>
                    </div>
                    """, unsafe_allow_html=True)
    
    # Weekly summary section
    if weekly_data:
        st.markdown("""
        <div class="bright-card" style="background: linear-gradient(135deg, #667eea, #764ba2); text-align: center; margin: 2rem 0;">
            <h2 class="glow-text" style="margin: 0; font-size: 2rem;">📊 Weekly Energy Summary</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Convert to DataFrame
        df = pd.DataFrame(weekly_data)
        
        # Weekly totals
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Total Weekly Energy", f"{df['Total Energy'].sum():.2f} kWh")
        
        with col2:
            st.metric("Average Daily Energy", f"{df['Total Energy'].mean():.2f} kWh")
        
        with col3:
            st.metric("Estimated Monthly Bill", f"₹{df['Total Energy'].sum() * 4.3 * 6:.2f}")
        
        with col4:
            highest_day = df.loc[df['Total Energy'].idxmax(), 'Day']
            st.metric("Highest Consumption Day", highest_day)
        
        # Weekly trends chart
        fig_line = px.line(
            df, 
            x='Day', 
            y='Total Energy',
            title='📈 Weekly Energy Consumption Trend',
            markers=True,
            color_discrete_sequence=['#ff6b6b']
        )
        fig_line.update_layout(
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            title_font_color='white',
            title_font_size=18,
            font_color='white',
            title_x=0.5,
            xaxis=dict(gridcolor='rgba(255,255,255,0.2)'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.2)')
        )
        fig_line.update_traces(
            line=dict(width=4),
            marker=dict(size=10, line=dict(width=2, color='white'))
        )
        st.plotly_chart(fig_line, use_container_width=True)
        
        # Temperature vs Energy correlation
        fig_scatter = px.scatter(
            df,
            x='Temperature',
            y='Total Energy',
            title='🌡️ Temperature vs Energy Consumption',
            trendline='ols',
            hover_data=['Day'],
            color_discrete_sequence=['#feca57']
        )
        fig_scatter.update_layout(
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            title_font_color='white',
            title_font_size=18,
            font_color='white',
            title_x=0.5,
            xaxis=dict(gridcolor='rgba(255,255,255,0.2)'),
            yaxis=dict(gridcolor='rgba(255,255,255,0.2)')
        )
        fig_scatter.update_traces(
            marker=dict(size=12, line=dict(width=2, color='white'))
        )
        st.plotly_chart(fig_scatter, use_container_width=True)
        
        # Detailed weekly breakdown
        st.subheader("📋 Detailed Weekly Breakdown")
        
        # Style the dataframe
        styled_df = df.style.format({
            'Total Energy': '{:.2f} kWh',
            'Temperature': '{:.0f}°C',
            'Lighting': '{:.2f}',
            'Fan/AC': '{:.2f}',
            'Appliances': '{:.2f}',
            'Water Heater': '{:.2f}',
            'Refrigerator': '{:.2f}'
        }).background_gradient(subset=['Total Energy'], cmap='YlOrRd')
        
        st.dataframe(styled_df, use_container_width=True)
        
        # Energy saving recommendations
        st.markdown("""
        <div class="bright-card" style="background: linear-gradient(135deg, #ff6b6b, #feca57); text-align: center; margin: 2rem 0;">
            <h2 class="glow-text" style="margin: 0; font-size: 2rem;">💡 Personalized Energy Saving Tips</h2>
        </div>
        """, unsafe_allow_html=True)
        
        avg_temp = df['Temperature'].mean()
        avg_energy = df['Total Energy'].mean()
        
        recommendations = []
        
        if avg_temp > 30:
            recommendations.append("🔥 Install ceiling fans to reduce AC load by 20-30%")
            recommendations.append("🌞 Use solar water heater to reduce electricity consumption")
            recommendations.append("🏠 Improve insulation to maintain cool temperatures")
        
        if avg_energy > 15:
            recommendations.append("💡 Switch to LED lights to reduce lighting energy by 80%")
            recommendations.append("⭐ Look for 5-star rated appliances for better efficiency")
            recommendations.append("🕒 Use timer-based water heaters")
        
        if flat_tenement == "tenement":
            recommendations.append("🏡 Consider rainwater harvesting to reduce water heating needs")
            recommendations.append("🌱 Plant trees around the house for natural cooling")
        
        recommendations.append("📱 Use smart power strips to eliminate standby power consumption")
        recommendations.append("🌀 Set AC temperature to 24°C instead of lower temperatures")
        
        for i, rec in enumerate(recommendations, 1):
            st.markdown(f"""
            <div class="bright-card" style="background: linear-gradient(135deg, #48dbfb, #54a0ff); margin: 0.5rem 0;">
                <p style="margin: 0; color: white; font-weight: 500;">{i}. {rec}</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Information section
    st.markdown("---")
    st.markdown("""
    <div class="bright-card" style="background: linear-gradient(135deg, #ff9ff3, #48dbfb); text-align: center; margin: 2rem 0;">
        <h2 class="glow-text" style="margin: 0; font-size: 2rem;">ℹ️ About This Calculator</h2>
    </div>
    """, unsafe_allow_html=True)
    
    with st.expander("How does weather affect energy consumption?"):
        st.write("""
        🌡️ **Temperature Impact on Energy Usage:**
        
        **Very Cold (Below 18°C):** ❄️
        - Fan usage drops to 10% of normal
        - Water heater usage may increase
        - Minimal air conditioning needed
        
        **Cool (18-22°C):** 🌤️
        - Fan usage at 30% of normal
        - Comfortable temperature, minimal cooling needed
        
        **Comfortable (22-26°C):** 😊
        - Fan usage at 60% of normal
        - Optimal temperature for energy efficiency
        
        **Warm (26-30°C):** 🌞
        - Fan usage at 80% of normal
        - May need occasional air conditioning
        
        **Hot (30-35°C):** 🔥
        - Full fan usage
        - Air conditioning becomes necessary
        
        **Very Hot (Above 35°C):** 🌋
        - Fan usage at 130% (includes AC)
        - High cooling requirements
        """)
    
    with st.expander("Energy calculation methodology"):
        st.write("""
        📊 **Realistic Energy Consumption (kWh per day):**
        
        **Flats:**
        - 1BHK: ~12.8 kWh/day
        - 2BHK: ~17.2 kWh/day  
        - 3BHK: ~22.2 kWh/day
        
        **Tenements:**
        - 1BHK: ~12.9 kWh/day
        - 2BHK: ~17.3 kWh/day
        - 3BHK: ~22.5 kWh/day
        
        **Appliance-wise breakdown:**
        - 💡 Lighting: LED bulbs and tube lights
        - 🌀 Fan/AC: Ceiling fans and air conditioning
        - 📱 Appliances: TV, washing machine, microwave
        - 🚿 Water Heater: Electric geyser
        - ❄️ Refrigerator: Standard home refrigerator
        
        *Values based on average Indian household consumption patterns*
        """)

if __name__ == "__main__":
    main()
