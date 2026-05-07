from StudyPlanner.core.models_services import Student
from StudyPlanner.core.json_storage import Storage
from StudyPlanner.core.service_provider import CourseManagement
from datetime import date

# A class that interacts with the user and the system it
#  is the bridge between the system and the user.


class Interactor:
    def __init__(self, path):
        self.Student = Student(path)
        self.manager = CourseManagement(self.Student)
        self._menu = ["Add Course", "Modify Course", "Delete course",
                      "Add Session", "Summary", "Exit"]
        self._path = path
        self.course_added = ["Add a different Course", "Modify Course"]
        self._summary = ["For all the courses", "Particular Course", "Weekly"]

    def find_initial_date(self):
        # When the system runs the first time,
        # it stores the date the student started to use the system/App
        a = date.today()
        self.Student._start = a
        return True

    def simplify(self, a):
        # The function that creates date,
        # its a helper function to get the days
        # after the previous day the programme was used.
        ar = []
        a = str(a)
        for i in range(len(a)):
            if a[i] == "-":
                ar += [i]
        numbers = []
        for i in range(len(ar)+1):
            if i == 0:
                numbers += [int(a[:ar[i]])]
            elif i == 1:
                numbers += [int(a[ar[i-1]+1:ar[i]])]
            else:
                numbers += [int(a[ar[i-1]+1:])]
        return date(numbers[0], numbers[1], numbers[2])

    def check_day_summary(self):
        # When the programme starts and theres student data saved already,
        # it checks if a week has passed, so the summary for that
        # particular week should be or made else return True as a confirmation
        # that its done theres no summary.
        p = date.today()
        today = self.simplify(p)
        last = self.simplify(self.Student._start)
        if last == today:
            return True
        days = today.__sub__(last)
        days = str(days)
        num = ""
        for i in range(len(days)):
            if days[i] == " ":
                break
            else:
                num += days[i]
        num = int(num)
        if num >= self.Student.days_to_a_week:
            for k in range(2):
                if k == 0:
                    if self.manager.summaryCourse() and self.Student._save():
                        pass
                else:
                    if num == self.Student.days_to_a_week:
                        self.Student.days_to_a_week = 6
                        self.Student._start = today
                        self.Student._week += 1
                    else:
                        c = num/6
                        real = 0
                        i = 0
                        if c != num//6:
                            real = num
                            while real/6 != real//6:
                                real += i
                                i += 1
                            self.Student.days_to_a_week = i
                            self.Student._start = today
                            self.Student._week += num//6
            if self.manager.summaryPrinting("All"):
                return True
        return True

    # Menu function , the core of it.
    def menu(self):
        for i in range(len(self._menu)):
            print(f"{i+1}. {self._menu[i]}.")
        print("Please Enter the service to be explored.")
        num = int(print.readInt())
        if num == 1:
            return self.add()
        elif num == 2:
            return self.modify()
        elif num == 3:
            return self.delete()
        elif num == 4:
            return self.session()
        elif num == 5:
            return self.summary()
        elif num == 6:
            print("Thank you!!")
            SystemExit(0)
            return False

    def add(self):
        new = {}
        print("Enter the name of ")
        print("the course with no space between.")
        course = print.readString()
        new["course"] = course
        if self.Student.check_course(course):
            print("Enter the number hours")
            print(" you want to spend on this course,per week.")
            number = int(print.readInt())
            i = 0
            while number <= 0:
                Exception("Enter a positive number greator than 0.")
                number = int(print.readInt())
                if i == 3:
                    Exception("Last attempt to choose the correct option.")
                elif i > 3:
                    Exception("System abort.")
                    return self.menu()
                i += 1
            new["weekly_hours"] = number
            print("Rate of the course's difficulty")
            print(" from the scale of 0 - 10.")
            number = int(print.readInt())
            i = 0
            while number <= 0:
                Exception("Enter a positive number between 0 and 10.")
                number = int(print.readInt())
                if i == 3:
                    Exception("Last attempt to choose the corect option.")
                elif i > 3:
                    Exception("System abort.")
                    return self.menu()
                i += 1
            new["difficulty_level"] = number
            course = new["course"]
            hours = new["weekly_hours"]
            diff = new["difficulty_level"]
            if self.Student.add_course(course, hours, diff):
                if self.Student._save():
                    print(f"{course} course successfully added.")
                    return self.menu()
            return True

        print(f"Course {course} is already added.")
        for i in range(len(self.course_added)):
            print(f"{i+1}. {self.course_added[i]}.")
        num = print.readInt()
        i = 0
        while not 1 <= num <= 2:
            print(f"Enter a number 1 or 2.")
            num = print.readInt()
            i += 1
            if i == 3:
                print("Last attempt to choose the correct option.")
                num = print.readInt()
            if i > 3:
                print("System abort.")
                return self.menu()
        if num == 1:
            return self.add()
        return self.modify(course)

    def modify(self, course=""):
        new = {}
        if course == "":
            print("Enter the name of the course to modify, ")
            print("with no space in between.")
            course = print.readString()

        new["course"] = course
        for j in range(3):
            if j == 0:
                print("Enter the number hours you want ")
                print("to spend on this course,per week.")
                num = print.readInt()
                i = 0
                while num <= 0:
                    print(f"Enter a positive number greater than 0.")
                    num = print.readInt()
                    i += 1
                    if i == 3:
                        print("Last attempt to choose ")
                        print("a correct option.")
                        num = print.readInt()
                    elif i > 3:
                        print("System abort.")
                        return self.menu()
                new["weekly_hours"] = num
            elif j == 1:
                print("Rate the courses difficulty on a scale of 10.")
                num = print.readInt()
                i = 0
                while not 0 < num <= 10:
                    print(f"Enter a positive number between 0 and 10.")
                    num = print.readInt()
                    i += 1
                    if i == 3:
                        print("Last attempt to choose ")
                        print("a correct option.")
                        num = print.readInt()
                    if i > 3:
                        print("System abort.")
                        return self.menu()
                new["difficulty_level"] = num
            else:
                course = new["course"]
                hours = new["weekly_hours"]
                diff = new["difficulty_level"]
                if self.Student.modify_course(course, hours, diff):
                    if self.Student._save():
                        print(f"{course} course successfully")
                        print(" modified.")
                        return self.menu()

    def session(self):

        new = {}
        today = str(date.today())
        new["date"] = str(today)
        for j in range(4):
            if j == 0:
                print(f"Enter the course for this session.")
                course = print.readString()
                if self.Student.check_course(course):
                    print(f"No such course,add this course first.")
                    return self.menu()
                new["course"] = course
            elif j == 1:
                print("How many hours for this session?")
                num = print.readFloat()
                i = 0
                while not 0.5 <= num <= 5:
                    print("Enter a number between 0.5 which")
                    print(" is half of an ")
                    print("hour and 5 which is 5 hours.")
                    num = print.readFloat()
                    if i == 3:
                        print("Last chance to enter a correct number.")
                        num = print.readFloat()
                    elif i > 3:
                        print("System abort.")
                        return True
                    i += 1
                new["duration"] = num
            elif j == 2:
                print("Your focus level between 0 and 10")
                num = print.readInt()
                i = 0
                while not 0 <= num <= 10:
                    print("Your focus level between 0 and 10")
                    num = print.readInt()
                    if i == 3:
                        print("Last chance to enter a correct number.")
                        num = print.readInt()
                    elif i > 3:
                        print("System abort.")
                        return True
                    i += 1
                new["focus_level"] = num
            else:
                course = new["course"]
                dura = new["duration"]
                hours = new["focus_level"]
                datee = new["date"]
                if self.Student.add_sessions(course,datee,dura,hours):
                    if self.Student._save():
                        print("Session added.")
                    return self.menu()

    def summary(self):

        course = "All"
        if self.Student._sessions:
            for k in range(2):
                if k == 0:
                    if self.manager.summaryCourse():
                        for i in range(len(self._summary)):
                            print(f"{i+1}. {self._summary[i]}.")
                        num = print.readInt()
                        i = 0
                        while not(1 <= num <= 3):
                            num = print.readInt()
                            print(f"Please choose option 1 or 2 or 3.")
                            if i == 3:
                                print("Last chance to enter a corrent option.")
                            if i > 3:
                                print("System abort.")
                                return True
                            i += 1
                        if num == 2:
                            print("The name of the course.")
                            course = print.readString()
                        elif num == 3:
                            print("1. Current Week.")
                            print("2. Other.")
                            num = print.readInt()
                            if num == 2:
                                if not len(self.Student._courses) == 1:
                                    print("We have week,")
                                    for i in range(len(self.Student._sessions)):
                                        if i == len(self.Student._sessions) - 1:
                                            print(f"{i+1}.")
                                        else:
                                            print(f"{i+1}, ")
                                        print("Which one do you want.")
                                    num = print.readInt()
                                    i = 0
                                    while not(1 <= num <= len(self.Student._sessions)):
                                        num = print.readInt()
                                        print(f"Choose options from 1 to ")
                                        print(f"{len(self.Student._sessions)}")
                                        print(".")
                                        if i == 3:
                                            print("Last chance to ")
                                            print("enter the corrent option.")
                                        if i > 3:
                                            print("System abort.")
                                            return True
                                        i += 1
                                    course = num
                                else:
                                    print("The summary that is available")
                                    print(" right now is of the first week only")
                                    print(", should we proceed.")
                                    print("1. Yes.")
                                    print("2. No.")
                                    num = print.readInt()
                                    if num == 1:
                                        return self.manager.summaryPrinting(course)
                                    return self.menu()
                            down = len(self.Student._sessions)
                            course = down
                else:
                    if self.manager.summaryPrinting(course):
                        return self.menu()
            raise Exception("No sessions added.")

    def delete(self):
        print("Be aware that even the course sessions")
        print(" will be deleted, should we continue?")
        print("1. Yes.")
        print("2. No.")
        num = print.readInt()
        if num == 2:
            return self.menu()
        print("The name of the course to delete.")
        course = print.readString()
        if (not self.Student.check_course(course)):
            if self.Student.delete_course(course) and self.Student._save():
                print(f"Course {course} successfully deleted.")
                return self.menu()
        print(f"No such course added.")
        return self.menu()
