import turtle as t
import time


def main():
    t.color("blue")
    t.begin_fill()

    for i in range(4):
        t.forward(100)
        t.left(90)
    t.end_fill()

    time.sleep(2)


if __name__ == '__main__':
    main()
