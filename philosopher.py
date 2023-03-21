import threading

# Without Deadlock Avoidance
def phil(philosophers, eat):

    forks = [1] * philosophers
    can_eat = []
    cannot_eat = []
    for p in eat:
        if forks[p] == 1 and forks[(p+1)%philosophers] == 1:
            forks[p] = 0
            forks[(p+1)%philosophers] = 0
            can_eat.append(p)
        else:
            cannot_eat.append(p)

    return can_eat, cannot_eat

# With Deadlock Avoidance
def phil_semaphores():

    class Philosopher(threading.Thread):

        def __init__(self, number, left_chopstick, right_chopstick, sem):
            threading.Thread.__init__(self)
            self.number = number
            self.left_chopstick = left_chopstick
            self.right_chopstick = right_chopstick
            self.sem = sem
        
        def run(self):
            if self.number not in allowed_to_eat:
                return
            
            with self.sem:
                self.left_chopstick.acquire()
                self.right_chopstick.acquire()
                print("Philosopher", self.number, "is eating.")
                self.right_chopstick.release()
                self.left_chopstick.release()

    n = int(input("Enter the number of philosophers: "))
    allowed_to_eat = set(map(int, input("Enter the philosophers who want to eat (space separated): ").split()))

    # Create chopsticks, semaphore, and philosophers
    chopsticks = [threading.Lock() for _ in range(n)]
    sem = threading.Semaphore((n+1)//2)
    philosophers = [Philosopher(i, chopsticks[i], chopsticks[(i+1)%n], sem) for i in range(n) if i in allowed_to_eat]

    # Start philosophers
    for philosopher in philosophers:
        philosopher.start()

    # Wait for philosophers to finish
    for philosopher in philosophers:
        philosopher.join()

def main():

    while True:

        print("1. Run Dining Philosophers Problem without deadlock avoidance")
        print("2. Run Dining Philosophers Problem with deadlock avoidance")
        print("3. Exit")

        choice = input("Enter your choice: ")
        if choice == "1":
            philosophers = int(input("Enter the number of philosophers: "))
            eat = list(map(int, input("Enter the philosophers who want to eat (space separated): ").split()))
            can_eat, cannot_eat = phil(philosophers, eat)

            if can_eat:
                print("The following philosophers can eat:", can_eat)
            if cannot_eat:
                print("The following philosophers cannot eat:", cannot_eat)

        elif choice == "2":
            phil_semaphores()
        elif choice == "3":
            break
        else:
            print("Invalid choice! Please try again.")

if __name__ == '__main__':
    main()