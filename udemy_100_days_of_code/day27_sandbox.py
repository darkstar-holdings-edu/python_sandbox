from tkinter import Button, Entry, Label, Tk


def main() -> None:
    def button_handler() -> None:
        label_1.config(text=input_1.get())

    window = Tk()
    window.title("Day 27")
    window.minsize(width=600, height=600)
    window.config(padx=20, pady=20)

    label_1 = Label(text="This is a label", font=("Arial", 24))
    label_1.grid(row=0, column=0, padx=20, pady=20)

    button_0 = Button(text="New Button")
    button_0.grid(row=0, column=2)

    button_1 = Button(text="Click Me!", command=button_handler)
    button_1.grid(row=1, column=1)

    input_1 = Entry(width=10)
    input_1.grid(row=2, column=3)

    window.mainloop()


if __name__ == "__main__":
    main()
