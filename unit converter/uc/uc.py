import streamlit as st 


st.set_page_config(
    layout="wide",
)

st.markdown(
    """
<style>
 .footer {
            text-align: center;
            padding: 1rem;
            font-size: 0.9rem;
            color: #64748b;
            margin-top: 2rem;
        }
.stButton>button {
    background: linear-gradient(#6366f1);
    color: navy; /* Convert text in navy blue */
    font-weight: 500;
    border-radius: 12px;
    width: 100%;
    border: none;
    box-shadow: 0px 4px 10px rgba(99, 102, 241, 0.4);
    transition: all 0.3s ease;
}

.stButton>button:hover {
    color: purple; /* Convert text turns yellow on hover */
    transform: translateY(0);
    box-shadow: 0px 6px 10px rgba(99, 102, 241, 0.6);
        </style>
        """, 
unsafe_allow_html=True,

)


def convert_temperature(value, from_unit, to_unit):
    """Convert temperature between Celsius, Fahrenheit, and Kelvin"""
   
    if from_unit == 'Celsius':
        kelvin = value + 273.15
    elif from_unit == 'Fahrenheit':
        kelvin = (value - 32) * 5/9 + 273.15
    elif from_unit == 'Kelvin':
        kelvin = value
    else:
        return None
    
    
    if to_unit == 'Celsius':
        return kelvin - 273.15
    elif to_unit == 'Fahrenheit':
        return (kelvin - 273.15) * 9/5 + 32
    elif to_unit == 'Kelvin':
        return kelvin
    else:
        return None


units = {
    ' 📏Length': {
        'meters': 1,
        'kilometers': 1000,
        'centimeters': 0.01,
        'millimeters': 0.001,
        'miles': 1609.34,
        'yards': 0.9144,
        'feet': 0.3048,
        'inches': 0.0254
    },
    '⚖️ Weight': {
        'kilograms': 1,
        'grams': 0.001,
        'milligrams': 0.000001,
        'pounds': 0.453592,
        'ounces': 0.0283495,
        'tons': 1000
    },
    '🌡️Temperature': {
        'Celsius': None,
        'Fahrenheit': None,
        'Kelvin': None
    },
    '🏞️ Area': {
        'square meters': 1,
        'square kilometers': 1e6,
        'square miles': 2589988.11,
        'acres': 4046.86,
        'hectares': 10000,
        'square feet': 0.092903,
        'square inches': 0.00064516
    },
    ' 🧪 Volume': {
        'liters': 1,
        'milliliters': 0.001,
        'cubic meters': 1000,
        'gallons': 3.78541,
        'cubic feet': 28.3168,
        'cubic inches': 0.0163871
    },
    ' ⏰ Time': {
        'seconds': 1,
        'minutes': 60,
        'hours': 3600,
        'days': 86400,
        'weeks': 604800,
        'years': 31536000  
    }
}


st.title(" <<< 📏 UNIT CONVERTER >>>")



category = st.selectbox("Select Measurement Category", list(units.keys()))


col1, col2 = st.columns(2)
with col1:
    from_unit = st.selectbox("From", units[category].keys())
with col2:
    to_unit = st.selectbox("To", units[category].keys())


value = st.number_input("Enter Value", value=0.0, format="%f")


if st.button(" 🔄 Convert"):
    try:
        if category == 'Temperature':
            result = convert_temperature(value, from_unit, to_unit)
        else:
        
            base_value = value * units[category][from_unit]
            result = base_value / units[category][to_unit]
        
      
        if abs(result) >= 10000 or abs(result) <= 0.001:
             st.success(f"{value} {from_unit} = {result:.4e} {to_unit}")
        else:
             st.success(f"{value} {from_unit} = {result:,.4f} {to_unit}")

            
            
    except Exception as e:
        st.error(f"Error in conversion: {str(e)}")


st.markdown("<div class='footer'>🚀 SK UNIT CONVERTER| © 2025 | <a href='#' style='color: #6366f1;'>Terms & Privacy</a></div>", unsafe_allow_html=True)