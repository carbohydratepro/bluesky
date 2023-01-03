train_text = []
test_text = []

for i, personID in enumerate(personID_list):
    print('personID', personID)

    with open("./data/personID{}.txt".format(personID), encoding="utf-8") as f:
        for bookID_str in f:
            #print(bookID)
            bookID_list = bookID_str.split( )

            # 50作品以上はダウンロードしてないのでカット
            if len(bookID_list) >= 50:
                bookID_list = bookID_list[:50]
            print('number of cards', len(bookID_list))

            for j, bookID in enumerate(bookID_list):

                # 先ほど保存した本文が含まれるhtmlを開く
                soup = BeautifulSoup(open("./data/text{}_{}.html".format(personID, bookID), encoding="shift_jis"))

                # 本文が書かれている<div>を取り出す
                main_text = soup.find("div", "main_text").text
                #print(main_text)

                # 最初の20作品はtrain_textに入れ、残りはtest_textに入れる
                if j < 20:
                    train_text.append(split_into_words(main_text, str(i)))
                    print('bookID\t{}\ttrain'.format(bookID))
                else:
                    test_text.append(split_into_words(main_text, str(i)))
                    print('bookID\t{}\ttest'.format(bookID))