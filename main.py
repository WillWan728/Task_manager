#   ==========Functions==============

# Function to register new users.
def reg_user(new_users, username_list):
    """
    Checks if username already exists in database
    if username is not used continue and enter new password
    Confirm the password is identical
    """
    while True:
        if new_users in username_list:
            print("That username is already in use on our system.")
            new_users = input("Please enter another username: ")
            continue
        else:
            print("Thank you")
            break
    new_password = input("Please enter a password: ")
    confirmation = input("Please confirm the password: ")
    if new_password == confirmation:
        print("The new user has now been registered")

        # Write to text file new username and password.
        user_file = open('user.txt', 'a')
        user_file.write("\n" + new_users + ", " + new_password)
        user_file.close()
    else:
        print("The passwords did not match. Please try again")


# Function to add tasks.
def add_task():
    """
    Ask user which user they want to assign new task
    Asks user for details of tasks the person needs to complete.
    """
    with open("tasks.txt", "a") as adding_task:
        task_for_person = input("Username of the person whom the task is assigned to:")
        title_task = input("Title of the task:")
        description = input("Description of task")
        current_date = input("Current date e.g 10 oct 2022:")
        due_date = input("Due date for task e.g 22 oct 2022:")
        task = input("Has the task been completed? Yes or No:").lower()

        # Adding tasks to txt file and print confirmation the task has been updated.
        adding_task.write("\n")
        adding_task.write(f"{task_for_person}, {title_task}, "
                          f"{description}, {current_date}, {due_date}, {task}")
        print("Task has been added.")


# Function to call all tasks from task.txt file
def task_dictionary():
    """
    Read all information from tasks.txt to dictionary.
    """
    with open("tasks.txt", "r") as task_file:
        task_dict = {}
        counter = 1

        # for each line in task_file strip and split the string.
        for line in task_file:
            line = line.strip()
            line = line.split(", ")
            task_dict[counter] = line
            counter += 1
        task_file.close()
        return task_dict


# Function to view all tasks
def view_all(task_dict):
    """
    Iterate the key-value pairs in the dictionary with the items() method.
    Use .format method to the specified values and insert them inside the string placeholder e.g {}
    """
    for key, value in task_dict.items():
        print(str(key) + ": " + '''
    Task assigned to:{}
    Title of task:{}
    Description:{}
    Date assigned:{}
    Due date:{}
    Completion:{}
    '''.format(task_dict[key][0], task_dict[key][1], task_dict[key][2],
               task_dict[key][3], task_dict[key][4], task_dict[key][5]))


# View mine function
def view_mine(task_dict):
    """
    Iterate the key value in the dictionary with the items() method.
    if the first key = to the user login - print only those tasks.
    """
    task_index = []
    for key, value in task_dict.items():
        if task_dict[key][0] == username_input:
            task_index.append(key)
            print(str(key) + ": " + '''
    Task assigned to:{}
    Title of task:{}
    Description:{}
    Date assigned:{}
    Due date:{}
    Completion:{}
    '''.format(task_dict[key][0], task_dict[key][1], task_dict[key][2],
               task_dict[key][3], task_dict[key][4], task_dict[key][5]))
    return task_index


# Mark complete function.
def mark_complete(task_dict, task_number):
    """
    Allows user to mark work complete
    Change the values in tasks to a string, so we can change No to Yes
    Write the string back to original file
    """
    task_dict[task_number][5] = "Yes"
    with open("tasks.txt", "w") as files:
        for value in task_dict.values():
            each_task = ""
            for item in value:
                each_task = each_task + "{}, ".format(item)
            each_task = each_task.strip(", ")
            each_task = each_task + "\n"
            files.write(each_task)
        files.close()
        print("Your task has been marked as completed.")


# function to change the user the task is assigned to
def change_user(tasks_dict, task_number):
    """
    If the task is complete do not allow user to change it
    Allow user to reassign the task to different employer
    """
    if tasks_dict[task_number][5] == "Yes":
        print("This task has been completed, you are not able to edit this.")
    else:
        change_person = input("Please enter the user you would like to reassign the task to.")
        while True:
            if change_person in users:  # if input = usernames in database continue
                tasks_dict[task_number][0] = change_person
                break
            else:
                print("User invalid please try again.")
                change_person = input("Please type the new user you would like to reassign the task to."
                                      "If you would like to return to the menu please enter -1.")
                if change_person != "-1":
                    continue
                if change_person == "-1":
                    print("Returning to main menu.")
                    break

        # write the edited dictionary back to the task file
        edit_file = open('tasks.txt', 'w')
        for value in tasks_dict.values():
            task_line = ""
            for item in value:
                task_line = task_line + "{}, ".format(item)
            task_line = task_line.strip(", ")
            task_line = task_line + "\n"
            edit_file.write(task_line)
        edit_file.close()
        print("Thank you. Your task has been reassigned to " + change_person + ".")


