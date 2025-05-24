import streamlit_authenticator as stauth

# 输入你想加密的密码
passwords = ["admin123", "123456"]

# 批量加密
hashed_passwords = stauth.Hasher(passwords).generate()

for i, hp in enumerate(hashed_passwords):
    print(f"密码 {passwords[i]} 的加密结果：\\n{hp}\\n")
