### **Interactive UK Electricity Cost Estimator**

This Streamlit application is a tool designed to help businesses and individuals in the UK estimate and project their annual electricity costs. It provides a transparent breakdown of the various charges that make up a total electricity bill, including wholesale prices, network charges, levies, and taxes.

#### **Features**

*   **Customizable Input**: Users can enter their annual electricity consumption and either use the pre-populated default values for various charges (based on UK market rates) or input custom values for each component.
    
*   **Cost Breakdown**: The app calculates and displays a clear breakdown of the annual costs, including the energy cost, standing charge, VAT, and a final total.
    
*   **15-Year Projection**: It projects the annual electricity costs over a 15-year period based on a user-defined annual escalation rate, providing a long-term financial outlook.
    
*   **Interactive Visualization**: A detailed line chart, powered by Plotly, visualizes the projected cost trends over the 15 years. This interactive graph allows users to easily see how each cost component contributes to the total over time.
    

#### **How to Run Locally**

1.  Clone this repository to your local machine.
    
2.  Navigate to the project directory.
    
3. Install the required libraries from the `requirements.txt` file:
````
pip install -r requirements.txt
````
    
4. Run the application using the Streamlit command:
```
streamlit run app.py
```
    
5.  The application will open automatically in your web browser.
    

#### **Deployment**

This application is designed for easy deployment on platforms like [Streamlit Community Cloud](https://share.streamlit.io/). The app.py and requirements.txt files are all that's needed to get the app running online.