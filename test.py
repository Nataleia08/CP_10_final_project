from spellchecker import SpellChecker
spell = SpellChecker()
misspelled = spell.unknown(['add', 'search', 'birthday', 'phone'])
for word in misspelled:
    print(spell.correction(word))

    print(spell.candidates(word))
