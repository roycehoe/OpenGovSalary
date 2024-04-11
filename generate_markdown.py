import json

from models import StaffResponse

with open("data.json") as file:
    loaded_file = json.load(file)
    all_staff_data = [StaffResponse(**i) for i in loaded_file]
    sorted_all_staff_data = sorted(
        all_staff_data, key=lambda staff: staff.salary, reverse=True
    )
    print("| Name | Title | Annual Salary |")
    print("| ---- | ---- | ---- |")
    for staff in sorted_all_staff_data:
        print(f"|{staff.name} | {staff.title} | ${staff.salary:,.0f}|")
