class lolbook:
    def __init__(self):
        self.username = ""
        self.password = ""
        self.logged_in = False
        #self.menu()

    def menu(self):
        user_input = input("Welcome to Lolbook!! Please choose an option:\n" \
        "1. Sign Up\n" \
        "2. Log In\n" \
        "3. Write a Post\n" \
        "4. Message a Friend\n" \
        "5. Log Out" \
        "-> " " ")
    
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
    
    def log_in(self):
        if self.username == "" or self.password == "":
            print("No account found. Please sign up first.")
        else:
            uname = input("Enter your email address: ")
            pword = input("Enter your password: ")
            if uname == self.username and pword == self.password:
                self.logged_in = True
                print("\n")
                print("Login successful!")
            else:
                print("Incorrect username or password.")
        print("\n")
        self.menu()
    
    def write_post(self):
        if self.logged_in:
            post = input("Write your post: ")
            print(f"The following has been posted : {post}")
        else:
            print("You must be logged in to write a post.")
        print("\n")
        self.menu()
    
    def message_friend(self):
        if self.logged_in:
            frnd = input("Enter your friend's name: ")
            msg = input("Enter your message: ")
            print(f"Message sent to {frnd}: {msg}")
        else:
            print("You must be logged in to message a friend.")
        print("\n")
        self.menu()
    
    def log_out(self):
        if self.logged_in:
            self.logged_in = False
            print("You have been logged out.")
        else:
            print("You are not logged in.")
        print("\n")
        self.menu()

obj = lolbook()