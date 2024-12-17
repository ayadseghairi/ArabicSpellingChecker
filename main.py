import tkinter as tk
from pyarabic.araby import tokenize, strip_tashkeel
import hunspell

hunspell_checker = hunspell.HunSpell('arb_alias.dic', 'arb_alias.aff')

class ArabicSpellingChecker:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Arabic Spelling Checker")
        self.root.geometry("600x600")

        self.text = tk.Text(self.root, font=("Arial", 14), wrap="word")
        self.text.tag_configure("right_align", justify="right")
        
        self.text.configure(insertbackground="black", wrap="word")
        self.text.pack(expand=True, fill='both')

        self.text.insert("1.0", "\u202B")
        self.text.tag_add("right_align", "1.0", "end")

        self.text.mark_set("insert", "1.0")

        self.text.bind("<KeyRelease>", self.check)

        self.root.mainloop()

    def check(self, event):
        content = self.text.get("1.0", tk.END).strip()
        for tag in self.text.tag_names():
            self.text.tag_delete(tag)

        tokens = tokenize(content)
        for word in tokens:
            cleaned_word = strip_tashkeel(word)
            if not hunspell_checker.spell(cleaned_word):
                self.highlight_word(word)

    def highlight_word(self, word):
        start_idx = "1.0"
        while True:
            start_idx = self.text.search(word, start_idx, stopindex=tk.END, nocase=True)
            if not start_idx:
                break
            end_idx = f"{start_idx.split('.')[0]}.{int(start_idx.split('.')[1]) + len(word)}"
            self.text.tag_add("misspelled", start_idx, end_idx)
            start_idx = end_idx

        self.text.tag_config("misspelled", background="red")

if __name__ == "__main__":
    ArabicSpellingChecker()
