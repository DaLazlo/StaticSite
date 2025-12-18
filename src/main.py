
from textnode import TextType, TextNode

print("hello world")

def main():
    textnode = TextNode("sometext", TextType.PLAIN, "http://localhost/")
    print(textnode)


if __name__=="__main__":
    main()

