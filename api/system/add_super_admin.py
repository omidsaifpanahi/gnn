from api.models.user import UserModel

if __name__ == "__main__":
    username = input("نام کاربری را وارد کنید: ")
    password = input("رمز عبور را وارد کنید: ")
    user = UserModel()
    user.add(username, password)
