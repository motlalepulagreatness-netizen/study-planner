import os
import json
from StudyPlanner.core.json_storage import  Storage
from StudyPlanner.core.models_services import Student

# Class that manages the courses.
class CourseManagement:
    def __init__(self,student):
        self.student = student

    # Creates or prepares the summary to be printed.
    def summaryCourse(self):
        summary = {}
        if self.student._sessions:
            for k in range(2):
                if k == 0:
                    data = self.student._sessions[f"Week {self.student._week}"]
                    new = {} ; now = {}
                    for j in data:
                        average = 0
                        num = self.total_time_per_course(j)
                        total = self.total_expected_per(j)
                        average = f"{(num/total)*100:.02f}"
                        new[j] = float(average)
                    now["Time_completion_percentage"] = new
                    summary[f"Week {self.student._week}"] = now
                else:
                    new = {}
                    data = self.student._sessions[f"Week {self.student._week}"]
                    for j in data:
                        number = self.difficulty_reach(j)
                        new[j] = float(number)
                    now = summary[f"Week {self.student._week}"]
                    now["Difficulty_reached"] = new
                    self.student._summary[f"Week {self.student._week}"] = now
            return True
                
    # Summary Printing.
    def summaryPrinting(self,option):
        array = [] ; names = []
        summary = self.student._summary[f"Week {self.student._week}"]
        for i in summary:            
            for j in summary[i]:
                array += [summary[i][j]]
                if j not in names:
                    names += [j]
        if option == "All":
            for i in range(len(array)//2):
                print(f"{names[i]}.")
                print(f"Time completion {array[i]}.")
                print(f"Difficulty approached {array[i+len(names)]}. \n")
            if len(names) != len(self.student._courses):
                absent = []
                for k in self.student._courses:
                    if k not in names:
                        absent += [k]
                string = ""
                for k in range(len(absent)):
                    if len(absent) == 1:
                        string = absent[k]
                    else:
                        if k != len(absent) - 1:
                            string += f"{absent[k]}, "
                        else:
                            string = string[:len(string)-2]
                            string += " and" + " " +absent[k]
                print(f"Other courses dont have sessions yet, courses like {string}. \n")
                return True
        elif type(option) == int:
            week =  self.student._summary[f"Week {option}"]
            array = [] ; names = []
            for j in week:
                array += [week[j]]
                if j not in names:
                    names += [j]
            for i in range(len(array)//2):
                print(f"{names[i]}.")
                print(f"Time completion {array[i]}.")
                print(f"Difficulty approached {array[i+len(names)]}. \n")
            return True
        else:
            for i in range(len(array)//2):
                if names[i] == option:
                    print("\n")
                    print(f"Time completion {array[i]}.")
                    print(f"Difficulty approached {array[i+len(names)]}. \n")
            return True
    
                    
    def total_time_per_course(self,course):
        # Total time spent on each course.
        if self.student._sessions:
            for i in self.student._sessions:
                if course in self.student._sessions[i]:
                    count = 0
                    for k in self.student._sessions[i][course]:
                        count += k["duration"]
                    return count
                                        
    def total_time(self):
        # Total time spent across all the courses. 
        if self.student._sessions:
            count = 0
            for k in self.student._sessions:
                for z in self.student._sessions[k]:
                    count += z["duration"]
            return count
        raise ValueError("No sessions.")

    def total_time_expected(self):
        # Total time expected to spend on all the courses.
        if self.student._courses:
            count = 0
            for k in self.student._courses:
                z = self.student._courses[k]
                count += z["weekly_hours"]
            return count
        raise ValueError("No course added.")
    
    def total_expected_per(self,course):
        if course in self.student._courses:
            data = self.student._courses[course]
            return data["weekly_hours"]
        return 0
    
    def difficulty_reach(self,course):
        if self.student._sessions:
            for i in self.student._sessions:
                if course in self.student._sessions[i]:
                    count = 0 ; counts = 0
                    for k in self.student._sessions[i][course]:
                        count += k["focus_level"]
                        counts += 1
                    expected = self.student._courses[course]["difficulty_level"]
                    if counts == 1:
                        average = f"{((count/expected)*100):.02f}"
                    else:
                        average = f"{((count/counts)*(expected)):.02f}"
                    return average         

    def check_summary(self,date):
        got = False ; num = ""
        for k in date:
            if k == " " and got == False:
                got = True
            elif not got:
                num += str(k)
        num = int(num)
        self.current_day = num
        if self.current_day >= self.student._end_week:
            self.summaryCourse()
            return True
        return True
