import datetime, re
import pytz
from pytz import *
# HOURLY BASIS NUMBER OF ORDER APIS AND INVOICE APIS
with open("/home/mintu/essentials/Smart Retail/logs/web-1/access.log.2", 'r') as serv1log1:
    startHour = "11"
    HourlyTrafficOrder = {}
    HourlyTrafficInvoice = {}
    countOrders = 0
    countInvoice = 0
    ResponseTimeOrders = []
    ResponseTimeInvoice = []

    for s1l1 in serv1log1:
        extractedList = s1l1.split('"')
        TimeDurations = extractedList[0].split()
        match = re.search(r'\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2}', s1l1)
        capturedDate = datetime.datetime.strptime(match.group(), '%d/%b/%Y:%H:%M:%S')
        datetime_gmt = capturedDate.replace(tzinfo=pytz.UTC)
        datetime_ist = datetime_gmt.astimezone(timezone('Asia/Kolkata'))
        hr = datetime_ist.strftime('%H')
        if hr == startHour:
            if '/v2/online_orders/ HTTP/1.1" 20' in s1l1:
                countOrders = countOrders + 1
                ResponseTimeOrders.append(float(TimeDurations[0]))
            elif '/create/invoice/ HTTP/1.1" 20' in s1l1:
                countInvoice = countInvoice + 1
                ResponseTimeInvoice.append(float(TimeDurations[0]))
        else:
            HourlyTrafficOrder[startHour] = countOrders
            HourlyTrafficInvoice[startHour] = countInvoice
            startHour = hr
            countOrders = 0
            countInvoice = 0
            if '/orders/ HTTP/1.1" 20' in s1l1:
                countOrders = 1
            elif '/create/invoice/ HTTP/1.1" 20' in s1l1:
                countInvoice = 1
order_max = max(HourlyTrafficOrder.keys(), key=(lambda k: HourlyTrafficOrder[k]))
invoice_max = max(HourlyTrafficInvoice.keys(), key=(lambda k: HourlyTrafficInvoice[k]))
ResponseTimeOrders.sort(reverse=True)
ResponseTimeInvoice.sort(reverse=True)

with open("/home/mintu/essentials/Smart Retail/logs/web-1/access.log.2", 'r') as serv1log1, open(
        "/home/mintu/essentials/Smart Retail/logs/Api Lists/apiCalledWithOrders", "w") as file:
    # file.write("\nApi calls happened with peak order hour: \n\n")
    for s1l1 in serv1log1:
        extractedList = s1l1.split('"')
        TimeDurations = extractedList[0].split()
        match = re.search(r'\d{2}/\w{3}/\d{4}:\d{2}:\d{2}:\d{2}', s1l1)
        capturedDate = datetime.datetime.strptime(match.group(), '%d/%b/%Y:%H:%M:%S')
        datetime_gmt = capturedDate.replace(tzinfo=pytz.UTC)
        datetime_ist = datetime_gmt.astimezone(timezone('Asia/Kolkata'))
        hr = datetime_ist.strftime('%H')
        if hr == order_max:
            apiDetails = extractedList[1].split()
            RequestType = apiDetails[0]
            apiUrl = apiDetails[1]
            Response = extractedList[2].split()
            ResponseCode = Response[0]
            file.write(
                "Request Type: " + RequestType + "   API Url: " + apiUrl + "   Response Code: " + ResponseCode + "\n")
file.close()
print("\nResponse Time for Orders: " + "\t")
print(*ResponseTimeOrders, sep=", ")
print("\nHourly Traffic for Order: " + "\t")
print(HourlyTrafficOrder)
print("\nMax orders occurred at " + str(order_max) + " with orders: " + str(HourlyTrafficOrder[order_max]))
print("\nTotal orders in the log files: " + "\t")
print(sum(HourlyTrafficOrder.values()))
print("\nResponse Time for Invoices: " + "\t")
print(*ResponseTimeInvoice, sep=", ")
print('\nMax invoice api calls occurred at ' + str(invoice_max) + ' with values: ' + str(
    HourlyTrafficInvoice[invoice_max]))
print("\nHourly Traffic for Invoices: " + "\t")
print(HourlyTrafficInvoice)
print("\nTotal invoices in the log files: " + "\t")
print(sum(HourlyTrafficInvoice.values()))
