
# https://stackoverflow.com/questions/19504350/how-to-convert-numbers-to-words-without-using-num2word-library

num2words = {
    1: "One", 2: "Two", 3: "Three", 4: "Four", 5: "Five",
    6: "Six", 7: "Seven", 8: "Eight", 9: "Nine", 10: "Ten",
    11: "Eleven", 12: "Twelve", 13: "Thirteen", 14: "Fourteen",
    15: "Fifteen", 16: "Sixteen", 17: "Seventeen", 18: "Eighteen",
    19: "Nineteen", 20: "Twenty", 30: "Thirty", 40: "Forty",
    50: "Fifty", 60: "Sixty", 70: "Seventy", 80: "Eighty",
    90: "Ninety", 0: "Zero"}


def num_2_words(n):
    """
    return a textual version of a 0-99 number
    """

    try:
        return num2words[n].lower()
    except KeyError:
        try:
            return num2words[n - n % 10].lower() + "-" + num2words[n % 10].lower()
        except KeyError:
            return "number out of range"


if __name__ == '__main__':

    for n in range(100):
        print(n, num_2_words(n))