# Function to change due date
def change_due_date(task_dict, task_num):
    """ Enable the due date for a task to be changed, only if the task isn't already complete"""
    if task_dict[task_num][5] == "Yes":
        print("This task is complete and cannot be edited")
    else:
        new_due_date = input("Please enter a new due date for this task: ")
        task_dict[task_num][4] = new_due_date
        task_file = open('tasks.txt', 'w')
        for value in task_dict.values():
            task_line = ""
            for item in value:
                task_line = task_line + "{}, ".format(item)
            task_line = task_line.rstrip(", ")
            task_line = task_line + "\n"
            task_file.write(task_line)
        task_file.close()
        print("Thank you. The due date has been changed.")


# Function to generate reports.
def generate_reports(tasks_dict):
    num_task = len(tasks_dict)  # Total tasks
    # count number of completed tasks
    counter = 0
    for value in tasks_dict.values():
        if value[5] == "Yes":
            counter += 1
    completed_task = counter

    # count incomplete tasks
    incomplete_counter = 0
    for value in tasks_dict.values():
        if value[5].lower() == "no":
            incomplete_counter += 1
    incomplete_task = incomplete_counter

    # Overdue tasks
    overdue_counter = 0
    for value in tasks_dict.values():
        if value[5].lower() == "no":
            from datetime import date
            from datetime import datetime
            today = date.today()
            task_data = value[4]
            due_date = datetime.strptime(task_data, "%d %b %Y").date()
            if due_date < today:
                overdue_counter += 1
    overdue_tasks = overdue_counter

    # Percentages
    incomplete_percentage = int(incomplete_task/num_task * 100)
    overdue_percentage = int(overdue_tasks/num_task * 100)

    # writing data into new txt file called task_overview
    with open("task_overview.txt", "w") as task_overview_file:
        task_overview_file.write(f"Total number of tasks generated and tracked:{num_task}\n")
        task_overview_file.write(f"Total number of completed tasks:{completed_task}\n")
        task_overview_file.write(f"Total number of uncompleted tasks: {incomplete_task}\n")
        task_overview_file.write(f"Total number of tasks that haven't "
                                 f"been completed and that are overdue:{overdue_tasks}\n")
        task_overview_file.write(f"Percentage of tasks that are incomplete:{incomplete_percentage}\n")
        task_overview_file.write(f"Percentage of tasks that are overdue:{overdue_percentage}\n")
        task_overview_file.close()


# Function to call all users
def list_of_users():
    with open("user.txt", "r") as total_users:
        users_registered = 0
        for each_user, line in enumerate(total_users):  # loop round each line and enumerate the times.
            users_registered += 1
        print("Total users:", each_user + 1)
    return users_registered


# User overview function
def user_overview(users_registered, task_dict):
    total_users = users_registered  # All users in user.txt
    total_tasks = len(task_dict)    # total tasks
    overview = open("user_overview.txt", "w")
    overview.write(f"Total number of users registered:{total_users}\n")
    overview.write(f"Total number of tasks generated and tracked:{total_tasks}\n")
    overview.write("..............................................\n")
    overview.close()
    for user in users:
        # create counters and add them to specific count.
        users_tasks = 0
        completed_tasks = 0
        overdue_tasks = 0

        # looping through the dictionary to find values to add in different counters.
        for value in task_dict.values():
            if value[0] == user:
                users_tasks += 1
            if value[5] == "Yes":
                completed_tasks += 1
            elif value[5] == "no":
                from datetime import date
                from datetime import datetime
                today = date.today()
                task_date = value[4]
                due_date = datetime.strptime(task_date, "%d %b %Y").date()
                if due_date < today:
                    overdue_tasks += 1

        # Calculate the maths problems
        percentage_all_tasks = int(users_tasks / total_tasks * 100)
        incomplete_tasks = users_tasks - completed_tasks
        if users_tasks > 0:
            complete_percentage = int(completed_tasks / users_tasks * 100)
            incomplete_percentage = int(incomplete_tasks / users_tasks * 100)
        else:
            complete_percentage = "No tasks assigned to user"
            incomplete_percentage = "No tasks assigned to user"
        if users_tasks - completed_tasks:
            overdue_percentage = int(overdue_tasks / incomplete_tasks * 100)
        else:
            overdue_percentage = "No overdue tasks"

        # write all the data into the new user overview file.
        with open("user_overview.txt", "a") as user_overview_file:
            user_overview_file.write(f"{user} tasks:\n")
            user_overview_file.write(f"Number of assigned tasks {users_tasks}\n")
            user_overview_file.write(f"Percentage of the total number of tasks"
                                     f" that have been assigned to {user}:{percentage_all_tasks}\n")
            user_overview_file.write(f"Percentage of tasks completed by {user}: {complete_percentage}\n")
            user_overview_file.write(f"Percentage of the tasks assigned to that "
                                     f"user that must still be completed: {incomplete_percentage}\n")
            user_overview_file.write(f"Percentage of tasks assigned to that user that have not yet "
                                     f"been completed and are overdue: {overdue_percentage}\n")
            user_overview_file.write("................................................\n")
            user_overview_file.close()


