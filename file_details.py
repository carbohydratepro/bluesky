# dbとmodelの内容メモ

'''
PE01.db
宮沢賢治 : 5
芥川龍之介 : 5
太宰治 : 5
夏目漱石 : 3

銀河鉄道の夜
注文の多い料理店
セロ弾きのゴーシュ
やまなし
どんぐりと山猫
羅生門
鼻
河童
歯車
老年
斜陽
走れメロス
津軽
お伽草紙
人間失格
吾輩は猫である
草枕
三四郎

PE02.db
宮沢賢治 : 261
夏目漱石 : 98
太宰治 : 272
芥川龍之介 : 373

PE03.db
宮沢賢治 : 5
夏目漱石 : 5
太宰治 : 5
芥川龍之介 : 5

PE04.db
宮沢賢治 : 10
夏目漱石 : 10
太宰治 : 10
芥川龍之介 : 10

PE05.db
宮沢賢治 : 30
夏目漱石 : 30
太宰治 : 30
芥川龍之介 : 30

PE06.db
宮沢賢治 : 50
夏目漱石 : 50
太宰治 : 50
芥川龍之介 : 50

PE07.db
宮沢賢治 : 80
夏目漱石 : 80
太宰治 : 80
芥川龍之介 : 80

'''

'''
PE0101.model
著者名をラベルに
dm=1, vector_size=300, min_count=1, epochs=20

PE0102.model
作品名をラベルに
dm=1, vector_size=300, min_count=1, epochs=20

PE0103.model


PE0201.model
著者名をラベルに
dm=1, vector_size=300, min_count=1, epochs=20
・精度高い

PE0301.model
著者名をラベルに
dm=1, vector_size=300, min_count=1, epochs=20
宮沢賢治 : 0.0 %
夏目漱石 : 100.0 %
太宰治 : 1.1235955056179776 %
芥川龍之介 : 49.184782608695656 %
正解率： 28.15040650406504 %

PE0302.model
著者名をラベルに
dm=0, vector_size=300, min_count=1, epochs=20

PE0401.model
著者名をラベルに
dm=1, vector_size=300, min_count=1, epochs=20

PE0402.model
著者名をラベルに
dm=0, vector_size=300, min_count=1, epochs=20

PE501.model
著者名をラベルに
dm=1, vector_size=300, min_count=1, epochs=20

PE502.model
著者名をラベルに
dm=0, vector_size=300, min_count=1, epochs=20

PE0601.model
著者名をラベルに
dm=1, vector_size=300, min_count=1, epochs=20
宮沢賢治 : 0.0 %
夏目漱石 : 60.416666666666664 %
太宰治 : 3.153153153153153 %
芥川龍之介 : 0.0 %
正解率： 4.477611940298507 %

PE0602.model
著者名をラベルに
dm=0, vector_size=300, min_count=1, epochs=20
宮沢賢治 : 0.0 %
夏目漱石 : 18.75 %
太宰治 : 100.0 %
芥川龍之介 : 0.0 %
正解率： 28.73134328358209 %

PE0701.model
著者名をラベルに
dm=1, vector_size=300, min_count=1, epochs=20
宮沢賢治 : 100.0 %
夏目漱石 : 11.11111111111111 %
太宰治 : 0.0 %
芥川龍之介 : 95.90443686006826 %
正解率： 67.83625730994152 %

PE0702.model
dm=0, vector_size=300, min_count=1, epochs=20
宮沢賢治 : 100.0 %
夏目漱石 : 0.0 %
太宰治 : 100.0 %
芥川龍之介 : 100.0 %
正解率： 75.0 %

'''