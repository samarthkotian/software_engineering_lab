def parse_booking(text):
    service, minutes = text.split(':')
    return service.strip().title(), float(minutes)

def duration_average(durations_csv):
    values = [int(r) for r in durations_csv.split(',')]
    return sum(values) // len(values)

def payable_bill(text):
    bill, discount = text.split('|')
    total = float(bill) * 1.18 - float(discount)
    return max(total, 0)

def main():
    print("==== Running parse_booking ====")
    user_input = input("Enter service:duration in min (e.g. haircut:45): ")
    result = parse_booking(user_input)
    print("Service and Duration:", result)

    print("\n==== Running duration_average ====")
    user_input = input("Enter durations as CSV (e.g. 30,45,60): ")
    result = duration_average(user_input)
    print("Average Duration:", result)

    print("\n==== Running payable_bill ====")
    user_input = input("Enter bill|discount (e.g. 800|100): ")
    result = payable_bill(user_input)
    print("Payable Bill:", result)

if __name__ == "__main__":
    main()
