class lolbook:
    def __init__(self):
        self.username = ""
        self.password = ""
        self.logged_in = False
        self.menu()

    def menu(self):
        user_input = input("Welcome to Lolbook!! Please choose an option:\n" \
        "1. Sign Up\n" \
        "2. Log In\n" \
        "3. Write a Post\n" \
        "4. Message a Friend\n" \
        "5. Log Out")
    
        if user_input == "1":
            self.sign_up()
        elif user_input == "2":
            self.log_in()
        elif user_input == "3":
            self.write_post()
        elif user_input == "4":
            self.message_friend()
        elif user_input == "5":
            self.log_out()
        else:
            print("Invalid option. Please try again.")
            self.menu()

    def sign_up(self):
        print("entering signup")
        self.username = input("Enter your email address: ")
        self.password = input("Create a password: ")
        print("Sign up successful! You can now log in.")
        self.menu()
    
obj = lolbook()