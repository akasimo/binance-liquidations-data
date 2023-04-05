import time

while True:
    print("Hello World")
    # create file named "hello.txt" and write "Hello World" in it
    with open("hello.txt", "w") as f:
        f.write("Hello World")
    # wait for 1 second
    time.sleep(1)
