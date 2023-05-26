def is_leap_year(year):
    if year%4==0 and year%100!=0 or year%400==0:
        print(year,"是闰年")
    else:
        print(year,"不是闰年")


if __name__ == "__main__":
    is_leap_year(1992)