import random
import pykakasi
import sys
import msvcrt  # For Windows key detection

# ANSI color codes
GREEN = "\033[92m"  # Green color for correct answers
RED = "\033[91m"    # Red color for incorrect answers
YELLOW = "\033[93m" # Yellow color for kanji characters
RESET = "\033[0m"   # Reset color to default

# Initialize Kakasi for Romaji conversion
kakasi = pykakasi.kakasi()
kakasi.setMode("H", "a")  # Hiragana to Romaji
kakasi.setMode("K", "a")  # Katakana to Romaji
kakasi.setMode("J", "a")  # Kanji to Romaji
converter = kakasi.getConverter()

# Complete JLPT N5 Kanji List (103 kanji)
kanji_list = [
    {"kanji": "日", "meaning": "sun, day", "on": ["ニチ", "ジツ"], "kun": ["ひ", "か"]},
    {"kanji": "月", "meaning": "moon, month", "on": ["ゲツ", "ガツ"], "kun": ["つき"]},
    {"kanji": "水", "meaning": "water", "on": ["スイ"], "kun": ["みず"]},
    {"kanji": "火", "meaning": "fire", "on": ["カ"], "kun": ["ひ"]},
    {"kanji": "木", "meaning": "tree, wood", "on": ["ボク", "モク"], "kun": ["き", "こ"]},
    {"kanji": "金", "meaning": "gold, money", "on": ["キン", "コン"], "kun": ["かね", "かな"]},
    {"kanji": "土", "meaning": "earth, soil", "on": ["ド", "ト"], "kun": ["つち"]},
    {"kanji": "人", "meaning": "person", "on": ["ジン", "ニン"], "kun": ["ひと"]},
    {"kanji": "年", "meaning": "year", "on": ["ネン"], "kun": ["とし"]},
    {"kanji": "上", "meaning": "up, above", "on": ["ジョウ", "ショウ"], "kun": ["うえ", "あ", "のぼ"]},
    {"kanji": "下", "meaning": "down, below", "on": ["カ", "ゲ"], "kun": ["した", "さ", "くだ", "お"]},
    {"kanji": "中", "meaning": "middle, inside", "on": ["チュウ"], "kun": ["なか"]},
    {"kanji": "大", "meaning": "big, large", "on": ["ダイ", "タイ"], "kun": ["おお"]},
    {"kanji": "小", "meaning": "small, little", "on": ["ショウ"], "kun": ["ちい", "こ"]},
    {"kanji": "山", "meaning": "mountain", "on": ["サン"], "kun": ["やま"]},
    {"kanji": "川", "meaning": "river", "on": ["セン"], "kun": ["かわ"]},
    {"kanji": "女", "meaning": "woman, female", "on": ["ジョ", "ニョ"], "kun": ["おんな", "め"]},
    {"kanji": "男", "meaning": "man, male", "on": ["ダン", "ナン"], "kun": ["おとこ"]},
    {"kanji": "子", "meaning": "child", "on": ["シ", "ス"], "kun": ["こ"]},
    {"kanji": "出", "meaning": "exit, go out", "on": ["シュツ", "スイ"], "kun": ["で", "だ"]},
    {"kanji": "入", "meaning": "enter, insert", "on": ["ニュウ"], "kun": ["はい", "い"]},
    {"kanji": "口", "meaning": "mouth, opening", "on": ["コウ", "ク"], "kun": ["くち"]},
    {"kanji": "手", "meaning": "hand", "on": ["シュ"], "kun": ["て"]},
    {"kanji": "足", "meaning": "foot, leg", "on": ["ソク"], "kun": ["あし", "た"]},
    {"kanji": "目", "meaning": "eye", "on": ["モク"], "kun": ["め"]},
    {"kanji": "耳", "meaning": "ear", "on": ["ジ"], "kun": ["みみ"]},
    {"kanji": "花", "meaning": "flower", "on": ["カ"], "kun": ["はな"]},
    {"kanji": "名", "meaning": "name", "on": ["メイ", "ミョウ"], "kun": ["な"]},
    {"kanji": "天", "meaning": "heaven, sky", "on": ["テン"], "kun": ["あめ", "あま"]},
    {"kanji": "気", "meaning": "spirit, mind", "on": ["キ", "ケ"], "kun": ["いき"]},
    {"kanji": "生", "meaning": "life, birth", "on": ["セイ", "ショウ"], "kun": ["い", "う", "お", "は", "なま"]},
    {"kanji": "魚", "meaning": "fish", "on": ["ギョ"], "kun": ["うお", "さかな"]},
    {"kanji": "車", "meaning": "car, vehicle", "on": ["シャ"], "kun": ["くるま"]},
    {"kanji": "何", "meaning": "what", "on": ["カ"], "kun": ["なに", "なん"]},
    {"kanji": "学", "meaning": "study, learning", "on": ["ガク"], "kun": ["まな"]},
    {"kanji": "校", "meaning": "school", "on": ["コウ"], "kun": []},
    {"kanji": "先", "meaning": "before, ahead", "on": ["セン"], "kun": ["さき"]},
    {"kanji": "私", "meaning": "I, private", "on": ["シ"], "kun": ["わたし", "わたくし"]},
    {"kanji": "今", "meaning": "now", "on": ["コン", "キン"], "kun": ["いま"]},
    {"kanji": "外", "meaning": "outside", "on": ["ガイ", "ゲ"], "kun": ["そと", "ほか", "はず"]},
    {"kanji": "国", "meaning": "country", "on": ["コク"], "kun": ["くに"]},
    {"kanji": "語", "meaning": "language, word", "on": ["ゴ"], "kun": ["かた"]},
    {"kanji": "時", "meaning": "time, hour", "on": ["ジ"], "kun": ["とき"]},
    {"kanji": "分", "meaning": "minute, part", "on": ["フン", "ブン"], "kun": ["わ"]},
    {"kanji": "半", "meaning": "half", "on": ["ハン"], "kun": ["なか"]},
    {"kanji": "聞", "meaning": "hear, ask", "on": ["ブン", "モン"], "kun": ["き"]},
    {"kanji": "見", "meaning": "see, look", "on": ["ケン"], "kun": ["み"]},
    {"kanji": "行", "meaning": "go", "on": ["コウ", "ギョウ", "アン"], "kun": ["い", "ゆ", "おこな"]},
    {"kanji": "来", "meaning": "come", "on": ["ライ"], "kun": ["く", "き"]},
    {"kanji": "食", "meaning": "eat, food", "on": ["ショク", "ジキ"], "kun": ["く", "た"]},
    {"kanji": "飲", "meaning": "drink", "on": ["イン"], "kun": ["の"]},
    {"kanji": "読", "meaning": "read", "on": ["ドク", "トウ", "トク"], "kun": ["よ"]},
    {"kanji": "書", "meaning": "write", "on": ["ショ"], "kun": ["か"]},
    {"kanji": "話", "meaning": "speak, talk", "on": ["ワ"], "kun": ["はな"]},
    {"kanji": "好", "meaning": "like, favorite", "on": ["コウ"], "kun": ["この", "す"]},
    {"kanji": "高", "meaning": "high, tall", "on": ["コウ"], "kun": ["たか"]},
    {"kanji": "安", "meaning": "cheap, safe", "on": ["アン"], "kun": ["やす"]},
    {"kanji": "新", "meaning": "new", "on": ["シン"], "kun": ["あたら", "あら", "にい"]},
    {"kanji": "古", "meaning": "old", "on": ["コ"], "kun": ["ふる"]},
    {"kanji": "多", "meaning": "many", "on": ["タ"], "kun": ["おお"]},
    {"kanji": "少", "meaning": "few", "on": ["ショウ"], "kun": ["すく", "すこ"]},
    {"kanji": "白", "meaning": "white", "on": ["ハク", "ビャク"], "kun": ["しろ", "しら"]},
    {"kanji": "赤", "meaning": "red", "on": ["セキ", "シャク"], "kun": ["あか"]},
    {"kanji": "青", "meaning": "blue", "on": ["セイ", "ショウ"], "kun": ["あお"]},
    {"kanji": "黒", "meaning": "black", "on": ["コク"], "kun": ["くろ"]},
    {"kanji": "田", "meaning": "rice field", "on": ["デン"], "kun": ["た"]},
    {"kanji": "町", "meaning": "town", "on": ["チョウ"], "kun": ["まち"]},
    {"kanji": "店", "meaning": "store, shop", "on": ["テン"], "kun": ["みせ"]},
    {"kanji": "家", "meaning": "house, home", "on": ["カ", "ケ"], "kun": ["いえ", "や"]},
    {"kanji": "買", "meaning": "buy", "on": ["バイ"], "kun": ["か"]},
    {"kanji": "道", "meaning": "road, way", "on": ["ドウ", "トウ"], "kun": ["みち"]},
    {"kanji": "間", "meaning": "interval, space", "on": ["カン", "ケン"], "kun": ["あいだ", "ま"]},
    {"kanji": "雨", "meaning": "rain", "on": ["ウ"], "kun": ["あめ", "あま"]},
    {"kanji": "電", "meaning": "electricity", "on": ["デン"], "kun": []},
    {"kanji": "話", "meaning": "talk, story", "on": ["ワ"], "kun": ["はな"]},
    {"kanji": "休", "meaning": "rest, holiday", "on": ["キュウ"], "kun": ["やす"]},
    {"kanji": "立", "meaning": "stand", "on": ["リツ", "リュウ"], "kun": ["た"]},
    {"kanji": "待", "meaning": "wait", "on": ["タイ"], "kun": ["ま"]},
    {"kanji": "言", "meaning": "say, word", "on": ["ゲン", "ゴン"], "kun": ["い", "こと"]},
    {"kanji": "思", "meaning": "think", "on": ["シ"], "kun": ["おも"]},
    {"kanji": "知", "meaning": "know", "on": ["チ"], "kun": ["し"]},
    {"kanji": "友", "meaning": "friend", "on": ["ユウ"], "kun": ["とも"]},
    {"kanji": "会", "meaning": "meeting, meet", "on": ["カイ", "エ"], "kun": ["あ"]},
    {"kanji": "長", "meaning": "long, chief", "on": ["チョウ"], "kun": ["なが"]},
    {"kanji": "間", "meaning": "between, interval", "on": ["カン", "ケン"], "kun": ["あいだ", "ま"]},
    {"kanji": "前", "meaning": "before, in front", "on": ["ゼン"], "kun": ["まえ"]},
    {"kanji": "後", "meaning": "after, behind", "on": ["ゴ", "コウ"], "kun": ["のち", "うし", "あと"]},
    {"kanji": "午", "meaning": "noon", "on": ["ゴ"], "kun": ["うま"]},
    {"kanji": "北", "meaning": "north", "on": ["ホク"], "kun": ["きた"]},
    {"kanji": "南", "meaning": "south", "on": ["ナン", "ナ"], "kun": ["みなみ"]},
    {"kanji": "東", "meaning": "east", "on": ["トウ"], "kun": ["ひがし"]},
    {"kanji": "西", "meaning": "west", "on": ["セイ", "サイ"], "kun": ["にし"]},
    {"kanji": "右", "meaning": "right", "on": ["ウ", "ユウ"], "kun": ["みぎ"]},
    {"kanji": "左", "meaning": "left", "on": ["サ", "シャ"], "kun": ["ひだり"]},
    {"kanji": "四", "meaning": "four", "on": ["シ"], "kun": ["よ", "よん"]},
    {"kanji": "三", "meaning": "three", "on": ["サン"], "kun": ["み", "みっ"]},
    {"kanji": "二", "meaning": "two", "on": ["ニ", "ジ"], "kun": ["ふた", "ふた"]},
    {"kanji": "一", "meaning": "one", "on": ["イチ", "イツ"], "kun": ["ひと"]},
    {"kanji": "五", "meaning": "five", "on": ["ゴ"], "kun": ["いつ", "いつ"]},
    {"kanji": "六", "meaning": "six", "on": ["ロク", "リク"], "kun": ["む", "むっ", "むい"]},
    {"kanji": "七", "meaning": "seven", "on": ["シチ"], "kun": ["なな", "なの"]},
    {"kanji": "八", "meaning": "eight", "on": ["ハチ"], "kun": ["や", "よう"]},
    {"kanji": "九", "meaning": "nine", "on": ["キュウ", "ク"], "kun": ["ここの"]},
    {"kanji": "十", "meaning": "ten", "on": ["ジュウ", "ジッ"], "kun": ["とお"]},
    {"kanji": "百", "meaning": "hundred", "on": ["ヒャク"], "kun": ["もも"]},
    {"kanji": "千", "meaning": "thousand", "on": ["セン"], "kun": ["ち"]},
    {"kanji": "万", "meaning": "ten thousand", "on": ["マン", "バン"], "kun": ["よろず"]},
]

