import platform
import time
import pandas as pd
import plotly.express as px
import numpy as np
import subprocess
import re
import numpy as np
import matplotlib.pyplot as plt

def get_wifi_signal_strength() -> int:
    """Get the signal strength of the wifi connection.
    
    Returns:
        The signal strength in dBm.
    """
    # Question 1: What is dBm? What values are considered good and bad for WiFi signal strength?
        # dBm is a unit of measurement for the strength of the signal. It takes in a value in mW and converts it to a log scale via:
        # dBm = 10 * log10(mW)

    # Question 2: Why do we need to check the OS? What is the difference between the commands for each OS?
        # The different OS have different methods used to get signal strength. They return different values and formats, so we need to have specifics regex for each.

    # Question 3: In your own words, what is subprocess.check_output doing? What does it return?
    # it runs a shell command and retrieves the output of that command.
    # HINT: https://docs.python.org/3/library/subprocess.html#subprocess.check_output

    # Question 4: In your own words, what is re.search doing? What does it return?
    # it is matching a regex for the output of the previously run shell command.
    # HINT: https://docs.python.org/3/library/re.html#re.search

    # Question 5: In the Windows case, why do we need to convert the signal quality to dBm?
    # signal quality is a percentage of maximal strength, which is -100 dbm, so we need to conver it.
    # HINT: https://learn.microsoft.com/en-us/windows/win32/api/wlanapi/ns-wlanapi-wlan_association_attributes?redirectedfrom=MSDN
    if platform.system() == 'Linux': # Linux
        output = subprocess.check_output("iwconfig wlan0", shell=True)
        match = re.search(r"Signal level=(-?\d+) dBm", output.decode('utf-8'))
        signal_strength = int(match.group(1))
    elif platform.system() == 'Windows': # Windows
        output = subprocess.check_output("netsh wlan show interfaces", shell=True)
        match = re.search(r"Signal\s*:\s*(\d+)%", output.decode('utf-8'))
        signal_quality = int(match.group(1))
        signal_strength = -100 + signal_quality / 2
    elif platform.system() == 'Darwin': # Mac
        output = subprocess.check_output("/System/Library/PrivateFrameworks/Apple80211.framework/Versions/Current/Resources/airport -I", shell=True)
        match = re.search(r"agrCtlRSSI:\s*(-?\d+)", output.decode('utf-8'))
        signal_strength = int(match.group(1))
    else:
        raise Exception("Unknown OS")

    return signal_strength

def main():
    # Choose at least 5 locations to sample the signal strength at
    # These can be rooms in your house, hallways, different floors, outside, etc. (as long as you can get a WiFi signal)
    locations = ['bedroom', 'living room', 'kitchen', 'bathroom', 'garage']
    samples_per_location = 10 # number of samples to take per location
    time_between_samples = 1 # time between samples (in seconds)

    data = [] # list of data points
    for location in locations:
        print(f"Go to the {location} and press enter to start sampling")
        input() # wait for the user to press enter
        signal_strengths = [] # list of signal strengths at this location

        # TODO: collect 10 samples of the signal strength at this location, waiting 1 second between each sample
        # HINT: use the get_wifi_signal_strength function
        for i in range(samples_per_location): # iterate to collect samples
            signal_strength = get_wifi_signal_strength() # collect signal
            signal_strengths.append(signal_strength) # append to list
            time.sleep(time_between_samples) # wait for 1 second

        
        # TODO: calculate the mean and standard deviation of the signal strengths you collected at this location
        signal_strength_mean = np.mean(signal_strengths)
        signal_strength_std = np.std(signal_strengths)

        # Question 6: What is the standard deviation? Why is it useful to calculate it?
        # standard deviation is the measure of variance that an average sample has from the mean. This can show the stability of the wifi signal.
        data.append((location, signal_strength_mean, signal_strength_std))

    # create a dataframe from the data
    df = pd.DataFrame(data, columns=['location', 'signal_strength_mean', 'signal_strength_std'])

    # Question 7: What is a dataframe? Why is it useful to use a dataframe to store the data?
    # a dataframe is basically the python version of an excel spreadsheet. It stores data in a 2D tabular format. 
    # It is useful because there are easy built in function to index and manipulate the data in whatever way you want.
    # HINT: https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.html
    # HINT: print the dataframe to see what it looks like
    # print(df)

    # TODO: plot the data as a bar chart using plotly
    # HINT: https://plotly.com/python/bar-charts/
    # NOTE: use the error_y parameter of px.bar to plot the error bars (1 standard deviation)
    #   documentation: https://plotly.com/python-api-reference/generated/plotly.express.bar.html
    fig, ax = plt.subplots()
    ax.bar(df['location'], df['signal_strength_mean'], yerr=df['signal_strength_std'])

    ax.set_title('WiFi Signal Strength by Location')
    ax.set_xlabel('Location')
    ax.set_ylabel('Signal Strength (dBm)')
    plt.xticks(rotation=45)

    plt.tight_layout()
    plt.show()


    # Question 8: Why is it important to plot the error bars? What do they tell us?
    # error bars are important because they give us key insight into the variance of the data we collected. Plotting this shows the stability of the singal.

    # write the plot to a file - make sure to commit the PNG file to your repository along with your code
    # write the plot to a file using matplotlib
    fig.savefig("signal_strength.png")

    # Question 9: What did you observe from the plot? How does the signal strength change as you move between locations?
    #             Why do you think signal strength is weaker in certain locations?
    # as I got further away, the signal got weaker and less stable. The best wifi is in my bedroom and living room!


if __name__ == "__main__":
    main()