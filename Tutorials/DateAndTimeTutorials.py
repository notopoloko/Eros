from PyQt5.QtCore import QDate, QTime, QDateTime, Qt

# QDate
now = QDate.currentDate()
print(now.toString(Qt.ISODate))
print(now.toString(Qt.DefaultLocaleLongDate))

d = QDate(2016, 12,23)

xmas1 = QDate(2016,12,24)
xmas2 = QDate(2017,12,24)

print('{0} days passed'.format(d.daysTo(xmas1)))
print('{0} days passed'.format(d.daysTo(xmas2)))

print('\n\nDays in month: {0}'.format(d.daysInMonth()))
print('Days in year: {0}\n'.format(d.daysInYear()))

print('Gregoriam date for today {0}'.format(d.toString(Qt.ISODate)))
print('Julian date for today {0}'.format(d.toJulianDay()))

# QDateTime
dateTime = QDateTime.currentDateTime()
print("\n\nLocal datetime",dateTime.toString(Qt.ISODate))
print("Universar datetime",dateTime.toUTC().toString(Qt.ISODate))

print('\n\nAdding 12 days: {0}'.format(dateTime.addDays(12).toString(Qt.ISODate)))
print('Sub 22 days: {0}'.format(dateTime.addDays(-22).toString(Qt.ISODate)))
print('Adding 50 seconds: {0}'.format(dateTime.addSecs(50).toString(Qt.ISODate)))
print('Adding 3 months: {0}'.format(dateTime.addMonths(3).toString(Qt.ISODate)))
print('Adding 12 years: {0}'.format(dateTime.addYears(12).toString(Qt.ISODate)))

print('\n\nTime zone: {0}'.format(dateTime.timeZoneAbbreviation()))
if dateTime.isDaylightTime():
    print('The current date falls in DST time\n')
else:
    print('The current date does not falls in DST time\n')

print('The offset from UTC is: {0} hours\n'.format(dateTime.offsetFromUtc()/3600))

windows_time = dateTime.toSecsSinceEpoch()
print(windows_time)

d = QDateTime.fromSecsSinceEpoch(windows_time)
print(d.toString(Qt.ISODate) + '\n')

# QTime
time = QTime.currentTime()
print(time.toString(Qt.DefaultLocaleLongDate))