from StudyPlanner.core.json_storage import Storage
from datetime import date

class Student:
    def __init__(self, path):
        self._courses = {}
        self._sessions = {}
        self._start = 0
        self.storage = Storage(path)
        self._summary = {}
        self._week = 1
        self.days_to_a_week = 6
        
    def add_course(self, name, weekly_hours, difficulty_level):
        if self._courses:
            self._courses[name] = {"weekly_hours":weekly_hours,"difficulty_level": difficulty_level}
            return True
        self._courses[name] = {"weekly_hours":weekly_hours,"difficulty_level": difficulty_level}
        return True
    
    def check_course(self, course):
        if course not in self._courses:
            return True
        return False

    def modify_course(self, name, weekly_hours, difficulty_level):
        if self._courses:
            if name in self._courses:
                self._courses[name] = {"weekly_hours":weekly_hours,"difficulty_level": difficulty_level}
                return True
        else:
            raise ValueError("No courses addded on the system.")

    def delete_course(self, name):
        new = {}
        for i in range(2):
            if i == 0:
                if self._courses:
                    if name in self._courses:
                        for k in self._courses:
                            if k != name:
                                new[k] = self._courses[k]
                        self._courses = new
                    else:
                        raise ValueError("No such course added on the system.")
                else:
                    raise ValueError("No courses added on the system.")
            else:
                if self._sessions:
                    new = {}
                    for j in self._sessions:
                        if name in self._sessions[j]:
                            for k in self._sessions[j]:
                                if k != name:
                                    new[k] = self._sessions[j][k]
                        self._sessions[j] = new
        return True

    def add_sessions(self, course, date, duration, focus_level):
        if self._sessions == {} or f"Week {self._week}" not in self._sessions:
            new = {}
            now = {}
            now["date"] = date ; now["duration"] = duration ; now["focus_level"] = focus_level
            new[course] = [now]
            self._sessions[f"Week {self._week}"] = new
            return True

        if f"Week {self._week}" in self._sessions:
            new = self._sessions[f"Week {self._week}"]
            now = {}
            now["date"] = date ; now["duration"] = duration ; now["focus_level"] = focus_level
            if course in new:
                new[course] += [now]
            else:
                new[course] = [now]   
            self._sessions[f"Week {self._week}"] = new
            return True
        
    def _save(self):
        save = {"courses":self._courses,"sessions":self._sessions,"Current_week":self._week,"weekly_summary":self._summary,"Start_Week":str(self._start),"Days_to_a_week":self.days_to_a_week}
        if self._summary == {} and self._sessions:
            save  = {"courses":self._courses,"sessions":self._sessions,"Current_week":self._week,"Start_Week":str(self._start),"Days_to_a_week":self.days_to_a_week}
        if self._sessions == {} and self._summary == {}:
            save = {"courses":self._courses,"Current_week":self._week,"Start_Week":str(self._start),"Days_to_a_week":self.days_to_a_week}
        if self._sessions == {} and self._summary:
            save = {"courses":self._courses,"Current_week":self._week,"weekly_summary":self._summary,"Start_Week":str(self._start),"Days_to_a_week":self.days_to_a_week}
        return self.storage.save(save)

    def _load(self):
        return self.storage.load()