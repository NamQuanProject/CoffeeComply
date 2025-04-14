import streamlit as st
from supabase_client import get_supabase

supabase = get_supabase()

# Title for the app
st.set_page_config(page_title="Supabase Login & Chat", layout="wide")

# Initialize session state if not already done
if "user" not in st.session_state:
    st.session_state.user = None
if "page" not in st.session_state:
    st.session_state.page = "login"  # Default page is login

# Function to handle login
def handle_login(email, password):
    try:
        st.session_state.page = "chat"  # Move to chat page after login
        res = supabase.auth.sign_in_with_password({"email": email, "password": password})
        user = res.user
        st.session_state.user = user
        st.success("Đăng nhập thành công!")
        st.experimental_rerun()
    except Exception as e:
        st.error(f"Lỗi: {e}")

# Function to handle sign-up
def handle_signup(email, password):
    try:
        res = supabase.auth.sign_up({"email": email, "password": password})
        st.success("Đăng ký thành công! Vui lòng xác nhận email.")
    except Exception as e:
        st.error(f"Lỗi: {e}")

# Function to log out
def handle_logout():
    st.session_state.user = None
    st.session_state.page = "login"  # Go back to login page
    st.experimental_rerun()

# Display the correct page based on the current session
if st.session_state.page == "login":
    # Login page
    st.title("Đăng nhập với Supabase")

    email = st.text_input("Email")
    password = st.text_input("Mật khẩu", type="password")
    
    option = st.radio("Chọn hành động", ["Đăng nhập", "Đăng ký"])
    
    if option == "Đăng nhập" and st.button("Đăng nhập"):
        handle_login(email, password)
    elif option == "Đăng ký" and st.button("Đăng ký"):
        handle_signup(email, password)
        
elif st.session_state.page == "chat":
    # Chat page
    st.title(f"Chào mừng {st.session_state.user['email']} đến với trang chat!")
    
    # Chat functionality (basic input box for now)
    message = st.text_input("Nhập tin nhắn:")
    
    if message:
        st.write(f"Bạn đã gửi tin nhắn: {message}")
    
    if st.button("Đăng xuất"):
        handle_logout()
