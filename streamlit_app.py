from dotenv import load_dotenv
import os
import anthropic
import streamlit as st

# Load environment variables
load_dotenv()
api_key = os.getenv("ANTHROPIC_API_KEY")

# Verify API key
if not api_key:
    st.error("API key not found. Please check your .env file.")
    st.stop()

def get_response(learning_goals):
    """Send user input to the AI model and get a response using the Messages API."""
    client = anthropic.Anthropic(api_key=api_key)  # Pass the API key
    
    # Constructing the refined prompt
    user_content = f"""
    ##CONTEXT##
    I'm developing clear, measurable tasks that break down learning goals into their component skills.
    
    ##OBJECTIVE##
    Break down each learning goal into component skills by:
    - Identifying action verbs in the goal (recognize, count, compare)
    - Noting specific quantities or constraints mentioned (up to 4, up to 10)
    - Identifying any special conditions (without counting, regardless of arrangement)
    
    For each component skill, write a task statement that:
    - Starts with an observable action verb (identify, create, state, compare)
    - Specifies exact quantities or materials to be used
    - Includes clear success criteria
    - Describes any special conditions or time constraints
    - Uses language that is measurable and observable
    
    Ensure each task:
    - Tests only one skill at a time
    - Is specific enough to be consistently scored
    - Could be repeated with different materials but same difficulty
    - Matches the cognitive level of the original goal
    
    ##INPUT##
    Original learning goals:
    {learning_goals}
    
    ##SAMPLE EXCHANGE##
    Input - Recognize and name groups of up to 4 objects and images without counting.
    Count and compare up to 10 objects and know the number remains the same regardless of the arrangement of the objects.
    
    Output - 
    1. Identify and name the total number of familiar objects (such as counters, blocks, or dots) shown for 3 seconds without counting, in quantities up to 4.
    2. Count a group of up to 10 objects using one-to-one correspondence and state the total quantity when complete.
    3. Compare two groups of objects (up to 10 each) and identify which group has more, fewer, or if they are equal.
    4. State whether the quantity of a group of objects (up to 10) has changed or stayed the same after the objects have been rearranged into a different configuration.
    5. Create a new group of objects that matches the quantity of a given group (up to 10 objects), using different items.
    """
    
    response = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        system="You are a helpful assistant that refines learning goals into precise, measurable tasks for assessment and instruction.",
        messages=[
            {"role": "user", "content": user_content}
        ],
        max_tokens=500,
        stream=False
    )
    
    return response.content[0].text

# Streamlit app UI
st.title("Learning Goal Breakdown Tool")
st.subheader("Refine learning goals into clear, measurable tasks.")

# Text input for learning goals
learning_goals = st.text_area("Enter the learning goals to break down:")

# Generate response
if st.button("Generate Tasks"):
    if learning_goals:
        with st.spinner("Generating tasks..."):
            try:
                response = get_response(learning_goals)
                st.success("Tasks Generated Successfully!")
                st.text_area("Generated Tasks", value=response, height=400)
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter learning goals to process.")
