# Intelligent Customer Service Operations

## 1. Project Overview

This project develops an AI-supported customer service operations system for banking.

TV6 is responsible for developing the **Streamlit Webapp and Dashboard**, which provides an interface for displaying customer tickets, AI-supported results, human review actions, and management information.

## 2. Webapp Requirements

The Webapp is developed using:

- Python 3.14
- Streamlit
- Pandas
- Openpyxl
- Plotly

The customer ticket data is loaded from:

`data/tickets.xlsx`

## 3. Webapp Development

The Webapp was developed step by step using Streamlit.

### 3.1. Load Customer Data

The Webapp reads customer ticket data from `tickets.xlsx` and displays the tickets in the Customer Ticket List.

### 3.2. Customer Ticket List

The Webapp displays customer tickets and provides filters for:

- Category
- Ticket Type

### 3.3. Ticket Detail

Users can select a **Ticket ID** to view:

- Customer Message
- Ticket ID
- Category
- Ticket Type
- Urgency

### 3.4. AI Analysis Interface

A dedicated interface was created to display AI analysis results, including:

- Intent
- Topic
- Product
- Amount
- Channel
- Transaction Time
- Transaction ID
- Sentiment
- Missing Information

### 3.5. Priority & Routing Interface

The Webapp provides a section for displaying:

- Urgency
- Priority
- Department
- Routing Reason

### 3.6. Knowledge Base and Draft Response

The interface includes:

- KB Found
- Source
- Confidence
- Reason
- Draft Response

### 3.7. Human Review

The Webapp provides three actions:

- **Edit**
- **Approve**
- **Escalate**

These functions support the Human-in-the-Loop process.

### 3.8. Management Dashboard

The Dashboard displays:

- Total Tickets
- Complaints
- Urgent Tickets
- Top Issue
- Ticket Type Distribution
- Complaint Trend

## 4. How to Run the Webapp

Open **Command Prompt (CMD)** and navigate to the project folder:

`cd C:\Intelligent_Customer_Service`

Check the Python version:

`py -3.14 --version`

Install the required libraries:

`py -3.14 -m pip install streamlit pandas openpyxl plotly`

Run the Webapp:

`py -3.14 -m streamlit run app\dashboard\dashboard.py`

Open the Webapp in a browser:

`http://localhost:8501`

To stop the Webapp, press `Ctrl + C` in the Command Prompt.

## 5. Human-in-the-Loop

The Webapp follows the **Human-in-the-Loop** approach.

AI supports employees by analyzing customer requests, suggesting priority and routing, retrieving relevant information, and generating draft responses.

Human reviewers are responsible for checking the results and using:

- **Edit:** Modify the response
- **Approve:** Approve the result
- **Escalate:** Send the ticket for further handling

## 6. Testing

The Webapp was tested on **Python 3.14** and **Streamlit**.

The following functions were tested:

- Loading customer data
- Ticket List
- Ticket Filtering
- Ticket Detail
- AI Analysis interface
- Priority & Routing interface
- Knowledge Base interface
- Human Review actions
- Management Dashboard
- Complaint Trend

The Webapp was successfully run on the local environment.

## 7. Current Status

The Webapp and Dashboard interface have been successfully developed and tested.

The interface is prepared for integration with the actual outputs from the AI Analysis, Priority & Routing, and Knowledge Base / RAG modules. These outputs have not yet been integrated into the Webapp.
