# app.py
import streamlit as st
import io
from database import init_db, SessionLocal, Event
from file_parser import parse_calendar, is_weekend
from llm_agent import get_vacation_recommendation

# Initialize the database
init_db()

st.title("AI Travel Agent")
st.write("Upload your calendar file (PDF, ICS, or CSV) to analyze holidays and plan extended vacations.")

# Sidebar instructions
st.sidebar.title("Instructions")
st.sidebar.info("""
1. Upload your calendar file.
2. The system will parse the events and mark weekends as holidays.
3. Click on the button to get vacation recommendations.
""")

# File uploader widget
uploaded_file = st.file_uploader("Choose a calendar file", type=["pdf", "ics", "csv"])
if uploaded_file is not None:
    file_type = uploaded_file.name.split('.')[-1].lower()
    st.write(f"Processing file of type: {file_type}")

    # Read file into a BytesIO object for parsing
    file_bytes = io.BytesIO(uploaded_file.read())
    events_list = parse_calendar(file_bytes, file_type)

    # Process and store events in the database
    session = SessionLocal()
    count_new = 0
    for event in events_list:
        event_date = event["date"]
        event_name = event.get("name", "")
        # Mark weekends as holidays.
        holiday_flag = is_weekend(event_date)
        # (Optional: add further logic to flag specific holiday names)
        
        # Avoid duplicate entries (simple check based on date and name)
        existing_event = session.query(Event).filter(Event.event_date == event_date, Event.event_name == event_name).first()
        if not existing_event:
            new_event = Event(event_date=event_date, event_name=event_name, holiday_flag=holiday_flag)
            session.add(new_event)
            count_new += 1
    session.commit()
    st.success(f"Processed and stored {count_new} new event(s).")

    # Display stored events
    st.subheader("Stored Calendar Events")
    events = session.query(Event).order_by(Event.event_date).all()
    if events:
        for e in events:
            st.write(f"{e.event_date}: {e.event_name} - Holiday: {e.holiday_flag}")
    else:
        st.write("No events found.")

    # Extract holiday dates for vacation recommendation
    holiday_dates = [e.event_date for e in events if e.holiday_flag]
    if st.button("Get Vacation Recommendation"):
        if not holiday_dates:
            st.warning("No holiday dates found in the stored events.")
        else:
            with st.spinner("Consulting AI Travel Agent..."):
                recommendation = get_vacation_recommendation(holiday_dates)
                st.subheader("Vacation Recommendation")
                st.write(recommendation)

# Basic Chat Interface (Optional)
st.subheader("Chat with AI Travel Agent")
user_input = st.text_input("Ask a question:")
if st.button("Send"):
    if user_input:
        with st.spinner("Thinking..."):
            # For demonstration, we call the recommendation function with an empty holiday list.
            # In a full implementation, you’d handle conversation context.
            response = get_vacation_recommendation([], extra_days=2)
            st.write(response)
