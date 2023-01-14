from wordcloud import WordCloud

fpath = '/Library/Fonts//Arial Unicode.ttf'
text = ' '.join(配列)

wordcloud = WordCloud(backgroud_color='white', font_path=fpath, width=800, height=600, max_words=500).generate(text)
print(wordcloud)
wordcloud.to_file('./wordcloud.png')