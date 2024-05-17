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
    weekly_hours = pd.DataFrame(columns=["Day", "Time", "Activity", 'Day of Week'])
    rows_list = []
    for line in data.split("\n"):
        if len(line) == 0:
            continue
        if line[0] in ["M", "T", "W", "F", "S"]:
            day :str = line.split(" ")[0]
            day_of_week :str = line.split(" ")[1]
        elif line[0] != "\t":
            activity_type :str = line.split(" ")[2]
            time : str= line.split(" - ")[1]
            total_time : float = sum([sum_time(i,x) for i, x in enumerate(time.split(" "))])
            rows_list.append({"Day":day, "Time":total_time, "Activity":activity_type, 'Day of Week':day_of_week})

    weekly_hours = pd.concat([weekly_hours, pd.DataFrame(rows_list)], ignore_index=True)
    # Filter out duplicate days
    table = weekly_hours.groupby(['Day', 'Day of Week']).sum().reset_index()
    for day in table['Day']:
        # If there are multiple entries for the same day, remove all but the last
        if (table['Day'] == day).sum() > 1:
            for counter, i in enumerate(weekly_hours['Day'] == day):
                if i:
                    weekly_hours.drop(counter, inplace=True)
                else:   
                    break
    # Sort the dictionary by day
    return weekly_hours

def get_total_time(weekly_hours:dict) -> float:
    return sum(weekly_hours.values())

def plot_aggr(data: pd.DataFrame, total_time : float = None):
    # Add a red line at 8 hours
    plt.axhline(y=8, color='r', linestyle='--')
    # Add the total time to the plot if available
    if total_time:
        plt.title(f"Total time last 7 days: {total_time} hours")
    ax = sns.histplot(data, x='Day', hue='Activity', weights='Time',
             multiple='stack')
    
    # Add the total height of each bar to the top of the bar
    heights = {}
    for counter, p in enumerate(ax.patches):
        # Get the height of the bin
        if p.get_x() in heights:
            heights[p.get_x()] += p.get_height()
        else:
            heights[p.get_x()] = p.get_height()
    # display the height of each bar
    for x in heights:
        ax.text(x = x+0.5, 
                y = heights[x]+.05, 
                s = '{:.2f}'.format(heights[x]), 
                ha = 'center')
    plt.ylabel("Hours (h)")
    plt.show()


def main():
    data = get_aggr()
    weekly_hours = parse_aggr(data)
    total_time = round(weekly_hours['Time'].sum(), 2)
    plot_aggr(weekly_hours, total_time)

if __name__ == "__main__":
    main()