class Employee:
    #special method/ dunder method - constructor
    def __init__(self):
        self.id = 123
        self.salary = 10000
        self.designation = "Developer"

    def travel(self, destination):
        print(f"Employee is travelling to {destination}")

sam = Employee()
sam.travel("New York")
