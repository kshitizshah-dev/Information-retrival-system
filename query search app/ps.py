from collections import defaultdict

# Example of defaultdict
d = defaultdict(int)  # Creates a defaultdict with default value 0 for integer keys
print(d['new_key hi'])    # This will return 0 without throwing an error, because int() returns 0
print(d['hi'])
print(d)
