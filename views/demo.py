import streamlit as st
from llama_index.llms import OpenAI,ChatMessage,MessageRole
import openai
from llama_index.prompts import ChatPromptTemplate
from llama_index.chat_engine import SimpleChatEngine
def load_demo():
    openai.api_key = st.secrets.openai_key


    st.title("Let's Achieve your goals")

    if "messages" not in st.session_state.keys(): # Initialize the chat messages history
        st.session_state.messages = [{'role': 'assistant', 'content': 'How may i help you!'}] 
        st.session_state.custom_chat_history = [
        
        ]
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.session_state.custom_chat_history.append(
                    ChatMessage(
                        role=MessageRole.USER,
                        content=msg["content"],
                    )
                )
            else:
                st.session_state.custom_chat_history.append(
                    ChatMessage(
                        role=MessageRole.ASSISTANT,
                        content=msg["content"],
                    )
                )
    if "chat_engine" not in st.session_state.keys():
        st.session_state.chat_engine = SimpleChatEngine.from_defaults(
            llm=OpenAI(temperature=0, model_name="gpt-4"),
            system_prompt=(
            "You are a mentor for humans who are in a confusion for finding and achieving goals in USA.Your goal is to ask user for their goal and help them in reaching their goal.you dont know anything about user's details. \n"
            "Greet the user when required and be kind to the user\n"
            "You should ask user some questions which are related to the profession the user wants to achieve. \n"
            "The questions should not be asked in a one go, ask questions in step by step manner.Asking questions should be like a conversational manner. \n"
            "You should ask the questions related to the requirements of the profession like age,marital status,gender,citizenship,required money and everything related to that profession,in step by step manner.After getting answer for one question,you should ask another question\n"
            "You should ask every question which are related to the profession,minimum 10 questions or more.after asking all the questions you should think of a plan from the users answers. \n"
            "you should analyze the user answers and give them a plan from next steps from their current position to achieve their goals in step by step manner. \n"
            "'Your suggested plan should to include everything that user should do to achieve their goals.'\n"
            "after giving the plan,you should ask user whether he/she have any doubts about the plan.\n"
            "Some rules to follow:\n"
            "1.don't use any hallucination\n"
            "2.Be kind to the user and greet them in a nice way. \n"
            "3.Don't give responses like a bot"
            "4.Dont ever forget to give the user a plan to achieve their goals in point wise only."
            "5.You should ask questions in a nice way,it should be not be like an interrogative question."
        ),
        verbose=True

        )

    if prompt := st.chat_input("Your question"): # Prompt for user input and save to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        st.session_state.custom_chat_history.append(
        ChatMessage(
            role=MessageRole.USER,
            content=prompt,
        ))

    for message in st.session_state.messages: # Display the prior chat messages
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # If last message is not from assistant, generate a new response
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                # print("s mess",st.session_state.messages)
                # st.session_state.custom_chat_history
                response = st.session_state.chat_engine.chat(prompt,st.session_state.custom_chat_history)
                st.write(response.response)
                message = {"role": "assistant", "content": response.response}
                st.session_state.messages.append(message) # Add response to message history
                st.session_state.custom_chat_history.append(
                ChatMessage(
                    role=MessageRole.ASSISTANT,
                    content=response.response,
                ))
