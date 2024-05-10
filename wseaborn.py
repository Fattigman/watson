import seaborn as sns
import seaborn.objects as so
import pandas as pd
import subprocess
from matplotlib import pyplot as plt
import warnings

# Yolo
warnings.filterwarnings("ignore")

def get_aggr() -> str:
    data:str  = subprocess.run(['watson', "aggregate"],  stdout=subprocess.PIPE).stdout.decode('utf-8')
    return data

def sum_time(i:int,x: str) -> float:
    if "m" in x:
        return int(x[:-1])/60
    elif "s" in x:
        return int(x[:-1])/3600
    return int(x[:-1])
    
def parse_aggr(data:str) -> pd.DataFrame:
    weekly_hours = pd.DataFrame(columns=["Day", "Time", "Activity"])
    rows_list = []
    for line in data.split("\n"):
        if len(line) == 0:
            continue
        if line[0] in ["M", "T", "W", "F", "S"]:
            day :str = line.split(" ")[0]
        elif line[0] != "\t":
            activity_type :str = line.split(" ")[2]
            time : str= line.split(" - ")[1]
            total_time : float = sum([sum_time(i,x) for i, x in enumerate(time.split(" "))])
            rows_list.append({"Day":day, "Time":total_time, "Activity":activity_type})

    weekly_hours = pd.concat([weekly_hours, pd.DataFrame(rows_list)], ignore_index=True)
    print(weekly_hours)
    # Sort the dictionary by day
    return weekly_hours

def get_total_time(weekly_hours:dict) -> float:
    return sum(weekly_hours.values())

def plot_aggr(data: pd.DataFrame, total_time : float = None):
    # Add a red line at 8 hours
    plt.axhline(y=8, color='r', linestyle='--')
    # Add the total time to the plot if available
    if total_time:
        plt.title(f"Total time: {total_time} hours")
    sns.histplot(data, x='Day', hue='Activity', weights='Time',
             multiple='stack')
    plt.show()

def main():
    data = get_aggr()
    weekly_hours = parse_aggr(data)
    #total_time = get_total_time(weekly_hours)
    plot_aggr(weekly_hours)

if __name__ == "__main__":
    main()