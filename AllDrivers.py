import numpy as np
import pandas as pd
import fastf1
import matplotlib.pyplot as plt
import streamlit as st
import fastf1.plotting

def allDrivers(session,option):
    session.load()
    match option:
            case "Position Changes":
                fig,ax = plt.subplots(figsize=(8.0,4.9))
                for drv in session.drivers:
                    drv_laps = session.laps.pick_driver(drv)
                    abb = drv_laps['Driver'].iloc[0]
                    color = fastf1.plotting.driver_color(abb)
                    ax.plot(drv_laps['LapNumber'],drv_laps['Position'],label = abb,color=color)
                ax.set_ylim([20.5,0.5])
                ax.set_yticks([1,5,10,15,20])
                ax.set_xlabel('Lap')
                ax.set_ylabel('Position')
                ax.legend(bbox_to_anchor=(1.0,1.02))
                plt.tight_layout()
                return fig
            case "Tyres Used":
                laps = session.laps
                drivers = session.drivers
                drivers = [session.get_driver(driver)["Abbreviation"] for driver in drivers]
                stints = laps[["Driver","Stint","Compound","LapNumber"]]
                stints = stints.groupby(["Driver","Stint","Compound"])
                stints = stints.count().reset_index()
                stints = stints.rename(columns={"LapNumber": "StintLength"})
                fig, ax = plt.subplots(figsize =(5,10))
                for driver in drivers:
                    driver_stints = stints.loc[stints["Driver"]==driver]
                    previous_stint_end = 0
                    for idx,row in driver_stints.iterrows():
                        plt.barh(
                            y=driver,width = row["StintLength"],left = previous_stint_end,color=fastf1.plotting.COMPOUND_COLORS[row["Compound"]],edgecolor = "black",fill = True
                        )
                        previous_stint_end += row["StintLength"]
                plt.xlabel("Lap Number")
                plt.grid(False)
                ax.invert_yaxis()
                plt.tight_layout()
                return fig
            case "Race History":
                fig,ax = plt.subplots(figsize=(8.0,4.9))
                driver_legend = {}
                for drv in session.drivers:
                    drv_laps = session.laps.pick_driver(drv)
                    abb = drv_laps['Driver'].iloc[0]
                    status_colors = {1: fastf1.plotting.driver_color(abb),  2: 'yellow',3: 'black', 4: 'orange', 5: 'red', 6: 'blue'}
                    status = drv_laps['TrackStatus'].values
                    colors = []
                    for i in range(len(drv_laps)):
                        if(len(str(status[i])) >1):
                            if(str(5) in str(status[i])):
                                status[i] = 5
                            elif(str(6) in str(status[i])):
                                status[i] = 6
                            elif(str(4) in str(status[i])):
                                status[i] = 4
                            elif(str(2) in str(status[i])):
                                status[i] = 2
                            else:
                                status[i] = 1
                        lapStatus = status[i]   
                        if(lapStatus in status_colors):
                            colors.append(status_colors[lapStatus])
                        else:
                            colors.append(fastf1.plotting.driver_color(abb))
                    ax.plot(drv_laps['LapNumber'].iloc[i],drv_laps['Position'].iloc[i],label = abb,color=colors)
                    driver_legend[abb] = status_colors[1]
                for driver, color in driver_legend.items():
                     ax.plot([], [], color=color, label=driver)

                ax.set_ylim([20.5,0.5])
                ax.set_yticks([1,5,10,15,20])
                ax.set_xlabel('Lap')
                ax.set_ylabel('Position')
                ax.legend(bbox_to_anchor=(1.0,1.02))
                plt.tight_layout()
                return fig
            case "Fastest Laps":
                drivers = session.drivers
                fig,ax = plt.subplots(figsize=(8.0,4.9))
                bar_width = 1
                i = 1
                largest = 0
                smallest = 10000
                fastest1 = 10000
                fastest2 = 1000
                fastest3 = 10000
                for drv in drivers:
                    drv_laps = session.laps.pick_driver(drv)
                    abb = drv_laps['Driver'].iloc[0]
                    try:
                        color = fastf1.plotting.driver_color(abb)
                    except:
                        color = 'red'
                    sector1 = float((drv_laps.pick_fastest().values[8]).total_seconds())
                    sector2 = float((drv_laps.pick_fastest().values[9]).total_seconds()) + sector1
                    sector3 = float((drv_laps.pick_fastest().values[10]).total_seconds()) + sector2
                    if(sector1 < fastest1):
                        fastest1 = sector1
                    if(sector2 < fastest2):
                        fastest2 = sector2
                    if(sector3 < fastest3):
                        fastest3 = sector3
                    times = [sector1,sector2,sector3]
                    if(max(times)>largest):
                        largest = max(times)
                    if(min(times)<smallest):
                        smallest = min(times)
                    x_positions = np.arange(3) + i * (3 + bar_width)
                    ax.bar(x_positions, [sector1, sector2, sector3],
                    width=bar_width, label=abb, color=color,edgecolor = 'black')
                    i+=1
                ax.axhline(y=fastest1,color = '#aa27ca',linestyle = '--')
                ax.axhline(y=fastest2,color = '#aa27ca',linestyle = '--')
                ax.axhline(y= fastest3,color = '#aa27ca',linestyle = '--')
                ax.axes.get_xaxis().set_visible(False)
                ax.set_ylim([smallest - 0.2, largest + 0.2])  
                ax.set_xlabel('Sector')
                ax.set_ylabel('Time (seconds)')
                ax.legend(bbox_to_anchor=(1.0, 1.02))
                plt.tight_layout()
                return fig
            case 'Pit Stop Times':
                fig,ax = plt.subplots(figsize=(8.0,4.9))
                laps = session.laps
                bar_width = 0.5
                drivers = session.drivers
                pit_stop_laps = session.laps.pick_box_laps()
                pit_stop_laps = pit_stop_laps.sort_values(by=['Driver','LapNumber'])
                pit_stop_laps = pit_stop_laps.reset_index()
                pit_stop_laps.loc[pit_stop_laps['Driver'].shift(-1) == pit_stop_laps['Driver'], 'PitStopTime'] = pit_stop_laps['PitOutTime'].shift(-1) - pit_stop_laps['PitInTime']
                pit_stop_laps = pit_stop_laps.dropna(subset=['PitStopTime'])
                pitStops = []
                for i in range (len(pit_stop_laps)):
                    pitStops += [[float((pit_stop_laps.values[i][32:][0]).total_seconds()),pit_stop_laps.values[i][2]]]
                pitStops.sort()
                pitStops = pitStops[:10]
                i = 0
                for times in pitStops:
                    try:
                        color = fastf1.plotting.driver_color(times[1])
                    except:
                        color = 'green'
                    x_positions = i * (0.2 +bar_width)
                    ax.bar(x_positions, times[0],width=bar_width, label=times[1], color=color,edgecolor = 'black')
                    i+=1
                ax.axes.get_xaxis().set_visible(False)
                ax.set_ylim([pitStops[0][0] - 0.2, pitStops[9][0] + 0.2])  
                ax.set_xlabel('Driver')
                ax.set_ylabel('Time (seconds)')
                ax.legend(bbox_to_anchor=(1.0, 1.02))
                plt.tight_layout()
                return fig

                  