# Function to call task stats
def task_stats():
    print("Overview of tasks:\n")
    with open("task_overview.txt", "r") as stats_task_overview:
        for line in stats_task_overview:
            print(line)
    stats_task_overview.close()


# Function to call all users stats
def user_stats():
    print("User tasks")
    with open("user_overview.txt", "r") as stats_user_overview:
        for line in stats_user_overview:
            print(line)
    stats_user_overview.close()


#   ==========Login in section==============
data = ""
with open("user.txt", "r") as f:

    for txt in f:
        data += txt
        data = data.replace("\n", ", ")
        usernames = data.split(", ")  # reads from the whole user.txt file and then adds all info into a list.
    f.close()
    users = []
    password = []

    # append the usernames to the users list and then the passwords into the password list.
    for lines in range(0, len(usernames)):
        if lines % 2 == 0:
            users.append(usernames[lines])  # if string is modulus by 2 append to username list.
        else:
            password.append((usernames[lines]))  # else append to password list.
    while True:
        # Asks for users input, if username is in the users list continue with the next step.
        username_input = input("Please enter your username:")
        if username_input in users:
            entry = True
            break
        else:
            entry = False
            print("Username not found, please try again.")

    user_index = users.index(username_input)  # finds the index of username input in the users list
    while True:
        password_input = input("Please enter your password:")
        if password_input == password[user_index]:  # check if the password matches the username input index.
            pass_entry = True  # allows them through to the main menu.
            break
        else:
            pass_entry = False
            print("Password incorrect, please try again.")

    # Presents menu to admin users
    while True:
        if username_input == "admin" and password_input == "adm1n":
            menu = input('''Select one of the following Options below:
                        r - Registering a user
                        a - Adding a task
                        va - View all tasks
                        vm - view my task
                        gr - Generate reports 
                        s - statistics 
                        e - Exit
                        : ''').lower()

        # Presents menu options to normal users
        else:
            menu = input('''Select one of the following Options below:
            a- Adding a task
            va - View all tasks
            vm - view my task
            e - Exit
            : ''').lower()

        # Register new user
        if menu == "r":
            if username_input == "admin":
                new_user = input("Please enter a new username: ")
                reg_user(new_user, users)
                print("\n")

        # Adding a task
        elif menu == 'a':
            add_task()

        # View all tasks
        elif menu == 'va':
            view_all(task_dictionary())

        # view my task
        elif menu == 'vm':
            index = view_mine(task_dictionary())
            select = int(input("Please enter the task number you would like to edit or enter -1 to return"
                               " main menu."))
            if select in index:  # check if select is in index list.
                choice = input("Please select from the following options:\n"
                               "m - mark task completed\n"
                               "a - assign to different user\n"
                               "d - change the due date of the task\n"
                               "e - exit\n"
                               ":")
                if choice.lower() == "m":
                    mark_complete(task_dictionary(), select)
                elif choice.lower() == "a":
                    change_user(task_dictionary(), select)
                elif choice.lower() == "d":
                    change_due_date(task_dictionary(), select)

            if select == -1:
                print("Thank you")

        elif menu == "gr":
            generate_reports(task_dictionary())
            user_overview(users, task_dictionary())
            print("Reports have been generated.")

        elif menu == "s" and username_input == "admin":
            user_stats()
            task_stats()

        elif menu == 'e':
            print('Goodbye!!!')
            exit()
    
        else:
            print("You have made a wrong choice, Please try again.")
