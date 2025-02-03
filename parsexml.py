import xml.etree.ElementTree as ET
tree = ET.parse('modified_sms_v2.xml')
root = tree.getroot()

''' 
Iterate through the xml file to extract and categorise SMS
into types: 
       -Incoming money
       -Payment to code holder
       -Transfers to Mobile Numbers
       -Bank Deposits
       -Airtime Bill Payments
       -Cash Power Bill Payments
       -Transactions Initiated by Third Parties
       -Withdrawals from Agents
       -Bank Transfers
       -Internet and Voice Bundle Purchases
'''

# Extract the data needed
for sms in root.findall('sms'):
    smsAddress = sms.get('address') # Get the text inside the address tag
    smsDate = sms.get('date') # Get the text inside the date tag
    smsBody = sms.get('body') # Get the text inside the body tag
    smsDateSent = sms.get('dateSent') # Get the text inside the date_sent tag
    smsReadableDate = sms.get('readableDate') # Get the text inside the readable_date tag

# Initialise of a nested dictionary to categorise transactions
transactionType = {}

# Define transaction categories
incoming = "Incoming Money"
code = "Payment to Code Holder"
mobileNumber = "Transfers to Mobile Numbers"
bankDeposits = "Bank Deposits"
airtime = "Airtime Bill Payments"
power = "Cash Power Bill Payments"
thirdParties = "Transactions Initiated by Third Parties"
withdrawals = "Withdrawals from Agents"
bankTransfers = "Bank Transfers"
bundlePurchases = "Internet and Voice Bundle Purchases"
others = "Text to ignore"

categories = [
    incoming, code, mobileNumber, bankDeposits, airtime,
    power, thirdParties, withdrawals, bankTransfers, bundlePurchases, others
]

# Initialize dictionary entries
for category in categories:
    transactionType[category] = []

# Print transaction types
#for category, transactions in transactionType.items():
    #print(category)
    #print(transactions)
    #print('***')

# Append data to dictionary
for sms in root.findall('sms'):
    smsBody = sms.get('body')
    if smsBody and "Airtime" in smsBody:
        transactionType[airtime].append(smsBody)
    elif smsBody and "Power" in smsBody:
        transactionType[power].append(smsBody)
    elif smsBody and "Bundles" in smsBody:
        transactionType[bundlePurchases].append(smsBody)
    elif smsBody and "via agent" in smsBody:
        transactionType[withdrawals].append(smsBody)
    elif smsBody and "deposit" in smsBody:
        transactionType[bankTransfers].append(smsBody)
    elif smsBody and "payment" in smsBody:
        transactionType[code].append(smsBody)
    elif smsBody and "transferred" in smsBody:
        transactionType[mobileNumber].append(smsBody)
    elif smsBody and "received" in smsBody:
         transactionType[incoming].append(smsBody)
    elif smsBody and "transaction" in smsBody:
         transactionType[thirdParties].append(smsBody)
    else:
        transactionType[others].append(smsBody)

# Print results
for category, transactions in transactionType.items():
     print(category)
     print(transactions)
     print('***')