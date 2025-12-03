import time

def timer(t):
    while t:
        for times in range(0,t+1):
            
            mins = times // 60
            sec = times % 60
            # If minute hasn't passed the 60 -> prints how many minutes and seconds have been passed
            if mins < 60:
                print(f"{mins} minute and {sec} seconds has been passed")
            # If minutes has passed the 60 -> It's dividing it for show hours and changing value of minutes (limits it to the 60)
            elif mins >= 60:
                hours = mins // 60
                mins -= hours * 60
                print(f"{hours} hours , {mins} minutes and {sec} seconds has been passed")

            time.sleep(1)
            t-= 1

t = input("Time? ")
t = int(t)
timer(t)
