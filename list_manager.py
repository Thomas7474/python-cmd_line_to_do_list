import os
from datetime import datetime

def add_task(tasks, description, due_date):
    tasks.append({"description": description, "due_date": due_date, "completed":False})
    print("Task Added Sucessfully...")

def view_task(tasks):
    if not tasks:
        print("No Tasks Found....!")
    else:
        today = datetime.today().date()
        for idx ,task in enumerate(tasks, start=1):           # so idx starts with 1 bcz 0 th list number is not practicable
           status = "✔" if task.get("completed") else " "
           try:
                due_date_obj = datetime.strptime(task['due_date'], "%d-%m-%Y").date()
                days_remaining = (due_date_obj - today).days 
           except ValueError:
               print(f"{idx}.[{status}] {task['description']} - Invalid due date format: {task['due_date']}")
               continue

        # Alert Logic
           if days_remaining == 0 and not task['completed']:
               alert= "⚠ Due Today!"
           elif days_remaining==1 and not task['completed']:
                alert = "⏰ Due Tomorrow!"
           elif 1<days_remaining <=3 and not task['completed']:
                alert = f"⏳ Due in {days_remaining} days"
           elif  days_remaining < 0 and not task["completed"]:
               alert = "❗ Overdue!"
           else:
               alert = ""
           print(f"{idx}. [{status}] {task['description']} - due_date: {task['due_date']} {alert}")

def delete_task(tasks, task_index):
    if 1<= task_index <= len(tasks):
        del tasks[task_index-1]
        print(f"Task {task_index} deleted succesfully :)")
    else:
        print("Invalid task index :(")


def update_task(tasks, task_index):
    if 1<=task_index<=len(tasks):
        task = tasks[task_index-1]
        new_description = input("Enter new descrption: ").strip()
        if new_description:
            task['description'] = new_description

        new_due_date = input("Enter new due date : ").strip()
        if new_due_date:
            task['due_date'] = new_due_date

        print(f"Task {task_index} updated successfully!")
    else:
        print("Invalid task index :(")



def mark_completed(tasks, task_index):
    if 1<= task_index <= len(tasks):
        tasks[task_index-1]["completed"] = True
        print(f"Task {task_index} marked completed ✔")
    else:
        print("Invalid task index :(")

def save_to_file(tasks, file_path):
    with open(file_path, 'w') as f:
        for task in tasks:
            line = f"{task['description']}|{task['due_date']}|{task['completed']}\n"
            f.write(line)

def  load_from_file(file_path):
    tasks=[]
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            for line in f:
                parts = line.strip().split('|')
                if len(parts)==3:
                    description, due_date, completed_str =parts
                    completed = completed_str.lower() == "true"
                elif len(parts) == 2:
                    description, due_date = parts
                    completed = False
                else:
                    print(f"Skipping invalid line: {line.strip()}")
                    continue
                tasks.append({
                    "description": description,
                    "due_date": due_date,
                    "completed": completed
                })
    return tasks


def main():
    tasks=[]
    file_path = "tasks.txt"

    tasks = load_from_file(file_path)

    while True:
        print("\n______________To - Do - List Manager____________")
        print("\nOptions")
        print("1. Add Task")
        print("2. View Tasks")
        print("3. Mark Task Completed")
        print("4. Delete Task")
        print("5. Update Task ")
        print("6. Exit ")        

        choice = input("Enter your choice(1/2/3/4/5/6):\t")

        if choice== '1':
            description = input("Enter the Description:   ").strip()

            while True:
                  due_date_input = input("Enter due_date (DD-MM-YYYY):  "   ).strip()
                  try:
                      due_date_obj = datetime.strptime(due_date_input, "%d-%m-%Y")
                      due_date = due_date_obj.strftime("%d-%m-%Y")
                      break
                  except ValueError:
                      print("Invalid Date Format")
                 
            add_task(tasks, description, due_date)
            save_to_file(tasks, file_path)



        elif choice=='2':
            view_task(tasks)



        elif choice== '3':
            if not tasks:
                print("No tasks available to mark as completed.")
            else:
                 view_task(tasks)
                 print()
            try:
                task_index = int(input("Enter the task_index to mark completed:  "))
                mark_completed(tasks, task_index)
                save_to_file(tasks, file_path)
            except ValueError:
             print("Please enter a valid number.")



        elif choice=='4':
         if not tasks:
            print("No Tasks found to Delete")
         else:
            view_task(tasks)
            print()
            try:
                task_index = int(input("Enter the task index to delete: "))
                delete_task(tasks, task_index)
                save_to_file(tasks, file_path)
            except ValueError:
                print("Please enter a valid number.")

        elif choice == '5':
          if not tasks:
            print("No Tasks found to update")
          else:
            view_task(tasks)
            print()
            try:
                task_index = int(input("Enter the task index to update: "))
                update_task(tasks, task_index)
                save_to_file(tasks, file_path)
            except ValueError:
                print("Please enter a valid number.")



        elif choice == '6':
            print(".....Exiting the To-Do List Application......\n")
            break

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()