def get_romaji(text):
    """Convert Japanese text to romaji using the new pykakasi API"""
    result = converter.convert(text)
    # The new API returns a list of dictionaries with 'hepburn' key for romaji
    return ''.join([item['hepburn'] for item in result])

def print_mode_help():
    """Print help information for different modes"""
    print("\nKanji Flash Quiz Modes:")
    print(f"{YELLOW}1{RESET}: All question types (meaning, on-yomi, kun-yomi)")
    print(f"{YELLOW}2{RESET}: Meaning questions only")
    print(f"{YELLOW}3{RESET}: On-yomi questions only")
    print(f"{YELLOW}4{RESET}: Kun-yomi questions only")
    print(f"{YELLOW}h{RESET}: Display this help message")
    print(f"{YELLOW}q{RESET}: Quit the program")
    print("Press the corresponding key at any time to switch modes.\n")

def quiz():
    try:
        # Set initial mode - 1: all, 2: meaning only, 3: on only, 4: kun only
        current_mode = 1
        modes = {
            1: ["meaning", "on", "kun"],  # All types
            2: ["meaning"],               # Meaning only
            3: ["on"],                    # On-yomi only
            4: ["kun"]                    # Kun-yomi only
        }
        
        print_mode_help()
        
        while True:
            # Check if a key is pressed without blocking
            if msvcrt.kbhit():
                key = msvcrt.getch().decode('utf-8', errors='ignore')
                if key == 'q':
                    raise KeyboardInterrupt  # Handle quit
                elif key in ['1', '2', '3', '4']:
                    current_mode = int(key)
                    print(f"\n{GREEN}Switched to Mode {current_mode}: {'/'.join(modes[current_mode])} questions.{RESET}\n")
                elif key == 'h':
                    print_mode_help()
                    continue
            
            kanji = random.choice(kanji_list)
            
            # Select question type based on current mode
            question_type = random.choice(modes[current_mode])
            
            print(f"What is the {YELLOW}{question_type}{RESET} of '{YELLOW}{kanji['kanji']}{RESET}'?")
            user_answer = input("Your answer: ").strip()
            
            # Check if the answer is actually a mode change command
            if user_answer in ['1', '2', '3', '4']:
                current_mode = int(user_answer)
                print(f"\n{GREEN}Switched to Mode {current_mode}: {'/'.join(modes[current_mode])} questions.{RESET}\n")
                continue
            elif user_answer == 'h':
                print_mode_help()
                continue
            elif user_answer == 'q':
                raise KeyboardInterrupt
            
            correct_answers = kanji[question_type] if isinstance(kanji[question_type], list) else [kanji[question_type]]
            
            if question_type == "meaning":
                # For meaning, just check if the answer is in the meaning string
                if ((user_answer.lower() != "") and (user_answer.lower() in kanji["meaning"].lower())):
                    other_meanings = kanji["meaning"].replace(user_answer.lower(), "").replace(",", "").strip()
                    if other_meanings:
                        print(f"{GREEN}Correct!{RESET}   (Also: {other_meanings})\n")
                    else:
                        print(f"{GREEN}Correct!{RESET}\n")
                else:
                    print(f"{RED}Wrong. The correct answer is: {kanji['meaning']}{RESET}")
                    print(f"Kanji {YELLOW}{kanji['kanji']}{RESET} full info:")
                    print(f"  - Meaning: {YELLOW}{kanji['meaning']}{RESET}")
                    print(f"  - On-yomi: {YELLOW}{', '.join(kanji['on'])}{RESET}")
                    print(f"  - Kun-yomi: {YELLOW}{', '.join(kanji['kun'])}{RESET}\n")
            else:
                # For on and kun readings, use romaji conversion
                correct_romaji = [get_romaji(answer) for answer in correct_answers]
                
                if user_answer in correct_answers or user_answer in correct_romaji:
                    # Get the matched answer
                    matched_answer = None
                    if user_answer in correct_answers:
                        matched_answer = user_answer
                    else:
                        for i, romaji in enumerate(correct_romaji):
                            if user_answer == romaji:
                                matched_answer = correct_answers[i]
                                break
                    
                    # Show other possible answers
                    other_answers = [a for a in correct_answers if a != matched_answer]
                    if other_answers:
                        other_romaji = [get_romaji(a) for a in other_answers]
                        other_display = [f"{a} ({r})" for a, r in zip(other_answers, other_romaji)]
                        print(f"{GREEN}Correct!{RESET}   (Also: {', '.join(other_display)})\n")
                    else:
                        print(f"{GREEN}Correct!{RESET}\n")
                else:
                    print(f"{RED}Wrong. The correct answer is: {', '.join(correct_answers)} (Romaji: {', '.join(correct_romaji)}){RESET}")
                    print(f"Kanji {YELLOW}{kanji['kanji']}{RESET} full info:")
                    print(f"  - Meaning: {YELLOW}{kanji['meaning']}{RESET}")
                    print(f"  - On-yomi: {YELLOW}{', '.join(kanji['on'])}{RESET}")
                    print(f"  - Kun-yomi: {YELLOW}{', '.join(kanji['kun'])}{RESET}\n")
    except KeyboardInterrupt:
        print(f"\n{GREEN}Thanks for studying! Goodbye.{RESET}")
        return

if __name__ == "__main__":
    print("JLPT N5 Kanji Quiz")
    print("You can switch modes anytime by pressing 1-4")
    print("Press CTRL-C or q to exit")
    quiz()
