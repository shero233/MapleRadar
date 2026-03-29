from datetime import datetime



tasks = []
scenarios = {
        "Grocery Inflation": "Loblaws_Price_Spike -> Boycott -> Travel_to_NoFrills -> 2hrs_Lost -> Stress",
        "TTC Service Cut": "TTC_Delay -> Late_for_Class -> Grade_Risk -> Probation",
        "Housing Crisis": "Rent_+$400 -> Move_to_North_York -> Long_Commute -> Burnout",
        "Rent Squeeze Loop": "Lease_Renewal_+$500 -> Salary_Stays_Same -> Cut_Groceries_&_Transit -> Constant_Financial_Anxiety",
        "Loblaws Sticker Shock": "Loblaws_Cost_30%_Up -> Lower_Quality_Food -> Energy_Levels_Drop -> Performance_Suffer",
        "TTC Delay Cascade": "TTC_Signal_Issues -> Late_to_Work_Repeatedly -> Manager_Warning -> Job_Risk_Increases",
        "Tuition Debt Spiral": "Tuition_Fees_Raise -> Larger_Student_Loans -> Interest_Accumulates -> Overwhelming_Debt",
        "Side Hustle Exhaustion": "Job_Not_Cover_Rent -> Multiple_Gig_Jobs -> Sleep_Schedule_Collapses -> Physical_&_Mental_Burnout",
        "Winter Cost Trap": "Heating_Bills_Surge -> Minimize_Usage -> Cold_Apartment -> Health_&_Mood_Deteriorate",
        "Food Bank Reliance": "Grocery_Costs_Rising -> Paycheck_Shortfall -> Visit_Food_Banks -> Emotional_Strain",
        "Commute Inflation": "Gas_Prices_Rise -> Driving_Unaffordable -> Crowded_TTC -> Long_Commute -> Work-Life_Balance_Collapse",
        "Housing Hunt Despair": "Search_Toronto_Rentals -> Bidding_Wars -> Repeated_Rejections -> Unsafe_or_Distant_Housing",
        "Healthcare Delay": "Delay_Seeing_Doctor -> Condition_Worsens -> Emergency_Situation -> Financial_Disruption"
    
    }
#Function to add a task to the list
def add_task():
    title = input("Enter task title: ")
    description = input("Enter task decription: ")
    try:
        duration = int(input("Enter amount of time to complete task (minutes): "))
    except ValueError:
        print("Invalid input for durction. Using 60 minutes by default")
        duration = 60
    try: 
        deadline_input = input("Enter task deadline (YYYY-MM-DD): ")
        deadline = datetime.strptime(deadline_input, "%Y-%m-%d")
    except ValueError:
        print("Invalid input for deadline. Please use the format YYYY-MM-DD.")
    energy_required = input("Enter amount of energy required to complete task (Low, Medium, High): ").lower()
    location = input("Enter task location: ")
    flexibility = input("Enter task flexibility (Low, Medium, High): ").lower()
    task = {"title": title, 
            "description": description, 
            "duration": duration, 
            "deadline": deadline, 
            "energy_required": energy_required, 
            "location": location, 
            "flexibility": flexibility
        }
    tasks.append(task)
    print("Task added successfully \n")
    

def view_tasks():
    if not tasks:
        print("No tasks to display. \n")
    else:
        for i, task in enumerate(tasks):
            print(f"\nTask {i+1}:  ")  
            print(f"Title: {task['title']}")
            print(f"Description: {task['description']}")
            print(f"Duration: {task['duration']} mins")
            print(f"Deadline: {task['deadline'].date()}")
            print(f"Energy: {task['energy_required']}")
            print(f"Location: {task['location']}")
            print(f"Flexibility: {task['flexibility']}")

    return

def parse_scenario(chain):
    #Converts scenario string into a list of steps
    steps = []
    parts = chain.split("->")
    for part in parts:
        steps.append(part.strip())
    
    return steps


def apply_effect(chain):
    state = st.session_state.user_state
    steps = chain.split("->")
    for step in steps:
        step = step.strip()
        if any(k in step for k in ["Lost", "Travel", "Commute", "Delay"]):
            state["available_time"] = max(0, state['available_time'] - 60) # 每次跳跃扣除1小时
            
        
        if any(k in step for k in ["Stress", "Anxiety", "Burnout", "Depression", "Struggle"]):
            state["energy_val"] = max(0, state["energy_val"] - 2)
            state["stress_level"] += 2
            
        
        if any(k in step for k in ["Risk", "Warning", "Penalty", "Debt"]):
            state["stress_level"] += 3

    
    if state["energy_val"] <= 3: state["energy_level"] = "low"
    elif state["energy_val"] >= 7: state["energy_level"] = "high"
    else: state["energy_level"] = "medium"


def score_task(task, state):
    days_left = max(0, (task["deadline"] - datetime.now()).days)
    urgency = 2 / (1 + days_left) # 增加权重
    

    energy_penalty = 0
    if state["energy_level"] == "low" and task["energy_required"] == "high":
        energy_penalty = -1.5 
    elif state["energy_level"] == "high" and task["energy_required"] == "high":
        energy_penalty = 0.5 
        
    
    time_pressure = (480 - state["available_time"]) / 480 
    
    stress_bonus = state["stress_level"] * 0.1
    
    return urgency + energy_penalty + stress_bonus + time_pressure

def reschedule_tasks(tasks,state):
    task_scores = []
    resceduled = []

    if not tasks:
        print("No tasks to reschedule. \n")
    else:
        for task in tasks:
            score = score_task(task,state)
            task_scores.append((score,task)) 
        
        for i in range(len(task_scores)):
            for j in range(i + 1, len(task_scores)):
                if task_scores[j][0] > task_scores[i][0]:
                    task_scores[i], task_scores[j] = task_scores[j], task_scores[i]

        resceduled = [task for score, task in task_scores]

    return resceduled
