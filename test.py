import argparse
from moomoo_fee_calculator import moomoo_fee_usd


def main():
    parser = argparse.ArgumentParser(description="Test moomoo_fee_calculator outputs.")
    parser.add_argument("-p", "--price", type=float, default=190.04, help="Stock price in USD")
    parser.add_argument("-q", "--quantities", type=int, nargs="+", default=[1, 2, 5], help="Share quantities to test")
    parser.add_argument("--fx", type=float, default=0.25346, help="1 MYR to USD rate")
    args = parser.parse_args()

    print(f"price={args.price}, fx={args.fx}")
    for qty in args.quantities:
        res = moomoo_fee_usd(args.price, qty, args.fx)
        print(f"shares={qty}: {res}")


if __name__ == "__main__":
    main()
