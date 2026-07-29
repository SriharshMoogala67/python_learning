class Employee: 
    def __init__(self, name: str): 
        self.name = name 
        self._salary = 0.0

    def calculate_salary(self) -> float:
        raise NotImplementedError(
            "Subclasses must implement calculate_salary()"
        )    
    
    def display_details(self) -> None:
        print(f"Employee: {self.name}")
        print(f"Salary: £{self.calculate_salary():.2f}")



class Fulltime(Employee): 
    def __init__(self, name: str, monthly_salary: float): 
        super().__init__(name)

        if monthly_salary < 0:
            raise ValueError("Monthly salary cannot be negative.")

        self._salary = monthly_salary

    def calculate_salary(self) -> float:
        return self._salary 


class parttime(Employee):
    
    def __init__(
            self,
        name: str,
        hourly_rate: float,
        hours_worked: float,
        ): 
        
        super().__init__(name)

        if hourly_rate < 0:
            raise ValueError("Hourly rate cannot be negative.")

        if hours_worked < 0:
            raise ValueError("Hours worked cannot be negative.")

        self.hourly_rate = hourly_rate
        self.hours_worked = hours_worked

    def calculate_salary(self) -> float:
        self._salary = self.hourly_rate * self.hours_worked
        return self._salary

employee1 = Fulltime("Harsh", 50000)
employee2 = parttime("Rahul", 500, 80)
employee3 = Fulltime("Aman", 60000)

employees = [employee1, employee2, employee3]

for employee in employees:
    employee.display_details()
    print()