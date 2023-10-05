# Define the period for MFI calculation
period = 14

# Sample price, high, and low data (you can replace this with your data)
closing_prices = [50.25, 51.50, 52.75, 52.00, 53.25, 53.75, 53.00, 52.50, 51.75, 50.00, 49.25, 49.00, 50.25, 51.00]
high_prices = [51.00, 52.25, 53.00, 52.75, 53.50, 54.00, 53.50, 53.00, 52.25, 51.25, 50.50, 50.25, 51.25, 52.00]
low_prices = [49.50, 50.75, 52.00, 51.50, 52.75, 53.25, 52.25, 51.75, 50.75, 48.75, 48.25, 49.00, 49.75, 50.50]
volume = [100000, 120000, 150000, 110000, 125000, 130000, 140000, 115000, 90000, 80000, 95000, 105000, 100000, 110000]
typical_prices = []
for i in range(0,14):
    typical_prices.append((high_prices[i] + low_prices[i] + closing_prices[i])/3)

raw_money_flow = [typical_prices[i] * volume[i] for i in range(0, len(typical_prices))]

positive_money_flow = [raw_money_flow[0]]  # Initialize with the first value of raw_money_flow
negative_money_flow = [0]

for i in range(1, len(typical_prices)):
    if typical_prices[i] > typical_prices[i - 1]:
        positive_money_flow.append(raw_money_flow[i])
        negative_money_flow.append(0)
    elif typical_prices[i] < typical_prices[i - 1]:
        positive_money_flow.append(0)
        negative_money_flow.append(raw_money_flow[i])
    else:
        positive_money_flow.append(0)
        negative_money_flow.append(0)

# Calculate money flow ratio (MFR)  
mfr = []  # Start with 0 for the first 'period' - 1 data points

sum_positive = sum(positive_money_flow)
sum_negative = sum(negative_money_flow)

if sum_negative == 0:
    mfr.append(0)
else:
    mfr.append(sum_positive / sum_negative)


mfi = [100 - (100 / (1 + m)) for m in mfr]

# Print the MFI values for the last 'period' days
print( mfi)
