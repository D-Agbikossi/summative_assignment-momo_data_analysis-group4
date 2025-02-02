import xml.etree.ElementTree as ET
tree = ET.parse('modified_sms_v2.xml')
root = tree.getroot()

''' Iterate through the xml file to extract and categorise SMS
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
       -Internet and Voice Bundle Purchases'''

# Extract the data needed
for sms in root.findall('sms'):
    smsAddress = sms.get('address') # Get the text inside the address tag
    smsDate = sms.get('date') # Get the text inside the date tag
    smsBody = sms.get('body') # Get the text inside the body tag
    smsDateSent = sms.get('dateSent') # Get the text inside the date_sent tag
    smsReadableDate = sms.get('readableDate') # Get the text inside the readable_date tag

    #print(smsAddress)
    #print(smsDate)
    #print(smsBody)
    #print(smsDateSent)
    #print(smsReadableDate)
    #print('***')

# Categorise the data
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

categories = [
    incoming, code, mobileNumber, bankDeposits, airtime,
    power, thirdParties, withdrawals, bankTransfers, bundlePurchases
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
     smsBody = sms.get('body')  # Make sure smsBody is assigned before using it
     if smsBody and "received" in smsBody.lower():  # Ensure smsBody is not None
         transactionType[incoming].append(smsBody)

# Print results
for category, transactions in transactionType.items():
     print(category)
     print(transactions)
     print('***')