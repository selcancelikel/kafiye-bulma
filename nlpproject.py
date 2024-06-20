from ZemberekAnalyzer import ZemberekAnalyzer, remove_turkish_characters

def find_rhyme_pairs(poem, analyzer: ZemberekAnalyzer):
    # Metni satirlara ayir
    lines = poem.lower().split('\n')
    # Kafiye eþleþmelerini bul
    rhyme_pairs = []
    for i, line1 in enumerate(lines):
        for j, line2 in enumerate(lines[i+1:], start=i+1):
            # Her iki satýrdaki kelimeleri ayýr
            words1 = line1.split()
            words2 = line2.split()
            # Satýrlarýn son kelimelerini al
            last_word1 = words1[-1]
            last_word2 = words2[-1]
            # Köklerin ve eklerin bulunmasý
            root_and_suffixes1 = analyzer.analyze_word(remove_turkish_characters(last_word1))
            root_and_suffixes2 = analyzer.analyze_word(remove_turkish_characters(last_word2))
            # root_and_suffixes1 = analyzer.analyze_word(last_word1)
            # root_and_suffixes2 = analyzer.analyze_word(last_word2)
            # Köklerin karþýlaþtýrýlmasý
            root1, suffix1 = root_and_suffixes1[0]
            root2, suffix2 = root_and_suffixes2[0]
            # Köklerin ve eklerin karþýlaþtýrýlmasý
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
            # Eþleþen harfler varsa, eþleþen kafiye çiftini listeye ekleyelim
            if redif:
                rhyme_pairs.append((last_word1, last_word2, kafiye, redif, flag))
                break  # Ýlk eþleþmeyi bulduðumuzda döngüden çýk
    return rhyme_pairs

# Kullanýcýdan þiir dörtlüðünü al
# print("Lütfen þiir dörtlüðünü girin (Çýkmak için 'x' tuþuna basýn):")
poem_lines = []
while True:
    line = input()
    if line.lower() == ' ':
        break
    poem_lines.append(line)

# Kullanýcýdan alýnan satýrlarý birleþtirerek þiir dörtlüðünü oluþtur
poem = "\n".join(poem_lines)

# ZemberekAnalyzer sýnýfýný baþlatma
analyzer = ZemberekAnalyzer()

# Kafiye eþleþmelerini bul
rhyme_pairs = find_rhyme_pairs(poem, analyzer)

# Kafiye eþleþmelerini yazdýr
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
