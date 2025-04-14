import streamlit as st
import time
from supabase_client import get_supabase
from crawler.analysis import handleUserPrompt

supabase = get_supabase()

st.set_page_config(page_title="Supabase Login & Chat", layout="wide")

# Session init
if "user" not in st.session_state:
    st.session_state.user = None
if "page" not in st.session_state:
    st.session_state.page = "login"
if "response_mode" not in st.session_state:
    st.session_state.response_mode = "normal"  # Default response mode
if "selected_role" not in st.session_state:
    st.session_state.selected_role = "farmers"  # Default role
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Functions
def handle_login(email, password):
    try:
        res = supabase.auth.sign_in_with_password({"email": email, "password": password})
        user = res.user
        if user:
            st.session_state.user = user
            st.session_state.page = "chat"
            st.success("Đăng nhập thành công!")
            st.rerun()
        else:
            st.error("Tài khoản hoặc mật khẩu không đúng.")
    except Exception as e:
        st.error(f"Lỗi khi đăng nhập: {e}")

def handle_signup(email, password):
    try:
        supabase.auth.sign_up({"email": email, "password": password})
        st.success("Đăng ký thành công! Vui lòng xác nhận email trước khi đăng nhập.")
    except Exception as e:
        st.error(f"Lỗi khi đăng ký: {e}")

def handle_logout():
    st.session_state.user = None
    st.session_state.page = "login"
    st.rerun()

def handle_reasoning_response(prompt, role):
    return handleUserPrompt(prompt=prompt, specific_user=role)

def handle_normal_response(prompt):
    return f"🤖 [Normal] AI phản hồi: '{prompt}' là một tin nhắn hay!"

def handle_role_response(prompt, role):
    if role == "farmers":
        return f"🌾 [Farmers] Thông tin về nông nghiệp: '{prompt}'"
    elif role == "exporters":
        return f"🚢 [Exporters] Thông tin về xuất khẩu: '{prompt}'"
    elif role == "importers":
        return f"📦 [Importers] Thông tin về nhập khẩu: '{prompt}'"
    return f"🤖 AI phản hồi: '{prompt}'"

def set_response_mode(mode):
    st.session_state.response_mode = mode
    st.rerun()

def set_role(role):
    st.session_state.selected_role = role
    st.rerun()

# UI
if st.session_state.page == "login":
    st.title("🔐 Đăng nhập với Supabase")

    email = st.text_input("Email")
    password = st.text_input("Mật khẩu", type="password")

    option = st.radio("Chọn hành động", ["Đăng nhập", "Đăng ký"])

    if option == "Đăng nhập" and st.button("Đăng nhập"):
        handle_login(email, password)
    elif option == "Đăng ký" and st.button("Đăng ký"):
        handle_signup(email, password)

