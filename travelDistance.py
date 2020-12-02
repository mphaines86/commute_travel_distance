import json
import glob
import datetime
import collections
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

files = glob.glob("Semantic Location History\\*\\*.json", recursive=True)
files = [x for x in files if float(x.split("\\")[-1][:4]) > 2018]
print(files)

formatter = "%Y-%m-%d"

distances = {}
for file in files:
    all_distances = []
    with open(file) as filehandler:
        data = json.load(filehandler)
    # print(data["timelineObjects"][0]["activitySegment"])

    for i in range(len(data["timelineObjects"])):
        # print(i)
        try:
            date = datetime.datetime.fromtimestamp(float(data["timelineObjects"][i]["activitySegment"]["duration"]["startTimestampMs"])/1000)
        except KeyError:
            continue
        date = date.strftime(formatter)
        # print(date)
        try:
            all_distances.append(data["timelineObjects"][i]["activitySegment"]["distance"])
            if date in distances.keys():
                distances[date] = distances[date] + float(data["timelineObjects"][i]["activitySegment"]["distance"]) * 0.000621371
            else:
                distances[date] = float(data["timelineObjects"][i]["activitySegment"]["distance"]) * 0.000621371
        except KeyError:
            continue
    print(file, sum(all_distances) * 0.000621371)



distances = collections.OrderedDict(sorted(distances.items()))
converted_dates = list(map(datetime.datetime.strptime, distances.keys(), len(distances.keys())*[formatter]))

date_set = set(converted_dates[0] + datetime.timedelta(x) for x in range((converted_dates[-1] - converted_dates[0]).days))
missing = sorted(date_set - set(converted_dates))

for d in missing:
    distances[d.strftime(formatter)] = 0

distances = collections.OrderedDict(sorted(distances.items()))
converted_dates = list(map(datetime.datetime.strptime, distances.keys(), len(distances.keys())*[formatter]))

months = mdates.MonthLocator()
weeks = mdates.DayLocator()
months_fmt = mdates.DateFormatter('%Y-%b')

plt.rcParams.update({'font.size': 14})

fig = plt.figure(num=None, figsize=(10, 6), dpi=300, facecolor='w', edgecolor='k')
ax = fig.add_subplot()
ax.scatter(converted_dates, distances.values(), s=20*2**0.5)

ax.xaxis.set_major_locator(months)
ax.xaxis.set_major_formatter(months_fmt)
# ax.xaxis.set_minor_locator(weeks)

datemin = datetime.datetime.strptime("2019-11-1", formatter)
datemax = datetime.datetime.strptime("2020-11-30", formatter)
ax.set_xlim(datemin, datemax)
ax.set_xlabel("Date")
ax.set_ylim(0, 100)
ax.set_ylabel("distance traveled per day (Miles)")

ax.plot([datemin, datetime.datetime.strptime("2020-10-10", formatter)], [40, 40], linestyle="--", color='darkorange', linewidth=2)
ax.plot([datemin, datetime.datetime.strptime("2020-10-10", formatter)], [20, 20], linestyle="--", color='darkgreen', linewidth=2)
ax.plot([datetime.datetime.strptime("2020-10-10", formatter), datemax], [8, 8], linestyle="--", color='darkorange', linewidth=2)
ax.plot([datetime.datetime.strptime("2020-10-10", formatter), datemax], [40, 40], linestyle="--", color='darkgreen', linewidth=2)
ax.axvline(datetime.datetime.strptime("2020-3-16", formatter), color='k', linewidth=2)
ax.axvline(datetime.datetime.strptime("2020-3-30", formatter), color='k', linewidth=2)
ax.axvline(datetime.datetime.strptime("2020-4-30", formatter), color='k', linewidth=2)
ax.axvline(datetime.datetime.strptime("2020-5-29", formatter), color='k', linewidth=2)
ax.axvline(datetime.datetime.strptime("2020-10-10", formatter), color='k', linewidth=2)

fig.autofmt_xdate()
plt.savefig("travel_data.png")
# plt.show()