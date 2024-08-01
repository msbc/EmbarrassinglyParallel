import argparse


def square(x):
    return x**2


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Square a number")
    parser.add_argument("x", type=float, help="Number to square")
    args = parser.parse_args()
    print(square(args.x))