elif st.session_state.page == "chat":
    # Custom CSS for button styling with green border effect
    st.markdown(
        """
        <style>
        .custom-logout {
            position: fixed;
            top: 10px;
            left: 10px;
            z-index: 9999;
        }
        .button-container {
            display: flex;
            justify-content: center;
            margin-bottom: 10px;
        }
        .custom-button {
            padding: 10px 20px;
            margin: 0 5px;
            border: 2px solid #ccc;
            border-radius: 5px;
            background-color: #f0f0f0;
            color: #333;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .custom-button:hover {
            background-color: #e0e0e0;
            border-color: #999;
        }
        .custom-button.active {
            border-color: #2e7d32;
            background-color: #f0f8f0;
        }
        .reasoning-btn {
            background-color: #f4f4f9;
        }
        .normal-btn {
            background-color: #e8e8e8;
        }
        .farmers-btn {
            background-color: #f0f7e6;
        }
        .exporters-btn {
            background-color: #e6f3f7;
        }
        .importers-btn {
            background-color: #f7e6e6;
        }
        .logout-btn {
            position: absolute;
            top: 10px;
            right: 10px;
            padding: 5px 15px;
            background-color: #f44336;
            color: white;
            border: none;
            border-radius: 4px;
            cursor: pointer;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    # # Logout button
    # st.markdown(
    #     f'''
    #     <button 
    #         class="logout-btn" 
    #         onclick="window.parent.postMessage({{target: 'streamlitApp', type: 'customEvent', name: 'logout'}}, '*')">
    #         🚪 Đăng xuất
    #     </button>
    #     ''',
    #     unsafe_allow_html=True
    # )
    
    # Custom event handler for logout
    if st.session_state.get('logout_clicked', False):
        handle_logout()
        st.session_state.logout_clicked = False 

    
    # JavaScript to handle custom events
    st.markdown(
        """
        <script>
        // Listen for messages from the buttons
        window.addEventListener('message', function(event) {
            if (event.data.target === 'streamlitApp') {
                if (event.data.type === 'customEvent') {
                    if (event.data.name === 'logout') {
                        window.parent.postMessage({type: 'streamlit:setComponentValue', value: true, key: 'logout_clicked'}, '*');
                    } else if (event.data.name === 'set_mode_reasoning') {
                        window.parent.postMessage({type: 'streamlit:setComponentValue', value: 'reasoning', key: 'response_mode'}, '*');
                    } else if (event.data.name === 'set_mode_normal') {
                        window.parent.postMessage({type: 'streamlit:setComponentValue', value: 'normal', key: 'response_mode'}, '*');
                    } else if (event.data.name === 'set_role_farmers') {
                        window.parent.postMessage({type: 'streamlit:setComponentValue', value: 'farmers', key: 'selected_role'}, '*');
                    } else if (event.data.name === 'set_role_exporters') {
                        window.parent.postMessage({type: 'streamlit:setComponentValue', value: 'exporters', key: 'selected_role'}, '*');
                    } else if (event.data.name === 'set_role_importers') {
                        window.parent.postMessage({type: 'streamlit:setComponentValue', value: 'importers', key: 'selected_role'}, '*');
                    }
                }
            }
        });
        </script>
        """,
        unsafe_allow_html=True
    )
    
    # Alternative implementation using Streamlit's native components
    # Comment out the above HTML button implementation and uncomment this section if the HTML/JS approach doesn't work
    st.write("")  # Add some spacing
    
    # Create two rows of buttons using columns
    st.write("### Mode & Role Selection")
    
    # First row - Response Mode
    mode_col1, mode_col2 = st.columns(2)
    with mode_col1:
        if st.button("🧠 Reasoning", key="reasoning_btn", 
                   help="Switch to Reasoning Mode"):
            st.session_state.response_mode = "reasoning"
            st.rerun()
    
    with mode_col2:
        if st.button("💬 Normal", key="normal_btn", 
                   help="Switch to Normal Mode"):
            st.session_state.response_mode = "normal"
            st.rerun()
    
    # Second row - Roles  
    role_col1, role_col2, role_col3 = st.columns(3)
    
    with role_col1:
        if st.button("🌾 Farmers", key="farmers_btn", 
                   help="Switch to Farmers Role"):
            st.session_state.selected_role = "farmers"
            st.rerun()
    
    with role_col2:
        if st.button("🚢 Exporters", key="exporters_btn", 
                   help="Switch to Exporters Role"):
            st.session_state.selected_role = "exporters"
            st.rerun()
    
    with role_col3:
        if st.button("📦 Importers", key="importers_btn", 
                   help="Switch to Importers Role"):
            st.session_state.selected_role = "importers"
            st.rerun()
    
    # Logout button
    if st.button("🚪 Đăng xuất", key="logout_btn"):
        handle_logout()

    st.title("💬 ChatGPT Mini")

    st.markdown(f"**Chế độ hiện tại:** `{st.session_state.response_mode}`")
    st.markdown(f"**Vai trò hiện tại:** `{st.session_state.selected_role}`")


    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.chat_input("Nhập tin nhắn...")
    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(user_input)

        # Generate response
        
        with st.chat_message("assistant"):
            with st.spinner("🤖 Mô hình đang suy nghĩ..."):
                time.sleep(1)

                if st.session_state.response_mode == "reasoning":
                    ai_reply = handle_reasoning_response(user_input, st.session_state.selected_role)
                else:
                    ai_reply = handle_role_response(user_input, st.session_state.selected_role)

                st.markdown(ai_reply)

        st.session_state.chat_history.append({"role": "assistant", "content": ai_reply})