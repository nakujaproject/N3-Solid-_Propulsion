import matplotlib.pyplot as plt

with open('1 grain static test results - test 1', 'r') as stream:
    contents = stream.readlines()
    contents = [val.strip() for val in contents]
    print(contents)
    true_val = []
    time = []
    for i in range(len(contents)):
        x = contents[i]
        y = x[16:]
        true_val.append(float(y))
    print(true_val)
    for i in range(len(true_val)):
        time.append((3.033*i)/len(true_val))

plt.plot(time, true_val)
plt.xlabel('TIME(s)')
plt.ylabel('THRUST(gF)')
plt.show()
