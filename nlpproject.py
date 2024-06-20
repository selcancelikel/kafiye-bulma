from ZemberekAnalyzer import ZemberekAnalyzer, remove_turkish_characters

def find_rhyme_pairs(poem, analyzer: ZemberekAnalyzer):
    # Metni satirlara ayir
    lines = poem.lower().split('\n')
    # Kafiye e�le�melerini bul
    rhyme_pairs = []
    for i, line1 in enumerate(lines):
        for j, line2 in enumerate(lines[i+1:], start=i+1):
            # Her iki sat�rdaki kelimeleri ay�r
            words1 = line1.split()
            words2 = line2.split()
            # Sat�rlar�n son kelimelerini al
            last_word1 = words1[-1]
            last_word2 = words2[-1]
            # K�klerin ve eklerin bulunmas�
            root_and_suffixes1 = analyzer.analyze_word(remove_turkish_characters(last_word1))
            root_and_suffixes2 = analyzer.analyze_word(remove_turkish_characters(last_word2))
            # root_and_suffixes1 = analyzer.analyze_word(last_word1)
            # root_and_suffixes2 = analyzer.analyze_word(last_word2)
            # K�klerin kar��la�t�r�lmas�
            root1, suffix1 = root_and_suffixes1[0]
            root2, suffix2 = root_and_suffixes2[0]
            # K�klerin ve eklerin kar��la�t�r�lmas�
            # matching_letters = ''
            kafiye = ''
            redif = ''
            flag=0
            
            for (char1, char2) in zip(reversed(root1), reversed(root2)):
                if char1 == char2:
                    # matching_letters = char1 + matching_letters
                   kafiye = char1 + kafiye
                else:
                    break
                

            if kafiye==root1:
                flag=1

            for (char1, char2) in zip(reversed(suffix1), reversed(suffix2)):
                if char1 == char2:
                    redif = char1 + redif
                else:
                    break
            # E�le�en harfler varsa, e�le�en kafiye �iftini listeye ekleyelim
            if redif:
                rhyme_pairs.append((last_word1, last_word2, kafiye, redif, flag))
                break  # �lk e�le�meyi buldu�umuzda d�ng�den ��k
    return rhyme_pairs

# Kullan�c�dan �iir d�rtl���n� al
# print("L�tfen �iir d�rtl���n� girin (��kmak i�in 'x' tu�una bas�n):")
poem_lines = []
while True:
    line = input()
    if line.lower() == ' ':
        break
    poem_lines.append(line)

# Kullan�c�dan al�nan sat�rlar� birle�tirerek �iir d�rtl���n� olu�tur
poem = "\n".join(poem_lines)

# ZemberekAnalyzer s�n�f�n� ba�latma
analyzer = ZemberekAnalyzer()

# Kafiye e�le�melerini bul
rhyme_pairs = find_rhyme_pairs(poem, analyzer)

# Kafiye e�le�melerini yazd�r
if rhyme_pairs:
    print("Kafiye :")
    for pair in rhyme_pairs:
        if pair[4]==0:
            print(f"{pair[0]} ile {pair[1]} arasnda kafiye: {pair[2]}")
            print(f"{pair[0]} ile {pair[1]} arasnda redif: {pair[3]}" )
            
        else:
            print("cinasli")
else:
    print("Kafiye  yok.")

# JVM'yi kapatma
analyzer.stop_jvm()
