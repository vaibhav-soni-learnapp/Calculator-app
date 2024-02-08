import streamlit as st
import matplotlib.pyplot as plt
import math

# Financial calculation 
def calculate_financials(start_year, income, expenses, salary_increment, expenses_increment, return_percentage):
    t = 30  # Assuming 30 years for calculation
    savings = []

    for i in range(t):
        annual_income = income * 12 * ((1 + salary_increment) ** i)
        annual_expenses = expenses * 12 * ((1 + expenses_increment) ** i)
        annual_savings = annual_income - annual_expenses
        savings.append(annual_savings)

    total_savings = sum(savings) * (1 + return_percentage / 100)
    
    ex_31 = expenses * 12 * (1.08 ** 31)
    runway = math.log(((total_savings * 0.08) / ex_31) + 1) / math.log(1.08)

    return total_savings, runway

# Function to create and display a donut chart
def plot_donut_chart(savings_with_return, savings_without_return):
    data = [savings_with_return, savings_without_return]
    labels = ['With Return', 'Without Return']
    colors = ['#ff9999','#66b3ff']

    fig, ax = plt.subplots()
    ax.pie(data, labels=labels, colors=colors, startangle=90, pctdistance=0.85, autopct='%1.1f%%')
    centre_circle = plt.Circle((0,0),0.70,fc='white')
    fig.gca().add_artist(centre_circle)
    ax.axis('equal')  
    plt.tight_layout()
    return fig

# Streamlit interface
st.title("Financial Runway and Savings Calculator")

st.date_input("Select your working year", format="DD/MM/YYYY", disabled=False, label_visibility="visible")
start_year = st.number_input("Year Started Working", min_value=1980, max_value=2024, value=2018, step=1)
income = st.number_input("Monthly Income", min_value=0, max_value=20000000, value=20000, step=1000)
expenses = st.number_input("Monthly Expenses", min_value=0, max_value=10000000, value=15000, step=500)
salary_increment = st.slider('Salary Increment (%)', min_value=0.0, max_value=100.0, format="%.2f") / 100
expenses_increment = st.slider('Expenses Increment (%)', min_value=0.0, max_value=100.0, format="%.2f") / 100
return_percentage = st.slider('Return Percentage (%)', min_value=0.0, max_value=100.0, format="%.2f") / 100


if st.button("Calculate"):
    savings_with_return, runway_with_return = calculate_financials(start_year, income, expenses, salary_increment, expenses_increment, return_percentage)
    savings_without_return, _ = calculate_financials(start_year, income, expenses, salary_increment, expenses_increment, 0)

    
    st.write("Total Runway without Return: ", runway_with_return)
    st.write("Total Savings without Return: ", savings_without_return)

    st.write("Total Savings with Return: ", savings_with_return)
    st.write("Total Runway with Return: ", runway_with_return)

    donut_chart = plot_donut_chart(savings_with_return, savings_without_return)
    st.pyplot(donut_chart)
