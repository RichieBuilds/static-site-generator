from textnode import TextNode, TextType


# TODO: Add exceptions.py
def main() -> None:
    dumy = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(dumy)

if __name__ == "__main__":
    main()