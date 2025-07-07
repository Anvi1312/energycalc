# Energy Consumption Calculator

## Overview

This is an advanced Streamlit-based web application that calculates energy consumption for residential properties based on housing type (flat or tenement) and BHK (bedroom-hall-kitchen) configuration. The application now features day-by-day energy tracking with weather-based adjustments, providing users with a comprehensive weekly energy analysis. The enhanced interface includes interactive charts, personalized recommendations, and realistic energy consumption calculations based on Indian residential patterns.

## System Architecture

### Frontend Architecture
- **Framework**: Streamlit - Python-based web framework for data applications
- **UI Components**: Form-based interface with input fields and interactive elements
- **Styling**: Streamlit's built-in styling with emoji-enhanced titles for better UX

### Backend Architecture
- **Language**: Python
- **Application Structure**: Single-file application (`app.py`)
- **Business Logic**: Calculation engine with predefined energy consumption formulas
- **Data Processing**: Real-time calculation based on user inputs

## Key Components

### 1. Energy Calculation Engine
- **Functions**: 
  - `calculate_base_energy(flat_tenement, bhk)`: Base energy consumption by appliance category
  - `calculate_weather_adjustment(temperature, base_fan_ac)`: Weather-based fan/AC adjustment
  - `calculate_daily_energy(flat_tenement, bhk, temperature)`: Daily consumption with weather factors
- **Purpose**: Advanced energy calculation with realistic consumption patterns
- **Parameters**: Housing type, BHK configuration, and daily temperature
- **Calculation Logic**: 
  - Realistic kWh values based on Indian residential patterns
  - Appliance-wise breakdown: lighting, fan/AC, appliances, water heater, refrigerator
  - Weather-based adjustments: temperature affects fan/AC usage from 10% to 130%
  - Daily energy ranges: 1BHK (12-13 kWh), 2BHK (17-18 kWh), 3BHK (22-23 kWh)

### 2. User Interface Components
- **Main Application**: `main()` function with enhanced Streamlit UI
- **Layout Structure**: 
  - Sidebar for personal and housing information
  - Tabbed interface for daily energy tracking (Monday-Sunday)
  - Weekly summary dashboard with charts and analytics
- **Interactive Elements**: 
  - Temperature sliders for each day (10-45°C range)
  - Real-time energy calculations with weather adjustments
  - Pie charts for daily energy breakdown
  - Line charts for weekly trends
  - Scatter plots for temperature vs energy correlation
- **Visual Enhancements**:
  - Custom CSS styling with gradient backgrounds
  - Emoji-enhanced tabs and headers
  - Color-coded weather descriptions
  - Responsive design with columns and metrics

### 3. Data Validation
- **Age Validation**: Numeric input with min/max constraints (1-120)
- **Housing Type Validation**: Dropdown selection to prevent invalid inputs
- **Error Handling**: Function returns None for invalid configurations

## Data Flow

1. **User Input Collection**: Users enter personal information and housing details through the Streamlit form
2. **Data Processing**: Form submission triggers the energy calculation function
3. **Calculation Logic**: Based on housing type and BHK, the system applies predefined multipliers
4. **Result Display**: Calculated energy consumption is presented to the user

## External Dependencies

### Core Dependencies
- **Streamlit**: Web application framework for Python
- **Pandas**: Data manipulation and analysis for weekly energy tracking
- **Plotly**: Interactive charting library for energy visualization
- **Python Standard Library**: Basic Python functionality including datetime

### Deployment Dependencies
- Python 3.x runtime environment
- Streamlit server for web hosting

## Deployment Strategy

### Local Development
- Direct execution via `streamlit run app.py`
- No database or external service requirements
- Self-contained application

### Production Deployment Options
- **Streamlit Cloud**: Native hosting platform for Streamlit apps
- **Docker**: Containerized deployment for cloud platforms
- **Traditional Web Hosting**: Any Python-compatible hosting service

## Changelog

- July 07, 2025: Initial setup with basic energy calculation
- July 07, 2025: Major enhancement - Added day-by-day tracking with weather-based adjustments
  - Implemented realistic energy consumption calculations based on Indian residential patterns
  - Added interactive weekly dashboard with charts and analytics
  - Integrated temperature-based fan/AC usage adjustments
  - Enhanced UI with custom styling, emojis, and responsive design
  - Added personalized energy-saving recommendations

## User Preferences

Preferred communication style: Simple, everyday language.