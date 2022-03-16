import threading
import time
import random

initNumOfHacker = 4
initNumOfEmployee = 4

mutex = threading.Semaphore(1)
barrier = threading.Semaphore(4)
hackerQueue = threading.Semaphore(0)
employeeQueue = threading.Semaphore(0)

waitingHacker = 0
waitingEmployee = 0


def board():
    pass


def rowBoat():
    print("The boat is crossing the river \n#################\n\n")


def hacker_arrive(name):
    global waitingHacker, waitingEmployee
    time.sleep(random.random() * 10)

    mutex.acquire()

    isCapt = False

    waitingHacker += 1

    if waitingHacker == 4:
        hackerQueue.release(4)
        waitingHacker = 0
        isCapt = True

    elif waitingHacker == 2 and waitingEmployee >= 2:
        hackerQueue.release(2)
        employeeQueue.release(2)

        waitingEmployee -= 2
        waitingHacker = 0

        isCapt = True

    else:
        mutex.release()

    hackerQueue.acquire()

    print("{} got on the boat\n".format(name))

    board()

    barrier.acquire()

    if isCapt is True:
        time.sleep(1)
        rowBoat()
        barrier.release(4)
        mutex.release()


def employee_arrive(name):
    global waitingEmployee, waitingHacker
    time.sleep(random.random() * 10)

    mutex.acquire()
    waitingEmployee += 1

    isCapt = False

    if waitingEmployee == 4:
        employeeQueue.release(4)
        waitingEmployee = 0
        isCapt = True

    elif waitingEmployee == 2 and waitingHacker >= 2:
        hackerQueue.release(2)
        employeeQueue.release(2)

        waitingHacker -= 2
        waitingEmployee = 0

        isCapt = True

    else:
        mutex.release()

    employeeQueue.acquire()

    print("{} got on the boat\n".format(name))

    board()

    barrier.acquire()

    if isCapt is True:
        time.sleep(1)
        rowBoat()
        barrier.release(4)
        mutex.release()


if __name__ == "__main__":
    # Create Semaphore
    hackerThread = []
    employeeThread = []

    print("River Crossing Problem By Phuc\n############\n")

    try:
        for i in range(0, initNumOfHacker):
            # print("Add hacker " + str(i))
            hackerThread.append(threading.Thread(target=hacker_arrive, args=("hacker_" + str(i),)))

        for i in range(0, initNumOfEmployee):
            employeeThread.append(threading.Thread(target=employee_arrive, args=("employee_" + str(i),)))
            # print("Add employee " + str(i))

        for i in range(0, max(len(hackerThread), len(employeeThread))):
            if i < len(hackerThread):
                hackerThread[i].start()

            if i < len(employeeThread):
                employeeThread[i].start()

        for i in range(0, max(len(hackerThread), len(employeeThread))):
            if i < len(hackerThread):
                hackerThread[i].join()

            if i < len(employeeThread):
                employeeThread[i].join()

        print("All passengers have left boat !")

    except Exception as e:
        print("ERROR {}".format(e))
