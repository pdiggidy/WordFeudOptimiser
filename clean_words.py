with open('english_words.txt', 'r') as f:
    words = f.read().splitlines()
    # 144884 words
print(len(words))
#filter words containing non-letters
words = [word for word in words if word.isalpha()]

#remove words over 15 characters
words = [word for word in words if len(word) <= 15]
# 75469 words

#Make all words lowercase
words = [word.lower() for word in words]

with open('cleaned_words.txt', 'w') as f:
    for word in words:
        f.write(word + '\n')

# Maybe: add plural words to the list